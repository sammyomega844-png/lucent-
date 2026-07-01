import { createFileRoute } from "@tanstack/react-router";
import { Shell } from "@/components/Shell";
import {
  actions,
  approvals,
  deals,
  forecast,
  kpis,
  renewals,
  timeline,
} from "@/data/mock";

declare const __BUILD_TIME__: string;
declare const __APP_VERSION__: string;

export const Route = createFileRoute("/status")({
  head: () => ({
    meta: [
      { title: "Lucent Status" },
      {
        name: "description",
        content:
          "Production readiness and live data signal status for the Lucent dashboard.",
      },
    ],
  }),
  component: StatusPage,
});

function BoolPill({ ok, label }: { ok: boolean; label: string }) {
  return (
    <span
      className={
        "inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium " +
        (ok
          ? "bg-emerald-500/15 text-emerald-700"
          : "bg-amber-500/15 text-amber-700")
      }
    >
      {ok ? "PASS" : "WARN"} Â· {label}
    </span>
  );
}

function StatusPage() {
  const checks = [
    { label: "Actions loaded", ok: actions.length > 0, value: actions.length },
    {
      label: "Forecast horizons",
      ok: forecast.length === 3,
      value: forecast.length,
    },
    { label: "KPI rows", ok: kpis.length > 0, value: kpis.length },
    { label: "Deal progression", ok: deals.length > 0, value: deals.length },
    {
      label: "Renewals available",
      ok: renewals.length > 0,
      value: renewals.length,
    },
    {
      label: "Timeline events",
      ok: timeline.length > 0,
      value: timeline.length,
    },
    {
      label: "Approvals visible",
      ok: approvals.length > 0,
      value: approvals.length,
    },
  ];

  const passCount = checks.filter((c) => c.ok).length;
  const score = Math.round((passCount / checks.length) * 100);

  return (
    <Shell>
      <section className="space-y-6">
        <div className="rounded-2xl border border-border bg-card p-6">
          <h1 className="text-2xl font-semibold text-foreground">
            System Status
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Quick live readiness snapshot for deployment checks and smoke tests.
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            <BoolPill ok={score >= 85} label={`Readiness ${score}%`} />
            <BoolPill ok={true} label={`Version ${__APP_VERSION__}`} />
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <article className="rounded-2xl border border-border bg-card p-5">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
              Build Information
            </h2>
            <dl className="mt-3 space-y-2 text-sm">
              <div className="flex justify-between gap-4">
                <dt className="text-muted-foreground">Build time</dt>
                <dd className="text-foreground">{__BUILD_TIME__}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-muted-foreground">App version</dt>
                <dd className="text-foreground">{__APP_VERSION__}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-muted-foreground">Environment</dt>
                <dd className="text-foreground">production candidate</dd>
              </div>
            </dl>
          </article>

          <article className="rounded-2xl border border-border bg-card p-5">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
              Data Health
            </h2>
            <ul className="mt-3 space-y-2">
              {checks.map((check) => (
                <li
                  key={check.label}
                  className="flex items-center justify-between rounded-lg border border-border/70 px-3 py-2"
                >
                  <span className="text-sm text-foreground">{check.label}</span>
                  <span className="text-xs text-muted-foreground">
                    {check.ok ? "OK" : "Check"} Â· {check.value}
                  </span>
                </li>
              ))}
            </ul>
          </article>
        </div>
      </section>
    </Shell>
  );
}
