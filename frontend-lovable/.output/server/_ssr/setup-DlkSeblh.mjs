import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { t as Shell } from "./Shell-DYfGwPs_.mjs";
import { i as Dot, n as CardHeader, r as Chip, t as Card } from "./primitives-BuKmOx9b.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/setup-DlkSeblh.js
var import_jsx_runtime = require_jsx_runtime();
var steps = [
	{
		n: 1,
		title: "Connect your sources",
		status: "healthy",
		note: "Calendar, inbox, CRM"
	},
	{
		n: 2,
		title: "Choose your operating cadence",
		status: "healthy",
		note: "Daily briefing, weekly review"
	},
	{
		n: 3,
		title: "Calibrate signals",
		status: "watch",
		note: "Renewal exposure thresholds"
	},
	{
		n: 4,
		title: "Invite your team",
		status: "watch",
		note: "Roles and visibility"
	}
];
var sources = [
	{
		name: "Google Calendar",
		status: "healthy",
		detail: "Connected · last sync 2 min ago"
	},
	{
		name: "Gmail",
		status: "healthy",
		detail: "Connected · 4 mailboxes"
	},
	{
		name: "Salesforce",
		status: "watch",
		detail: "Connected · permissions need review"
	},
	{
		name: "HubSpot",
		status: "healthy",
		detail: "Connected · 2-way sync"
	},
	{
		name: "Slack",
		status: "healthy",
		detail: "Connected · 3 channels"
	},
	{
		name: "Zoom",
		status: "watch",
		detail: "Connect to capture meeting recaps"
	}
];
function Setup() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Shell, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, { children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "text-[11px] uppercase tracking-[0.16em] text-muted-foreground",
				children: "Setup"
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h1", {
				className: "mt-2 font-display text-4xl text-foreground sm:text-5xl",
				children: [
					"Lucent is ",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
						className: "text-primary",
						children: "90% configured"
					}),
					"."
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "mt-2 max-w-2xl text-muted-foreground",
				children: "Finish two short steps and your morning briefing, follow-up autopilot, and revenue forecast will go live for your team."
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "mt-6 grid gap-3 md:grid-cols-4",
				children: steps.map((s) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "rounded-lg border border-border bg-surface-muted p-4",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex items-center justify-between",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
								className: "font-display text-2xl text-foreground",
								children: ["0", s.n]
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: s.status })]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mt-2 text-sm font-medium text-foreground",
							children: s.title
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "text-xs text-muted-foreground",
							children: s.note
						})
					]
				}, s.n))
			})
		] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "grid gap-6 lg:grid-cols-2",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
				eyebrow: "Sources",
				title: "Connected data",
				subtitle: "Where Lucent reads from."
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
				className: "space-y-2",
				children: sources.map((s) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
					className: "flex items-center justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "min-w-0",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "text-sm font-medium text-foreground",
							children: s.name
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "text-xs text-muted-foreground",
							children: s.detail
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
						status: s.status === "healthy" ? "healthy" : "watch",
						children: s.status === "healthy" ? "Connected" : "Action needed"
					})]
				}, s.name))
			})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
				eyebrow: "Cadence",
				title: "Operating rhythm",
				subtitle: "When Lucent shows up for you."
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
				className: "space-y-3",
				children: [
					{
						t: "Morning briefing",
						d: "Weekdays · 06:30 local",
						on: true
					},
					{
						t: "Midday pulse",
						d: "Weekdays · 12:30 local",
						on: false
					},
					{
						t: "End-of-day recap",
						d: "Weekdays · 18:00 local",
						on: true
					},
					{
						t: "Weekly performance review",
						d: "Mondays · 08:00 local",
						on: true
					}
				].map((r) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
					className: "flex items-center justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "text-sm font-medium text-foreground",
						children: r.t
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "text-xs text-muted-foreground",
						children: r.d
					})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
						role: "switch",
						"aria-checked": r.on,
						"aria-label": `Toggle ${r.t}`,
						className: "relative h-6 w-11 rounded-full transition " + (r.on ? "bg-primary" : "bg-border"),
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "absolute top-0.5 size-5 rounded-full bg-surface shadow transition " + (r.on ? "left-[22px]" : "left-0.5") })
					})]
				}, r.t))
			})] })]
		})]
	}) });
}
//#endregion
export { Setup as component };
