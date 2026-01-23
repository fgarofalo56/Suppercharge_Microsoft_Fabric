---
description: Create or manage Archon tasks for the current project
---

# Manage Tasks

Create, update, or manage Archon tasks for the current project.

## Task Operations

### List Tasks

```
# All project tasks
find_tasks(filter_by="project", filter_value="[PROJECT_ID]")

# By status
find_tasks(filter_by="status", filter_value="todo")
find_tasks(filter_by="status", filter_value="doing")
find_tasks(filter_by="status", filter_value="review")

# Search
find_tasks(query="authentication")
```

### Create Task

```
manage_task("create",
  project_id="[PROJECT_ID]",
  title="[Task title]",
  description="[Detailed description]",
  task_order=80,  # Priority 0-100, higher = more important
  feature="[Feature name]"
)
```

### Update Task

```
# Change status
manage_task("update", task_id="...", status="doing")
manage_task("update", task_id="...", status="review")
manage_task("update", task_id="...", status="done")

# Add notes
manage_task("update", task_id="...", description="Updated notes...")
```

### Delete Task

```
manage_task("delete", task_id="...")
```

## Task Guidelines

| Aspect          | Guideline                       |
| --------------- | ------------------------------- |
| **Size**        | 30 min - 4 hours of work        |
| **Title**       | Action-oriented (verb + object) |
| **Description** | Include acceptance criteria     |
| **Priority**    | 0-100 (higher = more important) |
| **Status Flow** | todo → doing → review → done    |

## Task Templates

**Feature Task:**

```
Title: Implement [feature name]
Description:
- [ ] Design the approach
- [ ] Implement core logic
- [ ] Add error handling
- [ ] Write tests
- [ ] Update documentation
```

**Bug Fix Task:**

```
Title: Fix [bug description]
Description:
- [ ] Reproduce the issue
- [ ] Identify root cause
- [ ] Implement fix
- [ ] Add regression test
- [ ] Verify fix
```

**Refactor Task:**

```
Title: Refactor [component]
Description:
- [ ] Analyze current implementation
- [ ] Plan refactoring approach
- [ ] Implement changes
- [ ] Ensure tests pass
- [ ] Update documentation
```

## Arguments

{input}

- `list`: Show all tasks
- `todo`: Show todo tasks
- `doing`: Show in-progress tasks
- `create <title>`: Create new task
- `done <task-id>`: Mark task complete
- `<task-id>`: Show specific task details
