#!/usr/bin/env bash
set -euo pipefail

repo="${1:-ArkFlame/FlameMC-Website}"
domain='flamemc.arkflame.com'
if [[ ! "$repo" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]; then
  printf 'Invalid repository; expected OWNER/REPO, got %q\n' "$repo" >&2
  exit 2
fi
if ! command -v gh >/dev/null 2>&1; then
  echo 'GitHub CLI required: https://cli.github.com/. Install gh and run gh auth login.' >&2
  exit 2
fi
if ! gh auth status >/dev/null 2>&1; then
  echo 'GitHub CLI is not authenticated. Run: gh auth login' >&2
  exit 2
fi

# This API requires repository Pages/Admin permissions; GITHUB_TOKEN in CI cannot switch the setting.
if gh api "repos/$repo/pages" --jq '.build_type' >/dev/null 2>&1; then
  gh api --method PUT "repos/$repo/pages" -f build_type=workflow >/dev/null
else
  echo 'No readable GitHub Pages configuration found. Checking repository access...' >&2
  gh api "repos/$repo" --jq .full_name >/dev/null
  # If Pages was not initialized, this creates it in workflow mode.
  gh api --method POST "repos/$repo/pages" -f build_type=workflow >/dev/null
fi

mode="$(gh api "repos/$repo/pages" --jq '.build_type')"
if [[ "$mode" != workflow ]]; then
  printf 'FAIL: Pages mode is %s, expected workflow\n' "$mode" >&2
  exit 1
fi
printf 'PASS: %s now publishes with GitHub Actions (not Jekyll).\n' "$repo"

cname="$(gh api "repos/$repo/pages" --jq '.cname // ""')"
if [[ "$cname" != "$domain" ]]; then
  printf 'Configuring custom domain %s ...\n' "$domain"
  gh api --method PUT "repos/$repo/pages" -f "cname=$domain" >/dev/null
  actual="$(gh api "repos/$repo/pages" --jq '.cname // ""')"
  [[ "$actual" == "$domain" ]] || { printf 'FAIL: Pages custom domain is %s\n' "$actual" >&2; exit 1; }
fi
printf 'PASS: GitHub Pages custom domain = %s\n' "$domain"

# Fail before dispatching if the website source and workflow were never pushed to main.
if ! gh api "repos/$repo/contents/.github/workflows/deploy.yml?ref=main" --jq '.path' >/dev/null 2>&1; then
  echo 'BLOCKED: .github/workflows/deploy.yml is not on remote main.' >&2
  echo 'Extract the full website archive into the repository root and commit/push the files to main, then rerun this script.' >&2
  exit 1
fi

printf 'Triggering the Astro deployment from main ...\n'
gh workflow run deploy.yml --repo "$repo" --ref main
printf 'PASS: requested GitHub Actions deployment.\n'
printf 'Check: https://github.com/%s/actions/workflows/deploy.yml\n' "$repo"
printf 'Then verify: https://%s/\n' "$domain"
