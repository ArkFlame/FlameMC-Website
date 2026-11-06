# FlameMC — Minecraft server software

Production Astro website for **https://flamemc.arkflame.com/**. FlameMC is **available now on BuiltByBit**: https://builtbybit.com/resources/flamemc-extreme-async-performance.133143/.

## Fix: GitHub Pages displays this README instead of the site

**Cause:** GitHub Pages is publishing `main` as a Jekyll/branch site instead of publishing the compiled Astro pages. The repository contains `.astro` source files; it does not contain a ready-to-serve root `index.html`. If the README appears at the public domain, check the Pages publishing source and the latest deployment artifact. If the README appears on `github.com` in the Code tab, that is normal repository behavior.

1. Open the actual repository at **Settings → Pages → Build and deployment → Source**, select **GitHub Actions** (not *Deploy from a branch*).
2. Go to **Actions → Build and deploy FlameMC website → Run workflow**, select **main**, and run it. The workflow checks the source, builds Astro, verifies that `dist/index.html` exists, then publishes **`dist/`**.
3. In **Settings → Pages**, set **Custom domain** to `flamemc.arkflame.com`. DNS needs a record `flamemc CNAME <actual-account-or-org>.github.io`. Enable **Enforce HTTPS** once available.

**Important:** If you see this README while browsing `github.com/.../flamemc-website`, that is *normal GitHub repository behavior*, not the public website. The actual website is `https://flamemc.arkflame.com/`.

The workflow only deploys on `main` or manual dispatch. GitHub Pages' **Source** setting cannot be reliably changed by a file committed to the repository. Confirm it once in Settings.

## Local development

Requires Node.js 22.12+ and npm (Node.js 24 recommended).

```bash
npm install
npm run dev
npm run check:static
npm run build
npm run check:deploy
npm run preview
```

- Source pages: `src/pages/`; articles: `src/content/guides/`.
- Compiled deployment output: `dist/` — **never publish the repository root**.
- HTML/CSS and small progressive-enhancement JS; no database, API server, hydration framework, hosted fonts, or trackers.
- GitHub Pages workflow: `.github/workflows/deploy.yml`.
- Domain: `astro.config.mjs` sets `site: 'https://flamemc.arkflame.com'`, intentionally without a `base` path. `public/CNAME` is copied into `dist/CNAME` for portability, but GitHub Actions-based Pages uses the custom domain configured in repository Settings; the CNAME file alone does not configure the domain.
- `public/.nojekyll` is copied into `dist/.nojekyll`.
- Every deployment verifies generated homepage, guides, critical assets, the CNAME and sitemap; it fails rather than publishing a README.

## Product content

The landing page showcases Folia regionized threading, FlameMC's compatibility approach, conceptual concurrency diagrams, and the live listing. Seven technical guides compare Paper, Folia, Canvas, UniverseSpigot, and FlameMC, explain region ownership, and discuss migration and plugin compatibility. Cross-architecture diagrams are **illustrative**, not measured TPS benchmarks. Plugin compatibility varies by build and workload.

## Limitations

The product itself and any claimed throughput are not benchmarked by this website project. GitHub repository settings, DNS and the production endpoint require deployment access; they cannot be modified by extracting the source archive.
