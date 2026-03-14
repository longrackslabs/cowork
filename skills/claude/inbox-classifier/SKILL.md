---
name: inbox
description: Use when user says "check my inbox", "train the classifier", "reset", or wants to review/update email classification rules
---

# Inbox Classifier Training

## Overview
Train the Gmail auto-labeling service by reviewing inbox emails, updating rules, and deploying changes. Rules live in GitHub (`longrackslabs/inbox-rules`), service runs on Linux (192.168.254.99).

Reference SOP: `~/cowork/sop/email-classifier.md`

## Quick Reference

| Resource | Location |
|----------|----------|
| Rules repo | `longrackslabs/inbox-rules` (file: `rules.md`) |
| Local clone | `~/src/inbox-rules/` |
| Service host | `192.168.254.99` (user: gpeden) |
| Service log | `~/.inbox-classifier/service.log` (on Linux) |
| Classifications log | `~/.inbox-classifier/classifications.jsonl` (on Linux) |
| Classifier code | `~/src/inbox-classifier/` |

## Workflow

### Check Inbox
```python
from inbox_classifier.gmail_auth import get_gmail_service
from inbox_classifier.email_fetcher import fetch_unread_emails, get_email_details
```
- Use Gmail API directly (NOT MCP — Claude Code has full API access)
- Find emails in INBOX without classifier labels (0_*, 1_*, 2_*, 3_*, 4_*, 7_*, 9_*)
- Show subject, sender, and current/suggested classification

### Update Rules
1. Edit `~/src/inbox-rules/rules.md`
2. `git add && git commit && git push` from `~/src/inbox-rules/`
3. Service picks up changes within 60 seconds

### Reset Emails
When user says "reset" — for specific emails or all:
- Remove classifier labels (0_Important, 1_Routine, 2_Receipts, 3_Optional, 4_Ads, 7_Test, 9_Fluff)
- Add INBOX + UNREAD labels back
- Service reclassifies on next cycle

### Check Service
```bash
ssh gpeden@192.168.254.99 'tail -20 ~/.inbox-classifier/service.log'
```

## Rules Format
Category headers define labels. Bullets are AI classification hints:
```
0_Important emails include:
- Security: password resets, security alerts

Skip classification for:
- from:ebay@ebay.com
```
- Number prefixes control sort order
- Skip rules are checked in code BEFORE AI classification
- Skip rules use simple `from:` or `subject:` per line (not combined)

## Common Mistakes
- Skip rules are one field per line — `from:x subject:y` on one line does NOT work
- "Uncertain" classifications return None (left in inbox), not defaulted to Important
- Service fetches rules from GitHub, not local filesystem
