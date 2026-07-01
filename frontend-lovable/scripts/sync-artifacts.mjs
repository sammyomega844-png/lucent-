import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const repoRoot = resolve(__dirname, "..", "..");
const frontendRoot = resolve(__dirname, "..");
const generatedDir = join(frontendRoot, "src", "data", "generated");

const artifactFiles = [
  "action_register.json",
  "follow_up_plan.json",
  "meeting_execution_plan.json",
  "customer_health_report.json",
  "pipeline_risk_report.json",
  "approval_workflow.json",
  "kpi_digest_report.json",
  "communication_timeline.json",
  "recommendations.json",
  "revenue_forecast.json",
  "deal_progression.json",
  "renewal_reminders.json",
  "weekly_digest.json",
];

if (!existsSync(generatedDir)) {
  mkdirSync(generatedDir, { recursive: true });
}

const copied = [];
const missing = [];

for (const fileName of artifactFiles) {
  const source = join(repoRoot, fileName);
  const target = join(generatedDir, fileName);

  if (!existsSync(source)) {
    missing.push(fileName);
    continue;
  }

  copyFileSync(source, target);
  copied.push(fileName);
}

if (copied.length) {
  console.log(
    `[sync-artifacts] Copied ${copied.length} file(s) to src/data/generated`,
  );
}

if (missing.length) {
  console.warn(
    `[sync-artifacts] Missing ${missing.length} file(s): ${missing.join(", ")}`,
  );
}

if (!copied.length) {
  console.error("[sync-artifacts] No artifacts were copied.");
  process.exit(1);
}
