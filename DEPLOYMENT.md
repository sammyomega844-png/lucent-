# Deployment Guide

## Pre-deploy checks

Run this from the repository root:

```powershell
cmd /c run_pipeline.bat
```

Expected result:
- backend update succeeds
- artifact sync copies JSON files into `frontend-lovable/src/data/generated`
- frontend build succeeds
- app health page is available at `/status`

## Netlify (recommended first)

This repository includes `netlify.toml` configured for the frontend app in `frontend-lovable`.

### One-time setup

1. Push repository to GitHub/GitLab/Bitbucket.
2. In Netlify, choose "Add new site" -> "Import an existing project".
3. Select this repository.
4. Netlify reads `netlify.toml` automatically.
5. Deploy.

### Build settings (if Netlify asks manually)

- Base directory: `frontend-lovable`
- Build command: `npm run build`
- Publish directory: `.output/public`
- Node version: `22`

### Production URL and custom domain

1. After first deploy, Netlify gives a URL like `https://<site-name>.netlify.app`.
2. In Site settings -> Domain management, add your custom domain.
3. Point DNS at Netlify as instructed (usually CNAME for subdomain, A/ALIAS for apex).
4. Enable HTTPS certificate (Netlify provisions it automatically).

### Automatic deploy on push to main

Workflow file: `.github/workflows/deploy-netlify.yml`

Add these GitHub repository secrets:

- `NETLIFY_AUTH_TOKEN`
- `NETLIFY_SITE_ID`

`NETLIFY_SITE_ID` can be the Netlify site ID, the site name, or the Netlify site URL. The deploy workflow resolves it to the correct site automatically.

Once secrets are set, every push to `main` auto-builds and deploys to Netlify.

## Vercel (alternative)

This repository includes `vercel.json` configured for static output.

1. Import repository in Vercel.
2. Vercel auto-detects `vercel.json`.
3. Deploy.
4. Add domain in Project settings -> Domains.

## Cloudflare Pages (alternative)

Use these settings in Cloudflare Pages:

- Build command: `npm --prefix frontend-lovable run build`
- Build output directory: `frontend-lovable/.output/public`
- Root directory: repository root

Then add your domain in Cloudflare Pages project settings.

## Optional CI gate before deploy

GitHub Actions already runs backend checks in `.github/workflows/ci.yml`.
If you want frontend lint/build in CI as a required deployment gate, add a second job for `frontend-lovable`.

## Notes

- The frontend auto-syncs data before `dev`, `build`, and `preview` via npm hooks.
- If backend artifacts are regenerated, deployment picks up latest JSON during build.
- Use `/status` after each deployment as a quick smoke-test for build metadata and live data checks.
