import { Link, useRouterState } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { IndustrySwitcher } from "@/components/IndustrySwitcher";

function Logo() {
  return (
    <Link to="/" className="flex items-center gap-2">
      <span className="grid size-7 place-items-center rounded-md bg-primary text-primary-foreground font-display text-lg leading-none">
        L
      </span>
      <span className="font-display text-xl tracking-tight text-foreground">
        Lucent
      </span>
      <span className="hidden text-[11px] uppercase tracking-[0.16em] text-muted-foreground sm:inline">
        Executive Intelligence
      </span>
    </Link>
  );
}

function NavLink({ to, children }: { to: string; children: ReactNode }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const active = pathname === to;
  return (
    <Link
      to={to}
      className={
        "rounded-md px-3 py-1.5 text-sm transition " +
        (active
          ? "bg-primary-soft text-primary"
          : "text-muted-foreground hover:bg-secondary hover:text-foreground")
      }
    >
      {children}
    </Link>
  );
}

export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-dvh">
      <header className="sticky top-0 z-30 border-b border-border/70 bg-background/70 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
          <Logo />
          <nav aria-label="Primary" className="flex items-center gap-1">
            <NavLink to="/">Dashboard</NavLink>
            <NavLink to="/setup">Setup</NavLink>
            <NavLink to="/help">Help</NavLink>
            <NavLink to="/status">Status</NavLink>
          </nav>
          <div className="hidden items-center gap-2 sm:flex">
            <IndustrySwitcher />
            <span className="chip chip-healthy">All systems calm</span>
            <span className="grid size-8 place-items-center rounded-full bg-primary text-primary-foreground text-sm font-medium">
              EM
            </span>
          </div>
        </div>
      </header>
      <main id="main" className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-10">
        {children}
      </main>
      <footer className="mx-auto max-w-7xl px-4 pb-10 pt-2 text-xs text-muted-foreground sm:px-6">
        © {new Date().getFullYear()} Lucent · Executive Intelligence Platform
      </footer>
    </div>
  );
}
