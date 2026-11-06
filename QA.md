# FlameMC Website — V2 Deployment Repair Verification

## Root cause and repair

**Symptom:** GitHub Pages displays the repository README rather than the website.

**Diagnosis:** GitHub Pages configured to publish the source branch runs Jekyll/Markdown instead of building Astro. When no root `index.html` is present, Pages may use `README.md` as the entry file. Correct target is the compiled Astro artifact `dist/index.html`.

**Change:** `.github/workflows/deploy.yml` builds Astro, verifies the resulting website and articles (`npm run check:deploy`), and uploads **only** `dist/`. `.nojekyll` is included. README documents exact Pages source selection and domain setup. No new frontend runtime/framework was introduced.

## Evidence

- `node tests/check-static.mjs` — **PASS**: seven guides, SEO canonical/schema, CNAME, product CTA, file paths, sitemap/RSS generation, and workflow publishing target.
- Chromium inline-content fixture: homepage 1440px and 390px, guides index 390px, Paper vs Folia article 390px, download page 390px — **PASS**: no horizontal overflow, broken loaded images, or JavaScript errors; BuiltByBit links present. On mobile, navigation expanded (`aria-expanded=true`) and closed after Escape (`false`).
- `flamemc-website-pages-fix-preview.png` — full desktop screenshot of the browser preview fixture.
- **Astro build not run:** `npm view astro@6.4.6` failed with DNS `EAI_AGAIN` from registry.npmjs.org. The workflow's production compile remains a CI gate, not a claimed local pass.
- **Not deployed:** GitHub repository Pages settings/DNS/live URL are not accessible for mutation here. Selecting **Source → GitHub Actions** is required once, even when the workflow and custom `CNAME` exist.

Browser fixture generation is not an Astro compiler and therefore does not certify the production build.
