import { useEffect, useRef, useState } from "react";
import { useIndustry } from "@/context/IndustryContext";

export function IndustrySwitcher() {
  const { industry, all, setIndustryId } = useIndustry();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onDocClick(e: MouseEvent) {
      if (!ref.current?.contains(e.target as Node)) setOpen(false);
    }
    function onEsc(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    document.addEventListener("mousedown", onDocClick);
    document.addEventListener("keydown", onEsc);
    return () => {
      document.removeEventListener("mousedown", onDocClick);
      document.removeEventListener("keydown", onEsc);
    };
  }, []);

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-haspopup="listbox"
        aria-expanded={open}
        className="inline-flex items-center gap-2 rounded-md border border-border bg-background px-3 py-1.5 text-sm text-foreground transition hover:bg-secondary"
      >
        <span className="text-[10px] font-medium uppercase tracking-[0.16em] text-muted-foreground">
          Workspace
        </span>
        <span className="font-medium">{industry.name}</span>
        <span aria-hidden className="text-muted-foreground">
          ▾
        </span>
      </button>
      {open ? (
        <div
          role="listbox"
          className="absolute right-0 z-40 mt-2 w-72 overflow-hidden rounded-lg border border-border bg-background shadow-xl"
        >
          <div className="px-3 py-2 text-[11px] uppercase tracking-[0.14em] text-muted-foreground">
            Switch industry
          </div>
          <ul className="max-h-80 overflow-auto py-1">
            {all.map((p) => {
              const active = p.id === industry.id;
              return (
                <li key={p.id}>
                  <button
                    type="button"
                    role="option"
                    aria-selected={active}
                    onClick={() => {
                      setIndustryId(p.id);
                      setOpen(false);
                    }}
                    className={
                      "flex w-full flex-col items-start gap-0.5 px-3 py-2 text-left text-sm transition " +
                      (active
                        ? "bg-primary-soft text-primary"
                        : "text-foreground hover:bg-secondary")
                    }
                  >
                    <span className="font-medium">{p.name}</span>
                    <span className="text-xs text-muted-foreground">
                      {p.tagline}
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
