import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { t as Shell } from "./Shell-DYfGwPs_.mjs";
import { c as forecast, g as timeline, l as kpis, n as actions, o as deals, p as renewals, r as approvals } from "./mock-B6rfRqWa.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/status-BTdrl1Dg.js
var import_jsx_runtime = require_jsx_runtime();
function BoolPill({ ok, label }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
		className: "inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium " + (ok ? "bg-emerald-500/15 text-emerald-700" : "bg-amber-500/15 text-amber-700"),
		children: [
			ok ? "PASS" : "WARN",
			" Â· ",
			label
		]
	});
}
function StatusPage() {
	const checks = [
		{
			label: "Actions loaded",
			ok: actions.length > 0,
			value: actions.length
		},
		{
			label: "Forecast horizons",
			ok: forecast.length === 3,
			value: forecast.length
		},
		{
			label: "KPI rows",
			ok: kpis.length > 0,
			value: kpis.length
		},
		{
			label: "Deal progression",
			ok: deals.length > 0,
			value: deals.length
		},
		{
			label: "Renewals available",
			ok: renewals.length > 0,
			value: renewals.length
		},
		{
			label: "Timeline events",
			ok: timeline.length > 0,
			value: timeline.length
		},
		{
			label: "Approvals visible",
			ok: approvals.length > 0,
			value: approvals.length
		}
	];
	const passCount = checks.filter((c) => c.ok).length;
	const score = Math.round(passCount / checks.length * 100);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Shell, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
		className: "space-y-6",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "rounded-2xl border border-border bg-card p-6",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
					className: "text-2xl font-semibold text-foreground",
					children: "System Status"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "mt-2 text-sm text-muted-foreground",
					children: "Quick live readiness snapshot for deployment checks and smoke tests."
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-4 flex flex-wrap gap-2",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(BoolPill, {
						ok: score >= 85,
						label: `Readiness ${score}%`
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(BoolPill, {
						ok: true,
						label: `Version 0.0.0`
					})]
				})
			]
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "grid gap-4 md:grid-cols-2",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("article", {
				className: "rounded-2xl border border-border bg-card p-5",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "text-sm font-semibold uppercase tracking-wide text-muted-foreground",
					children: "Build Information"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("dl", {
					className: "mt-3 space-y-2 text-sm",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex justify-between gap-4",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("dt", {
								className: "text-muted-foreground",
								children: "Build time"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("dd", {
								className: "text-foreground",
								children: "2026-07-01T15:15:27.970Z"
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex justify-between gap-4",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("dt", {
								className: "text-muted-foreground",
								children: "App version"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("dd", {
								className: "text-foreground",
								children: "0.0.0"
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex justify-between gap-4",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("dt", {
								className: "text-muted-foreground",
								children: "Environment"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("dd", {
								className: "text-foreground",
								children: "production candidate"
							})]
						})
					]
				})]
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("article", {
				className: "rounded-2xl border border-border bg-card p-5",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "text-sm font-semibold uppercase tracking-wide text-muted-foreground",
					children: "Data Health"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "mt-3 space-y-2",
					children: checks.map((check) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "flex items-center justify-between rounded-lg border border-border/70 px-3 py-2",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-sm text-foreground",
							children: check.label
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
							className: "text-xs text-muted-foreground",
							children: [
								check.ok ? "OK" : "Check",
								" Â· ",
								check.value
							]
						})]
					}, check.label))
				})]
			})]
		})]
	}) });
}
//#endregion
export { StatusPage as component };
