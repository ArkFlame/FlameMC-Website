#!/usr/bin/env bash
set -euo pipefail
repo="${1:-ArkFlame/FlameMC-Website}"
if ! command -v gh >/dev/null; then echo 'Install GitHub CLI (gh) first.' >&2; exit 2; fi
gh auth status >/dev/null || { echo 'Run gh auth login first' >&2; exit 2; }
echo '--- GitHub Pages ---'
gh api "repos/$repo/pages" --jq '"Mode: \(.build_type) | CNAME: \(.cname // "(none)") | State: \(.status)"'
echo '--- Latest custom workflow ---'
gh run list --repo "$repo" --workflow deploy.yml --limit 3
echo '--- Live website ---'
body="$(curl --fail --silent --show-error --location --max-time 20 --compressed 'https://flamemc.arkflame.com/')"
if [[ "$body" == *'Scale your world.'* && "$body" == *'Keep your plugins.'* && "$body" == *'flamemc-extreme-async-performance.133143'* ]]; then
  echo 'PASS: live domain is serving the FlameMC product homepage.'
else
  echo 'FAIL: live domain is not serving the expected FlameMC homepage.' >&2
  echo 'Check Pages Source = GitHub Actions, the latest deploy.yml run, and the configured custom domain.' >&2
  exit 1
fi
