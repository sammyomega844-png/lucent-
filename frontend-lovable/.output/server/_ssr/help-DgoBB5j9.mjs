import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { t as Shell } from "./Shell-DYfGwPs_.mjs";
import { n as CardHeader, r as Chip, t as Card } from "./primitives-BuKmOx9b.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/help-DgoBB5j9.js
var import_jsx_runtime = require_jsx_runtime();
var topics = [
	{
		group: "Getting started",
		items: [
			{
				title: "Reading your Day Score",
				desc: "What goes into the score and how to react when it shifts."
			},
			{
				title: "Configuring your morning briefing",
				desc: "Tune what shows up in your 6:30 briefing."
			},
			{
				title: "Connecting calendars and inboxes",
				desc: "Bring meetings, threads, and decisions into Lucent."
			}
		]
	},
	{
		group: "Revenue & pipeline",
		items: [
			{
				title: "How forecast confidence is computed",
				desc: "Signals, weights, and the 30/60/90 windows."
			},
			{
				title: "Tagging at-risk deals",
				desc: "Override risk signals when you have more context."
			},
			{
				title: "Renewal save plays",
				desc: "Pre-built plays for overdue and this-month renewals."
			}
		]
	},
	{
		group: "Workflow & approvals",
		items: [
			{
				title: "Approval routing",
				desc: "How approvals are queued and escalated."
			},
			{
				title: "Follow-up Autopilot voice",
				desc: "Train Autopilot to draft in your tone."
			},
			{
				title: "Meeting to execution",
				desc: "Decisions, actions, and owners auto-extracted."
			}
		]
	}
];
function Help() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Shell, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Card, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-6 lg:grid-cols-[1.2fr_1fr] lg:items-center",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "text-[11px] uppercase tracking-[0.16em] text-muted-foreground",
						children: "Help Center"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
						className: "mt-2 font-display text-4xl text-foreground sm:text-5xl",
						children: "Run Lucent like an executive operator."
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-3 max-w-xl text-muted-foreground",
						children: "Short, opinionated guides for getting more out of every signal Lucent surfaces — without becoming a tool you have to babysit."
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mt-5",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("label", {
							className: "sr-only",
							htmlFor: "help-search",
							children: "Search help"
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("input", {
							id: "help-search",
							type: "search",
							placeholder: "Search guides, e.g. ‘renewal save play’",
							className: "w-full rounded-lg border border-border bg-surface px-4 py-3 text-sm shadow-sm outline-none transition focus:border-foreground/30 focus:ring-2 focus:ring-ring"
						})]
					})
				] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "grid grid-cols-2 gap-3",
					children: [
						{
							k: "Avg. time saved / week",
							v: "6.2h"
						},
						{
							k: "Avg. action acceptance",
							v: "82%"
						},
						{
							k: "Renewal save lift",
							v: "+14%"
						},
						{
							k: "Forecast accuracy",
							v: "94%"
						}
					].map((s) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "rounded-lg border border-border bg-surface-muted p-4",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "text-[11px] uppercase tracking-wider text-muted-foreground",
							children: s.k
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mt-1 font-display text-3xl text-foreground",
							children: s.v
						})]
					}, s.k))
				})]
			}) }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "grid gap-6 lg:grid-cols-3",
				children: topics.map((t) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
					eyebrow: "Guides",
					title: t.group
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "space-y-3",
					children: t.items.map((i) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "rounded-lg border border-border bg-surface-muted p-3 transition hover:border-foreground/20",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "text-sm font-medium text-foreground",
								children: i.title
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mt-1 text-sm text-muted-foreground",
								children: i.desc
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
								className: "mt-2 text-xs font-medium text-primary hover:underline",
								children: "Read guide →"
							})
						]
					}, i.title))
				})] }, t.group))
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
				eyebrow: "Talk to us",
				title: "Still stuck? Reach a human.",
				right: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
					status: "healthy",
					children: "< 2h response"
				})
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "grid gap-3 sm:grid-cols-3",
				children: [
					{
						t: "Concierge onboarding",
						d: "Pair with a Lucent specialist for setup."
					},
					{
						t: "Customer Slack",
						d: "Drop a question, get answers from operators like you."
					},
					{
						t: "Email support",
						d: "Send transcripts, screenshots, ideas — we read everything."
					}
				].map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "rounded-lg border border-border bg-surface-muted p-4",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "text-sm font-medium text-foreground",
						children: c.t
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-1 text-sm text-muted-foreground",
						children: c.d
					})]
				}, c.t))
			})] })
		]
	}) });
}
//#endregion
export { Help as component };
