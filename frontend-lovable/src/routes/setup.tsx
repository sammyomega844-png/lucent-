import { createFileRoute } from "@tanstack/react-router";
import { Shell } from "@/components/Shell";
import { Card, CardHeader, Chip, Dot } from "@/components/dashboard/primitives";

export const Route = createFileRoute("/setup")({
  head: () => ({
    meta: [
      { title: "Setup — Lucent" },
      {
        name: "description",
        content:
          "Connect Lucent to your calendar, inbox, CRM, and data sources in minutes.",
      },
      { property: "og:title", content: "Setup — Lucent" },
      {
        property: "og:description",
        content:
          "Connect Lucent to your calendar, inbox, CRM, and data sources in minutes.",
      },
    ],
  }),
  component: Setup,
});

const steps = [
  {
    n: 1,
    title: "Connect your sources",
    status: "healthy",
    note: "Calendar, inbox, CRM",
  },
  {
    n: 2,
    title: "Choose your operating cadence",
    status: "healthy",
    note: "Daily briefing, weekly review",
  },
  {
    n: 3,
    title: "Calibrate signals",
    status: "watch",
    note: "Renewal exposure thresholds",
  },
  {
    n: 4,
    title: "Invite your team",
    status: "watch",
    note: "Roles and visibility",
  },
];

const sources = [
  {
    name: "Google Calendar",
    status: "healthy",
    detail: "Connected · last sync 2 min ago",
  },
  { name: "Gmail", status: "healthy", detail: "Connected · 4 mailboxes" },
  {
    name: "Salesforce",
    status: "watch",
    detail: "Connected · permissions need review",
  },
  { name: "HubSpot", status: "healthy", detail: "Connected · 2-way sync" },
  { name: "Slack", status: "healthy", detail: "Connected · 3 channels" },
  {
    name: "Zoom",
    status: "watch",
    detail: "Connect to capture meeting recaps",
  },
] as const;

function Setup() {
  return (
    <Shell>
      <div className="space-y-6">
        <Card>
          <div className="text-[11px] uppercase tracking-[0.16em] text-muted-foreground">
            Setup
          </div>
          <h1 className="mt-2 font-display text-4xl text-foreground sm:text-5xl">
            Lucent is <span className="text-primary">90% configured</span>.
          </h1>
          <p className="mt-2 max-w-2xl text-muted-foreground">
            Finish two short steps and your morning briefing, follow-up
            autopilot, and revenue forecast will go live for your team.
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-4">
            {steps.map((s) => (
              <div
                key={s.n}
                className="rounded-lg border border-border bg-surface-muted p-4"
              >
                <div className="flex items-center justify-between">
                  <span className="font-display text-2xl text-foreground">
                    0{s.n}
                  </span>
                  <Dot status={s.status as "healthy" | "watch"} />
                </div>
                <div className="mt-2 text-sm font-medium text-foreground">
                  {s.title}
                </div>
                <div className="text-xs text-muted-foreground">{s.note}</div>
              </div>
            ))}
          </div>
        </Card>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader
              eyebrow="Sources"
              title="Connected data"
              subtitle="Where Lucent reads from."
            />
            <ul className="space-y-2">
              {sources.map((s) => (
                <li
                  key={s.name}
                  className="flex items-center justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3"
                >
                  <div className="min-w-0">
                    <div className="text-sm font-medium text-foreground">
                      {s.name}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {s.detail}
                    </div>
                  </div>
                  <Chip status={s.status === "healthy" ? "healthy" : "watch"}>
                    {s.status === "healthy" ? "Connected" : "Action needed"}
                  </Chip>
                </li>
              ))}
            </ul>
          </Card>

          <Card>
            <CardHeader
              eyebrow="Cadence"
              title="Operating rhythm"
              subtitle="When Lucent shows up for you."
            />
            <ul className="space-y-3">
              {[
                {
                  t: "Morning briefing",
                  d: "Weekdays · 06:30 local",
                  on: true,
                },
                { t: "Midday pulse", d: "Weekdays · 12:30 local", on: false },
                {
                  t: "End-of-day recap",
                  d: "Weekdays · 18:00 local",
                  on: true,
                },
                {
                  t: "Weekly performance review",
                  d: "Mondays · 08:00 local",
                  on: true,
                },
              ].map((r) => (
                <li
                  key={r.t}
                  className="flex items-center justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3"
                >
                  <div>
                    <div className="text-sm font-medium text-foreground">
                      {r.t}
                    </div>
                    <div className="text-xs text-muted-foreground">{r.d}</div>
                  </div>
                  <button
                    role="switch"
                    aria-checked={r.on}
                    aria-label={`Toggle ${r.t}`}
                    className={
                      "relative h-6 w-11 rounded-full transition " +
                      (r.on ? "bg-primary" : "bg-border")
                    }
                  >
                    <span
                      className={
                        "absolute top-0.5 size-5 rounded-full bg-surface shadow transition " +
                        (r.on ? "left-[22px]" : "left-0.5")
                      }
                    />
                  </button>
                </li>
              ))}
            </ul>
          </Card>
        </div>
      </div>
    </Shell>
  );
}
