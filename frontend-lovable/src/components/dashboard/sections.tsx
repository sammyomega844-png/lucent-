import { Card, CardHeader, Chip, Dot, TrendArrow } from "./primitives";
import {
  actions,
  accountHealth,
  approvals,
  briefing,
  dayScore,
  deals,
  followUps,
  forecast,
  kpis,
  meetings,
  pipelineRisks,
  recommendations,
  renewals,
  sentiment,
  surfaces,
  timeline,
  weekly,
} from "@/data/mock";

export function HeroSection() {
  return (
    <Card id="hero" className="relative overflow-hidden p-6 sm:p-8">
      <div className="grid gap-6 lg:grid-cols-[1.1fr_1fr] lg:items-center">
        <div>
          <div className="mb-2 flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.18em] text-muted-foreground">
            <span className="inline-block size-1.5 rounded-full bg-healthy" />
            Today · Strategic Pulse
          </div>
          <h1 className="font-display text-4xl leading-[1.05] text-foreground sm:text-5xl lg:text-6xl">
            Your day is <span className="text-primary">on plan</span>, with two
            moments that need your attention.
          </h1>
          <p className="mt-4 max-w-xl text-base text-muted-foreground sm:text-lg">
            {dayScore.pulse}
          </p>
          <div className="mt-6 flex flex-wrap items-center gap-2">
            <Chip status="primary">3 enterprise deals advanced</Chip>
            <Chip status="watch">2 renewals need exec touch</Chip>
            <Chip status="healthy">Forecast confidence 78%</Chip>
          </div>
        </div>

        <div className="card-surface relative p-6">
          <div className="flex items-baseline gap-3">
            <div className="font-display text-7xl leading-none text-foreground">
              {dayScore.score}
            </div>
            <div className="text-sm font-medium text-healthy">
              +{dayScore.delta} vs yesterday
            </div>
          </div>
          <div className="mt-1 text-xs uppercase tracking-[0.14em] text-muted-foreground">
            Day Score
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3">
            {dayScore.readiness.map((r) => (
              <div
                key={r.label}
                className="rounded-lg border border-border bg-surface-muted p-3"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[11px] uppercase tracking-wider text-muted-foreground">
                    {r.label}
                  </span>
                  <Dot status={r.status} />
                </div>
                <div className="mt-1 font-display text-2xl text-foreground">
                  {typeof r.value === "number" && r.value < 1
                    ? `${Math.round(r.value * 100)}%`
                    : r.value}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}

export function ActionRegister() {
  return (
    <Card id="actions">
      <CardHeader
        eyebrow="Operating cadence"
        title="Action Register"
        subtitle="What only you can do today."
        right={<Chip status="primary">{actions.length} open</Chip>}
      />
      <ul className="divide-y divide-border">
        {actions.map((a) => (
          <li
            key={a.id}
            className="flex items-center justify-between gap-3 py-3 first:pt-0 last:pb-0"
          >
            <div className="flex min-w-0 items-center gap-3">
              <Dot status={a.status} />
              <div className="min-w-0">
                <div className="truncate text-sm font-medium text-foreground">
                  {a.title}
                </div>
                <div className="text-xs text-muted-foreground">
                  {a.owner} · {a.due}
                </div>
              </div>
            </div>
            <Chip
              status={
                a.priority === "P0"
                  ? "risk"
                  : a.priority === "P1"
                    ? "watch"
                    : "neutral"
              }
            >
              {a.priority}
            </Chip>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function FollowUpAutopilot() {
  return (
    <Card id="followups">
      <CardHeader
        eyebrow="Autopilot"
        title="Follow-up Autopilot"
        subtitle="Drafts queued and waiting for your nod."
        right={<Chip status="healthy">All drafted</Chip>}
      />
      <ul className="space-y-3">
        {followUps.map((f) => (
          <li
            key={f.id}
            className="rounded-lg border border-border bg-surface-muted p-3"
          >
            <div className="flex items-center justify-between gap-2">
              <div className="text-sm font-medium text-foreground">
                {f.contact}{" "}
                <span className="text-muted-foreground">· {f.company}</span>
              </div>
              <Chip status="neutral">{f.channel}</Chip>
            </div>
            <p className="mt-1 text-sm text-muted-foreground">{f.draft}</p>
            <div className="mt-2 flex items-center justify-between text-xs text-muted-foreground">
              <span>Scheduled {f.scheduled}</span>
              <button className="font-medium text-primary hover:underline">
                Review draft →
              </button>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function MeetingToExecution() {
  return (
    <Card id="meetings">
      <CardHeader
        eyebrow="From talk to action"
        title="Meeting to Execution"
        subtitle="Decisions and actions captured automatically."
      />
      <ul className="space-y-3">
        {meetings.map((m) => (
          <li
            key={m.id}
            className="flex items-center justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3"
          >
            <div className="min-w-0">
              <div className="truncate text-sm font-medium text-foreground">
                {m.title}
              </div>
              <div className="text-xs text-muted-foreground">
                {m.attendees.join(" · ")} · {m.time}
              </div>
            </div>
            <div className="flex shrink-0 items-center gap-2">
              <Chip status="primary">{m.decisions} decisions</Chip>
              <Chip status="healthy">{m.actions} actions</Chip>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function CustomerHealthRadar() {
  return (
    <Card id="health">
      <CardHeader
        eyebrow="Customer signal"
        title="Customer Health Radar"
        subtitle="Composite signal across product, support, and exec engagement."
      />
      <div className="overflow-hidden rounded-lg border border-border">
        <table className="w-full text-sm">
          <thead className="bg-surface-muted text-left text-xs uppercase tracking-wider text-muted-foreground">
            <tr>
              <th className="px-3 py-2">Account</th>
              <th className="px-3 py-2">ARR</th>
              <th className="px-3 py-2">Signal</th>
              <th className="px-3 py-2 hidden md:table-cell">Owner</th>
              <th className="px-3 py-2 text-right">Last touch</th>
            </tr>
          </thead>
          <tbody>
            {accountHealth.map((a) => (
              <tr key={a.account} className="border-t border-border">
                <td className="px-3 py-3">
                  <div className="flex items-center gap-2">
                    <Dot status={a.status} />
                    <span className="font-medium text-foreground">
                      {a.account}
                    </span>
                  </div>
                </td>
                <td className="px-3 py-3 text-muted-foreground">{a.arr}</td>
                <td className="px-3 py-3 text-muted-foreground">{a.signal}</td>
                <td className="px-3 py-3 hidden text-muted-foreground md:table-cell">
                  {a.owner}
                </td>
                <td className="px-3 py-3 text-right text-muted-foreground">
                  {a.lastTouch}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

export function PipelineRiskRadar() {
  return (
    <Card id="pipeline-risk">
      <CardHeader
        eyebrow="Forecast hygiene"
        title="Pipeline Risk Radar"
        subtitle="Deals trending sideways before they slip."
      />
      <ul className="space-y-3">
        {pipelineRisks.map((p) => (
          <li
            key={p.deal}
            className="flex items-start justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3"
          >
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <Dot status={p.risk} />
                <span className="text-sm font-medium text-foreground">
                  {p.deal}
                </span>
              </div>
              <div className="mt-1 text-xs text-muted-foreground">
                {p.stage} · {p.reason}
              </div>
            </div>
            <div className="font-display text-lg text-foreground">
              {p.value}
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function ApprovalWorkflow() {
  return (
    <Card id="approvals">
      <CardHeader
        eyebrow="Decision queue"
        title="Approval Workflow"
        subtitle="Cleared in one screen, with context."
      />
      <ul className="divide-y divide-border">
        {approvals.map((a) => (
          <li
            key={a.id}
            className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3 py-3 first:pt-0 last:pb-0"
          >
            <div className="min-w-0">
              <div className="truncate text-sm font-medium text-foreground">
                {a.title}
              </div>
              <div className="text-xs text-muted-foreground">
                {a.requester} · {a.amount} · {a.age} old
              </div>
            </div>
            <Chip
              status={
                a.status === "Approved"
                  ? "healthy"
                  : a.status === "Blocked"
                    ? "risk"
                    : "watch"
              }
            >
              {a.status}
            </Chip>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function EmailSentiment() {
  return (
    <Card id="sentiment">
      <CardHeader
        eyebrow="Relationship signal"
        title="Email Sentiment"
        subtitle="How key threads are actually trending."
      />
      <ul className="space-y-2">
        {sentiment.map((s) => {
          const pct = Math.round(((s.score + 1) / 2) * 100);
          const color =
            s.score > 0.25
              ? "bg-healthy"
              : s.score < -0.1
                ? "bg-risk"
                : "bg-watch";
          return (
            <li
              key={s.thread}
              className="rounded-lg border border-border bg-surface-muted p-3"
            >
              <div className="flex items-center justify-between gap-2">
                <div className="min-w-0">
                  <div className="truncate text-sm font-medium text-foreground">
                    {s.thread}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {s.account} · {s.lastReply}
                  </div>
                </div>
                <div className="flex shrink-0 items-center gap-2 text-xs text-muted-foreground">
                  <TrendArrow trend={s.trend} />
                  {Math.round(s.score * 100)}
                </div>
              </div>
              <div
                className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-border"
                role="progressbar"
                aria-valuenow={pct}
                aria-valuemin={0}
                aria-valuemax={100}
              >
                <div
                  className={`h-full ${color}`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </li>
          );
        })}
      </ul>
    </Card>
  );
}

export function Recommendations() {
  return (
    <Card id="recommendations">
      <CardHeader
        eyebrow="Next best moves"
        title="Recommendations"
        subtitle="Ranked by impact and effort, not noise."
      />
      <ul className="grid gap-3 md:grid-cols-2">
        {recommendations.map((r) => (
          <li
            key={r.id}
            className="rounded-lg border border-border bg-surface-muted p-4"
          >
            <div className="flex items-center justify-between gap-2">
              <div className="text-sm font-semibold text-foreground">
                {r.title}
              </div>
              <Chip status={r.impact === "High" ? "primary" : "neutral"}>
                {r.impact} impact
              </Chip>
            </div>
            <p className="mt-1 text-sm text-muted-foreground">{r.rationale}</p>
            <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
              <span>Effort: {r.effort}</span>
              <button className="font-medium text-primary hover:underline">
                Run play →
              </button>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function KpiDigest() {
  return (
    <Card id="kpi">
      <CardHeader
        eyebrow="What moved"
        title="KPI Digest"
        subtitle="Trend, delta, and flags at a glance."
      />
      <div className="grid grid-cols-2 gap-3 md:grid-cols-3">
        {kpis.map((k) => (
          <div
            key={k.label}
            className="rounded-lg border border-border bg-surface-muted p-4"
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] uppercase tracking-wider text-muted-foreground">
                {k.label}
              </span>
              {k.flag ? <Dot status={k.flag} /> : null}
            </div>
            <div className="mt-1 font-display text-3xl text-foreground">
              {k.value}
            </div>
            <div className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
              <TrendArrow trend={k.trend} /> {k.delta}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

export function CommunicationTimeline() {
  return (
    <Card id="timeline">
      <CardHeader
        eyebrow="Across accounts"
        title="Communication Timeline"
        subtitle="Today, in chronological order."
      />
      <ol className="relative ml-3 space-y-4 border-l border-border pl-5">
        {timeline.map((t) => (
          <li key={t.id} className="relative">
            <span className="absolute -left-[26px] top-1 grid size-4 place-items-center rounded-full border border-border bg-surface">
              <span className="size-1.5 rounded-full bg-primary" />
            </span>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <span className="font-mono">{t.time}</span>
              <Chip status="neutral">{t.type}</Chip>
              <span>· {t.account}</span>
            </div>
            <p className="mt-1 text-sm text-foreground">{t.summary}</p>
          </li>
        ))}
      </ol>
    </Card>
  );
}

export function RevenueForecast() {
  return (
    <Card id="forecast">
      <CardHeader
        eyebrow="Revenue"
        title="Revenue Forecast"
        subtitle="Committed, best case, and pipeline by window."
      />
      <div className="grid gap-3 md:grid-cols-3">
        {forecast.map((f) => (
          <div
            key={f.window}
            className="rounded-xl border border-border bg-gradient-to-br from-surface to-surface-muted p-5"
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] uppercase tracking-[0.16em] text-muted-foreground">
                Next {f.window}
              </span>
              <Chip
                status={
                  f.confidence > 0.75
                    ? "healthy"
                    : f.confidence > 0.65
                      ? "watch"
                      : "risk"
                }
              >
                {Math.round(f.confidence * 100)}% conf
              </Chip>
            </div>
            <div className="mt-3 font-display text-4xl text-foreground">
              {f.committed}
            </div>
            <div className="mt-1 text-xs text-muted-foreground">committed</div>
            <div className="mt-4 space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Best case</span>
                <span className="text-foreground">{f.best}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Pipeline</span>
                <span className="text-foreground">{f.pipeline}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

export function DealProgression() {
  const onTrack = deals.filter((d) => d.movement === "on-track");
  const stuck = deals.filter((d) => d.movement === "stuck");
  return (
    <Card id="deals">
      <CardHeader
        eyebrow="Deal motion"
        title="Deal Progression"
        subtitle="Where momentum is, and where it isn't."
      />
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground">
            <Dot status="healthy" /> On track ({onTrack.length})
          </div>
          <ul className="space-y-2">
            {onTrack.map((d) => (
              <li
                key={d.name}
                className="rounded-lg border border-border bg-surface-muted p-3"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-foreground">
                    {d.name}
                  </span>
                  <span className="text-sm text-foreground">{d.value}</span>
                </div>
                <div className="text-xs text-muted-foreground">
                  {d.stage} · {d.days}d in stage
                </div>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground">
            <Dot status="risk" /> Stuck ({stuck.length})
          </div>
          <ul className="space-y-2">
            {stuck.map((d) => (
              <li
                key={d.name}
                className="rounded-lg border border-border bg-surface-muted p-3"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-foreground">
                    {d.name}
                  </span>
                  <span className="text-sm text-foreground">{d.value}</span>
                </div>
                <div className="text-xs text-muted-foreground">
                  {d.stage} · {d.days}d in stage
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </Card>
  );
}

export function RenewalReminders() {
  const groups: Array<{
    label: string;
    bucket: "overdue" | "this-month" | "upcoming";
    status: "risk" | "watch" | "healthy";
  }> = [
    { label: "Overdue", bucket: "overdue", status: "risk" },
    { label: "This month", bucket: "this-month", status: "watch" },
    { label: "Upcoming", bucket: "upcoming", status: "healthy" },
  ];
  return (
    <Card id="renewals">
      <CardHeader
        eyebrow="Retention"
        title="Renewal Reminders"
        subtitle="Where renewal attention is needed, in order."
      />
      <div className="grid gap-4 md:grid-cols-3">
        {groups.map((g) => {
          const rows = renewals.filter((r) => r.bucket === g.bucket);
          return (
            <div key={g.bucket}>
              <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground">
                <Dot status={g.status} /> {g.label} ({rows.length})
              </div>
              <ul className="space-y-2">
                {rows.map((r) => (
                  <li
                    key={r.account}
                    className="rounded-lg border border-border bg-surface-muted p-3"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-foreground">
                        {r.account}
                      </span>
                      <span className="text-sm text-foreground">{r.arr}</span>
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {r.date} · {r.owner}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

export function BriefingPreview() {
  return (
    <Card
      id="briefing"
      className="bg-gradient-to-br from-surface to-primary-soft/40"
    >
      <CardHeader
        eyebrow="Morning briefing"
        title="Today's Executive Briefing"
        subtitle={briefing.prepared}
        right={<Chip status="primary">Auto-prepared</Chip>}
      />
      <p className="font-display text-2xl leading-snug text-foreground">
        {briefing.headline}
      </p>
      <ul className="mt-4 space-y-3">
        {briefing.bullets.map((b, i) => (
          <li key={i} className="flex gap-3 text-sm text-foreground">
            <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-primary" />
            <span>{b}</span>
          </li>
        ))}
      </ul>
      <div className="mt-5 flex flex-wrap gap-2">
        <button className="rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground transition hover:opacity-90">
          Open full briefing
        </button>
        <button className="rounded-md border border-border bg-surface px-3 py-2 text-sm font-medium text-foreground transition hover:border-foreground/30">
          Share with team
        </button>
      </div>
    </Card>
  );
}

export function WeeklyPerformanceTable() {
  return (
    <Card id="weekly">
      <CardHeader
        eyebrow="Team"
        title="Weekly Performance"
        subtitle="Pace against plan and pipeline contribution."
      />
      <div className="overflow-hidden rounded-lg border border-border">
        <table className="w-full text-sm">
          <thead className="bg-surface-muted text-left text-xs uppercase tracking-wider text-muted-foreground">
            <tr>
              <th className="px-3 py-2">Rep</th>
              <th className="px-3 py-2">Meetings</th>
              <th className="px-3 py-2">Pipeline</th>
              <th className="px-3 py-2">Won</th>
              <th className="px-3 py-2 text-right">Attainment</th>
            </tr>
          </thead>
          <tbody>
            {weekly.map((r) => {
              const a = Math.round(r.attainment * 100);
              const status =
                r.attainment >= 1
                  ? "healthy"
                  : r.attainment >= 0.85
                    ? "watch"
                    : "risk";
              return (
                <tr key={r.rep} className="border-t border-border">
                  <td className="px-3 py-3 font-medium text-foreground">
                    {r.rep}
                  </td>
                  <td className="px-3 py-3 text-muted-foreground">
                    {r.meetings}
                  </td>
                  <td className="px-3 py-3 text-muted-foreground">
                    {r.pipeline}
                  </td>
                  <td className="px-3 py-3 text-muted-foreground">{r.won}</td>
                  <td className="px-3 py-3 text-right">
                    <Chip status={status}>{a}%</Chip>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

export function ProductReadiness() {
  return (
    <Card id="readiness">
      <CardHeader
        eyebrow="Surfaces"
        title="Product Readiness"
        subtitle="Generated views, fresh and linked."
      />
      <ul className="grid gap-2 sm:grid-cols-2">
        {surfaces.map((s) => (
          <li key={s.name}>
            <a
              href={s.href}
              className="flex items-center justify-between gap-3 rounded-lg border border-border bg-surface-muted p-3 transition hover:border-foreground/20"
            >
              <div className="flex min-w-0 items-center gap-2">
                <Dot status={s.status} />
                <div className="min-w-0">
                  <div className="truncate text-sm font-medium text-foreground">
                    {s.name}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    Updated {s.updated}
                  </div>
                </div>
              </div>
              <span className="text-primary">→</span>
            </a>
          </li>
        ))}
      </ul>
    </Card>
  );
}
