## Goal

Let users toggle, reorder, and save which dashboard modules show for each industry (Sales, Accounting, Real Estate, etc.). Preferences persist per industry in `localStorage` so switching workspaces restores that industry's saved layout.

## Scope

Frontend only. No changes to mock data shape or business logic — this is a presentation layer feature over the existing sections in `src/routes/index.tsx` and `IndustryModules.tsx`.

## What the user sees

1. A new **"Customize"** button in the dashboard header row (next to `SectionJump` / near the hero) opens a side panel (shadcn `Sheet`).
2. Panel lists every module available for the current industry with:
   - A visibility toggle (shadcn `Switch`).
   - Drag handle to reorder (native HTML5 drag-and-drop — no new dependency).
   - "Reset to default" and "Save" buttons.
3. Dashboard re-renders sections in the saved order, hiding disabled ones.
4. `SectionJump` pill nav reflects the same order/visibility.
5. Switching industries via `IndustrySwitcher` loads that industry's saved layout (or default if none saved).

## Technical design

### New file: `src/context/DashboardLayoutContext.tsx`

- Provides `{ layout, setVisible, reorder, reset, isVisible, orderedIds }` scoped to the current `industryId` (read from `useIndustry`).
- Shape stored: `Record<IndustryId, { order: string[]; hidden: string[] }>` under key `lucent.layout.v1`.
- Defaults derived from a per-industry module registry (see below).

### New file: `src/data/dashboardModules.ts`

- Central registry mapping `moduleId → { id, label, industries: IndustryId[] | "all" }`.
- Covers both the shared executive sections already in `sections.tsx` (hero, briefing, actions, pipeline-risk, forecast, etc.) and the industry-specific ones (`industry-kpis`, `industry-modules`, `industry-playbooks`, `connectors`).
- Per-industry default order = filter registry by industry.

### New file: `src/components/dashboard/CustomizePanel.tsx`

- shadcn `Sheet` triggered by a "Customize modules" button.
- Renders draggable list; uses HTML5 `draggable` + `onDragStart/onDragOver/onDrop` (kept simple, no `dnd-kit` dep).
- Calls context actions; shows a "Saved" toast via existing `sonner`.

### Edit: `src/routes/index.tsx`

- Replace the current hardcoded section order with a mapping loop driven by `orderedIds` from the layout context.
- Each `moduleId` maps to the JSX section component (small `renderModule(id)` switch).
- `JUMP_ITEMS` becomes derived from the same ordered/visible list.

### Edit: `src/components/dashboard/SectionJump.tsx`

- Accept `items` prop instead of hardcoded list (already close to this shape) so it reflects the live layout.

### Edit: `src/routes/__root.tsx`

- Wrap children in `DashboardLayoutProvider` (inside `IndustryProvider`) so context is available app-wide.

### Persistence

- `localStorage` key `lucent.layout.v1`, JSON-serialized. Guarded with try/catch (matches existing `IndustryContext` pattern).
- Migration: if key missing or industry entry missing, fall back to registry defaults.

## Out of scope

- Cross-device sync (no backend).
- Adding/removing modules that aren't already defined in mock data.
- Renaming modules.

## Acceptance

- Toggling a module off in Accounting hides it immediately and after reload.
- Reordering AR Aging above KPIs persists and reflects in `SectionJump`.
- Switching to Real Estate shows its own saved layout (independent from Accounting).
- "Reset to default" restores the industry's registry order.
