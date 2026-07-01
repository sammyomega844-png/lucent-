import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useIndustry } from "./IndustryContext";
import type { IndustryId } from "@/data/industries";
import {
  DASHBOARD_MODULES,
  defaultOrderFor,
  modulesForIndustry,
  type DashboardModule,
  type ModuleId,
} from "@/data/dashboardModules";

interface IndustryLayout {
  order: ModuleId[];
  hidden: ModuleId[];
}

type LayoutMap = Partial<Record<IndustryId, IndustryLayout>>;

interface Ctx {
  modules: DashboardModule[]; // available for current industry (any order)
  orderedIds: ModuleId[]; // visible modules in saved order
  allOrderedIds: ModuleId[]; // all modules (visible + hidden) in saved order
  isVisible: (id: ModuleId) => boolean;
  toggle: (id: ModuleId) => void;
  reorder: (from: number, to: number) => void;
  reset: () => void;
}

const LayoutCtx = createContext<Ctx | null>(null);
const STORAGE_KEY = "lucent.layout.v1";

function loadMap(): LayoutMap {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return {};
    return JSON.parse(raw) as LayoutMap;
  } catch {
    return {};
  }
}

function saveMap(map: LayoutMap) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(map));
  } catch {
    // ignore
  }
}

/** Reconcile a stored layout with the registry:
 *  - drop ids that no longer exist for this industry
 *  - append any new registry ids to the end
 *  - keep pinned modules always first and visible
 */
function reconcile(
  industryId: IndustryId,
  stored?: IndustryLayout,
): IndustryLayout {
  const available = modulesForIndustry(industryId);
  const availableIds = new Set(available.map((m) => m.id));
  const pinnedIds = available.filter((m) => m.pinned).map((m) => m.id);

  const baseOrder = stored?.order?.filter((id) => availableIds.has(id)) ?? [];
  const missing = available
    .map((m) => m.id)
    .filter((id) => !baseOrder.includes(id));
  let order = [...baseOrder, ...missing];

  // Ensure pinned come first, in registry order.
  order = [...pinnedIds, ...order.filter((id) => !pinnedIds.includes(id))];

  const hidden = (stored?.hidden ?? []).filter(
    (id) => availableIds.has(id) && !pinnedIds.includes(id),
  );

  return { order, hidden };
}

export function DashboardLayoutProvider({ children }: { children: ReactNode }) {
  const { industryId } = useIndustry();
  const [map, setMap] = useState<LayoutMap>({});

  useEffect(() => {
    setMap(loadMap());
  }, []);

  const layout = useMemo(
    () => reconcile(industryId, map[industryId]),
    [industryId, map],
  );

  const persist = useCallback(
    (next: IndustryLayout) => {
      setMap((prev) => {
        const updated = { ...prev, [industryId]: next };
        saveMap(updated);
        return updated;
      });
    },
    [industryId],
  );

  const toggle = useCallback(
    (id: ModuleId) => {
      const mod = DASHBOARD_MODULES.find((m) => m.id === id);
      if (!mod || mod.pinned) return;
      const isHidden = layout.hidden.includes(id);
      persist({
        order: layout.order,
        hidden: isHidden
          ? layout.hidden.filter((x) => x !== id)
          : [...layout.hidden, id],
      });
    },
    [layout, persist],
  );

  const reorder = useCallback(
    (from: number, to: number) => {
      if (from === to) return;
      const next = [...layout.order];
      const [moved] = next.splice(from, 1);
      if (!moved) return;
      // Prevent moving a non-pinned into the pinned prefix or vice versa.
      const mod = DASHBOARD_MODULES.find((m) => m.id === moved);
      if (mod?.pinned) return;
      const pinnedCount = layout.order.filter(
        (id) => DASHBOARD_MODULES.find((m) => m.id === id)?.pinned,
      ).length;
      const clampedTo = Math.max(pinnedCount, Math.min(to, next.length));
      next.splice(clampedTo, 0, moved);
      persist({ order: next, hidden: layout.hidden });
    },
    [layout, persist],
  );

  const reset = useCallback(() => {
    persist({ order: defaultOrderFor(industryId), hidden: [] });
  }, [industryId, persist]);

  const value = useMemo<Ctx>(() => {
    const hiddenSet = new Set(layout.hidden);
    return {
      modules: modulesForIndustry(industryId),
      orderedIds: layout.order.filter((id) => !hiddenSet.has(id)),
      allOrderedIds: layout.order,
      isVisible: (id) => !hiddenSet.has(id),
      toggle,
      reorder,
      reset,
    };
  }, [industryId, layout, toggle, reorder, reset]);

  return <LayoutCtx.Provider value={value}>{children}</LayoutCtx.Provider>;
}

export function useDashboardLayout(): Ctx {
  const ctx = useContext(LayoutCtx);
  if (!ctx)
    throw new Error(
      "useDashboardLayout must be used inside DashboardLayoutProvider",
    );
  return ctx;
}
