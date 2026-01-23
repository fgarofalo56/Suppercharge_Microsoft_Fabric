# Autonomous Agent Harness - Reference Documentation

Complete technical reference for setting up and running autonomous coding agent projects.

## Architecture Overview

### Two-Agent System

The harness uses a two-agent architecture to address discrete session limitations:

```
┌─────────────────────────────────────────────────────────────┐
│                    INITIALIZER AGENT                        │
│                     (First Session)                         │
│                                                             │
│  1. Parse application specification                         │
│  2. Create Archon project & tasks                          │
│  3. Generate project scaffold                              │
│  4. Initialize development environment                     │
│  5. Create META task for handoffs                          │
│  6. Commit initial structure                               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     CODING AGENT                            │
│                 (Subsequent Sessions)                       │
│                                                             │
│  For each session:                                         │
│  1. Review progress (claude-progress.txt, git log)         │
│  2. Query Archon for current task status                   │
│  3. Run health checks on completed features                │
│  4. Select highest-priority TODO task                      │
│  5. Implement feature with tests                           │
│  6. Update Archon task status                              │
│  7. Commit changes, update progress                        │
│  8. Clean handoff for next session                         │
└─────────────────────────────────────────────────────────────┘
```

### State Management with Archon MCP

Unlike file-based or Linear-based state management, this harness uses Archon MCP for:

| Component | Purpose | Archon Tool |
|-----------|---------|-------------|
| Project Identity | Track project metadata | `find_projects()`, `manage_project()` |
| Task Registry | All features as tasks | `find_tasks()`, `manage_task()` |
| Session Handoffs | META task with notes | `manage_task("update")` |
| Progress Tracking | Task status workflow | Status: todo/doing/review/done |
| Feature Grouping | Organize related tasks | `feature` field |

### Context Preservation

Context is preserved across sessions via multiple channels:

1. **Archon Tasks**: Primary source of truth for work items
2. **claude-progress.txt**: Human-readable session summaries
3. **features.json**: Feature registry with test status
4. **Git History**: Commit messages with context
5. **META Task**: Handoff notes and blockers

---

## Configuration Schema

### .archon_project.json

```json
{
  "$schema": "https://example.com/archon-project-schema.json",
  "project_id": {
    "type": "string",
    "format": "uuid",
    "description": "Archon project UUID"
  },
  "project_name": {
    "type": "string",
    "description": "Human-readable project name"
  },
  "created_at": {
    "type": "string",
    "format": "date-time"
  },
  "status": {
    "type": "string",
    "enum": ["initializing", "active", "paused", "completed"]
  },
  "config": {
    "max_features": { "type": "integer", "default": 30 },
    "max_iterations": { "type": "integer", "default": 50 },
    "model": { "type": "string" },
    "testing_strategy": { "type": "string" }
  }
}
```

