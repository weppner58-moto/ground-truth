#!/usr/bin/env bash
# One-time setup for the Ground Truth registration gate. Run on the Mac from the repo:
#   cd ~/ground-truth && bash tools/setup-gate.sh
# It signs you in to Cloudflare in the browser, creates the KV namespace that keeps the registrations,
# writes its id into wrangler.toml, sets the two secrets, commits and pushes. Re-running is safe.
set -euo pipefail
cd "$(dirname "$0")/.."
npx --yes wrangler whoami >/dev/null 2>&1 || npx --yes wrangler login
if grep -q '^# \[\[kv_namespaces\]\]' wrangler.toml; then
  echo "Creating the KV namespace groundtruth-readers"
  out=$(npx --yes wrangler kv namespace create GT_LIST 2>&1) || { echo "$out"; exit 1; }
  id=$(echo "$out" | grep -oE 'id = "[0-9a-f]+"' | head -1 | grep -oE '[0-9a-f]{20,}')
  [ -n "$id" ] || { echo "Could not read the namespace id from:"; echo "$out"; exit 1; }
  python3 - "$id" <<'PY'
import sys, re
p = "wrangler.toml"; s = open(p).read()
s = s.replace('# [[kv_namespaces]]\n# binding = "GT_LIST"\n# id = "PASTE_THE_NAMESPACE_ID_HERE"',
              '[[kv_namespaces]]\nbinding = "GT_LIST"\nid = "%s"' % sys.argv[1])
open(p, "w").write(s)
PY
  echo "wrangler.toml now binds GT_LIST to $id"
fi
gate=$(openssl rand -hex 32); admin=$(openssl rand -hex 24)
printf '%s' "$gate"  | npx --yes wrangler secret put GATE_SECRET  >/dev/null
printf '%s' "$admin" | npx --yes wrangler secret put ADMIN_TOKEN >/dev/null
echo
echo "Secrets set. Your registrations list, as CSV, is at:"
echo "  https://contactpatchadvisory.com/groundtruth/registrations?token=$admin"
echo "Keep that line somewhere private; it is the only place the token is shown."
echo
find .git -name '*.lock' -delete 2>/dev/null || true
git add wrangler.toml && git commit -qm "Gate: KV namespace for registrations" || true
git push origin HEAD:main
echo "Pushed. Cloudflare redeploys in about a minute; the gate is then live with the list stored."
