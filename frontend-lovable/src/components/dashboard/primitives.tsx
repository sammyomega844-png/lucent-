import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Card({
  children,
  className,
  id,
  as: As = "section",
}: {
  children: ReactNode;
  className?: string;
  id?: string;
  as?: "section" | "div" | "article";
}) {
  return (
    <As
      id={id}
      className={cn(
        "card-surface card-surface-hover p-5 sm:p-6 reveal",
        className,
      )}
    >
      {children}
    </As>
  );
}

export function CardHeader({
  title,
  subtitle,
  right,
  eyebrow,
}: {
  title: string;
  subtitle?: string;
  right?: ReactNode;
  eyebrow?: string;
}) {
  return (
    <header className="mb-4 flex items-start justify-between gap-4">
      <div className="min-w-0">
        {eyebrow ? (
          <div className="mb-1 text-[11px] font-medium uppercase tracking-[0.14em] text-muted-foreground">
            {eyebrow}
          </div>
        ) : null}
        <h3 className="font-display text-xl text-foreground sm:text-2xl">
          {title}
        </h3>
        {subtitle ? (
          <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
        ) : null}
      </div>
      {right ? <div className="shrink-0">{right}</div> : null}
    </header>
  );
}

export function Chip({
  status,
  children,
  className,
}: {
  status?: "healthy" | "watch" | "risk" | "primary" | "neutral";
  children: ReactNode;
  className?: string;
}) {
  const cls =
    status === "healthy"
      ? "chip chip-healthy"
      : status === "watch"
        ? "chip chip-watch"
        : status === "risk"
          ? "chip chip-risk"
          : status === "primary"
            ? "chip chip-primary"
            : "chip";
  return <span className={cn(cls, className)}>{children}</span>;
}

export function Dot({ status }: { status: "healthy" | "watch" | "risk" }) {
  const bg =
    status === "healthy"
      ? "bg-healthy"
      : status === "watch"
        ? "bg-watch"
        : "bg-risk";
  return (
    <span aria-hidden className={cn("inline-block size-2 rounded-full", bg)} />
  );
}

export function TrendArrow({ trend }: { trend: "up" | "down" | "flat" }) {
  if (trend === "up")
    return (
      <span aria-label="up" className="text-healthy">
        ▲
      </span>
    );
  if (trend === "down")
    return (
      <span aria-label="down" className="text-risk">
        ▼
      </span>
    );
  return (
    <span aria-label="flat" className="text-muted-foreground">
      ▬
    </span>
  );
}
