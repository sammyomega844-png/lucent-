import { createFileRoute } from "@tanstack/react-router";
import { Fragment } from "react";
import { Shell } from "@/components/Shell";
import { ProductTour } from "@/components/ProductTour";
import { SectionJump } from "@/components/dashboard/SectionJump";
import { ConnectorsPanel } from "@/components/dashboard/ConnectorsPanel";
import { CustomizePanel } from "@/components/dashboard/CustomizePanel";
import {
  IndustryKpis,
  IndustryModulesGrid,
  IndustryPlaybooks,
} from "@/components/dashboard/IndustryModules";
import {
  ActionRegister,
  ApprovalWorkflow,
  BriefingPreview,
  CommunicationTimeline,
  CustomerHealthRadar,
  DealProgression,
  EmailSentiment,
  FollowUpAutopilot,
  HeroSection,
  KpiDigest,
  MeetingToExecution,
  PipelineRiskRadar,
  ProductReadiness,
  Recommendations,
  RenewalReminders,
  RevenueForecast,
  WeeklyPerformanceTable,
} from "@/components/dashboard/sections";
import { useDashboardLayout } from "@/context/DashboardLayoutContext";
import { DASHBOARD_MODULES, type ModuleId } from "@/data/dashboardModules";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Lucent — Executive Intelligence Platform" },
      {
        name: "description",
        content:
          "Lucent is an executive intelligence platform that turns daily business signals into the few moves that matter.",
      },
      {
        property: "og:title",
        content: "Lucent — Executive Intelligence Platform",
      },
      {
        property: "og:description",
        content:
          "One place to see daily business intelligence and the recommended actions for founders, operators, and executives.",
      },
    ],
  }),
  component: Dashboard,
});

function renderModule(id: ModuleId) {
  switch (id) {
    case "hero":
      return <HeroSection />;
    case "industry-kpis":
      return <IndustryKpis />;
    case "industry-modules":
      return <IndustryModulesGrid />;
    case "industry-playbooks":
      return <IndustryPlaybooks />;
    case "connectors":
      return <ConnectorsPanel />;
    case "briefing":
      return <BriefingPreview />;
    case "actions":
      return <ActionRegister />;
    case "followups":
      return <FollowUpAutopilot />;
    case "meetings":
      return <MeetingToExecution />;
    case "kpi":
      return <KpiDigest />;
    case "forecast":
      return <RevenueForecast />;
    case "pipeline-risk":
      return <PipelineRiskRadar />;
    case "deals":
      return <DealProgression />;
    case "health":
      return <CustomerHealthRadar />;
    case "sentiment":
      return <EmailSentiment />;
    case "recommendations":
      return <Recommendations />;
    case "renewals":
      return <RenewalReminders />;
    case "timeline":
      return <CommunicationTimeline />;
    case "approvals":
      return <ApprovalWorkflow />;
    case "weekly":
      return <WeeklyPerformanceTable />;
    case "readiness":
      return <ProductReadiness />;
    default:
      return null;
  }
}

function Dashboard() {
  const { orderedIds } = useDashboardLayout();
  const heroId: ModuleId = "hero";
  const hero = orderedIds.find((id) => id === heroId);
  const rest = orderedIds.filter((id) => id !== heroId);

  const jumpItems = orderedIds.map((id) => {
    const meta = DASHBOARD_MODULES.find((m) => m.id === id);
    return { id, label: meta?.label ?? id };
  });

  return (
    <Shell>
      <div className="space-y-6">
        {hero ? renderModule(hero) : null}

        <div className="flex items-center justify-between gap-3">
          <div className="min-w-0 flex-1">
            <SectionJump items={jumpItems.filter((i) => i.id !== heroId)} />
          </div>
          <div className="shrink-0 pt-2">
            <CustomizePanel />
          </div>
        </div>

        {rest.map((id) => (
          <Fragment key={id}>{renderModule(id)}</Fragment>
        ))}
      </div>

      <ProductTour />
    </Shell>
  );
}
