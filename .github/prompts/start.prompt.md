---
description: Execute the mandatory startup checklist before beginning work
---

# Session Start Protocol

Execute the complete startup checklist before we begin any work.

## Startup Steps

### 1. Load Project Context

- Check for `.github/copilot-instructions.md` and read it
- Check for any project-specific configuration files

### 2. Load Archon Project Context

Query Archon for the current project state:

```
find_projects(query="[current-codebase-name]")
find_documents(project_id="[PROJECT_ID]", query="Session Memory")
find_tasks(filter_by="project", filter_value="[PROJECT_ID]")
find_tasks(filter_by="status", filter_value="doing")
```

### 3. Review Git Status

Check what has changed:

```bash
git status
git log --oneline -5
git branch --show-current
```

### 4. Check for Blockers

- Review any tasks marked as blocked
- Check for failing tests or builds
- Note any pending PRs needing attention

### 5. Project Status Briefing

Provide a structured briefing:

```markdown
## 📊 Project Status Briefing

### Current State

- **Branch**: [current branch]
- **Last Commit**: [commit message]
- **Uncommitted Changes**: [yes/no - list if any]

### Archon Tasks

- **In Progress**: [list]
- **Blocked**: [list]
- **Ready (Todo)**: [top 3]

### Session Memory

- **Last Session Focus**: [from session doc]
- **Decisions Made**: [list]
- **Blockers**: [list]

### 🎯 Recommended Next Steps

1. [Option A - Continue previous work]
2. [Option B - New priority items]
3. [Option C - Maintenance tasks]
```

Do not skip any steps. Actually execute the commands, don't just describe them.

{input}
