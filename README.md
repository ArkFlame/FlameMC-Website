# FlameMC Website — Static GitHub Pages Release V6

**No Astro build, npm, lockfiles, GitHub Pages settings API, or deployment workflow is required.**

This repository is a complete, prebuilt static website for **https://flamemc.arkflame.com/**.

## Publishing

1. Commit **all files from this release at the repository root** of `ArkFlame/FlameMC-Website` on branch `main` (not inside an additional folder). Replace the old Astro `src/`, `public/`, `package.json` and obsolete deploy workflow — the released website is already compiled. Keep `.nojekyll` even though it is hidden on some systems.
2. In GitHub **Settings → Pages**, use **Deploy from a branch**, `main` and `/(root)`. This is the configuration matching the provided Jekyll logs.
3. Verify that both `index.html` and the **empty file** `.nojekyll` appear in the repository's root on `main`. `CNAME` must contain exactly `flamemc.arkflame.com`.
4. When Pages finishes publishing, open https://flamemc.arkflame.com/ and https://flamemc.arkflame.com/guides/ . The repository Code tab will show this README; that is normal.

## Why it works with your current configuration

GitHub Pages branch publishing traditionally runs Jekyll. A root `.nojekyll` disables Jekyll; GitHub deploys HTML/CSS/JS directly. This package also contains **no `.astro` files**, so a fallback Jekyll build has no Astro frontmatter to parse. The root `index.html` takes precedence over README rendering.

**Files you must see at the root:** `index.html`, `.nojekyll`, `CNAME`, `styles/`, `scripts/`, `assets/`, `guides/`, `download/`, `sitemap.xml`, `rss.xml`.

## Content

- Main landing page with animation, architecture visualization, and BuiltByBit download CTA
- 7 guides under `/guides/`, linked by sitemap and RSS
- Download page, metadata, Open Graph image, 404, robots.txt
- No external runtime dependencies, fonts, tracking, or JavaScript hydration

## Domain

`CNAME` contains `flamemc.arkflame.com`. The DNS record should be `flamemc` → `arkflame.github.io` for this organization. Confirm the domain is assigned to this repository in Settings → Pages and HTTPS is enabled once its certificate has been issued.

## Verification and risks

The release is ready for direct branch publishing; the actual GitHub repository, Pages configuration, DNS, and external HTTPS endpoint cannot be changed or certified from an unauthenticated archive. Do not upload this archive as a single file; extract it and push its contents. If the site still shows README after an actual publishing run, inspect Pages' source branch/folder and the deployed hostname rather than editing the HTML.
