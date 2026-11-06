# FlameMC — Minecraft server software

Production Astro website for **https://flamemc.arkflame.com/**. FlameMC is **available now on BuiltByBit**: https://builtbybit.com/resources/flamemc-extreme-async-performance.133143/.

## Fix the Jekyll build error (Pages source setting)

A run named **`pages build and deployment`** containing `actions/jekyll-build-pages@v1` means GitHub is attempting to build the repository's `.astro` source as Jekyll. The Astro templates are not Jekyll YAML frontmatter. **Do not edit them to satisfy Jekyll.** This is a GitHub repository setting, not an Astro template error.

**One-time fix (repository admin):**

1. Open **Settings → Pages → Build and deployment → Source** in `ArkFlame/FlameMC-Website`.
2. Select **GitHub Actions**, not **Deploy from a branch**.
3. In **Actions**, run **Build and deploy FlameMC website** on `main` after pushing this repository.

Or configure the source through the authenticated GitHub CLI:

```bash
bash scripts/fix-github-pages.sh ArkFlame/FlameMC-Website
```

The script only changes the Pages publishing mode to `workflow` and verifies it. It requires a GitHub account with repository admin / Pages management permissions. It does **not** push repository changes, update DNS, or deploy without the workflow being run.

The workflow is `.github/workflows/deploy.yml`: it installs Node dependencies, validates source, builds Astro, verifies `dist/index.html`, uploads `dist/` as a Pages artifact, and deploys with `actions/deploy-pages`. It also detects accidental `legacy` publishing configuration with an actionable error message.

The custom domain remains `flamemc.arkflame.com`, configured under Settings → Pages and through DNS. `public/CNAME` alone does not set GitHub Pages' domain. A README appearing under the GitHub **Code** tab is normal; only seeing it at the actual website URL indicates a publishing problem.

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