### .claude_settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(node:*)",
      "Bash(npx:*)",
      "Bash(git:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(pip:*)",
      "Bash(pip3:*)",
      "Bash(poetry:*)",
      "Bash(pytest:*)",
      "Bash(cargo:*)",
      "Bash(go:*)",
      "Read",
      "Write",
      "Edit",
      "MultiEdit",
      "Glob",
      "Grep",
      "LS"
    ],
    "deny": [
      "Bash(rm -rf /*)",
      "Bash(sudo:*)",
      "Bash(curl|wget *://)",
      "Bash(chmod 777:*)",
      "Bash(dd:*)"
    ]
  },
  "mcp_servers": {
    "archon": {
      "required": true,
      "description": "State management and task tracking"
    },
    "playwright-mcp": {
      "required": false,
      "description": "Browser automation for E2E testing"
    },
    "github": {
      "required": false,
      "description": "Repository operations"
    }
  },
  "model": "claude-opus-4-5-20251101",
  "max_iterations": 50,
  "sandbox": {
    "enabled": true,
    "filesystem_restrictions": true,
    "network_restrictions": false
  }
}
```

### features.json Schema

```json
{
  "$schema": "https://example.com/features-schema.json",
  "version": "1.0",
  "total_features": { "type": "integer" },
  "completed": { "type": "integer" },
  "passing": { "type": "integer" },
  "failing": { "type": "integer" },
  "in_progress": { "type": "integer" },
  "features": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "id": { "type": "integer" },
        "archon_task_id": { "type": "string", "format": "uuid" },
        "name": { "type": "string" },
        "description": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["pending", "in_progress", "passing", "failing", "skipped"]
        },
        "implemented_at": { "type": "string", "format": "date" },
        "tested": { "type": "boolean" },
        "test_results": {
          "type": "object",
          "properties": {
            "unit": { "type": "string", "enum": ["pass", "fail", "skip", "none"] },
            "integration": { "type": "string", "enum": ["pass", "fail", "skip", "none"] },
            "e2e": { "type": "string", "enum": ["pass", "fail", "skip", "none"] },
            "failure_reason": { "type": "string" }
          }
        },
        "dependencies": {
          "type": "array",
          "items": { "type": "integer" }
        }
      },
      "required": ["id", "name", "status"]
    }
  }
}
```

---

## Task Structure Guidelines

### Task Granularity

Each task should represent 30 minutes to 4 hours of work:

**Good Task Examples:**
- "Implement user registration API endpoint"
- "Create login form component with validation"
- "Set up database schema for users table"
- "Add JWT authentication middleware"

**Bad Task Examples (too broad):**
- "Build authentication system"
- "Create the frontend"
- "Implement all API endpoints"

**Bad Task Examples (too narrow):**
- "Add email field to form"
- "Fix typo in button text"
- "Import lodash package"

### Task Template

```json
{
  "title": "Implement user registration API endpoint",
  "description": "Create POST /api/auth/register endpoint that:\n\n## Requirements:\n- Accept email, password, name\n- Validate email format and password strength\n- Hash password with bcrypt\n- Store user in database\n- Return JWT token on success\n\n## Acceptance Criteria:\n- [ ] Endpoint responds to POST /api/auth/register\n- [ ] Returns 201 with token on success\n- [ ] Returns 400 for invalid email\n- [ ] Returns 400 for weak password\n- [ ] Returns 409 for duplicate email\n\n## Test Steps:\n1. Send valid registration request\n2. Verify user in database\n3. Verify JWT token is valid\n4. Test with invalid email\n5. Test with duplicate email",
  "status": "todo",
  "task_order": 85,
  "feature": "Authentication",
  "assignee": "Coding Agent"
}
```

### Feature Groupings

Organize tasks into logical feature groups:

| Feature | Description | Priority Range |
|---------|-------------|----------------|
| Setup | Environment, dependencies, config | 95-100 |
| Database | Schema, migrations, models | 85-94 |
| Authentication | Login, registration, sessions | 75-84 |
| Core API | Main business logic endpoints | 55-74 |
| Frontend | UI components and pages | 35-54 |
| Integration | Third-party services | 25-34 |
| Testing | Test suites and coverage | 15-24 |
| Documentation | API docs, README, guides | 5-14 |
| Polish | Error handling, edge cases | 1-4 |

---

## Session Protocol

### Session Start Checklist

```markdown
## Session Startup

1. [ ] Verify working directory: `pwd`
2. [ ] Check git status: `git status`
3. [ ] Read progress file: `cat claude-progress.txt`
4. [ ] Review recent commits: `git log --oneline -10`
5. [ ] Query Archon for tasks:
   ```
   find_tasks(filter_by="project", filter_value="<PROJECT_ID>")
   ```
6. [ ] Identify current task (status="doing") or select next TODO
7. [ ] Run test suite: `npm test` / `pytest`
8. [ ] If tests fail, fix before proceeding
```

### Session End Checklist

```markdown
## Session Handoff

1. [ ] All changes committed with descriptive messages
2. [ ] Current task status updated in Archon
3. [ ] features.json updated with test results
4. [ ] claude-progress.txt updated:
   - Tasks completed this session
   - Current task status
   - Blockers or issues
   - Context for next session
5. [ ] META task updated in Archon
6. [ ] Codebase in clean, runnable state
7. [ ] No failing tests (or documented why)
```

### Progress File Format

```markdown
# Project Progress: <PROJECT_NAME>

## Session: 2024-01-15 14:30

### Completed This Session:
- [x] Task #5: User registration endpoint (DONE)
- [x] Task #6: Password hashing with bcrypt (DONE)
- [ ] Task #7: JWT token generation (IN PROGRESS - 70%)

### Test Results:
- Unit tests: 45/45 passing
- Integration: 12/12 passing
- E2E: 8/10 passing (2 flaky, need investigation)

### Blockers:
- None currently

### Decisions Made:
- Using bcrypt with cost factor 12 for password hashing
- JWT tokens expire after 7 days with refresh token flow

### Next Session Priority:
1. Complete Task #7 (JWT generation)
2. Start Task #8 (Login endpoint)
3. Investigate flaky E2E tests

### Notes:
- Email service integration postponed to v1.1
- Database indexes added for email lookup performance

---

## Session: 2024-01-14 10:00
[Previous session notes...]
```

---

## Testing Integration

### Playwright MCP Testing

```python
# Navigate to application
mcp__playwright__browser_navigate(url="http://localhost:3000")

# Take accessibility snapshot (preferred over screenshot)
mcp__playwright__browser_snapshot()

# Fill form fields
mcp__playwright__browser_type(
    element="Email input field",
    ref="input[name='email']",
    text="test@example.com"
)

# Click button
mcp__playwright__browser_click(
    element="Submit button",
    ref="button[type='submit']"
)

# Wait for result
mcp__playwright__browser_wait_for(text="Registration successful")

# Verify result
snapshot = mcp__playwright__browser_snapshot()
assert "Welcome" in snapshot
```

### Test Result Recording

After running tests, update features.json:

```python
import json

