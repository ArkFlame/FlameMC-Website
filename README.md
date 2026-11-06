# FlameMC Website · Astro 6

Static, responsive product website for FlameMC. Deploys with GitHub Actions to **https://flamemc.arkflame.com**. No server, database, JS framework hydration, hosted fonts, or third-party trackers.

## Requirements

- Node.js 22.12+ (Node 24 recommended on CI)
- npm

```bash
npm install
npm run dev
npm run check:static
npm run build
npm run preview
```

Astro outputs `dist/`. The HTML page is `src/pages/index.astro`. CSS, assets, and progressive-enhancement JavaScript are in `public/`.

## GitHub Pages deployment

1. Push these files into the desired **flamemc-website** GitHub repository, using `main` as the deployment branch.
2. In repository **Settings → Pages**, set **Build and deployment → Source → GitHub Actions**.
3. In the same section, set **Custom domain** to `flamemc.arkflame.com` and save. GitHub's Pages configuration must recognize the domain even when the workflow includes a `CNAME` file.
4. In the `arkflame.com` DNS zone, add **CNAME**: `flamemc` → `<your-actual-GitHub-account-or-organization>.github.io` (do not append `/flamemc-website` and do not point to `arkflame.com`).
5. Run `.github/workflows/deploy.yml` on `main`. Once GitHub finishes TLS certificate provisioning, enable **Enforce HTTPS**.

`astro.config.mjs` intentionally uses `site: 'https://flamemc.arkflame.com'` and **no** `base` path, because this is a custom-domain project site.

The official Astro action requires a package-manager choice or a lockfile. This repository uses direct `npm install` in GitHub Actions, so the first deployment doesn't depend on an unavailable generated lockfile. Commit `package-lock.json` after your first successful `npm install` locally, then optionally change the CI step to `npm ci` for deterministic installs.

## Content and claims

- The site describes Folia-based regionized threading and FlameMC's owner-aware compatibility approach, not universal acceleration or 100% Paper plugin compatibility.
- The scheduling/CPU comparison is a **conceptual diagram**, explicitly labeled **not a benchmark**. It intentionally does **not** reproduce the uploaded example's unverified TPS and CPU figures.
- Compatibility varies with plugin code and operation. Test plugin workloads on your target build.
- Before public launch, verify the project's public source/download URL and add a real, verified destination in the header CTA if available. Current CTAs scroll to in-page explanatory sections or link to the known ArkFlame Studios site.

## Design/technical details

- Primary pages: single long-form landing page with header, hero, advantages, ownership diagram, conceptual comparison, compatibility section, FAQs, and CTA.
- CSS animations and a small vanilla JS controller; honors `prefers-reduced-motion`.
- Responsive across 320–1920px. Semantic headings, keyboard-accessible nav, focus indicators, alt text, FAQ native `details` elements.
- Metadata: canonical URL, Open Graph image, robots.txt, sitemap.xml, SVG favicon, and CNAME.

## Not included / operational risks

- No live server benchmarks or measured compatibility matrix was supplied.
- No CMS, downloads backend, telemetry, cookies, contact form or external runtime service.
- DNS/Pages settings and deployment to the user’s repository cannot be changed from this archive.
