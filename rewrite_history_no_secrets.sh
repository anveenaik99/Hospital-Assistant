#!/bin/sh
# Rewrites git history to a single commit without the exposed secret.
# Run from repo root: sh rewrite_history_no_secrets.sh
# Then: git push -f origin main

set -e
echo "Creating fresh history (one commit, no secrets)..."

# Current branch name (usually main or master)
BRANCH=$(git branch --show-current)

# Create orphan branch (no history)
git checkout --orphan temp_clean

# Unstage so we only commit current working tree (not old index)
git reset

# Stage current files (respects .gitignore; .env stays untracked)
git add -A

# One clean commit
git commit -m "Initial commit: Pediatric Care System - AI-Powered Healthcare Assistant"

# Replace old branch: delete and rename
git branch -D "$BRANCH"
git branch -m "$BRANCH"

echo "Done. History is now a single commit. Run: git push -f origin $BRANCH"
