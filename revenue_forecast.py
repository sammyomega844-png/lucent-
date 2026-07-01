"""
Revenue Forecast — projects 30 / 60 / 90 day revenue from the active
pipeline using a simple close-rate model derived from CRM history.
No paid APIs. Fully offline.
"""

import json
import math
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REPORT_FILE = "revenue_forecast.json"

# Default close-rate assumptions by status when no history is available
_DEFAULT_CLOSE_RATES = {
    "qualified": 0.40,
    "contacted": 0.15,
    "new": 0.08,
}

# Days assumed to close from each status if no velocity data
_DEFAULT_DAYS_TO_CLOSE = {
    "qualified": 21,
    "contacted": 45,
    "new": 60,
}


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _safe_text(value, max_len=80):
    return str(value or "").strip()[:max_len]


def _parse_date(value):
    text = _safe_text(value, max_len=40)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            continue
    return None


def _velocity_days(crm_df):
    """
    Estimate average days from Created_At to close (Lost or last contact)
    using historical rows where data is available.
    Returns a dict of {status_lower: avg_days} or empty dict.
    """
    from datetime import date
    today = date.today()
    durations = {}
    for _, row in crm_df.iterrows():
        status = _safe_text(row.get("Status", "")).lower()
        created = _parse_date(row.get("Created_At", ""))
        last = _parse_date(row.get("Last_Contact", ""))
        if not created:
            continue
        end = last or today
        days = (end - created).days
        if days > 0:
            durations.setdefault(status, []).append(days)

    return {
        status: round(sum(vals) / len(vals))
        for status, vals in durations.items()
        if vals
    }


def _close_rate_from_history(crm_df):
    """
    Compute historical close rate as Won / (Won + Lost) where Won = Qualified.
    Returns a float 0–1, or None if insufficient data.
    """
    total = len(crm_df)
    if total == 0:
        return None
    won = sum(1 for _, r in crm_df.iterrows() if _safe_text(r.get("Status", "")).lower() == "qualified")
    lost = sum(1 for _, r in crm_df.iterrows() if _safe_text(r.get("Status", "")).lower() == "lost")
    denominator = won + lost
    if denominator == 0:
        return None
    return round(won / denominator, 3)


def build_revenue_forecast(crm_df, horizons=(30, 60, 90)):
    if crm_df is None or getattr(crm_df, "empty", True):
        return {
            "generated_at": _now_iso(),
            "summary": "Revenue forecast: no CRM data.",
            "horizons": {},
            "active_deals": [],
        }

    historical_close_rate = _close_rate_from_history(crm_df)
    velocity = _velocity_days(crm_df)

    active_deals = []
    for _, row in crm_df.iterrows():
        status = _safe_text(row.get("Status", "")).lower()
        if status == "lost":
            continue

        value = _safe_float(row.get("Lead_Value", 0))
        created = _parse_date(row.get("Created_At", ""))
        last = _parse_date(row.get("Last_Contact", ""))

        # Days in pipeline so far
        from datetime import date
        today = date.today()
        age_days = (today - created).days if created else 0

        # Expected days to close for this status
        expected_days = velocity.get(status) or _DEFAULT_DAYS_TO_CLOSE.get(status, 45)
        days_remaining = max(expected_days - age_days, 1)

        # Close rate for this status
        if historical_close_rate is not None and status == "qualified":
            close_rate = historical_close_rate
        else:
            close_rate = _DEFAULT_CLOSE_RATES.get(status, 0.10)

        active_deals.append({
            "company": _safe_text(row.get("Company", "Unknown"), max_len=80),
            "lead_name": _safe_text(row.get("Lead_Name", ""), max_len=80),
            "status": _safe_text(row.get("Status", ""), max_len=40),
            "value": value,
            "age_days": age_days,
            "days_remaining": days_remaining,
            "close_rate": close_rate,
            "expected_revenue": round(value * close_rate, 2),
        })

    # Build horizon projections
    horizon_results = {}
    for h in horizons:
        deals_in_window = [d for d in active_deals if d["days_remaining"] <= h]
        projected = sum(d["expected_revenue"] for d in deals_in_window)
        best_case = sum(d["value"] for d in deals_in_window)
        horizon_results[str(h)] = {
            "days": h,
            "deal_count": len(deals_in_window),
            "projected_revenue": round(projected, 2),
            "best_case_revenue": round(best_case, 2),
        }

    total_pipeline = sum(d["value"] for d in active_deals)
    total_projected_90 = horizon_results.get("90", {}).get("projected_revenue", 0)

    summary_bits = [
        f"Revenue forecast: {len(active_deals)} active deal(s), ${total_pipeline:,.0f} total pipeline"
    ]
    for h in horizons:
        r = horizon_results.get(str(h), {})
        summary_bits.append(
            f"{h}d: ${r.get('projected_revenue', 0):,.0f} projected ({r.get('deal_count', 0)} deal(s))"
        )

    return {
        "generated_at": _now_iso(),
        "summary": "; ".join(summary_bits) + ".",
        "horizons": horizon_results,
        "active_deals": active_deals,
        "total_pipeline": total_pipeline,
        "historical_close_rate": historical_close_rate,
    }


def write_revenue_forecast(path=DEFAULT_REPORT_FILE, **kwargs):
    data = build_revenue_forecast(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_revenue_forecast(path=DEFAULT_REPORT_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "summary": "No revenue forecast yet.", "horizons": {}, "active_deals": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "summary": "No revenue forecast yet.", "horizons": {}, "active_deals": []}
