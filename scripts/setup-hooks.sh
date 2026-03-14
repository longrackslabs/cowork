#!/bin/bash
# Install global git hooks to prevent secret leakage
# Run this once on a new machine

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
GLOBAL_HOOKS_DIR="$HOME/.git-hooks"

mkdir -p "$GLOBAL_HOOKS_DIR"

install_hook() {
  local name="$1"
  local src="$SCRIPTS_DIR/hooks/$name"
  local dst="$GLOBAL_HOOKS_DIR/$name"

  if [ ! -f "$src" ]; then
    echo "ERROR: Hook source not found: $src"
    exit 1
  fi

  cp "$src" "$dst"
  chmod +x "$dst"
  echo "Installed: $name -> $dst"
}

install_hook "pre-commit"

# Register global hooks dir with git
git config --global core.hooksPath "$GLOBAL_HOOKS_DIR"
echo "Set core.hooksPath to $GLOBAL_HOOKS_DIR"
echo "Done."
