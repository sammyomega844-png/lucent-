import { useState } from "react";
import { Card, CardHeader, Chip } from "./primitives";

type ConnStatus = "connected" | "watch" | "available";

type Connector = {
  id: string;
  name: string;
  category: "CRM" | "Comms" | "Calendar" | "Data" | "Billing" | "Docs";
  status: ConnStatus;
  initial: string;
  tone: string; // tailwind bg color class for the tile glyph
};

const CONNECTORS: Connector[] = [
  {
    id: "salesforce",
    name: "Salesforce",
    category: "CRM",
    status: "watch",
    initial: "SF",
    tone: "bg-[#00A1E0]",
  },
  {
    id: "hubspot",
    name: "HubSpot",
    category: "CRM",
    status: "connected",
    initial: "HS",
    tone: "bg-[#FF7A59]",
  },
  {
    id: "gmail",
    name: "Gmail",
    category: "Comms",
    status: "connected",
    initial: "GM",
    tone: "bg-[#EA4335]",
  },
  {
    id: "gcal",
    name: "Calendar",
    category: "Calendar",
    status: "connected",
    initial: "GC",
    tone: "bg-[#4285F4]",
  },
  {
    id: "slack",
    name: "Slack",
    category: "Comms",
    status: "connected",
    initial: "SL",
    tone: "bg-[#4A154B]",
  },
  {
    id: "zoom",
    name: "Zoom",
    category: "Comms",
    status: "watch",
    initial: "ZM",
    tone: "bg-[#2D8CFF]",
  },
  {
    id: "notion",
    name: "Notion",
    category: "Docs",
    status: "connected",
    initial: "NO",
    tone: "bg-foreground",
  },
  {
    id: "stripe",
    name: "Stripe",
    category: "Billing",
    status: "connected",
    initial: "ST",
    tone: "bg-[#635BFF]",
  },
  {
    id: "snowflake",
    name: "Snowflake",
    category: "Data",
    status: "available",
    initial: "SN",
    tone: "bg-[#29B5E8]",
  },
  {
    id: "linear",
    name: "Linear",
    category: "Docs",
    status: "available",
    initial: "LN",
    tone: "bg-[#5E6AD2]",
  },
  {
    id: "gong",
    name: "Gong",
    category: "Comms",
    status: "available",
    initial: "GO",
    tone: "bg-[#7C3AED]",
  },
  {
    id: "zendesk",
    name: "Zendesk",
    category: "Comms",
    status: "available",
    initial: "ZD",
    tone: "bg-[#03363D]",
  },
];

const FILTERS = [
  "All",
  "CRM",
  "Comms",
  "Calendar",
  "Data",
  "Billing",
  "Docs",
] as const;

function statusChip(s: ConnStatus) {
  if (s === "connected") return <Chip status="healthy">Connected</Chip>;
  if (s === "watch") return <Chip status="watch">Review</Chip>;
  return <Chip>Available</Chip>;
}

export function ConnectorsPanel() {
  const [filter, setFilter] = useState<(typeof FILTERS)[number]>("All");
  const visible = CONNECTORS.filter(
    (c) => filter === "All" || c.category === filter,
  );
  const connected = CONNECTORS.filter((c) => c.status === "connected").length;

  return (
    <Card id="connectors">
      <CardHeader
        eyebrow="Connectors"
        title="Quick access"
        subtitle={`${connected} of ${CONNECTORS.length} sources connected · click a tile to manage.`}
        right={
          <a
            href="/setup"
            className="rounded-md border border-border bg-surface px-3 py-1.5 text-xs font-medium text-foreground transition hover:bg-secondary"
          >
            Manage all
          </a>
        }
      />

      <div className="mb-3 flex flex-wrap gap-1.5">
        {FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={
              "rounded-full px-3 py-1 text-xs font-medium transition " +
              (filter === f
                ? "bg-primary text-primary-foreground"
                : "border border-border bg-surface text-muted-foreground hover:text-foreground")
            }
          >
            {f}
          </button>
        ))}
      </div>

      <ul className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4">
        {visible.map((c) => (
          <li key={c.id}>
            <button
              type="button"
              className="group flex w-full items-center gap-3 rounded-lg border border-border bg-surface p-3 text-left transition hover:-translate-y-0.5 hover:border-primary/30 hover:shadow-[var(--shadow-card)]"
            >
              <span
                className={
                  "grid size-9 shrink-0 place-items-center rounded-md text-xs font-semibold text-white " +
                  c.tone
                }
                aria-hidden
              >
                {c.initial}
              </span>
              <span className="min-w-0 flex-1">
                <span className="block truncate text-sm font-medium text-foreground">
                  {c.name}
                </span>
                <span className="block text-[11px] text-muted-foreground">
                  {c.category}
                </span>
              </span>
              <span className="shrink-0">{statusChip(c.status)}</span>
            </button>
          </li>
        ))}
      </ul>
    </Card>
  );
}
