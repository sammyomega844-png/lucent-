import { n as __toESM } from "../_runtime.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { n as useIndustry } from "./IndustryContext-BipHHbci.mjs";
import { a as DialogPortal, i as DialogOverlay, n as DialogContent, o as DialogTitle, r as DialogDescription, s as DialogTrigger, t as Dialog } from "../_libs/@radix-ui/react-dialog+[...].mjs";
import { t as Shell } from "./Shell-DYfGwPs_.mjs";
import { a as TrendArrow, i as Dot, n as CardHeader, o as cn, r as Chip, t as Card } from "./primitives-BuKmOx9b.mjs";
import { r as useDashboardLayout, t as DASHBOARD_MODULES } from "./DashboardLayoutContext-ClhCll-G.mjs";
import { _ as weekly, a as dayScore, c as forecast, d as pipelineRisks, f as recommendations, g as timeline, h as surfaces, i as briefing, l as kpis, m as sentiment, n as actions, o as deals, p as renewals, r as approvals, s as followUps, t as accountHealth, u as meetings } from "./mock-PXzSbStU.mjs";
import { a as EyeOff, i as Eye, n as RotateCcw, o as ArrowUp, r as GripVertical, s as ArrowDown, t as SlidersHorizontal } from "../_libs/lucide-react.mjs";
import { n as SwitchThumb, t as Switch$1 } from "../_libs/@radix-ui/react-switch+[...].mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/routes-kpjF5gKl.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
var STEPS = [
	{
		title: "Start with the Pulse",
		body: "Your day opens with a Day Score, a strategic pulse, and the few signals that decide whether today goes well.",
		target: "Hero & Day Score"
	},
	{
		title: "Clear the Action Register",
		body: "Only the moves that need you. Priorities are calibrated against deals, renewals, and team health.",
		target: "Action Register & Approvals"
	},
	{
		title: "Let Autopilot draft for you",
		body: "Follow-ups, meeting recaps, and next steps are drafted. You review, edit, and send — nothing falls through.",
		target: "Follow-up Autopilot"
	},
	{
		title: "See revenue with confidence",
		body: "Forecast, deal motion, and renewals are stitched together so you can commit a number you trust.",
		target: "Forecast, Deals & Renewals"
	},
	{
		title: "Briefings, ready before you are",
		body: "A morning briefing summarizes the night, the day, and the plays to run — written in your voice.",
		target: "Executive Briefing"
	}
];
function ProductTour() {
	const [open, setOpen] = (0, import_react.useState)(false);
	const [step, setStep] = (0, import_react.useState)(0);
	(0, import_react.useEffect)(() => {
		const onKey = (e) => {
			if (!open) return;
			if (e.key === "Escape") setOpen(false);
			if (e.key === "ArrowRight") setStep((s) => Math.min(STEPS.length - 1, s + 1));
			if (e.key === "ArrowLeft") setStep((s) => Math.max(0, s - 1));
		};
		window.addEventListener("keydown", onKey);
		return () => window.removeEventListener("keydown", onKey);
	}, [open]);
	const current = STEPS[step];
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
		type: "button",
		onClick: () => {
			setStep(0);
			setOpen(true);
		},
		className: "fixed bottom-6 right-6 z-40 inline-flex items-center gap-2 rounded-full bg-primary px-4 py-3 text-sm font-medium text-primary-foreground shadow-[0_12px_40px_-12px_oklch(0.32_0.06_210/0.5)] transition hover:scale-[1.02] hover:opacity-95",
		"aria-label": "Open product tour",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
			className: "grid size-5 place-items-center rounded-full bg-primary-foreground text-primary text-[11px] font-bold",
			children: "?"
		}), "Product Tour"]
	}), open ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "fixed inset-0 z-50 grid place-items-center bg-foreground/30 px-4 backdrop-blur-sm",
		role: "dialog",
		"aria-modal": "true",
		"aria-labelledby": "tour-title",
		onClick: () => setOpen(false),
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "card-surface w-full max-w-lg p-6 reveal",
			onClick: (e) => e.stopPropagation(),
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "flex items-center justify-between text-xs uppercase tracking-[0.16em] text-muted-foreground",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Lucent Tour" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: [
						step + 1,
						" / ",
						STEPS.length
					] })]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					id: "tour-title",
					className: "mt-2 font-display text-3xl text-foreground",
					children: current.title
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
					className: "mt-2 text-sm text-muted-foreground",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
							className: "font-medium text-foreground",
							children: [current.target, "."]
						}),
						" ",
						current.body
					]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "mt-5 h-1 w-full overflow-hidden rounded-full bg-border",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "h-full bg-primary transition-all",
						style: { width: `${(step + 1) / STEPS.length * 100}%` }
					})
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-5 flex items-center justify-between",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
						className: "text-sm text-muted-foreground hover:text-foreground",
						onClick: () => setOpen(false),
						children: "Skip tour"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center gap-2",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
							className: "rounded-md border border-border bg-surface px-3 py-2 text-sm font-medium text-foreground disabled:opacity-40",
							onClick: () => setStep((s) => Math.max(0, s - 1)),
							disabled: step === 0,
							children: "Back"
						}), step < STEPS.length - 1 ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
							className: "rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground hover:opacity-90",
							onClick: () => setStep((s) => s + 1),
							children: "Next"
						}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
							className: "rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground hover:opacity-90",
							onClick: () => setOpen(false),
							children: "Get started"
						})]
					})]
				})
			]
		})
	}) : null] });
}
function SectionJump({ items }) {
	const [active, setActive] = (0, import_react.useState)(items[0]?.id ?? "");
	(0, import_react.useEffect)(() => {
		const elements = items.map((i) => document.getElementById(i.id)).filter((el) => !!el);
		if (elements.length === 0) return;
		const observer = new IntersectionObserver((entries) => {
			const visible = entries.filter((e) => e.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
			if (visible[0]) setActive(visible[0].target.id);
		}, {
			rootMargin: "-30% 0px -55% 0px",
			threshold: [
				0,
				.25,
				.5,
				1
			]
		});
		elements.forEach((el) => observer.observe(el));
		return () => observer.disconnect();
	}, [items]);
	const jumpTo = (id) => {
		const el = document.getElementById(id);
		if (!el) return;
		const top = el.getBoundingClientRect().top + window.scrollY - 96;
		window.scrollTo({
			top,
			behavior: "smooth"
		});
	};
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("nav", {
		"aria-label": "Jump to section",
		className: "sticky top-[60px] z-20 -mx-4 border-y border-border/60 bg-background/80 px-4 py-2 backdrop-blur sm:-mx-6 sm:px-6",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "flex gap-1.5 overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden",
			children: items.map((i) => {
				return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
					onClick: () => jumpTo(i.id),
					className: "shrink-0 rounded-full px-3 py-1.5 text-xs font-medium transition " + (active === i.id ? "bg-foreground text-background" : "border border-border bg-surface text-muted-foreground hover:text-foreground"),
					children: i.label
				}, i.id);
			})
		})
	});
}
var CONNECTORS = [
	{
		id: "salesforce",
		name: "Salesforce",
		category: "CRM",
		status: "watch",
		initial: "SF",
		tone: "bg-[#00A1E0]"
	},
	{
		id: "hubspot",
		name: "HubSpot",
		category: "CRM",
		status: "connected",
		initial: "HS",
		tone: "bg-[#FF7A59]"
	},
	{
		id: "gmail",
		name: "Gmail",
		category: "Comms",
		status: "connected",
		initial: "GM",
		tone: "bg-[#EA4335]"
	},
	{
		id: "gcal",
		name: "Calendar",
		category: "Calendar",
		status: "connected",
		initial: "GC",
		tone: "bg-[#4285F4]"
	},
	{
		id: "slack",
		name: "Slack",
		category: "Comms",
		status: "connected",
		initial: "SL",
		tone: "bg-[#4A154B]"
	},
	{
		id: "zoom",
		name: "Zoom",
		category: "Comms",
		status: "watch",
		initial: "ZM",
		tone: "bg-[#2D8CFF]"
	},
	{
		id: "notion",
		name: "Notion",
		category: "Docs",
		status: "connected",
		initial: "NO",
		tone: "bg-foreground"
	},
	{
		id: "stripe",
		name: "Stripe",
		category: "Billing",
		status: "connected",
		initial: "ST",
		tone: "bg-[#635BFF]"
	},
	{
		id: "snowflake",
		name: "Snowflake",
		category: "Data",
		status: "available",
		initial: "SN",
		tone: "bg-[#29B5E8]"
	},
	{
		id: "linear",
		name: "Linear",
		category: "Docs",
		status: "available",
		initial: "LN",
		tone: "bg-[#5E6AD2]"
	},
	{
		id: "gong",
		name: "Gong",
		category: "Comms",
		status: "available",
		initial: "GO",
		tone: "bg-[#7C3AED]"
	},
	{
		id: "zendesk",
		name: "Zendesk",
		category: "Comms",
		status: "available",
		initial: "ZD",
		tone: "bg-[#03363D]"
	}
];
var FILTERS = [
	"All",
	"CRM",
	"Comms",
	"Calendar",
	"Data",
	"Billing",
	"Docs"
];
function statusChip(s) {
	if (s === "connected") return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
		status: "healthy",
		children: "Connected"
	});
	if (s === "watch") return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
		status: "watch",
		children: "Review"
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, { children: "Available" });
}
function ConnectorsPanel() {
	const [filter, setFilter] = (0, import_react.useState)("All");
	const visible = CONNECTORS.filter((c) => filter === "All" || c.category === filter);
	const connected = CONNECTORS.filter((c) => c.status === "connected").length;
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "connectors",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
				eyebrow: "Connectors",
				title: "Quick access",
				subtitle: `${connected} of ${CONNECTORS.length} sources connected · click a tile to manage.`,
				right: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("a", {
					href: "/setup",
					className: "rounded-md border border-border bg-surface px-3 py-1.5 text-xs font-medium text-foreground transition hover:bg-secondary",
					children: "Manage all"
				})
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "mb-3 flex flex-wrap gap-1.5",
				children: FILTERS.map((f) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
					onClick: () => setFilter(f),
					className: "rounded-full px-3 py-1 text-xs font-medium transition " + (filter === f ? "bg-primary text-primary-foreground" : "border border-border bg-surface text-muted-foreground hover:text-foreground"),
					children: f
				}, f))
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
				className: "grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4",
				children: visible.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
					type: "button",
					className: "group flex w-full items-center gap-3 rounded-lg border border-border bg-surface p-3 text-left transition hover:-translate-y-0.5 hover:border-primary/30 hover:shadow-[var(--shadow-card)]",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "grid size-9 shrink-0 place-items-center rounded-md text-xs font-semibold text-white " + c.tone,
							"aria-hidden": true,
							children: c.initial
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
							className: "min-w-0 flex-1",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "block truncate text-sm font-medium text-foreground",
								children: c.name
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "block text-[11px] text-muted-foreground",
								children: c.category
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "shrink-0",
							children: statusChip(c.status)
						})
					]
				}) }, c.id))
			})
		]
	});
}
var Sheet = Dialog;
var SheetTrigger = DialogTrigger;
var SheetPortal = DialogPortal;
var SheetOverlay = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(DialogOverlay, {
	ref,
	className: cn("fixed inset-0 z-50 bg-black/40 backdrop-blur-[1px] data-[state=open]:animate-in data-[state=closed]:animate-out", className),
	...props
}));
SheetOverlay.displayName = DialogOverlay.displayName;
var sideClasses = {
	top: "inset-x-0 top-0 border-b data-[state=open]:animate-in data-[state=closed]:animate-out",
	right: "inset-y-0 right-0 h-full border-l data-[state=open]:animate-in data-[state=closed]:animate-out",
	bottom: "inset-x-0 bottom-0 border-t data-[state=open]:animate-in data-[state=closed]:animate-out",
	left: "inset-y-0 left-0 h-full border-r data-[state=open]:animate-in data-[state=closed]:animate-out"
};
var SheetContent = import_react.forwardRef(({ side = "right", className, children, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SheetPortal, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SheetOverlay, {}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(DialogContent, {
	ref,
	className: cn("fixed z-50 bg-background p-6 shadow-xl transition ease-in-out", sideClasses[side], className),
	...props,
	children
})] }));
SheetContent.displayName = DialogContent.displayName;
var SheetHeader = ({ className, ...props }) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
	className: cn("flex flex-col space-y-1.5 text-left", className),
	...props
});
SheetHeader.displayName = "SheetHeader";
var SheetTitle = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(DialogTitle, {
	ref,
	className: cn("text-lg font-semibold text-foreground", className),
	...props
}));
SheetTitle.displayName = DialogTitle.displayName;
var SheetDescription = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(DialogDescription, {
	ref,
	className: cn("text-sm text-muted-foreground", className),
	...props
}));
SheetDescription.displayName = DialogDescription.displayName;
var Switch = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Switch$1, {
	ref,
	className: cn("peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent", "transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2", "data-[state=checked]:bg-primary data-[state=unchecked]:bg-border", "disabled:cursor-not-allowed disabled:opacity-50", className),
	...props,
	children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SwitchThumb, { className: cn("pointer-events-none block h-5 w-5 rounded-full bg-white shadow-lg ring-0 transition-transform", "data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0") })
}));
Switch.displayName = Switch$1.displayName;
function moduleMeta(id) {
	return DASHBOARD_MODULES.find((m) => m.id === id);
}
function CustomizePanel() {
	const { allOrderedIds, isVisible, toggle, reorder, reset } = useDashboardLayout();
	const { industry } = useIndustry();
	const [dragIndex, setDragIndex] = (0, import_react.useState)(null);
	const [overIndex, setOverIndex] = (0, import_react.useState)(null);
	const [grabbedIndex, setGrabbedIndex] = (0, import_react.useState)(null);
	const [announcement, setAnnouncement] = (0, import_react.useState)("");
	const handleRefs = (0, import_react.useRef)({});
	const pendingFocusId = (0, import_react.useRef)(null);
	(0, import_react.useEffect)(() => {
		if (pendingFocusId.current) {
			handleRefs.current[pendingFocusId.current]?.focus();
			pendingFocusId.current = null;
		}
	}, [allOrderedIds]);
	const pinnedCount = allOrderedIds.filter((id) => moduleMeta(id).pinned).length;
	const onPointerDrop = (target) => {
		if (dragIndex === null) return;
		reorder(dragIndex, target);
		setDragIndex(null);
		setOverIndex(null);
	};
	const moveByKeyboard = (from, direction) => {
		const id = allOrderedIds[from];
		if (!id) return;
		const meta = moduleMeta(id);
		if (meta.pinned) return;
		const to = from + direction;
		if (to < pinnedCount || to >= allOrderedIds.length) return;
		pendingFocusId.current = id;
		reorder(from, to);
		setAnnouncement(`${meta.label} moved to position ${to - pinnedCount + 1} of ${allOrderedIds.length - pinnedCount}.`);
	};
	const onHandleKeyDown = (event, index) => {
		const id = allOrderedIds[index];
		if (!id) return;
		const meta = moduleMeta(id);
		if (meta.pinned) return;
		if (event.key === " " || event.key === "Enter") {
			event.preventDefault();
			if (grabbedIndex === index) {
				setGrabbedIndex(null);
				setAnnouncement(`${meta.label} dropped.`);
			} else {
				setGrabbedIndex(index);
				setAnnouncement(`${meta.label} grabbed. Use arrow keys to move, space to drop, escape to cancel.`);
			}
			return;
		}
		if (event.key === "Escape" && grabbedIndex !== null) {
			event.preventDefault();
			setGrabbedIndex(null);
			setAnnouncement(`Reorder cancelled.`);
			return;
		}
		if (event.key === "ArrowUp" || event.key === "ArrowDown") {
			if (grabbedIndex !== index) return;
			event.preventDefault();
			moveByKeyboard(index, event.key === "ArrowUp" ? -1 : 1);
		}
	};
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Sheet, {
		onOpenChange: (open) => {
			if (!open) {
				setGrabbedIndex(null);
				setAnnouncement("");
			}
		},
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SheetTrigger, {
			asChild: true,
			children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
				type: "button",
				className: "inline-flex items-center gap-2 rounded-md border border-border bg-background px-3 py-1.5 text-xs font-medium text-foreground transition hover:bg-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SlidersHorizontal, {
					className: "h-3.5 w-3.5",
					"aria-hidden": "true"
				}), "Customize"]
			})
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SheetContent, {
			side: "right",
			className: "w-full sm:max-w-md overflow-y-auto",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SheetHeader, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SheetTitle, { children: "Customize dashboard" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SheetDescription, { children: [
					"Toggle and reorder modules for the ",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("b", { children: industry.name }),
					" workspace. Changes save automatically and apply only to this industry."
				] })] }),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					id: "reorder-instructions",
					className: "mt-3 text-[11px] text-muted-foreground",
					children: "Drag a handle, or focus a handle and press Space to pick up a module, then Arrow Up / Arrow Down to move it, Space to drop, Escape to cancel."
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					role: "status",
					"aria-live": "polite",
					"aria-atomic": "true",
					className: "sr-only",
					children: announcement
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-4 flex items-center justify-between text-xs text-muted-foreground",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: [allOrderedIds.length, " modules"] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
						type: "button",
						onClick: reset,
						className: "inline-flex items-center gap-1 rounded-md border border-border px-2 py-1 text-foreground transition hover:bg-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(RotateCcw, {
							className: "h-3 w-3",
							"aria-hidden": "true"
						}), "Reset to default"]
					})]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "mt-4 space-y-1.5",
					"aria-label": "Dashboard modules, reorderable",
					children: allOrderedIds.map((id, index) => {
						const meta = moduleMeta(id);
						const visible = isVisible(id);
						const dragging = dragIndex === index;
						const over = overIndex === index;
						const grabbed = grabbedIndex === index;
						const reorderablePosition = meta.pinned ? null : `${index - pinnedCount + 1} of ${allOrderedIds.length - pinnedCount}`;
						return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
							draggable: !meta.pinned,
							onDragStart: (e) => {
								if (meta.pinned) {
									e.preventDefault();
									return;
								}
								setDragIndex(index);
								e.dataTransfer.effectAllowed = "move";
							},
							onDragOver: (e) => {
								e.preventDefault();
								setOverIndex(index);
							},
							onDragLeave: () => setOverIndex((cur) => cur === index ? null : cur),
							onDrop: (e) => {
								e.preventDefault();
								onPointerDrop(index);
							},
							onDragEnd: () => {
								setDragIndex(null);
								setOverIndex(null);
							},
							className: "flex items-center gap-3 rounded-lg border border-border bg-background px-3 py-2 transition " + (dragging ? "opacity-40 " : "") + (over && !dragging ? "ring-2 ring-primary/50 " : "") + (grabbed ? "ring-2 ring-primary " : "") + (!visible ? "opacity-60 " : ""),
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
									type: "button",
									ref: (el) => {
										handleRefs.current[id] = el;
									},
									disabled: meta.pinned,
									"aria-disabled": meta.pinned,
									"aria-describedby": "reorder-instructions",
									"aria-pressed": grabbed,
									"aria-label": meta.pinned ? `${meta.label} is pinned and cannot be reordered` : grabbed ? `${meta.label}, grabbed. Position ${reorderablePosition}. Use arrow keys to move.` : `Reorder ${meta.label}. Position ${reorderablePosition}. Press space to pick up.`,
									onKeyDown: (e) => onHandleKeyDown(e, index),
									onBlur: () => {
										if (grabbedIndex === index) {
											setGrabbedIndex(null);
											setAnnouncement("Reorder cancelled.");
										}
									},
									className: "flex h-6 w-6 items-center justify-center rounded text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring " + (meta.pinned ? "cursor-not-allowed opacity-30" : "cursor-grab active:cursor-grabbing hover:bg-secondary"),
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(GripVertical, {
										className: "h-4 w-4",
										"aria-hidden": "true"
									})
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "min-w-0 flex-1",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
										className: "flex items-center gap-2",
										children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
											className: "text-sm font-medium text-foreground",
											children: meta.label
										}), meta.pinned ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
											className: "rounded-full bg-secondary px-1.5 py-0.5 text-[10px] uppercase tracking-wider text-muted-foreground",
											children: "Pinned"
										}) : null]
									}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
										className: "truncate text-xs text-muted-foreground",
										children: meta.description
									})]
								}),
								!meta.pinned ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "flex items-center gap-1",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
										type: "button",
										onClick: () => moveByKeyboard(index, -1),
										disabled: index <= pinnedCount,
										"aria-label": `Move ${meta.label} up`,
										className: "flex h-7 w-7 items-center justify-center rounded text-muted-foreground transition hover:bg-secondary hover:text-foreground disabled:opacity-30 disabled:hover:bg-transparent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
										children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowUp, {
											className: "h-3.5 w-3.5",
											"aria-hidden": "true"
										})
									}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
										type: "button",
										onClick: () => moveByKeyboard(index, 1),
										disabled: index >= allOrderedIds.length - 1,
										"aria-label": `Move ${meta.label} down`,
										className: "flex h-7 w-7 items-center justify-center rounded text-muted-foreground transition hover:bg-secondary hover:text-foreground disabled:opacity-30 disabled:hover:bg-transparent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
										children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowDown, {
											className: "h-3.5 w-3.5",
											"aria-hidden": "true"
										})
									})]
								}) : null,
								meta.pinned ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Eye, {
									className: "h-4 w-4 text-muted-foreground",
									"aria-label": "Always visible"
								}) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "flex items-center gap-2",
									children: [visible ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Eye, {
										className: "h-4 w-4 text-muted-foreground",
										"aria-hidden": "true"
									}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EyeOff, {
										className: "h-4 w-4 text-muted-foreground",
										"aria-hidden": "true"
									}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Switch, {
										checked: visible,
										onCheckedChange: () => toggle(id),
										"aria-label": `${meta.label} visible on dashboard`
									})]
								})
							]
						}, id);
					})
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "mt-6 text-[11px] text-muted-foreground",
					children: "Tip: layouts are saved separately for each industry, so Accounting and Real Estate can have completely different dashboards."
				})
			]
		})]
	});
}
function IndustryKpis() {
	const { industry } = useIndustry();
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "industry-kpis",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: industry.name,
			title: "Operating KPIs",
			subtitle: industry.tagline,
			right: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Chip, {
				status: "primary",
				children: [industry.kpis.length, " metrics"]
			})
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "grid gap-3 sm:grid-cols-2 lg:grid-cols-3",
			children: industry.kpis.map((k) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "rounded-lg border border-border/70 bg-background/60 p-4",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between text-[11px] uppercase tracking-[0.14em] text-muted-foreground",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: k.label }), k.flag ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: k.flag }) : null]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-2 font-display text-3xl text-foreground",
						children: k.value
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mt-1 flex items-center gap-1 text-xs text-muted-foreground",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(TrendArrow, { trend: k.trend }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: k.delta })]
					})
				]
			}, k.label))
		})]
	});
}
function IndustryModulesGrid() {
	const { industry } = useIndustry();
	if (industry.modules.length === 0) return null;
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		id: "industry-modules",
		className: "grid gap-6 lg:grid-cols-2",
		children: industry.modules.map((mod) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
			id: mod.id,
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
				title: mod.title,
				subtitle: mod.subtitle,
				right: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, { children: mod.rows.length })
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "overflow-hidden rounded-lg border border-border/70",
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("table", {
					className: "w-full text-sm",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("thead", {
						className: "bg-secondary/60 text-[11px] uppercase tracking-[0.12em] text-muted-foreground",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tr", { children: mod.columns.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2 text-left font-medium",
							children: c
						}, c)) })
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", { children: mod.rows.map((r, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", {
						className: "border-t border-border/60 align-top",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("td", {
								className: "px-3 py-2.5",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
									className: "font-medium text-foreground",
									children: r.primary
								}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
									className: "text-xs text-muted-foreground",
									children: r.secondary
								})]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
								className: "px-3 py-2.5 text-muted-foreground",
								children: r.secondary.split(" · ")[0]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
								className: "px-3 py-2.5 font-medium text-foreground",
								children: r.value
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
								className: "px-3 py-2.5",
								children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "flex items-center gap-2",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: r.status }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
										className: "text-xs text-muted-foreground",
										children: r.note
									})]
								})
							})
						]
					}, i)) })]
				})
			})]
		}, mod.id))
	});
}
function IndustryPlaybooks() {
	const { industry } = useIndustry();
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "industry-playbooks",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			title: "Recommended plays",
			subtitle: `Tailored for ${industry.name.toLowerCase()}`
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
			className: "space-y-3",
			children: industry.playbooks.map((p) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
				className: "flex items-start justify-between gap-4 rounded-lg border border-border/70 p-3",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "min-w-0",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "font-medium text-foreground",
						children: p.title
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "text-xs text-muted-foreground",
						children: p.rationale
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Chip, {
					status: p.impact === "High" ? "primary" : p.impact === "Medium" ? "watch" : "neutral",
					children: [p.impact, " impact"]
				})]
			}, p.title))
		})]
	});
}
function HeroSection() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Card, {
		id: "hero",
		className: "relative overflow-hidden p-6 sm:p-8",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "grid gap-6 lg:grid-cols-[1.1fr_1fr] lg:items-center",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mb-2 flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.18em] text-muted-foreground",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "inline-block size-1.5 rounded-full bg-healthy" }), "Today · Strategic Pulse"]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h1", {
					className: "font-display text-4xl leading-[1.05] text-foreground sm:text-5xl lg:text-6xl",
					children: [
						"Your day is ",
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-primary",
							children: "on plan"
						}),
						", with two moments that need your attention."
					]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "mt-4 max-w-xl text-base text-muted-foreground sm:text-lg",
					children: dayScore.pulse
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-6 flex flex-wrap items-center gap-2",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
							status: "primary",
							children: "3 enterprise deals advanced"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
							status: "watch",
							children: "2 renewals need exec touch"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
							status: "healthy",
							children: "Forecast confidence 78%"
						})
					]
				})
			] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "card-surface relative p-6",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-baseline gap-3",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "font-display text-7xl leading-none text-foreground",
							children: dayScore.score
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "text-sm font-medium text-healthy",
							children: [
								"+",
								dayScore.delta,
								" vs yesterday"
							]
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-1 text-xs uppercase tracking-[0.14em] text-muted-foreground",
						children: "Day Score"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-6 grid grid-cols-2 gap-3",
						children: dayScore.readiness.map((r) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "rounded-lg border border-border bg-surface-muted p-3",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "flex items-center justify-between",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "text-[11px] uppercase tracking-wider text-muted-foreground",
									children: r.label
								}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: r.status })]
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mt-1 font-display text-2xl text-foreground",
								children: typeof r.value === "number" && r.value < 1 ? `${Math.round(r.value * 100)}%` : r.value
							})]
						}, r.label))
					})
				]
			})]
		})
	});
}
function ActionRegister() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "actions",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Operating cadence",
			title: "Action Register",
			subtitle: "What only you can do today.",
			right: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Chip, {
				status: "primary",
				children: [actions.length, " open"]
			})
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
			className: "divide-y divide-border",
			children: actions.map((a) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
				className: "flex items-center justify-between gap-3 py-3 first:pt-0 last:pb-0",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "flex min-w-0 items-center gap-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: a.status }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "min-w-0",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "truncate text-sm font-medium text-foreground",
							children: a.title
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "text-xs text-muted-foreground",
							children: [
								a.owner,
								" · ",
								a.due
							]
						})]
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
					status: a.priority === "P0" ? "risk" : a.priority === "P1" ? "watch" : "neutral",
					children: a.priority
				})]
			}, a.id))
		})]
	});
}
function FollowUpAutopilot() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "followups",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Autopilot",
			title: "Follow-up Autopilot",
			subtitle: "Drafts queued and waiting for your nod.",
			right: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
				status: "healthy",
				children: "All drafted"
			})
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
			className: "space-y-3",
			children: followUps.map((f) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
				className: "rounded-lg border border-border bg-surface-muted p-3",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between gap-2",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "text-sm font-medium text-foreground",
							children: [
								f.contact,
								" ",
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
									className: "text-muted-foreground",
									children: ["· ", f.company]
								})
							]
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
							status: "neutral",
							children: f.channel
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-1 text-sm text-muted-foreground",
						children: f.draft
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mt-2 flex items-center justify-between text-xs text-muted-foreground",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: ["Scheduled ", f.scheduled] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
							className: "font-medium text-primary hover:underline",
							children: "Review draft →"
						})]
					})
				]
			}, f.id))
		})]
	});
}
function MeetingToExecution() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "meetings",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "From talk to action",
			title: "Meeting to Execution",
			subtitle: "Decisions and actions captured automatically."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
			className: "space-y-3",
			children: meetings.map((m) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
				className: "flex items-center justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "min-w-0",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "truncate text-sm font-medium text-foreground",
						children: m.title
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "text-xs text-muted-foreground",
						children: [
							m.attendees.join(" · "),
							" · ",
							m.time
						]
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "flex shrink-0 items-center gap-2",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Chip, {
						status: "primary",
						children: [m.decisions, " decisions"]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Chip, {
						status: "healthy",
						children: [m.actions, " actions"]
					})]
				})]
			}, m.id))
		})]
	});
}
function CustomerHealthRadar() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "health",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Customer signal",
			title: "Customer Health Radar",
			subtitle: "Composite signal across product, support, and exec engagement."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "overflow-hidden rounded-lg border border-border",
			children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("table", {
				className: "w-full text-sm",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("thead", {
					className: "bg-surface-muted text-left text-xs uppercase tracking-wider text-muted-foreground",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2",
							children: "Account"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2",
							children: "ARR"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2",
							children: "Signal"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2 hidden md:table-cell",
							children: "Owner"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2 text-right",
							children: "Last touch"
						})
					] })
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", { children: accountHealth.map((a) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", {
					className: "border-t border-border",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
							className: "px-3 py-3",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "flex items-center gap-2",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: a.status }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "font-medium text-foreground",
									children: a.account
								})]
							})
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
							className: "px-3 py-3 text-muted-foreground",
							children: a.arr
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
							className: "px-3 py-3 text-muted-foreground",
							children: a.signal
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
							className: "px-3 py-3 hidden text-muted-foreground md:table-cell",
							children: a.owner
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
							className: "px-3 py-3 text-right text-muted-foreground",
							children: a.lastTouch
						})
					]
				}, a.account)) })]
			})
		})]
	});
}
function PipelineRiskRadar() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "pipeline-risk",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Forecast hygiene",
			title: "Pipeline Risk Radar",
			subtitle: "Deals trending sideways before they slip."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
			className: "space-y-3",
			children: pipelineRisks.map((p) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
				className: "flex items-start justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "min-w-0",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center gap-2",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: p.risk }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-sm font-medium text-foreground",
							children: p.deal
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mt-1 text-xs text-muted-foreground",
						children: [
							p.stage,
							" · ",
							p.reason
						]
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "font-display text-lg text-foreground",
					children: p.value
				})]
			}, p.deal))
		})]
	});
}
function ApprovalWorkflow() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "approvals",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Decision queue",
			title: "Approval Workflow",
			subtitle: "Cleared in one screen, with context."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
			className: "divide-y divide-border",
			children: approvals.map((a) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
				className: "grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3 py-3 first:pt-0 last:pb-0",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "min-w-0",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "truncate text-sm font-medium text-foreground",
						children: a.title
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "text-xs text-muted-foreground",
						children: [
							a.requester,
							" · ",
							a.amount,
							" · ",
							a.age,
							" old"
						]
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
					status: a.status === "Approved" ? "healthy" : a.status === "Blocked" ? "risk" : "watch",
					children: a.status
				})]
			}, a.id))
		})]
	});
}
function EmailSentiment() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "sentiment",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Relationship signal",
			title: "Email Sentiment",
			subtitle: "How key threads are actually trending."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
			className: "space-y-2",
			children: sentiment.map((s) => {
				const pct = Math.round((s.score + 1) / 2 * 100);
				const color = s.score > .25 ? "bg-healthy" : s.score < -.1 ? "bg-risk" : "bg-watch";
				return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
					className: "rounded-lg border border-border bg-surface-muted p-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between gap-2",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "min-w-0",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "truncate text-sm font-medium text-foreground",
								children: s.thread
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "text-xs text-muted-foreground",
								children: [
									s.account,
									" · ",
									s.lastReply
								]
							})]
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex shrink-0 items-center gap-2 text-xs text-muted-foreground",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(TrendArrow, { trend: s.trend }), Math.round(s.score * 100)]
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-2 h-1.5 w-full overflow-hidden rounded-full bg-border",
						role: "progressbar",
						"aria-valuenow": pct,
						"aria-valuemin": 0,
						"aria-valuemax": 100,
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: `h-full ${color}`,
							style: { width: `${pct}%` }
						})
					})]
				}, s.thread);
			})
		})]
	});
}
function Recommendations() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "recommendations",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Next best moves",
			title: "Recommendations",
			subtitle: "Ranked by impact and effort, not noise."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
			className: "grid gap-3 md:grid-cols-2",
			children: recommendations.map((r) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
				className: "rounded-lg border border-border bg-surface-muted p-4",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between gap-2",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "text-sm font-semibold text-foreground",
							children: r.title
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Chip, {
							status: r.impact === "High" ? "primary" : "neutral",
							children: [r.impact, " impact"]
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-1 text-sm text-muted-foreground",
						children: r.rationale
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mt-3 flex items-center justify-between text-xs text-muted-foreground",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: ["Effort: ", r.effort] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
							className: "font-medium text-primary hover:underline",
							children: "Run play →"
						})]
					})
				]
			}, r.id))
		})]
	});
}
function KpiDigest() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "kpi",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "What moved",
			title: "KPI Digest",
			subtitle: "Trend, delta, and flags at a glance."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "grid grid-cols-2 gap-3 md:grid-cols-3",
			children: kpis.map((k) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "rounded-lg border border-border bg-surface-muted p-4",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-[11px] uppercase tracking-wider text-muted-foreground",
							children: k.label
						}), k.flag ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: k.flag }) : null]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-1 font-display text-3xl text-foreground",
						children: k.value
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mt-1 flex items-center gap-1 text-xs text-muted-foreground",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(TrendArrow, { trend: k.trend }),
							" ",
							k.delta
						]
					})
				]
			}, k.label))
		})]
	});
}
function CommunicationTimeline() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "timeline",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Across accounts",
			title: "Communication Timeline",
			subtitle: "Today, in chronological order."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ol", {
			className: "relative ml-3 space-y-4 border-l border-border pl-5",
			children: timeline.map((t) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
				className: "relative",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
						className: "absolute -left-[26px] top-1 grid size-4 place-items-center rounded-full border border-border bg-surface",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "size-1.5 rounded-full bg-primary" })
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center gap-2 text-xs text-muted-foreground",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "font-mono",
								children: t.time
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
								status: "neutral",
								children: t.type
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: ["· ", t.account] })
						]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-1 text-sm text-foreground",
						children: t.summary
					})
				]
			}, t.id))
		})]
	});
}
function RevenueForecast() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "forecast",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Revenue",
			title: "Revenue Forecast",
			subtitle: "Committed, best case, and pipeline by window."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "grid gap-3 md:grid-cols-3",
			children: forecast.map((f) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "rounded-xl border border-border bg-gradient-to-br from-surface to-surface-muted p-5",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
							className: "text-[11px] uppercase tracking-[0.16em] text-muted-foreground",
							children: ["Next ", f.window]
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Chip, {
							status: f.confidence > .75 ? "healthy" : f.confidence > .65 ? "watch" : "risk",
							children: [Math.round(f.confidence * 100), "% conf"]
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-3 font-display text-4xl text-foreground",
						children: f.committed
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-1 text-xs text-muted-foreground",
						children: "committed"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mt-4 space-y-1 text-sm",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex justify-between",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-muted-foreground",
								children: "Best case"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-foreground",
								children: f.best
							})]
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex justify-between",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-muted-foreground",
								children: "Pipeline"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-foreground",
								children: f.pipeline
							})]
						})]
					})
				]
			}, f.window))
		})]
	});
}
function DealProgression() {
	const onTrack = deals.filter((d) => d.movement === "on-track");
	const stuck = deals.filter((d) => d.movement === "stuck");
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "deals",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Deal motion",
			title: "Deal Progression",
			subtitle: "Where momentum is, and where it isn't."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "grid gap-4 md:grid-cols-2",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "mb-2 flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: "healthy" }),
					" On track (",
					onTrack.length,
					")"
				]
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
				className: "space-y-2",
				children: onTrack.map((d) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
					className: "rounded-lg border border-border bg-surface-muted p-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-sm font-medium text-foreground",
							children: d.name
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-sm text-foreground",
							children: d.value
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "text-xs text-muted-foreground",
						children: [
							d.stage,
							" · ",
							d.days,
							"d in stage"
						]
					})]
				}, d.name))
			})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "mb-2 flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: "risk" }),
					" Stuck (",
					stuck.length,
					")"
				]
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
				className: "space-y-2",
				children: stuck.map((d) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
					className: "rounded-lg border border-border bg-surface-muted p-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-sm font-medium text-foreground",
							children: d.name
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-sm text-foreground",
							children: d.value
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "text-xs text-muted-foreground",
						children: [
							d.stage,
							" · ",
							d.days,
							"d in stage"
						]
					})]
				}, d.name))
			})] })]
		})]
	});
}
function RenewalReminders() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "renewals",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Retention",
			title: "Renewal Reminders",
			subtitle: "Where renewal attention is needed, in order."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "grid gap-4 md:grid-cols-3",
			children: [
				{
					label: "Overdue",
					bucket: "overdue",
					status: "risk"
				},
				{
					label: "This month",
					bucket: "this-month",
					status: "watch"
				},
				{
					label: "Upcoming",
					bucket: "upcoming",
					status: "healthy"
				}
			].map((g) => {
				const rows = renewals.filter((r) => r.bucket === g.bucket);
				return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mb-2 flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: g.status }),
						" ",
						g.label,
						" (",
						rows.length,
						")"
					]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "space-y-2",
					children: rows.map((r) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "rounded-lg border border-border bg-surface-muted p-3",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex items-center justify-between",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-sm font-medium text-foreground",
								children: r.account
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-sm text-foreground",
								children: r.arr
							})]
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "text-xs text-muted-foreground",
							children: [
								r.date,
								" · ",
								r.owner
							]
						})]
					}, r.account))
				})] }, g.bucket);
			})
		})]
	});
}
function BriefingPreview() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "briefing",
		className: "bg-gradient-to-br from-surface to-primary-soft/40",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
				eyebrow: "Morning briefing",
				title: "Today's Executive Briefing",
				subtitle: briefing.prepared,
				right: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Chip, {
					status: "primary",
					children: "Auto-prepared"
				})
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "font-display text-2xl leading-snug text-foreground",
				children: briefing.headline
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
				className: "mt-4 space-y-3",
				children: briefing.bullets.map((b, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
					className: "flex gap-3 text-sm text-foreground",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "mt-1.5 size-1.5 shrink-0 rounded-full bg-primary" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: b })]
				}, i))
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "mt-5 flex flex-wrap gap-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
					className: "rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground transition hover:opacity-90",
					children: "Open full briefing"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
					className: "rounded-md border border-border bg-surface px-3 py-2 text-sm font-medium text-foreground transition hover:border-foreground/30",
					children: "Share with team"
				})]
			})
		]
	});
}
function WeeklyPerformanceTable() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "weekly",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Team",
			title: "Weekly Performance",
			subtitle: "Pace against plan and pipeline contribution."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "overflow-hidden rounded-lg border border-border",
			children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("table", {
				className: "w-full text-sm",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("thead", {
					className: "bg-surface-muted text-left text-xs uppercase tracking-wider text-muted-foreground",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2",
							children: "Rep"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2",
							children: "Meetings"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2",
							children: "Pipeline"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2",
							children: "Won"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
							className: "px-3 py-2 text-right",
							children: "Attainment"
						})
					] })
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", { children: weekly.map((r) => {
					const a = Math.round(r.attainment * 100);
					const status = r.attainment >= 1 ? "healthy" : r.attainment >= .85 ? "watch" : "risk";
					return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", {
						className: "border-t border-border",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
								className: "px-3 py-3 font-medium text-foreground",
								children: r.rep
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
								className: "px-3 py-3 text-muted-foreground",
								children: r.meetings
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
								className: "px-3 py-3 text-muted-foreground",
								children: r.pipeline
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
								className: "px-3 py-3 text-muted-foreground",
								children: r.won
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
								className: "px-3 py-3 text-right",
								children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Chip, {
									status,
									children: [a, "%"]
								})
							})
						]
					}, r.rep);
				}) })]
			})
		})]
	});
}
function ProductReadiness() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Card, {
		id: "readiness",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CardHeader, {
			eyebrow: "Surfaces",
			title: "Product Readiness",
			subtitle: "Generated views, fresh and linked."
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
			className: "grid gap-2 sm:grid-cols-2",
			children: surfaces.map((s) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("a", {
				href: s.href,
				className: "flex items-center justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3 transition hover:border-foreground/20",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "flex min-w-0 items-center gap-2",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Dot, { status: s.status }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "min-w-0",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "truncate text-sm font-medium text-foreground",
							children: s.name
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "text-xs text-muted-foreground",
							children: ["Updated ", s.updated]
						})]
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "text-primary",
					children: "→"
				})]
			}) }, s.name))
		})]
	});
}
function renderModule(id) {
	switch (id) {
		case "hero": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(HeroSection, {});
		case "industry-kpis": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(IndustryKpis, {});
		case "industry-modules": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(IndustryModulesGrid, {});
		case "industry-playbooks": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(IndustryPlaybooks, {});
		case "connectors": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ConnectorsPanel, {});
		case "briefing": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(BriefingPreview, {});
		case "actions": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ActionRegister, {});
		case "followups": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(FollowUpAutopilot, {});
		case "meetings": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(MeetingToExecution, {});
		case "kpi": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(KpiDigest, {});
		case "forecast": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(RevenueForecast, {});
		case "pipeline-risk": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(PipelineRiskRadar, {});
		case "deals": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(DealProgression, {});
		case "health": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(CustomerHealthRadar, {});
		case "sentiment": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmailSentiment, {});
		case "recommendations": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Recommendations, {});
		case "renewals": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(RenewalReminders, {});
		case "timeline": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(CommunicationTimeline, {});
		case "approvals": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ApprovalWorkflow, {});
		case "weekly": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(WeeklyPerformanceTable, {});
		case "readiness": return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ProductReadiness, {});
		default: return null;
	}
}
function Dashboard() {
	const { orderedIds } = useDashboardLayout();
	const heroId = "hero";
	const hero = orderedIds.find((id) => id === heroId);
	const rest = orderedIds.filter((id) => id !== heroId);
	const jumpItems = orderedIds.map((id) => {
		return {
			id,
			label: DASHBOARD_MODULES.find((m) => m.id === id)?.label ?? id
		};
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Shell, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			hero ? renderModule(hero) : null,
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "flex items-center justify-between gap-3",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "min-w-0 flex-1",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SectionJump, { items: jumpItems.filter((i) => i.id !== heroId) })
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "shrink-0 pt-2",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(CustomizePanel, {})
				})]
			}),
			rest.map((id) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_react.Fragment, { children: renderModule(id) }, id))
		]
	}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ProductTour, {})] });
}
//#endregion
export { Dashboard as component };
