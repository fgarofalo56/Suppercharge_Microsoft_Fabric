---
mode: agent
description: Review a pull request in an isolated Git worktree
tools: []
---

# Worktree Review

Set up an isolated worktree to review a pull request without disrupting your current work.

## Context

You are helping the user review a PR in a clean, isolated environment. This keeps their current work untouched while they can run tests, check functionality, and provide thorough review.

## Instructions

1. **Get PR Info** (ask if not provided):
   - PR number
   - Repository (if not current)

2. **Generate Commands**:
   Provide commands to fetch, create worktree, and set up for review.

3. **Review Checklist**:
   Suggest what to check in the review.

4. **Cleanup Commands**:
   Show how to remove the worktree after review.

## Example

**User Input**: "Review PR #123"

**Response**:

### Setting Up PR Review Worktree

**Step 1: Fetch the PR**
```bash
git fetch origin pull/123/head:pr-123
```

**Step 2: Create isolated review worktree**
```bash
git worktree add ../[repo-name]-pr-123 pr-123
cd ../[repo-name]-pr-123
```

**Step 3: Set up for testing**
```bash
# Install dependencies
npm install  # or relevant setup command

# Run tests
npm test

# Start the app (if applicable)
npm start
```

### Review Checklist

- [ ] **Code Quality**: Is the code clean and well-structured?
- [ ] **Tests**: Are there adequate tests? Do they pass?
- [ ] **Functionality**: Does the feature work as described?
- [ ] **Edge Cases**: Are edge cases handled?
- [ ] **Performance**: Any performance concerns?
- [ ] **Security**: Any security issues?
- [ ] **Documentation**: Is documentation updated?

### Providing Feedback

```bash
# If you need to suggest changes, you can create a branch
git checkout -b pr-123-suggestions
# Make changes, commit, and reference in review comments
```

### After Review - Cleanup

```bash
# Return to your work
cd ../[repo-name]

# Remove the review worktree
git worktree remove ../[repo-name]-pr-123

# Delete the local branch
git branch -d pr-123
```

### Quick Reference

| Action | Command |
|--------|---------|
| Go to review | `cd ../[repo-name]-pr-123` |
| Return to work | `cd ../[repo-name]` |
| List worktrees | `git worktree list` |

Would you like me to include any specific testing commands for this project?

## User Request

{{{ input }}}
