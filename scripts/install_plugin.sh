#!/usr/bin/env bash
# Installs/updates the Rosetta plugin for Xournal++ (copies to the user's plugin folder).
# Run from anywhere; re-run after every plugin change (Xournal++ loads it at boot).

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$REPO/xournalpp-plugin/rosetta"
DST="${XDG_CONFIG_HOME:-$HOME/.config}/xournalpp/plugins/rosetta"

if [[ ! -d "$SRC" ]]; then
  echo "ERROR: plugin not found at $SRC" >&2
  exit 1
fi

mkdir -p "$DST"
cp -r "$SRC"/* "$DST"

echo "Plugin installed at $DST"
echo "Restart Xournal++ and use Plugin > 'Rosetta: reconhecer contas' (Ctrl+M)."
