import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { t as clsx } from "../_libs/clsx.mjs";
import { t as twMerge } from "../_libs/tailwind-merge.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/primitives-BuKmOx9b.js
var import_jsx_runtime = require_jsx_runtime();
function cn(...inputs) {
	return twMerge(clsx(inputs));
}
function Card({ children, className, id, as: As = "section" }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(As, {
		id,
		className: cn("card-surface card-surface-hover p-5 sm:p-6 reveal", className),
		children
	});
}
function CardHeader({ title, subtitle, right, eyebrow }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
		className: "mb-4 flex items-start justify-between gap-4",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "min-w-0",
			children: [
				eyebrow ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "mb-1 text-[11px] font-medium uppercase tracking-[0.14em] text-muted-foreground",
					children: eyebrow
				}) : null,
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h3", {
					className: "font-display text-xl text-foreground sm:text-2xl",
					children: title
				}),
				subtitle ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "mt-1 text-sm text-muted-foreground",
					children: subtitle
				}) : null
			]
		}), right ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "shrink-0",
			children: right
		}) : null]
	});
}
function Chip({ status, children, className }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
		className: cn(status === "healthy" ? "chip chip-healthy" : status === "watch" ? "chip chip-watch" : status === "risk" ? "chip chip-risk" : status === "primary" ? "chip chip-primary" : "chip", className),
		children
	});
}
function Dot({ status }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
		"aria-hidden": true,
		className: cn("inline-block size-2 rounded-full", status === "healthy" ? "bg-healthy" : status === "watch" ? "bg-watch" : "bg-risk")
	});
}
function TrendArrow({ trend }) {
	if (trend === "up") return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
		"aria-label": "up",
		className: "text-healthy",
		children: "▲"
	});
	if (trend === "down") return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
		"aria-label": "down",
		className: "text-risk",
		children: "▼"
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
		"aria-label": "flat",
		className: "text-muted-foreground",
		children: "▬"
	});
}
//#endregion
export { TrendArrow as a, Dot as i, CardHeader as n, cn as o, Chip as r, Card as t };
