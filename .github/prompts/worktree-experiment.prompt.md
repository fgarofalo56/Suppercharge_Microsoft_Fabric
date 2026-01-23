---
mode: agent
description: Create a locked Git worktree for long-running experiments
tools: []
---

# Worktree Experiment

Create a locked worktree for experimental work that may span days or weeks.

## Context

You are helping the user create a protected experimental worktree. These are for trying out major changes, architectural experiments, or proof-of-concepts that shouldn't be accidentally deleted.

## Instructions

1. **Understand the Experiment** (ask if not provided):
   - What are you experimenting with?
   - How long will this experiment run?
   - Should it be based on main or another branch?

2. **Create Locked Worktree**:
   Provide commands to create and lock the worktree.

3. **Explain Protection**:
   What locking means and how to manage the experiment.

4. **Eventual Cleanup**:
   How to conclude the experiment (merge or discard).

## Example

**User Input**: "I want to experiment with a new database architecture"

**Response**:

### Creating Experiment Worktree: Database Architecture

**Step 1: Create the experimental worktree**
```bash
# Create worktree with new experiment branch
git worktree add -b experiment/new-db-architecture \
  ../[repo-name]-experiment-db origin/main
```

**Step 2: Lock the worktree (prevents accidental deletion)**
```bash
git worktree lock --reason "Database architecture experiment - in progress" \
  ../[repo-name]-experiment-db
```

**Step 3: Set up the experiment**
```bash
cd ../[repo-name]-experiment-db

# Install dependencies
npm install

# Open in VS Code
code .
```

### Working on the Experiment

```bash
# Switch to experiment
cd ../[repo-name]-experiment-db

# Regular commits
git add .
git commit -m "experiment: try new connection pooling"

# Push to remote (for backup)
git push -u origin experiment/new-db-architecture

# Return to main work
cd ../[repo-name]
```

### Checking Worktree Status

```bash
# See all worktrees and lock status
git worktree list --porcelain

# See just the list
git worktree list
```

### Concluding the Experiment

**If successful - merge the changes:**
```bash
# In main repo
cd ../[repo-name]

# Unlock and create PR
git worktree unlock ../[repo-name]-experiment-db

# Push and create PR via GitHub
git push origin experiment/new-db-architecture
gh pr create --title "feat: New database architecture"

# After merge, cleanup
git worktree remove ../[repo-name]-experiment-db
git branch -d experiment/new-db-architecture
```

**If abandoned - discard the changes:**
```bash
cd ../[repo-name]

# Unlock first
git worktree unlock ../[repo-name]-experiment-db

# Force remove (discards uncommitted changes)
git worktree remove --force ../[repo-name]-experiment-db

# Delete the branch
git branch -D experiment/new-db-architecture
```

### Why Lock Experiments?

| Protection | Benefit |
|------------|---------|
| Prevents `git worktree remove` | Can't accidentally delete days of work |
| Survives `git worktree prune` | Won't be cleaned up as "stale" |
| Clear reason message | Remember why it exists |

Would you like me to suggest a different branch naming convention or base branch?

## User Request

{{{ input }}}
