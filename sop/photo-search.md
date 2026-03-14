# SOP: Photo Search & Gallery

## Where Things Live

| Thing | Location |
|-------|----------|
| Photos | `~/Library/CloudStorage/Dropbox/Photos/YYYY/` |
| JSONL index | `~/Library/CloudStorage/Dropbox/Photos/YYYY/.photo-index.jsonl` |
| Project index | `~/Library/CloudStorage/Dropbox/.claude/memory/projects.yaml` |
| Search script | `~/src/project-photos/find-project-photos.sh` |
| Gallery outputs | `~/cowork/galleries/` |
| Camera rename service | `~/src/camera-rename/` |

> **Note:** `~/Dropbox` is a broken symlink — always use `~/Library/CloudStorage/Dropbox`

---

## Searching Photos

### By project name
```bash
~/src/project-photos/find-project-photos.sh "H2C"
```
Looks up keywords from `projects.yaml`, searches filenames + JSONL index, opens HTML gallery.

### By keyword
```bash
~/src/project-photos/find-project-photos.sh -k "nozzle,hotend"
```

### List available projects
```bash
~/src/project-photos/find-project-photos.sh
```

Galleries save to `~/cowork/galleries/` and open in your browser automatically.

---

## Building a Gallery (Cowork / Python)

Use Cowork to generate a self-contained gallery (base64 embedded, fully portable):

1. Tell Cowork: *"Build a gallery of photos from [date] between [time1] and [time2]"*
2. It uses Python + Pillow to embed thumbnails as base64 — no file path dependencies
3. Output goes to `~/cowork/galleries/[name]-gallery.html`

Key details the gallery script must follow (documented in `memory/projects/camera-rename.md`):
- Sort by datetime extracted from filename (oldest to newest)
- Apply `ImageOps.exif_transpose()` for rotation correction
- Thumbnail at 400×400 max, embed as `data:image/jpeg;base64,...`
- Size slider (120–400px, default 180px) + lightbox with arrow nav

---

## JSONL Index Health Check

```bash
# Count photos vs indexed
python3 - << 'EOF'
import json, os, glob
year = "2026"
base = f"{os.environ['HOME']}/Library/CloudStorage/Dropbox/Photos/{year}"
index = f"{base}/.photo-index.jsonl"
indexed = set(json.loads(l)['file'] for l in open(index) if l.strip())
photos = set(os.path.basename(p) for p in glob.glob(f"{base}/*.jpg") + glob.glob(f"{base}/*.jpeg"))
print(f"Photos: {len(photos)} | Indexed: {len(indexed)} | Gap: {len(photos - indexed)}")
EOF
```

### Backfill missing entries
```bash
cd ~/src/camera-rename
python3 backfill-index.py --year 2026
```

---

## Adding a New Project to projects.yaml

Edit `~/Library/CloudStorage/Dropbox/.claude/memory/projects.yaml`:

```yaml
  My New Project:
    description: "What this project is"
    keywords:
      - keyword1
      - keyword2
    date_range: "2026-02"
```

---

## Testing the Search Script

```bash
# Quick smoke test — should find photos and open a gallery
~/src/project-photos/find-project-photos.sh -k "bambu"

# Test project lookup
~/src/project-photos/find-project-photos.sh "H2C"

# Verify paths are not broken
grep "PHOTOS_DIR\|PROJECTS_FILE\|GALLERY_DIR" ~/src/project-photos/find-project-photos.sh
# Should show Library/CloudStorage/Dropbox paths (NOT ~/Dropbox)
```

---

## Camera Rename Service

Runs as a launchd service on macOS. Watches `~/Library/CloudStorage/Dropbox/Camera Uploads/` and:
1. Renames incoming photos with AI slugs (Sonnet model)
2. Writes JSONL index entries to `Photos/YYYY/.photo-index.jsonl`

Check if it's running:
```bash
launchctl list | grep rename-camera
```

Logs:
```bash
tail -f ~/Library/Logs/rename-camera-uploads.log
```
