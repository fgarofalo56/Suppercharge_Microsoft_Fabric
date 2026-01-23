---
name: speckit.taskstoissues
description: Convert tasks from tasks.md into GitHub Issues for project tracking and team collaboration.
mode: agent
tools:
  - filesystem
  - terminal
  - github
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Convert the task breakdown from tasks.md into GitHub Issues, enabling project tracking and team collaboration using GitHub's native issue tracking.

## Execution Flow

### 1. Prerequisites Check

Run prerequisite check:

```powershell
# PowerShell
.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks

# Bash
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
```

Parse JSON for `FEATURE_DIR`, `TASKS`.

### 2. Load Tasks

Read `tasks.md` and extract:
- Feature name
- All task items with their IDs, descriptions, and story assignments
- Phase groupings
- Parallel markers [P]

### 3. Determine Issue Structure

For each user story phase, create:
- **Parent Issue**: The user story itself (epic-like)
- **Child Issues**: Individual tasks linked to the parent

### 4. Issue Template

For each task, create an issue with:

```markdown
## Task: [Task Description]

**Task ID**: [T001]
**User Story**: [US1 - Story Title]
**Phase**: [Phase Name]
**Parallel**: [Yes/No]

### Description
[Extracted from task description]

### File Path
`[path/to/file.ext]`

### Acceptance Criteria
- [ ] Implementation complete
- [ ] Tests passing (if applicable)
- [ ] Code reviewed

### Dependencies
- Depends on: [List any blocking tasks]
- Blocks: [List tasks this blocks]

### Labels
- `speckit`
- `[phase-name]`
- `[user-story-label]`
```

### 5. Create Issues

Using GitHub CLI (`gh`):

```bash
# Create user story issue (parent)
gh issue create \
  --title "[US1] User Story Title" \
  --body "..." \
  --label "speckit,user-story,P1"

# Create task issues
gh issue create \
  --title "[T001] Task description" \
  --body "..." \
  --label "speckit,task,US1"
```

### 6. Link Issues

After creating issues:
- Reference parent issue in child issues
- Add task references to parent issue body
- Create issue links if supported

### 7. Create Project Board (Optional)

If user requests, create a GitHub Project board:

```bash
# Create project
gh project create --title "[Feature Name] Implementation"

# Add issues to project
gh project item-add [project-number] --url [issue-url]
```

### 8. Report Summary

```markdown
## Issues Created

### User Stories
| Story | Issue # | Title | Labels |
|-------|---------|-------|--------|
| US1 | #123 | [Title] | P1, user-story |
| US2 | #124 | [Title] | P2, user-story |

### Tasks
| Task | Issue # | Story | Title |
|------|---------|-------|-------|
| T001 | #125 | US1 | [Title] |
| T002 | #126 | US1 | [Title] |

### Summary
- **Total Issues Created**: X
- **User Story Issues**: X
- **Task Issues**: X
- **Project Board**: [Link if created]

### Next Steps
1. Assign issues to team members
2. Set milestones
3. Begin Phase 1 implementation
```

## Configuration Options

From user input (`$ARGUMENTS`):

- `--dry-run`: Show what would be created without creating
- `--milestone [name]`: Assign all issues to a milestone
- `--assignee [username]`: Assign all issues to a user
- `--project`: Create a project board
- `--labels [list]`: Additional labels to add

## GitHub CLI Requirements

This command requires the GitHub CLI (`gh`) to be installed and authenticated:

```bash
# Check installation
gh --version

# Authenticate if needed
gh auth login
```

## Notes

- Issues are created in the current repository
- Task dependencies are noted in issue bodies (GitHub doesn't have native dependencies)
- Parallel tasks [P] are noted but not enforced by GitHub
- User story issues can be used as "epics" for grouping
