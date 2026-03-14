# cowork

Agent-agnostic SOPs and skills for George's AI assistant setup. Works across machines and AI agents (Claude Code, Gemini CLI, etc.).

## Structure

```
cowork/
  sop/              ← Agent-agnostic SOPs (plain markdown, the real logic)
  skills/
    claude/         ← Claude Code skill wrappers (SKILL.md)
```

Other repos cloned here (gitignored — managed separately):
- `george-os/` — personal operating system / leadership framework
- `career/` — career stuff

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

Symlink skills so Claude Code picks them up:

```bash
# Back up existing skills if any
mv ~/.claude/skills ~/.claude/skills.bak

# Symlink
ln -s ~/cowork/skills/claude ~/.claude/skills
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
gemini skills link ~/cowork/skills/claude/inventory
gemini skills link ~/cowork/skills/claude/lri
gemini skills link ~/cowork/skills/claude/bbp
gemini skills link ~/cowork/skills/claude/restock
```

Configure MCPs in `~/.gemini/settings.json` — see existing Linux/Mac config for credentials.

### 5. KiCad skills (Mac only)

KiCad skills are managed by the `kicad-happy` repo, not cowork. Clone and link separately.

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
