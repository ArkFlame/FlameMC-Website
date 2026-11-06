#!/usr/bin/env bash
set -euo pipefail

# The repository hosts Astro source, not a Jekyll site. Switch Pages to the
# custom Actions workflow rather than publishing the unbuilt source branch.
repo="${1:-ArkFlame/FlameMC-Website}"
if [[ ! "$repo" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]; then
  echo "Expected OWNER/REPO, got: $repo" >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo 'Install GitHub CLI (gh) first, then run gh auth login.' >&2
  exit 2
fi

if ! gh auth status >/dev/null 2>&1; then
  echo 'Authenticate first: gh auth login' >&2
  exit 2
fi

printf 'Configuring Pages for %s ...\n' "$repo"
gh api --method PUT "repos/$repo/pages" -f build_type=workflow >/dev/null

build_type="$(gh api "repos/$repo/pages" --jq '.build_type // "unknown"')"
if [[ "$build_type" != workflow ]]; then
  echo "Unexpected Pages publishing mode: $build_type" >&2
  exit 1
fi

printf 'PASS: %s uses GitHub Actions publishing.\n' "$repo"
printf 'Now push the website to main, then run the custom deploy workflow:\n'
printf '  gh workflow run deploy.yml --repo %s --ref main\n' "$repo"
