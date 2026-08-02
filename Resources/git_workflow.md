# Git Workflow Guide

## Daily Commit Pattern (7 contributions)

```bash
# Commit 1 — Python files
git add Day-XX/Python/
git commit -m "Day-XX: Python — description"

# Commit 2 — DSA files
git add Day-XX/DSA/
git commit -m "Day-XX: DSA — problems solved"

# Commit 3 — AI core files
git add Day-XX/AI/
git commit -m "Day-XX: AI — project description"

# Commit 4 — Notes
git add Day-XX/Notes/
git commit -m "Day-XX: Notes — topics covered"

# Commit 5 — README
git add Day-XX/README.md
git commit -m "Day-XX: README added"

# Commit 6 — Resources
git add Day-XX/Resources.md
git commit -m "Day-XX: Resources added"

# Commit 7 — Main README update
git add README.md
git commit -m "docs: Mark Day-XX as completed"

git push
```

## Useful Git Commands

```bash
git status                    # see changed files
git log --oneline -10         # last 10 commits
git diff                      # see unstaged changes
git add -p                    # stage changes interactively
git commit --amend            # edit last commit message
git stash                     # temporarily save changes
git stash pop                 # restore stashed changes
```

## Commit Message Format

```
type: short description

Types:
  feat     → new feature or file
  fix      → bug fix
  docs     → documentation update
  chore    → config, gitignore, etc.
  refactor → code improvement
  journal  → learning journal update
```

## Branch Strategy

```bash
git checkout -b feature/day-08    # create new branch
git checkout main                 # switch to main
git merge feature/day-08          # merge branch
git branch -d feature/day-08      # delete branch
```
