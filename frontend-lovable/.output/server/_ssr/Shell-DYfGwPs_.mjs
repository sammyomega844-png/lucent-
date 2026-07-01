import { n as __toESM } from "../_runtime.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { n as useIndustry } from "./IndustryContext-BipHHbci.mjs";
import { g as Link, l as useRouterState } from "../_libs/@tanstack/react-router+[...].mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/Shell-DYfGwPs_.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
function IndustrySwitcher() {
	const { industry, all, setIndustryId } = useIndustry();
	const [open, setOpen] = (0, import_react.useState)(false);
	const ref = (0, import_react.useRef)(null);
	(0, import_react.useEffect)(() => {
		function onDocClick(e) {
			if (!ref.current?.contains(e.target)) setOpen(false);
		}
		function onEsc(e) {
			if (e.key === "Escape") setOpen(false);
		}
		document.addEventListener("mousedown", onDocClick);
		document.addEventListener("keydown", onEsc);
		return () => {
			document.removeEventListener("mousedown", onDocClick);
			document.removeEventListener("keydown", onEsc);
		};
	}, []);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		ref,
		className: "relative",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
			type: "button",
			onClick: () => setOpen((o) => !o),
			"aria-haspopup": "listbox",
			"aria-expanded": open,
			className: "inline-flex items-center gap-2 rounded-md border border-border bg-background px-3 py-1.5 text-sm text-foreground transition hover:bg-secondary",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "text-[10px] font-medium uppercase tracking-[0.16em] text-muted-foreground",
					children: "Workspace"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "font-medium",
					children: industry.name
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					"aria-hidden": true,
					className: "text-muted-foreground",
					children: "▾"
				})
			]
		}), open ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			role: "listbox",
			className: "absolute right-0 z-40 mt-2 w-72 overflow-hidden rounded-lg border border-border bg-background shadow-xl",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "px-3 py-2 text-[11px] uppercase tracking-[0.14em] text-muted-foreground",
				children: "Switch industry"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
				className: "max-h-80 overflow-auto py-1",
				children: all.map((p) => {
					const active = p.id === industry.id;
					return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
						type: "button",
						role: "option",
						"aria-selected": active,
						onClick: () => {
							setIndustryId(p.id);
							setOpen(false);
						},
						className: "flex w-full flex-col items-start gap-0.5 px-3 py-2 text-left text-sm transition " + (active ? "bg-primary-soft text-primary" : "text-foreground hover:bg-secondary"),
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "font-medium",
							children: p.name
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-xs text-muted-foreground",
							children: p.tagline
						})]
					}) }, p.id);
				})
			})]
		}) : null]
	});
}
function Logo() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Link, {
		to: "/",
		className: "flex items-center gap-2",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "grid size-7 place-items-center rounded-md bg-primary text-primary-foreground font-display text-lg leading-none",
				children: "L"
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "font-display text-xl tracking-tight text-foreground",
				children: "Lucent"
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "hidden text-[11px] uppercase tracking-[0.16em] text-muted-foreground sm:inline",
				children: "Executive Intelligence"
			})
		]
	});
}
function NavLink({ to, children }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Link, {
		to,
		className: "rounded-md px-3 py-1.5 text-sm transition " + (useRouterState({ select: (s) => s.location.pathname }) === to ? "bg-primary-soft text-primary" : "text-muted-foreground hover:bg-secondary hover:text-foreground"),
		children
	});
}
function Shell({ children }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "min-h-dvh",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("header", {
				className: "sticky top-0 z-30 border-b border-border/70 bg-background/70 backdrop-blur",
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Logo, {}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("nav", {
							"aria-label": "Primary",
							className: "flex items-center gap-1",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(NavLink, {
									to: "/",
									children: "Dashboard"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(NavLink, {
									to: "/setup",
									children: "Setup"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(NavLink, {
									to: "/help",
									children: "Help"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(NavLink, {
									to: "/status",
									children: "Status"
								})
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "hidden items-center gap-2 sm:flex",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(IndustrySwitcher, {}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "chip chip-healthy",
									children: "All systems calm"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "grid size-8 place-items-center rounded-full bg-primary text-primary-foreground text-sm font-medium",
									children: "EM"
								})
							]
						})
					]
				})
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("main", {
				id: "main",
				className: "mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-10",
				children
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("footer", {
				className: "mx-auto max-w-7xl px-4 pb-10 pt-2 text-xs text-muted-foreground sm:px-6",
				children: [
					"© ",
					(/* @__PURE__ */ new Date()).getFullYear(),
					" Lucent · Executive Intelligence Platform"
				]
			})
		]
	});
}
//#endregion
export { Shell as t };
