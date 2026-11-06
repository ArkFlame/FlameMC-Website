# FlameMC GitHub Pages V5 — Verification

## Root cause

The user-supplied Actions log invokes `actions/jekyll-build-pages@v1` and reports YAML parsing errors on `.astro` source files. This confirms the Pages publishing configuration is `legacy` (branch/Jekyll), or a workflow using Jekyll remains active. Deploying compiled Astro requires Pages `build_type=workflow`. A source-code-only patch cannot flip this repository setting.

## Source verification performed

- `node tests/check-static.mjs`: PASS — seven articles, CTA links, assets, metadata, sitemap/RSS references, accessibility checks.
- `bash -n scripts/fix-github-pages.sh scripts/diagnose-github-pages.sh`: PASS.
- GitHub workflow parsed with Python YAML loader: PASS — push and manual triggers, `contents:read`, `pages:write`, `id-token:write`, Astro `npm run build`, `npm run check:deploy`, artifact path `./dist`, deployment action.
- `public/CNAME`: PASS — contains `flamemc.arkflame.com`.
- Repair script with mocked GitHub CLI: PASS — edits Pages `build_type=workflow`, assigns custom domain if needed, confirms remote workflow, triggers `deploy.yml` on `main`.

## Not executed / risks

- No authenticated GitHub admin access in this environment. The live Pages publishing source has NOT been changed.
- No public GitHub repository fetch from this runtime, and no DNS/site response verification.
- `npm run build` and production dist validation require installing Astro dependencies; npm registry unavailable in this environment.
- Before changing or copying archive contents into a live clone, preserve any uncommitted work. This package does not reset, delete, or mutate existing user files on GitHub.

## Required deployment proof

1. Repository Pages API `.build_type == "workflow"`.
2. `deploy.yml` custom workflow reaches a successful deploy (as distinct from `pages build and deployment` Jekyll run).
3. `https://flamemc.arkflame.com/` returns an HTML homepage containing `Scale your world.` and `Keep your plugins.`, and a BuiltByBit download link.
