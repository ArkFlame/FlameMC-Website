# QA report — FlameMC website v1

## Browser-verified source rendering

The homepage's `.astro` file contains ordinary semantic HTML (no server-side expressions). For browser QA, it was rendered directly after inlining the bundled public CSS/JS/assets, without a network server. This tests HTML/CSS/JS behavior but **does not substitute for an `astro build`**.

- Chromium screenshots generated at 1440, 900, 390, and 320 px widths.
- No horizontal overflow at any tested width.
- No broken image in final screenshot pass.
- All `[data-reveal]` sections became visible during scrolling.
- No JavaScript page errors at tested widths.
- 390px navigation opens via toggle and closes with Escape.
- Reduced-motion media query tested at 320px.
- Static test checks local resource existence, fragment destinations, CNAME and benchmark disclaimer.

## Unverified / requires connected build environment

- **Astro 6.4.6 installation and `npm run build`:** package registry DNS unavailable (`EAI_AGAIN`). The generated GitHub Actions workflow performs the install, static check, build, and Pages deployment in GitHub's own runner.
- GitHub Pages activation, DNS CNAME, custom-domain verification, and HTTPS: external account changes are not in this archive.
- Firefox and Safari visual regression.
- Server/plugin performance claims: illustrative visual, not measured benchmarks.

## Command executed

```text
node tests/check-static.mjs  => PASS
python tests/visual-test.py => PASS visual checks, 4 breakpoints
npm view astro@6.4.6       => BLOCKED EAI_AGAIN (registry DNS)
```

See `previews/qa.json` for machine-readable viewport results.
