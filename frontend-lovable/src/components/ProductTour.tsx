import { useEffect, useState } from "react";

const STEPS = [
  {
    title: "Start with the Pulse",
    body: "Your day opens with a Day Score, a strategic pulse, and the few signals that decide whether today goes well.",
    target: "Hero & Day Score",
  },
  {
    title: "Clear the Action Register",
    body: "Only the moves that need you. Priorities are calibrated against deals, renewals, and team health.",
    target: "Action Register & Approvals",
  },
  {
    title: "Let Autopilot draft for you",
    body: "Follow-ups, meeting recaps, and next steps are drafted. You review, edit, and send — nothing falls through.",
    target: "Follow-up Autopilot",
  },
  {
    title: "See revenue with confidence",
    body: "Forecast, deal motion, and renewals are stitched together so you can commit a number you trust.",
    target: "Forecast, Deals & Renewals",
  },
  {
    title: "Briefings, ready before you are",
    body: "A morning briefing summarizes the night, the day, and the plays to run — written in your voice.",
    target: "Executive Briefing",
  },
];

export function ProductTour() {
  const [open, setOpen] = useState(false);
  const [step, setStep] = useState(0);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!open) return;
      if (e.key === "Escape") setOpen(false);
      if (e.key === "ArrowRight")
        setStep((s) => Math.min(STEPS.length - 1, s + 1));
      if (e.key === "ArrowLeft") setStep((s) => Math.max(0, s - 1));
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  const current = STEPS[step];

  return (
    <>
      <button
        type="button"
        onClick={() => {
          setStep(0);
          setOpen(true);
        }}
        className="fixed bottom-6 right-6 z-40 inline-flex items-center gap-2 rounded-full bg-primary px-4 py-3 text-sm font-medium text-primary-foreground shadow-[0_12px_40px_-12px_oklch(0.32_0.06_210/0.5)] transition hover:scale-[1.02] hover:opacity-95"
        aria-label="Open product tour"
      >
        <span className="grid size-5 place-items-center rounded-full bg-primary-foreground text-primary text-[11px] font-bold">
          ?
        </span>
        Product Tour
      </button>

      {open ? (
        <div
          className="fixed inset-0 z-50 grid place-items-center bg-foreground/30 px-4 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-labelledby="tour-title"
          onClick={() => setOpen(false)}
        >
          <div
            className="card-surface w-full max-w-lg p-6 reveal"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between text-xs uppercase tracking-[0.16em] text-muted-foreground">
              <span>Lucent Tour</span>
              <span>
                {step + 1} / {STEPS.length}
              </span>
            </div>
            <h2
              id="tour-title"
              className="mt-2 font-display text-3xl text-foreground"
            >
              {current.title}
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              <span className="font-medium text-foreground">
                {current.target}.
              </span>{" "}
              {current.body}
            </p>

            <div className="mt-5 h-1 w-full overflow-hidden rounded-full bg-border">
              <div
                className="h-full bg-primary transition-all"
                style={{ width: `${((step + 1) / STEPS.length) * 100}%` }}
              />
            </div>

            <div className="mt-5 flex items-center justify-between">
              <button
                className="text-sm text-muted-foreground hover:text-foreground"
                onClick={() => setOpen(false)}
              >
                Skip tour
              </button>
              <div className="flex items-center gap-2">
                <button
                  className="rounded-md border border-border bg-surface px-3 py-2 text-sm font-medium text-foreground disabled:opacity-40"
                  onClick={() => setStep((s) => Math.max(0, s - 1))}
                  disabled={step === 0}
                >
                  Back
                </button>
                {step < STEPS.length - 1 ? (
                  <button
                    className="rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground hover:opacity-90"
                    onClick={() => setStep((s) => s + 1)}
                  >
                    Next
                  </button>
                ) : (
                  <button
                    className="rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground hover:opacity-90"
                    onClick={() => setOpen(false)}
                  >
                    Get started
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
