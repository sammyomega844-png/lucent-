import { useEffect, useState } from "react";

export type JumpItem = { id: string; label: string };

export function SectionJump({ items }: { items: JumpItem[] }) {
  const [active, setActive] = useState<string>(items[0]?.id ?? "");

  useEffect(() => {
    const elements = items
      .map((i) => document.getElementById(i.id))
      .filter((el): el is HTMLElement => !!el);

    if (elements.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
        if (visible[0]) setActive(visible[0].target.id);
      },
      { rootMargin: "-30% 0px -55% 0px", threshold: [0, 0.25, 0.5, 1] },
    );

    elements.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [items]);

  const jumpTo = (id: string) => {
    const el = document.getElementById(id);
    if (!el) return;
    const top = el.getBoundingClientRect().top + window.scrollY - 96;
    window.scrollTo({ top, behavior: "smooth" });
  };

  return (
    <nav
      aria-label="Jump to section"
      className="sticky top-[60px] z-20 -mx-4 border-y border-border/60 bg-background/80 px-4 py-2 backdrop-blur sm:-mx-6 sm:px-6"
    >
      <div className="flex gap-1.5 overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {items.map((i) => {
          const isActive = active === i.id;
          return (
            <button
              key={i.id}
              onClick={() => jumpTo(i.id)}
              className={
                "shrink-0 rounded-full px-3 py-1.5 text-xs font-medium transition " +
                (isActive
                  ? "bg-foreground text-background"
                  : "border border-border bg-surface text-muted-foreground hover:text-foreground")
              }
            >
              {i.label}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
