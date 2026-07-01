/* eslint-disable @typescript-eslint/no-explicit-any */
export type Trend = "up" | "down" | "flat";
export type Status = "healthy" | "watch" | "risk";

import actionRegisterData from "./generated/action_register.json";
import followUpData from "./generated/follow_up_plan.json";
import meetingExecutionData from "./generated/meeting_execution_plan.json";
import customerHealthData from "./generated/customer_health_report.json";
import pipelineRiskData from "./generated/pipeline_risk_report.json";
import approvalWorkflowData from "./generated/approval_workflow.json";
import kpiDigestData from "./generated/kpi_digest_report.json";
import communicationTimelineData from "./generated/communication_timeline.json";
import recommendationsData from "./generated/recommendations.json";
import revenueForecastData from "./generated/revenue_forecast.json";
import dealProgressionData from "./generated/deal_progression.json";
import renewalRemindersData from "./generated/renewal_reminders.json";
import weeklyDigestData from "./generated/weekly_digest.json";

export interface DayScore {
  score: number;
  delta: number;
  pulse: string;
  readiness: { label: string; value: number; status: Status }[];
}

export interface ActionItem {
  id: string;
  title: string;
  owner: string;
  due: string;
  priority: "P0" | "P1" | "P2";
  status: Status;
}

export interface FollowUp {
  id: string;
  contact: string;
  company: string;
  channel: "Email" | "Call" | "LinkedIn";
  draft: string;
  scheduled: string;
}

export interface MeetingItem {
  id: string;
  title: string;
  attendees: string[];
  decisions: number;
  actions: number;
  time: string;
}

export interface AccountHealth {
  account: string;
  arr: string;
  status: Status;
  signal: string;
  owner: string;
  lastTouch: string;
}

export interface PipelineRisk {
  deal: string;
  stage: string;
  value: string;
  risk: Status;
  reason: string;
}

export interface Approval {
  id: string;
  title: string;
  requester: string;
  amount: string;
  age: string;
  status: "Pending" | "Approved" | "Blocked";
}

export interface SentimentRow {
  thread: string;
  account: string;
  score: number; // -1..1
  trend: Trend;
  lastReply: string;
}

export interface Recommendation {
  id: string;
  title: string;
  rationale: string;
  impact: "High" | "Medium" | "Low";
  effort: "Low" | "Medium" | "High";
}

export interface KPI {
  label: string;
  value: string;
  delta: string;
  trend: Trend;
  flag?: Status;
}

export interface TimelineEvent {
  id: string;
  time: string;
  type: "Email" | "Call" | "Meeting" | "Note";
  summary: string;
  account: string;
}

export interface ForecastBucket {
  window: "30d" | "60d" | "90d";
  committed: string;
  best: string;
  pipeline: string;
  confidence: number;
}

export interface DealProgress {
  name: string;
  stage: string;
  value: string;
  movement: "on-track" | "stuck";
  days: number;
}

export interface Renewal {
  account: string;
  arr: string;
  date: string;
  bucket: "overdue" | "this-month" | "upcoming";
  owner: string;
}

export interface WeeklyPerformance {
  rep: string;
  meetings: number;
  pipeline: string;
  won: string;
  attainment: number;
}

export interface ReadinessSurface {
  name: string;
  href: string;
  status: Status;
  updated: string;
}

const actionRegister = actionRegisterData as any;
const followUpPlan = followUpData as any;
const meetingExecution = meetingExecutionData as any;
const customerHealth = customerHealthData as any;
const pipelineRisk = pipelineRiskData as any;
const approvalWorkflow = approvalWorkflowData as any;
const kpiDigest = kpiDigestData as any;
const communicationTimeline = communicationTimelineData as any;
const recommendationsReport = recommendationsData as any;
const revenueForecast = revenueForecastData as any;
const dealProgression = dealProgressionData as any;
const renewalReminders = renewalRemindersData as any;
const weeklyDigest = weeklyDigestData as any;

