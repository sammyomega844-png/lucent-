import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  DEFAULT_INDUSTRY,
  getIndustry,
  INDUSTRIES,
  type IndustryId,
  type IndustryPreset,
} from "@/data/industries";

interface Ctx {
  industryId: IndustryId;
  industry: IndustryPreset;
  setIndustryId: (id: IndustryId) => void;
  all: IndustryPreset[];
}

const IndustryCtx = createContext<Ctx | null>(null);
const STORAGE_KEY = "lucent.industry";

export function IndustryProvider({ children }: { children: ReactNode }) {
  const [industryId, setIndustryIdState] =
    useState<IndustryId>(DEFAULT_INDUSTRY);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY) as IndustryId | null;
      if (stored && INDUSTRIES.some((i) => i.id === stored)) {
        setIndustryIdState(stored);
      }
    } catch {
      // ignore
    }
  }, []);

  const setIndustryId = (id: IndustryId) => {
    setIndustryIdState(id);
    try {
      localStorage.setItem(STORAGE_KEY, id);
    } catch {
      // ignore
    }
  };

  const value = useMemo<Ctx>(
    () => ({
      industryId,
      industry: getIndustry(industryId),
      setIndustryId,
      all: INDUSTRIES,
    }),
    [industryId],
  );

  return <IndustryCtx.Provider value={value}>{children}</IndustryCtx.Provider>;
}

export function useIndustry(): Ctx {
  const ctx = useContext(IndustryCtx);
  if (!ctx) throw new Error("useIndustry must be used inside IndustryProvider");
  return ctx;
}