def update_feature_status(feature_id, test_results):
    with open('features.json', 'r') as f:
        data = json.load(f)

    for feature in data['features']:
        if feature['id'] == feature_id:
            feature['tested'] = True
            feature['test_results'] = test_results

            # Determine overall status
            if all(r in ['pass', 'none'] for r in test_results.values()):
                feature['status'] = 'passing'
                data['passing'] += 1
            else:
                feature['status'] = 'failing'
                data['failing'] += 1
            break

    with open('features.json', 'w') as f:
        json.dump(data, f, indent=2)
```

---

## Error Recovery

### Stuck Task Recovery

```python
# Find stuck tasks (doing for too long)
find_tasks(filter_by="status", filter_value="doing")

# Reset to todo
manage_task("update", task_id="<TASK_ID>", status="todo")

# Add note about issue
manage_task("update",
    task_id="<TASK_ID>",
    description="<ORIGINAL_DESC>\n\n---\nRecovery Note: Task was stuck, reset on <DATE>. Issue: <DESCRIPTION>"
)
```

### Failed Feature Recovery

```python
# Identify failing features
with open('features.json') as f:
    data = json.load(f)
    failing = [f for f in data['features'] if f['status'] == 'failing']

# For each failing feature, find the Archon task and add debugging notes
for feature in failing:
    task_id = feature['archon_task_id']
    failure = feature['test_results'].get('failure_reason', 'Unknown')

    manage_task("update",
        task_id=task_id,
        status="todo",  # Reset to todo
        description=f"Feature needs fix:\n\nFailure: {failure}\n\nPrevious implementation notes: ..."
    )
```

### Context Recovery

If context is lost between sessions:

1. **Read Progress File**:
   ```bash
   cat claude-progress.txt
   ```

2. **Query Archon**:
   ```python
   # Get project details
   find_projects(project_id="<PROJECT_ID>")

   # Get all tasks
   find_tasks(filter_by="project", filter_value="<PROJECT_ID>")

   # Get META task for handoff notes
   find_tasks(query="META Session")
   ```

3. **Check Git History**:
   ```bash
   git log --oneline -20
   git show HEAD --stat
   ```

4. **Review Features**:
   ```bash
   cat features.json | jq '.features | length'
   cat features.json | jq '.features[] | select(.status=="failing")'
   ```

---

## Integration Patterns

### With GitHub Skill

```python
# Create GitHub repo and link to Archon
# 1. Use GitHub skill to create repo
gh repo create <PROJECT_NAME> --public --description "<DESCRIPTION>"

# 2. Update Archon project with repo URL
manage_project("update",
    project_id="<PROJECT_ID>",
    github_repo="https://github.com/<USER>/<PROJECT_NAME>"
)

# 3. Push initial commit
git remote add origin git@github.com:<USER>/<PROJECT_NAME>.git
git push -u origin main
```

### With Browser Testing

```python
# Start dev server in background
# (In separate terminal or background process)
npm run dev &

# Run E2E tests via Playwright MCP
async def run_e2e_tests():
    await mcp__playwright__browser_navigate(url="http://localhost:3000")

    # Test login flow
    await mcp__playwright__browser_type(
        element="Email",
        ref="#email",
        text="test@example.com"
    )
    await mcp__playwright__browser_type(
        element="Password",
        ref="#password",
        text="testpass123"
    )
    await mcp__playwright__browser_click(
        element="Login button",
        ref="#login-btn"
    )

    # Verify redirect
    await mcp__playwright__browser_wait_for(text="Dashboard")
    snapshot = await mcp__playwright__browser_snapshot()

    return "Dashboard" in snapshot
```

---

## Quick Reference Commands

### Archon Project Management

| Action | Command |
|--------|---------|
| Create project | `manage_project("create", title="...", description="...")` |
| Get project | `find_projects(project_id="uuid")` |
| Update project | `manage_project("update", project_id="uuid", ...)` |
| Delete project | `manage_project("delete", project_id="uuid")` |

### Archon Task Management

| Action | Command |
|--------|---------|
| Create task | `manage_task("create", project_id="...", title="...", ...)` |
| Get task | `find_tasks(task_id="uuid")` |
| List project tasks | `find_tasks(filter_by="project", filter_value="uuid")` |
| Filter by status | `find_tasks(filter_by="status", filter_value="todo")` |
| Search tasks | `find_tasks(query="auth")` |
| Start task | `manage_task("update", task_id="uuid", status="doing")` |
| Complete task | `manage_task("update", task_id="uuid", status="done")` |

### File Operations

| Action | Command |
|--------|---------|
| Update progress | `echo "## Session..." >> claude-progress.txt` |
| View features | `cat features.json \| jq '.'` |
| Check config | `cat .claude_settings.json` |
| View project info | `cat .archon_project.json` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-22 | Initial release with Archon integration |
