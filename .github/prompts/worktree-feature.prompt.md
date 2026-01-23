---
mode: agent
description: Start a new feature in an isolated Git worktree
tools: []
---

# Worktree Feature

Start a new feature branch in an isolated Git worktree for parallel development.

## Context

You are helping the user create a new feature branch in a separate worktree, allowing them to work on multiple features simultaneously without stashing or losing context.

## Instructions

1. **Gather Info** (ask if not provided):
   - Feature name/branch name
   - Base branch (default: main)
   - Any setup commands needed (npm install, etc.)?

2. **Generate Commands**:
   Provide the exact commands to create and set up the worktree.

3. **Explain the workflow**:
   How to switch between worktrees and clean up when done.

## Example

**User Input**: "Start a feature for user authentication"

**Response**:

### Creating Feature Worktree: user-auth

**Step 1: Create the worktree**
```bash
# From your main repository directory
git fetch origin main
git worktree add -b feature/user-auth ../[repo-name]-feature-user-auth origin/main
```

**Step 2: Set up the worktree**
```bash
cd ../[repo-name]-feature-user-auth

# Install dependencies (if needed)
npm install  # or pip install -r requirements.txt, etc.

# Open in VS Code
code .
```

**Step 3: Start developing**
Your main repo is untouched. Work freely on this feature:
```bash
# Make changes, commit as usual
git add .
git commit -m "feat(auth): add login component"
git push -u origin feature/user-auth
```

**Switching Between Features**
```bash
# Go to main work
cd ../[repo-name]

# Go to this feature
cd ../[repo-name]-feature-user-auth
```

**When Done (after PR merged)**
```bash
cd ../[repo-name]
git worktree remove ../[repo-name]-feature-user-auth
git branch -d feature/user-auth
```

### Tips
- Each worktree has its own `node_modules` - run install commands
- Commits and pushes work normally from any worktree
- Use `git worktree list` to see all your worktrees

Would you like me to adjust the branch name or base branch?

## User Request

{{{ input }}}
