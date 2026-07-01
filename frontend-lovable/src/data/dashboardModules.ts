import type { IndustryId } from "./industries";

export type ModuleId =
  | "hero"
  | "industry-kpis"
  | "industry-modules"
  | "industry-playbooks"
  | "connectors"
  | "briefing"
  | "actions"
  | "followups"
  | "meetings"
  | "kpi"
  | "forecast"
  | "pipeline-risk"
  | "deals"
  | "health"
  | "sentiment"
  | "recommendations"
  | "renewals"
  | "timeline"
  | "approvals"
  | "weekly"
  | "readiness";

export interface DashboardModule {
  id: ModuleId;
  label: string;
  description: string;
  /** "all" or an explicit list of industries where this module is available. */
  industries: "all" | IndustryId[];
  /** Hero is pinned — cannot be hidden or reordered. */
  pinned?: boolean;
}

export const DASHBOARD_MODULES: DashboardModule[] = [
  {
    id: "hero",
    label: "Today's pulse",
    description: "Executive summary for the day",
    industries: "all",
    pinned: true,
  },
  {
    id: "industry-kpis",
    label: "Industry KPIs",
    description: "Operating metrics tuned to your workspace",
    industries: "all",
  },
  {
    id: "industry-modules",
    label: "Industry modules",
    description: "Workflows specific to this industry",
    industries: [
      "accounting",
      "real-estate",
      "professional-services",
      "healthcare",
      "ecommerce",
    ],
  },
  {
    id: "industry-playbooks",
    label: "Recommended plays",
    description: "Tailored recommendations",
    industries: "all",
  },
  {
    id: "connectors",
    label: "Connectors",
    description: "Quick access to data sources",
    industries: "all",
  },
  {
    id: "briefing",
    label: "Daily briefing",
    description: "Narrative morning briefing",
    industries: "all",
  },
  {
    id: "actions",
    label: "Action register",
    description: "Open actions across the team",
    industries: "all",
  },
  {
    id: "followups",
    label: "Follow-up autopilot",
    description: "Drafted follow-ups awaiting approval",
    industries: ["sales", "professional-services", "real-estate"],
  },
  {
    id: "meetings",
    label: "Meeting to execution",
    description: "Meeting outcomes converted to work",
    industries: "all",
  },
  {
    id: "kpi",
    label: "KPI digest",
    description: "Executive KPI snapshot",
    industries: "all",
  },
  {
    id: "forecast",
    label: "Revenue forecast",
    description: "Quarterly forecast with commit bands",
    industries: ["sales", "accounting", "professional-services", "ecommerce"],
  },
  {
    id: "pipeline-risk",
    label: "Pipeline risk radar",
    description: "Deals with slipping signals",
    industries: ["sales", "real-estate", "professional-services"],
  },
  {
    id: "deals",
    label: "Deal progression",
    description: "Stage movement this week",
    industries: ["sales", "real-estate"],
  },
  {
    id: "health",
    label: "Account health",
    description: "Customer health scoring",
    industries: ["sales", "professional-services", "healthcare"],
  },
  {
    id: "sentiment",
    label: "Email sentiment",
    description: "Signals across customer threads",
    industries: ["sales", "professional-services", "healthcare"],
  },
  {
    id: "recommendations",
    label: "Recommendations",
    description: "AI-suggested next moves",
    industries: "all",
  },
  {
    id: "renewals",
    label: "Renewal reminders",
    description: "Upcoming contract renewals",
    industries: ["sales", "real-estate", "professional-services"],
  },
  {
    id: "timeline",
    label: "Communication timeline",
    description: "Recent stakeholder touches",
    industries: "all",
  },
  {
    id: "approvals",
    label: "Approvals",
    description: "Items awaiting sign-off",
    industries: "all",
  },
  {
    id: "weekly",
    label: "Weekly performance",
    description: "Rolling weekly scorecard",
    industries: "all",
  },
  {
    id: "readiness",
    label: "Product readiness",
    description: "Launch and rollout readiness",
    industries: ["sales", "ecommerce", "professional-services"],
  },
];

export function modulesForIndustry(id: IndustryId): DashboardModule[] {
  return DASHBOARD_MODULES.filter(
    (m) => m.industries === "all" || m.industries.includes(id),
  );
}

export function defaultOrderFor(id: IndustryId): ModuleId[] {
  return modulesForIndustry(id).map((m) => m.id);
}
