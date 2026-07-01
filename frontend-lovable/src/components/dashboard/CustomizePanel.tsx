import { useEffect, useRef, useState, type KeyboardEvent } from "react";
import {
  ArrowDown,
  ArrowUp,
  Eye,
  EyeOff,
  GripVertical,
  RotateCcw,
  SlidersHorizontal,
} from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Switch } from "@/components/ui/switch";
import { useDashboardLayout } from "@/context/DashboardLayoutContext";
import { useIndustry } from "@/context/IndustryContext";
import { DASHBOARD_MODULES, type ModuleId } from "@/data/dashboardModules";

function moduleMeta(id: ModuleId) {
  return DASHBOARD_MODULES.find((m) => m.id === id)!;
}

export function CustomizePanel() {
  const { allOrderedIds, isVisible, toggle, reorder, reset } =
    useDashboardLayout();
  const { industry } = useIndustry();

  // Pointer drag state
  const [dragIndex, setDragIndex] = useState<number | null>(null);
  const [overIndex, setOverIndex] = useState<number | null>(null);

  // Keyboard "grab" state — WAI-ARIA drag-and-drop pattern.
  // When a handle is activated with Space/Enter, subsequent Arrow keys
  // move the item; Space/Enter drops; Escape cancels.
  const [grabbedIndex, setGrabbedIndex] = useState<number | null>(null);
  const [announcement, setAnnouncement] = useState("");
  const handleRefs = useRef<Record<string, HTMLButtonElement | null>>({});

  // After a keyboard reorder, restore focus to the moved item's handle.
  const pendingFocusId = useRef<ModuleId | null>(null);
  useEffect(() => {
    if (pendingFocusId.current) {
      const el = handleRefs.current[pendingFocusId.current];
      el?.focus();
      pendingFocusId.current = null;
    }
  }, [allOrderedIds]);

  const pinnedCount = allOrderedIds.filter(
    (id) => moduleMeta(id).pinned,
  ).length;

  const onPointerDrop = (target: number) => {
    if (dragIndex === null) return;
    reorder(dragIndex, target);
    setDragIndex(null);
    setOverIndex(null);
  };

  const moveByKeyboard = (from: number, direction: -1 | 1) => {
    const id = allOrderedIds[from];
    if (!id) return;
    const meta = moduleMeta(id);
    if (meta.pinned) return;
    const to = from + direction;
    if (to < pinnedCount || to >= allOrderedIds.length) return;
    pendingFocusId.current = id;
    reorder(from, to);
    setAnnouncement(
      `${meta.label} moved to position ${to - pinnedCount + 1} of ${
        allOrderedIds.length - pinnedCount
      }.`,
    );
  };

  const onHandleKeyDown = (
    event: KeyboardEvent<HTMLButtonElement>,
    index: number,
  ) => {
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
        setAnnouncement(
          `${meta.label} grabbed. Use arrow keys to move, space to drop, escape to cancel.`,
        );
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
      // Only reorder when the item is actively "grabbed" — otherwise let
      // the browser handle normal focus traversal.
      if (grabbedIndex !== index) return;
      event.preventDefault();
      moveByKeyboard(index, event.key === "ArrowUp" ? -1 : 1);
    }
  };

  return (
    <Sheet
      onOpenChange={(open) => {
        if (!open) {
          setGrabbedIndex(null);
          setAnnouncement("");
        }
      }}
    >
      <SheetTrigger asChild>
        <button
          type="button"
          className="inline-flex items-center gap-2 rounded-md border border-border bg-background px-3 py-1.5 text-xs font-medium text-foreground transition hover:bg-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        >
          <SlidersHorizontal className="h-3.5 w-3.5" aria-hidden="true" />
          Customize
        </button>
      </SheetTrigger>
      <SheetContent side="right" className="w-full sm:max-w-md overflow-y-auto">
        <SheetHeader>
          <SheetTitle>Customize dashboard</SheetTitle>
          <SheetDescription>
            Toggle and reorder modules for the <b>{industry.name}</b> workspace.
            Changes save automatically and apply only to this industry.
          </SheetDescription>
        </SheetHeader>

        <p
          id="reorder-instructions"
          className="mt-3 text-[11px] text-muted-foreground"
        >
          Drag a handle, or focus a handle and press Space to pick up a module,
          then Arrow Up / Arrow Down to move it, Space to drop, Escape to
          cancel.
        </p>

        <div
          role="status"
          aria-live="polite"
          aria-atomic="true"
          className="sr-only"
        >
          {announcement}
        </div>

        <div className="mt-4 flex items-center justify-between text-xs text-muted-foreground">
          <span>{allOrderedIds.length} modules</span>
          <button
            type="button"
            onClick={reset}
            className="inline-flex items-center gap-1 rounded-md border border-border px-2 py-1 text-foreground transition hover:bg-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            <RotateCcw className="h-3 w-3" aria-hidden="true" />
            Reset to default
          </button>
        </div>

        <ul
          className="mt-4 space-y-1.5"
          aria-label="Dashboard modules, reorderable"
        >
          {allOrderedIds.map((id, index) => {
            const meta = moduleMeta(id);
            const visible = isVisible(id);
            const dragging = dragIndex === index;
            const over = overIndex === index;
            const grabbed = grabbedIndex === index;
            const reorderablePosition = meta.pinned
              ? null
              : `${index - pinnedCount + 1} of ${
                  allOrderedIds.length - pinnedCount
                }`;

            return (
              <li
                key={id}
                draggable={!meta.pinned}
                onDragStart={(e) => {
                  if (meta.pinned) {
                    e.preventDefault();
                    return;
                  }
                  setDragIndex(index);
                  e.dataTransfer.effectAllowed = "move";
                }}
                onDragOver={(e) => {
                  e.preventDefault();
                  setOverIndex(index);
                }}
                onDragLeave={() =>
                  setOverIndex((cur) => (cur === index ? null : cur))
                }
                onDrop={(e) => {
                  e.preventDefault();
                  onPointerDrop(index);
                }}
                onDragEnd={() => {
                  setDragIndex(null);
                  setOverIndex(null);
                }}
                className={
                  "flex items-center gap-3 rounded-lg border border-border bg-background px-3 py-2 transition " +
                  (dragging ? "opacity-40 " : "") +
                  (over && !dragging ? "ring-2 ring-primary/50 " : "") +
                  (grabbed ? "ring-2 ring-primary " : "") +
                  (!visible ? "opacity-60 " : "")
                }
              >
                <button
                  type="button"
                  ref={(el) => {
                    handleRefs.current[id] = el;
                  }}
                  disabled={meta.pinned}
                  aria-disabled={meta.pinned}
                  aria-describedby="reorder-instructions"
                  aria-pressed={grabbed}
                  aria-label={
                    meta.pinned
                      ? `${meta.label} is pinned and cannot be reordered`
                      : grabbed
                        ? `${meta.label}, grabbed. Position ${reorderablePosition}. Use arrow keys to move.`
                        : `Reorder ${meta.label}. Position ${reorderablePosition}. Press space to pick up.`
                  }
                  onKeyDown={(e) => onHandleKeyDown(e, index)}
                  onBlur={() => {
                    if (grabbedIndex === index) {
                      setGrabbedIndex(null);
                      setAnnouncement("Reorder cancelled.");
                    }
                  }}
                  className={
                    "flex h-6 w-6 items-center justify-center rounded text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring " +
                    (meta.pinned
                      ? "cursor-not-allowed opacity-30"
                      : "cursor-grab active:cursor-grabbing hover:bg-secondary")
                  }
                >
                  <GripVertical className="h-4 w-4" aria-hidden="true" />
                </button>

                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-foreground">
                      {meta.label}
                    </span>
                    {meta.pinned ? (
                      <span className="rounded-full bg-secondary px-1.5 py-0.5 text-[10px] uppercase tracking-wider text-muted-foreground">
                        Pinned
                      </span>
                    ) : null}
                  </div>
                  <div className="truncate text-xs text-muted-foreground">
                    {meta.description}
                  </div>
                </div>

                {!meta.pinned ? (
                  <div className="flex items-center gap-1">
                    <button
                      type="button"
                      onClick={() => moveByKeyboard(index, -1)}
                      disabled={index <= pinnedCount}
                      aria-label={`Move ${meta.label} up`}
                      className="flex h-7 w-7 items-center justify-center rounded text-muted-foreground transition hover:bg-secondary hover:text-foreground disabled:opacity-30 disabled:hover:bg-transparent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                    >
                      <ArrowUp className="h-3.5 w-3.5" aria-hidden="true" />
                    </button>
                    <button
                      type="button"
                      onClick={() => moveByKeyboard(index, 1)}
                      disabled={index >= allOrderedIds.length - 1}
                      aria-label={`Move ${meta.label} down`}
                      className="flex h-7 w-7 items-center justify-center rounded text-muted-foreground transition hover:bg-secondary hover:text-foreground disabled:opacity-30 disabled:hover:bg-transparent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                    >
                      <ArrowDown className="h-3.5 w-3.5" aria-hidden="true" />
                    </button>
                  </div>
                ) : null}

                {meta.pinned ? (
                  <Eye
                    className="h-4 w-4 text-muted-foreground"
                    aria-label="Always visible"
                  />
                ) : (
                  <div className="flex items-center gap-2">
                    {visible ? (
                      <Eye
                        className="h-4 w-4 text-muted-foreground"
                        aria-hidden="true"
                      />
                    ) : (
                      <EyeOff
                        className="h-4 w-4 text-muted-foreground"
                        aria-hidden="true"
                      />
                    )}
                    <Switch
                      checked={visible}
                      onCheckedChange={() => toggle(id)}
                      aria-label={`${meta.label} visible on dashboard`}
                    />
                  </div>
                )}
              </li>
            );
          })}
        </ul>

        <p className="mt-6 text-[11px] text-muted-foreground">
          Tip: layouts are saved separately for each industry, so Accounting and
          Real Estate can have completely different dashboards.
        </p>
      </SheetContent>
    </Sheet>
  );
}
