Set-Location "c:\Users\DELL\Downloads\office-briefing\frontend-lovable"

$dirs = @(
  "src",
  "src/routes",
  "src/components",
  "src/components/dashboard",
  "src/components/ui",
  "src/context",
  "src/data",
  "src/lib"
)

foreach ($d in $dirs) {
  New-Item -ItemType Directory -Force -Path $d | Out-Null
}

Move-Item -Force __root.tsx src/routes/__root.tsx
Move-Item -Force index.tsx src/routes/index.tsx
Move-Item -Force help.tsx src/routes/help.tsx
Move-Item -Force setup.tsx src/routes/setup.tsx

Move-Item -Force Shell.tsx src/components/Shell.tsx
Move-Item -Force ProductTour.tsx src/components/ProductTour.tsx
Move-Item -Force IndustrySwitcher.tsx src/components/IndustrySwitcher.tsx

Move-Item -Force SectionJump.tsx src/components/dashboard/SectionJump.tsx
Move-Item -Force ConnectorsPanel.tsx src/components/dashboard/ConnectorsPanel.tsx
Move-Item -Force CustomizePanel.tsx src/components/dashboard/CustomizePanel.tsx
Move-Item -Force IndustryModules.tsx src/components/dashboard/IndustryModules.tsx
Move-Item -Force sections.tsx src/components/dashboard/sections.tsx
Move-Item -Force primitives.tsx src/components/dashboard/primitives.tsx
Move-Item -Force use-mobile.tsx src/components/dashboard/use-mobile.tsx

Move-Item -Force DashboardLayoutContext.tsx src/context/DashboardLayoutContext.tsx
Move-Item -Force IndustryContext.tsx src/context/IndustryContext.tsx

Move-Item -Force dashboardModules.ts src/data/dashboardModules.ts
Move-Item -Force industries.ts src/data/industries.ts
Move-Item -Force mock.ts src/data/mock.ts

Move-Item -Force utils.ts src/lib/utils.ts
Move-Item -Force lovable-error-reporting.ts src/lib/lovable-error-reporting.ts
Move-Item -Force error-capture.ts src/lib/error-capture.ts
Move-Item -Force error-page.ts src/lib/error-page.ts

Move-Item -Force router.tsx src/router.tsx
Move-Item -Force routeTree.gen.ts src/routeTree.gen.ts
Move-Item -Force server.ts src/server.ts
Move-Item -Force start.ts src/start.ts
Move-Item -Force styles.css src/styles.css

Write-Output "restructure_done"
