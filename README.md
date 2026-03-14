# cowork

Agent-agnostic SOPs and skills for George's AI assistant setup. Works across machines and AI agents (Claude Code, Gemini CLI, etc.).

## Structure

```
cowork/
  sop/              ← Agent-agnostic SOPs (plain markdown, the real logic)
  skills/
    claude/         ← Claude Code skill wrappers (SKILL.md)
    gemini/         ← Gemini CLI skill wrappers (SKILL.md)
```

Other repos cloned here (gitignored — managed separately):
- `george-os/` — personal operating system / leadership framework
- `career/` — career stuff
- `kicad-happy/` — KiCad electronics skills

Anything cloned inside `~/cowork/` that isn't part of this repo should be added to `.gitignore`.

## How It Works

SOPs contain all the logic. Skills are thin wrappers that tell an agent "read this SOP and follow it exactly." When you update a SOP, all agents pick up the change automatically.

Each agent has its own skill format, but they all point to the same SOP files.

## Setup on a New Machine

### 1. Clone cowork

```bash
git clone git@github.com:longrackslabs/cowork.git ~/cowork
```

### 2. Clone other repos

```bash
git clone git@github.com:longrackslabs/george-os.git ~/cowork/george-os
git clone git@github.com:longrackslabs/career.git ~/cowork/career
```

### 3. Claude Code

Symlink each skill individually (don't replace the whole `~/.claude/skills/` directory — other skills like superpowers live there too):

```bash
mkdir -p ~/.claude/skills
ln -s ~/cowork/skills/claude/inventory ~/.claude/skills/inventory
ln -s ~/cowork/skills/claude/lri ~/.claude/skills/lri
ln -s ~/cowork/skills/claude/bbp ~/.claude/skills/bbp
ln -s ~/cowork/skills/claude/restock ~/.claude/skills/restock
```

### 4. Gemini CLI

Install Gemini CLI (requires Node 20+):

```bash
# Install nvm if needed
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
source ~/.zshrc
nvm install 20 && nvm alias default 20

# Install Gemini CLI
npm install -g @google/gemini-cli
```

Add API key to `~/.zshrc`:

```bash
export GEMINI_API_KEY="your-key-here"
```

Link skills:

```bash
gemini skills link ~/cowork/skills/gemini/inventory
gemini skills link ~/cowork/skills/gemini/lri
gemini skills link ~/cowork/skills/gemini/bbp
gemini skills link ~/cowork/skills/gemini/restock
```

Configure MCPs in `~/.gemini/settings.json` — see existing Linux/Mac config for credentials.

### 5. KiCad skills

KiCad skills are managed by the `kicad-happy` repo, not cowork. Clone into `~/cowork/kicad-happy` (already gitignored) and symlink individually:

```bash
git clone git@github.com:longrackslabs/kicad-happy.git ~/cowork/kicad-happy

for skill in bom digikey jlcpcb kicad lcsc mouser pcbway; do
  ln -s ~/cowork/kicad-happy/$skill ~/.claude/skills/$skill
done
```

### 6. Git hooks (secret scanning)

A global pre-commit hook blocks commits containing API keys, tokens, and credentials. Run once per machine:

```bash
bash ~/cowork/scripts/setup-hooks.sh
```

This installs `scripts/hooks/pre-commit` to `~/.git-hooks/` and sets `core.hooksPath` globally. It covers Anthropic, OpenAI, GitHub, Google, Slack, eBay, AWS keys, PEM private keys, and generic patterns like `API_KEY=`, `PASSWORD=`, etc.

False positive? Use `git commit --no-verify` (with caution). To update the hook after a pull: re-run `setup-hooks.sh`.

## Syncing Changes

```bash
cd ~/cowork && git pull
```

To update from any machine:

```bash
# Edit a SOP or skill
git add -A && git commit -m "update X" && git push
# On other machines: git pull
```

## Skills

| Skill | Trigger | SOP |
|-------|---------|-----|
| inventory | `/inventory X,Y,Z` | `sop/longracks-inventory.md` |
| lri | `/lri X,Y,Z` | `sop/longracks-inventory.md` |
| restock | `/restock` | `sop/bambu-nozzle-restock.md` |
| bbp | `/bbp` + invoice screenshot | `sop/bambu-order.md` |
