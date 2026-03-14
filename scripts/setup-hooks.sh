#!/bin/bash
# Install git hooks for ~/cowork
# Run this once after cloning on a new machine

HOOKS_DIR="$(git -C "$(dirname "$0")/.." rev-parse --git-dir)/hooks"
SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"

install_hook() {
  local name="$1"
  local src="$SCRIPTS_DIR/hooks/$name"
  local dst="$HOOKS_DIR/$name"

  if [ ! -f "$src" ]; then
    echo "ERROR: Hook source not found: $src"
    exit 1
  fi

  cp "$src" "$dst"
  chmod +x "$dst"
  echo "Installed: $name"
}

install_hook "pre-commit"
echo "Done."
