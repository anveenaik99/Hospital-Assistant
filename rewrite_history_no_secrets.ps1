# Rewrites git history to a single commit without the exposed secret.
# Run from repo root in PowerShell: .\rewrite_history_no_secrets.ps1
# Then: git push -f origin main

$ErrorActionPreference = "Stop"
Write-Host "Creating fresh history (one commit, no secrets)..."

$branch = git branch --show-current
if (-not $branch) { $branch = "main" }

# Create orphan branch (no history)
git checkout --orphan temp_clean

# Unstage so we only commit current working tree (not old index)
git reset

# Stage current files (respects .gitignore; .env stays untracked)
git add -A

# One clean commit
git commit -m "Initial commit: Pediatric Care System - AI-Powered Healthcare Assistant"

# Replace old branch: delete and rename
git branch -D $branch
git branch -m $branch

Write-Host "Done. History is now a single commit. Run: git push -f origin $branch"
