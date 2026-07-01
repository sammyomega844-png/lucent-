import { createFileRoute } from "@tanstack/react-router";
import { Shell } from "@/components/Shell";
import { Card, CardHeader, Chip } from "@/components/dashboard/primitives";

export const Route = createFileRoute("/help")({
  head: () => ({
    meta: [
      { title: "Help Center — Lucent" },
      {
        name: "description",
        content:
          "Guides, tours, and playbooks for getting the most out of Lucent.",
      },
      { property: "og:title", content: "Help Center — Lucent" },
      {
        property: "og:description",
        content:
          "Guides, tours, and playbooks for getting the most out of Lucent.",
      },
    ],
  }),
  component: Help,
});

const topics = [
  {
    group: "Getting started",
    items: [
      {
        title: "Reading your Day Score",
        desc: "What goes into the score and how to react when it shifts.",
      },
      {
        title: "Configuring your morning briefing",
        desc: "Tune what shows up in your 6:30 briefing.",
      },
      {
        title: "Connecting calendars and inboxes",
        desc: "Bring meetings, threads, and decisions into Lucent.",
      },
    ],
  },
  {
    group: "Revenue & pipeline",
    items: [
      {
        title: "How forecast confidence is computed",
        desc: "Signals, weights, and the 30/60/90 windows.",
      },
      {
        title: "Tagging at-risk deals",
        desc: "Override risk signals when you have more context.",
      },
      {
        title: "Renewal save plays",
        desc: "Pre-built plays for overdue and this-month renewals.",
      },
    ],
  },
  {
    group: "Workflow & approvals",
    items: [
      {
        title: "Approval routing",
        desc: "How approvals are queued and escalated.",
      },
      {
        title: "Follow-up Autopilot voice",
        desc: "Train Autopilot to draft in your tone.",
      },
      {
        title: "Meeting to execution",
        desc: "Decisions, actions, and owners auto-extracted.",
      },
    ],
  },
];

function Help() {
  return (
    <Shell>
      <div className="space-y-6">
        <Card>
          <div className="grid gap-6 lg:grid-cols-[1.2fr_1fr] lg:items-center">
            <div>
              <div className="text-[11px] uppercase tracking-[0.16em] text-muted-foreground">
                Help Center
              </div>
              <h1 className="mt-2 font-display text-4xl text-foreground sm:text-5xl">
                Run Lucent like an executive operator.
              </h1>
              <p className="mt-3 max-w-xl text-muted-foreground">
                Short, opinionated guides for getting more out of every signal
                Lucent surfaces — without becoming a tool you have to babysit.
              </p>
              <div className="mt-5">
                <label className="sr-only" htmlFor="help-search">
                  Search help
                </label>
                <input
                  id="help-search"
                  type="search"
                  placeholder="Search guides, e.g. ‘renewal save play’"
                  className="w-full rounded-lg border border-border bg-surface px-4 py-3 text-sm shadow-sm outline-none transition focus:border-foreground/30 focus:ring-2 focus:ring-ring"
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {[
                { k: "Avg. time saved / week", v: "6.2h" },
                { k: "Avg. action acceptance", v: "82%" },
                { k: "Renewal save lift", v: "+14%" },
                { k: "Forecast accuracy", v: "94%" },
              ].map((s) => (
                <div
                  key={s.k}
                  className="rounded-lg border border-border bg-surface-muted p-4"
                >
                  <div className="text-[11px] uppercase tracking-wider text-muted-foreground">
                    {s.k}
                  </div>
                  <div className="mt-1 font-display text-3xl text-foreground">
                    {s.v}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Card>

        <div className="grid gap-6 lg:grid-cols-3">
          {topics.map((t) => (
            <Card key={t.group}>
              <CardHeader eyebrow="Guides" title={t.group} />
              <ul className="space-y-3">
                {t.items.map((i) => (
                  <li
                    key={i.title}
                    className="rounded-lg border border-border bg-surface-muted p-3 transition hover:border-foreground/20"
                  >
                    <div className="text-sm font-medium text-foreground">
                      {i.title}
                    </div>
                    <div className="mt-1 text-sm text-muted-foreground">
                      {i.desc}
                    </div>
                    <button className="mt-2 text-xs font-medium text-primary hover:underline">
                      Read guide →
                    </button>
                  </li>
                ))}
              </ul>
            </Card>
          ))}
        </div>

        <Card>
          <CardHeader
            eyebrow="Talk to us"
            title="Still stuck? Reach a human."
            right={<Chip status="healthy">&lt; 2h response</Chip>}
          />
          <div className="grid gap-3 sm:grid-cols-3">
            {[
              {
                t: "Concierge onboarding",
                d: "Pair with a Lucent specialist for setup.",
              },
              {
                t: "Customer Slack",
                d: "Drop a question, get answers from operators like you.",
              },
              {
                t: "Email support",
                d: "Send transcripts, screenshots, ideas — we read everything.",
              },
            ].map((c) => (
              <div
                key={c.t}
                className="rounded-lg border border-border bg-surface-muted p-4"
              >
                <div className="text-sm font-medium text-foreground">{c.t}</div>
                <div className="mt-1 text-sm text-muted-foreground">{c.d}</div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </Shell>
  );
}
