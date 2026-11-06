# FlameMC Website — Astro 6

Source for **https://flamemc.arkflame.com/**. Download FlameMC on [BuiltByBit](https://builtbybit.com/resources/flamemc-extreme-async-performance.133143/).

## Fix: GitHub Pages is running Jekyll instead of Astro

If an Actions log says `actions/jekyll-build-pages@v1` or `Invalid YAML front matter in src/pages/*.astro`, the **repository's Pages publishing source is still set to "Deploy from a branch."** Astro files contain JavaScript/TypeScript frontmatter, not Jekyll YAML. Do not edit them for Jekyll and do not publish the repository root.

**One-time correction:** In [repository Settings → Pages](https://github.com/ArkFlame/FlameMC-Website/settings/pages), change **Build and deployment → Source → GitHub Actions**. Then run the `Build and deploy FlameMC website` workflow from [Actions](https://github.com/ArkFlame/FlameMC-Website/actions/workflows/deploy.yml), using `main`.

**Command-line equivalent (requires repository Pages/Admin permissions):**

```bash
bash scripts/fix-github-pages.sh ArkFlame/FlameMC-Website
```

This script switches Pages to Actions, verifies the custom domain, and triggers the deployment **only if the workflow exists on remote main**. It does not commit, push, or overwrite repository files. The GitHub CLI must be installed and authenticated via `gh auth login`. If GitHub denies the Pages settings API call, use the Settings UI; a normal workflow `GITHUB_TOKEN` cannot grant itself repository admin permissions.

After the workflow completes, verify the live page, not the repository's **Code** tab:

```bash
bash scripts/diagnose-github-pages.sh ArkFlame/FlameMC-Website
```

The repo's Code tab will always show `README.md`; that is expected and is not the website.

## Install, develop, build

Use **Node.js 24** in CI. Node.js **22.12+** is supported by Astro 6.

```bash
npm install
npm run check:static
npm run build
npm run check:deploy
npm run dev
```

The site lives under `src/pages` with seven SEO articles in `src/content/guides`. Assets are in `public/`. `npm run build` creates `dist/`. Only `dist/` is uploaded through `.github/workflows/deploy.yml`. It uses `actions/configure-pages`, `actions/upload-pages-artifact`, and `actions/deploy-pages` following the [GitHub Pages custom Actions workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Custom domain

- Pages custom domain: `flamemc.arkflame.com`
- Astro config `site: 'https://flamemc.arkflame.com'`, **no `base` prefix**.
- DNS: `flamemc` CNAME to your GitHub Pages account/organization's `*.github.io` endpoint.
- `public/CNAME` is bundled as `dist/CNAME`. It is **not** a substitute for configuring the domain in Pages settings.
- `public/.nojekyll` is bundled as `dist/.nojekyll`; it **cannot** switch Pages away from a Jekyll build.

## Release contents

The landing page describes Folia regionized threading, FlameMC's compatibility approach, interactive conceptual diagrams, FAQs, and the available BuiltByBit listing. The seven guides cover Paper, Folia, Canvas, UniverseSpigot, migration, and region threading. Conceptual scheduling illustrations are not benchmark results; compatibility varies by workload and server build.

## Verification limitations

Local static checks can verify source correctness and workflow structure. The full Astro build requires npm dependencies. The live repository setting, custom-domain DNS, GitHub Actions run, and public page response must be verified after applying the one-time Pages configuration change. No source archive can change the live GitHub Pages publishing mode without GitHub administration access.