function money(value: unknown): string {
  const n = Number(value || 0);
  return `$${n.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
}

function safeText(value: unknown, fallback = ""): string {
  const text = String(value ?? "").trim();
  return text || fallback;
}

function toStatus(input: unknown): Status {
  const text = safeText(input).toLowerCase();
  if (text.includes("risk") || text === "blocked") return "risk";
  if (text.includes("watch") || text.includes("pending")) return "watch";
  return "healthy";
}

function toTrend(input: unknown): Trend {
  const text = safeText(input).toLowerCase();
  if (text.includes("declin") || text === "down") return "down";
  if (text.includes("improv") || text === "up") return "up";
  return "flat";
}

const chCounts = customerHealth?.counts || {};
const prCounts = pipelineRisk?.counts || {};
const kpiFlags: string[] = kpiDigest?.flags || [];

const baseScore = 80;
const scorePenalty =
  Number(chCounts.risk || 0) * 8 +
  Number(prCounts.risk || 0) * 7 +
  kpiFlags.length * 2;
const computedScore = Math.max(35, Math.min(96, baseScore - scorePenalty));

export const dayScore: DayScore = {
  score: computedScore,
  delta: Math.max(1, 6 - Math.min(5, kpiFlags.length)),
  pulse: safeText(
    recommendationsReport?.summary,
    "Daily intelligence generated from live operational signals.",
  ),
  readiness: [
    {
      label: "Pipeline Coverage",
      value: Number(revenueForecast?.total_pipeline || 0) / 1000,
      status: Number(prCounts.risk || 0) > 0 ? "watch" : "healthy",
    },
    {
      label: "Forecast Confidence",
      value:
        Number(revenueForecast?.horizons?.["90"]?.projected_revenue || 0) > 0
          ? 0.78
          : 0.55,
      status: Number(prCounts.risk || 0) > 0 ? "watch" : "healthy",
    },
    {
      label: "Renewal Exposure",
      value:
        Number(renewalReminders?.counts?.overdue || 0) /
        Math.max(1, Number(renewalReminders?.counts?.total || 1)),
      status:
        Number(renewalReminders?.counts?.overdue || 0) > 0 ? "risk" : "healthy",
    },
    {
      label: "Open Approvals",
      value: Number(approvalWorkflow?.counts?.total_pending || 0),
      status:
        Number(approvalWorkflow?.counts?.total_pending || 0) > 0
          ? "watch"
          : "healthy",
    },
  ],
};

export const actions: ActionItem[] = (actionRegister?.items || []).map(
  (item: any, i: number) => ({
    id: `a${i + 1}`,
    title: safeText(item?.title, "Untitled action"),
    owner: safeText(item?.owner, "Unassigned"),
    due: safeText(item?.due_date, "No due date"),
    priority:
      Number(item?.score || 0) >= 85
        ? "P0"
        : Number(item?.score || 0) >= 70
          ? "P1"
          : "P2",
    status: toStatus(item?.priority || item?.reason),
  }),
);

export const followUps: FollowUp[] = (followUpPlan?.items || []).map(
  (item: any, i: number) => ({
    id: `f${i + 1}`,
    contact: safeText(item?.owner, "Owner"),
    company: safeText(item?.title, "Account"),
    channel: safeText(item?.source).toLowerCase().includes("email")
      ? "Email"
      : safeText(item?.source).toLowerCase().includes("task")
        ? "Call"
        : "LinkedIn",
    draft: safeText(
      item?.nudge_body || item?.nudge_subject || item?.reason,
      "Follow-up needed",
    ),
    scheduled: safeText(item?.due_date, "Queued"),
  }),
);

export const meetings: MeetingItem[] = (meetingExecution?.items || []).map(
  (item: any, i: number) => ({
    id: `m${i + 1}`,
    title: safeText(item?.title, "Execution item"),
    attendees: [safeText(item?.owner, "Owner")],
    decisions: Math.max(1, Math.round(Number(item?.score || 50) / 40)),
    actions: 1,
    time: safeText(item?.due_date, "This week"),
  }),
);

export const accountHealth: AccountHealth[] = (customerHealth?.items || []).map(
  (item: any) => ({
    account: safeText(item?.company, "Account"),
    arr: money(item?.lead_value),
    status: toStatus(item?.bucket),
    signal: safeText(item?.reason, "No signal"),
    owner: safeText(item?.lead_name, "Owner"),
    lastTouch: safeText(item?.status, "Unknown"),
  }),
);

export const pipelineRisks: PipelineRisk[] = (pipelineRisk?.items || []).map(
  (item: any) => ({
    deal: `${safeText(item?.company, "Deal")} - ${safeText(item?.status, "Stage")}`,
    stage: safeText(item?.status, "Unknown"),
    value: money(item?.lead_value),
    risk: toStatus(item?.bucket),
    reason: safeText(item?.reason, "No reason"),
  }),
);

const pending = Number(approvalWorkflow?.counts?.total_pending || 0);
const approved = Number(approvalWorkflow?.counts?.total_approved || 0);
const blocked = Number(approvalWorkflow?.counts?.total_rejected || 0);
const approvalItems = approvalWorkflow?.items || [];

export const approvals: Approval[] = [
  ...approvalItems.map((item: any, i: number) => ({
    id: safeText(item?.draft_id, `ap${i + 1}`),
    title: safeText(item?.subject, "Draft approval"),
    requester: safeText(item?.recipient, "Unknown"),
    amount: "-",
    age: safeText(item?.created_at, "now"),
    status: "Pending" as const,
  })),
  ...(approvalItems.length === 0
    ? [
        {
          id: "ap-pending",
          title: `Pending approvals: ${pending}`,
          requester: "Workflow",
          amount: "-",
          age: "live",
          status:
            pending > 0
              ? ("Pending" as const)
              : approved > 0
                ? ("Approved" as const)
                : blocked > 0
                  ? ("Blocked" as const)
                  : ("Approved" as const),
        },
      ]
    : []),
];

export const sentiment: SentimentRow[] = (pipelineRisk?.items || []).map(
  (item: any, i: number) => {
    const status = toStatus(item?.bucket);
    const score = status === "healthy" ? 0.5 : status === "watch" ? 0.1 : -0.45;
    return {
      thread: safeText(item?.next_step, "Deal signal"),
      account: safeText(item?.company, "Account"),
      score,
      trend: status === "healthy" ? "up" : status === "watch" ? "flat" : "down",
      lastReply: safeText(item?.status, "recent"),
    };
  },
);

export const recommendations: Recommendation[] = (
  recommendationsReport?.items || []
).map((item: any, i: number) => ({
  id: `r${i + 1}`,
  title: safeText(item?.title, "Recommendation"),
  rationale: safeText(item?.rationale, "No rationale"),
  impact: safeText(item?.priority).toLowerCase() === "high" ? "High" : "Medium",
  effort: "Medium",
}));

const kpiMap = kpiDigest?.kpis || {};
export const kpis: KPI[] = Object.keys(kpiMap).map((key) => {
  const row = kpiMap[key] || {};
  return {
    label: key.replace(/_/g, " ").replace(/\b\w/g, (m) => m.toUpperCase()),
    value: key.includes("value")
      ? money(row?.latest)
      : String(row?.latest ?? "-"),
    delta: `avg ${row?.avg ?? "-"}`,
    trend: toTrend(row?.trend),
    flag: toTrend(row?.trend) === "down" ? "watch" : undefined,
  };
});

export const timeline: TimelineEvent[] = Object.entries(
  communicationTimeline?.accounts || {},
)
  .flatMap(([company, account]: any, idx: number) =>
    (account?.touches || []).map((touch: any, j: number) => ({
      id: `t${idx + 1}-${j + 1}`,
      time: safeText(touch?.date, "--:--").slice(0, 10),
      type: safeText(touch?.source, "Note").toLowerCase().includes("email")
        ? "Email"
        : safeText(touch?.source).toLowerCase().includes("task")
          ? "Call"
          : safeText(touch?.source).toLowerCase().includes("meeting")
            ? "Meeting"
            : "Note",
      summary: safeText(touch?.summary, "No summary"),
      account: String(company),
    })),
  )
  .slice(0, 8);

export const forecast: ForecastBucket[] = ["30", "60", "90"].map((h) => {
  const row = revenueForecast?.horizons?.[h] || {};
  const projected = Number(row?.projected_revenue || 0);
  const best = Number(row?.best_case_revenue || 0);
  const confidence = best > 0 ? Math.min(1, projected / best + 0.25) : 0.5;
  return {
    window: `${h}d` as "30d" | "60d" | "90d",
    committed: money(projected),
    best: money(best),
    pipeline: money(revenueForecast?.total_pipeline || 0),
    confidence,
  };
});

export const deals: DealProgress[] = (dealProgression?.items || []).map(
  (item: any) => ({
    name: safeText(item?.company, "Deal"),
    stage: safeText(item?.status, "Stage"),
    value: money(item?.lead_value),
    movement:
      safeText(item?.stage_label).toLowerCase() === "stuck"
        ? "stuck"
        : "on-track",
    days: Number(item?.days_since_contact || 0),
  }),
);

export const renewals: Renewal[] = (renewalReminders?.items || []).map(
  (item: any) => ({
    account: safeText(item?.company, "Account"),
    arr: money(item?.lead_value),
    date: safeText(item?.renewal_date, "Unknown"),
    bucket:
      safeText(item?.urgency, "upcoming") === "overdue"
        ? "overdue"
        : safeText(item?.urgency) === "this_month"
          ? "this-month"
          : "upcoming",
    owner: safeText(item?.lead_name, "Owner"),
  }),
);

export const weekly: WeeklyPerformance[] = (weeklyDigest?.days || []).map(
  (row: any, i: number) => {
    const completed = Number(row?.completed || 0);
    const highOpen = Number(row?.high_open || 0);
    const qualified = Number(row?.qualified || 0);
    const attainment = Math.max(
      0.5,
      Math.min(1.2, completed / Math.max(1, highOpen + 1)),
    );
    return {
      rep: safeText(row?.date, `Day ${i + 1}`),
      meetings: completed + highOpen,
      pipeline: money(row?.pipeline_value || 0),
      won: money(qualified * 1000),
      attainment,
    };
  },
);

export const surfaces: ReadinessSurface[] = [
  {
    name: "Daily Executive Briefing",
    href: "/executive_briefing.html",
    status: "healthy",
    updated: safeText(actionRegister?.generated_at, "recent"),
  },
  {
    name: "Account Health Radar",
    href: "#health",
    status: Number(customerHealth?.counts?.risk || 0) > 0 ? "watch" : "healthy",
    updated: safeText(customerHealth?.generated_at, "recent"),
  },
  {
    name: "Renewal Save Plays",
    href: "#renewals",
    status:
      Number(renewalReminders?.counts?.overdue || 0) > 0 ? "risk" : "healthy",
    updated: safeText(renewalReminders?.generated_at, "recent"),
  },
  {
    name: "Forecast Workbook",
    href: "#forecast",
    status: Number(pipelineRisk?.counts?.risk || 0) > 0 ? "watch" : "healthy",
    updated: safeText(revenueForecast?.generated_at, "recent"),
  },
];

export const briefing = {
  headline: safeText(
    recommendationsReport?.summary,
    "Daily briefing generated from live operational data.",
  ),
  bullets: [
    safeText(actionRegister?.summary, "Action register updated."),
    safeText(pipelineRisk?.summary, "Pipeline risk reviewed."),
    safeText(customerHealth?.summary, "Customer health scored."),
  ],
  prepared: `Prepared from live artifacts \u00b7 ${safeText(actionRegister?.generated_at, "now")}`,
};
