---
description: View git differences between commits, branches, or working directory
---

# Git Diff

View differences between commits, branches, or working directory.

## Views

### Unstaged Changes (Default)

```bash
git diff
```

### Staged Changes

```bash
git diff --staged
```

### All Changes

```bash
git diff HEAD
```

### Between Branches

```bash
# What's in feature that's not in main
git diff main..feature

# What changed between branches
git diff main...feature
```

### Between Commits

```bash
git diff <commit1> <commit2>
git diff HEAD~5 HEAD
```

### Specific File

```bash
git diff -- <file-path>
git diff --staged -- <file-path>
```

## Output Formats

| Command                      | Output                    |
| ---------------------------- | ------------------------- |
| `git diff --stat`            | Files changed, lines +/-  |
| `git diff --name-only`       | Just file paths           |
| `git diff --name-status`     | Files with A/M/D/R status |
| `git diff --compact-summary` | One line per file         |
| `git diff --word-diff`       | Word-level changes        |

## Options

| Flag            | Purpose                          |
| --------------- | -------------------------------- |
| `-w`            | Ignore all whitespace            |
| `-b`            | Ignore whitespace changes        |
| `-U5`           | Show 5 lines context (default 3) |
| `--color-words` | Color at word level              |

## Reading Diff Output

- `-` lines (red): Removed
- `+` lines (green): Added
- `@@` lines: Location (hunk header)
- No prefix: Context lines

## Summary

After showing diff, summarize:

- X files changed
- Y insertions (+)
- Z deletions (-)

## Arguments

{input}

- No args: Show unstaged changes
- `staged`: Staged changes only
- `all`: Both staged and unstaged
- `stat`: Statistics only
- `<branch>`: Diff against branch
- `<file>`: Diff specific file
