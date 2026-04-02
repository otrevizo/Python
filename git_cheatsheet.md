# Git Cheatsheet

A practical reference for everyday git workflows using the Terminal.
For the full git command guide see: https://github.com/git-guides

> **Note:** GitHub Desktop is a graphical alternative to Terminal git.
> This cheatsheet focuses on Terminal commands, which work on any machine
> and give you full control. All commands assume macOS / Linux (zsh or bash).

---

## Setup — First Time Only

```bash
# Set your identity (used in every commit)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Store credentials in macOS Keychain (enter PAT once, never again)
git config --global credential.helper osxkeychain

# Verify your config
git config --list
```

> **GitHub authentication:** GitHub no longer accepts your account password
> for git operations. Use a **Personal Access Token (PAT)** instead.
> Generate one at: https://github.com/settings/tokens
> Select scope: `repo`. Save it in a password manager (e.g. KeePass).

---

## Starting Out — Clone a Repo

Your local repos live in `~/GitHub/` — one subfolder per repo.

```bash
# Navigate to your GitHub folder
cd ~/GitHub

# Clone a repo (creates a subfolder automatically)
git clone https://github.com/username/repo-name.git

# Enter the repo
cd repo-name
```

---

## Daily Workflow — The Core Three

This is the sequence you will use every day:

```bash
# 1. Stage your changes
git add <filename>           # Stage a specific file
git add .                    # Stage ALL changed files in current folder

# 2. Commit with a clear message
git commit -m "Brief description of what changed and why"

# 3. Push to GitHub
git push
```

### Good commit messages
```bash
# Good — clear and specific
git commit -m "Add logistic regression vignette with classification report"
git commit -m "Fix freq='M' to freq='ME' — pandas 2.2 breaking change"
git commit -m "Update README — add machine_learning folder description"

# Avoid — too vague
git commit -m "update"
git commit -m "fix"
git commit -m "changes"
```

---

## Check What's Happening

```bash
# What files have changed? What is staged?
git status

# Recent commit history — one line per commit
git log --oneline

# Full commit history with dates and authors
git log

# Show changes in a specific file (not yet staged)
git diff <filename>

# Show what is staged and ready to commit
git diff --staged

# Show which remote repo you are connected to
git remote -v
```

---

## Pulling — Get Latest Changes from GitHub

Always pull before you start working, especially in shared repos:

```bash
# Pull latest changes from GitHub
git pull

# Pull from a specific branch
git pull origin main
```

---

## Branching — Work Safely on New Features

Branches let you work on something new without affecting `main`.

```bash
# List all local branches (* marks current branch)
git branch

# Create a new branch
git branch feature-my-new-analysis

# Switch to that branch
git checkout feature-my-new-analysis

# Shortcut — create and switch in one step
git checkout -b feature-my-new-analysis

# Push a new branch to GitHub for the first time
git push --set-upstream origin feature-my-new-analysis
```

### Merge a branch back into main

```bash
# Switch back to main
git checkout main

# Pull latest main first (good habit)
git pull

# Merge your feature branch into main
git merge feature-my-new-analysis

# Push the merged main to GitHub
git push

# Delete the branch locally after merging (optional, keeps things clean)
git branch -d feature-my-new-analysis
```

---

## .gitignore — Tell Git What to Ignore

A `.gitignore` file in your repo root tells git to never track certain files.
Common entries for Python / JupyterLab projects:

```
.ipynb_checkpoints/
.virtual_documents/
.DS_Store
__pycache__/
*.pyc
myenv/
.env
```

```bash
# After editing .gitignore, remove already-tracked files from git
git rm -r --cached <file-or-folder>
git add .gitignore
git commit -m "Update .gitignore"
git push
```

---

## Typical Session — Start to Finish

```bash
# 1. Open Terminal and navigate to your repo
cd ~/GitHub/Python

# 2. Activate your Python environment
source ~/.venvs/myenv/bin/activate

# 3. Pull latest changes
git pull

# 4. Do your work in JupyterLab or editor
jupyter lab

# 5. When done — stage, commit, push
git status                              # Review what changed
git add machine_learning/my_notebook.ipynb
git commit -m "Add KNN vignette with confusion matrix"
git push
```

---

## Quick Reference Card

| Command | What it does |
|---|---|
| `git clone <url>` | Download a repo to your machine |
| `git status` | Show changed / staged files |
| `git add <file>` | Stage a file for commit |
| `git add .` | Stage all changed files |
| `git commit -m "msg"` | Save staged changes with a message |
| `git push` | Upload commits to GitHub |
| `git pull` | Download latest changes from GitHub |
| `git log --oneline` | Show recent commit history |
| `git diff <file>` | Show unstaged changes in a file |
| `git branch` | List branches |
| `git checkout -b <name>` | Create and switch to a new branch |
| `git merge <branch>` | Merge a branch into current branch |
| `git branch -d <name>` | Delete a branch after merging |
| `git remote -v` | Show connected remote repo |
| `git config --list` | Show your git configuration |

---

## GitHub Desktop — Graphical Alternative

If you prefer a visual interface, **GitHub Desktop** handles clone, commit,
push, pull, and branching through a point-and-click UI. It shares the same
underlying git — switching between Terminal and GitHub Desktop on the same
repo is safe.

Download: https://desktop.github.com

> **Recommendation:** Learn Terminal git first — it works everywhere and gives
> you full control. Use GitHub Desktop for quick commits when convenient.

---

*Reference: https://github.com/git-guides*
