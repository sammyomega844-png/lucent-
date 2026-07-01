import { useIndustry } from "@/context/IndustryContext";
import { Card, CardHeader, Chip, Dot, TrendArrow } from "./primitives";

export function IndustryKpis() {
  const { industry } = useIndustry();
  return (
    <Card id="industry-kpis">
      <CardHeader
        eyebrow={industry.name}
        title="Operating KPIs"
        subtitle={industry.tagline}
        right={<Chip status="primary">{industry.kpis.length} metrics</Chip>}
      />
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {industry.kpis.map((k) => (
          <div
            key={k.label}
            className="rounded-lg border border-border/70 bg-background/60 p-4"
          >
            <div className="flex items-center justify-between text-[11px] uppercase tracking-[0.14em] text-muted-foreground">
              <span>{k.label}</span>
              {k.flag ? <Dot status={k.flag} /> : null}
            </div>
            <div className="mt-2 font-display text-3xl text-foreground">
              {k.value}
            </div>
            <div className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
              <TrendArrow trend={k.trend} />
              <span>{k.delta}</span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

export function IndustryModulesGrid() {
  const { industry } = useIndustry();
  if (industry.modules.length === 0) return null;

  return (
    <div id="industry-modules" className="grid gap-6 lg:grid-cols-2">
      {industry.modules.map((mod) => (
        <Card key={mod.id} id={mod.id}>
          <CardHeader
            title={mod.title}
            subtitle={mod.subtitle}
            right={<Chip>{mod.rows.length}</Chip>}
          />
          <div className="overflow-hidden rounded-lg border border-border/70">
            <table className="w-full text-sm">
              <thead className="bg-secondary/60 text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
                <tr>
                  {mod.columns.map((c) => (
                    <th key={c} className="px-3 py-2 text-left font-medium">
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {mod.rows.map((r, i) => (
                  <tr key={i} className="border-t border-border/60 align-top">
                    <td className="px-3 py-2.5">
                      <div className="font-medium text-foreground">
                        {r.primary}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {r.secondary}
                      </div>
                    </td>
                    <td className="px-3 py-2.5 text-muted-foreground">
                      {r.secondary.split(" · ")[0]}
                    </td>
                    <td className="px-3 py-2.5 font-medium text-foreground">
                      {r.value}
                    </td>
                    <td className="px-3 py-2.5">
                      <div className="flex items-center gap-2">
                        <Dot status={r.status} />
                        <span className="text-xs text-muted-foreground">
                          {r.note}
                        </span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      ))}
    </div>
  );
}

export function IndustryPlaybooks() {
  const { industry } = useIndustry();
  return (
    <Card id="industry-playbooks">
      <CardHeader
        title="Recommended plays"
        subtitle={`Tailored for ${industry.name.toLowerCase()}`}
      />
      <ul className="space-y-3">
        {industry.playbooks.map((p) => (
          <li
            key={p.title}
            className="flex items-start justify-between gap-4 rounded-lg border border-border/70 p-3"
          >
            <div className="min-w-0">
              <div className="font-medium text-foreground">{p.title}</div>
              <div className="text-xs text-muted-foreground">{p.rationale}</div>
            </div>
            <Chip
              status={
                p.impact === "High"
                  ? "primary"
                  : p.impact === "Medium"
                    ? "watch"
                    : "neutral"
              }
            >
              {p.impact} impact
            </Chip>
          </li>
        ))}
      </ul>
    </Card>
  );
}
