# Ralph Wiggum Reference Guide

Comprehensive reference for all Ralph Wiggum features, configuration options, and integration patterns.

---

## Table of Contents

- [Loop Configuration](#loop-configuration)
- [Archon State Management](#archon-state-management)
- [Prompt Templates](#prompt-templates)
- [Framework Integration](#framework-integration)
- [Advanced Patterns](#advanced-patterns)
- [API Reference](#api-reference)

---

## Loop Configuration

### Basic Configuration

```json
{
  "loop_id": "ralph-<TIMESTAMP>",
  "prompt": "Task description with completion criteria",
  "max_iterations": 50,
  "completion_promise": "COMPLETE",
  "mode": "background"
}
```

### Full Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `loop_id` | string | auto-generated | Unique identifier for the loop |
| `prompt` | string | required | The task prompt for the AI agent |
| `prompt_file` | string | null | Path to prompt file (alternative to inline) |
| `max_iterations` | number | 50 | Maximum iterations before stopping |
| `completion_promise` | string | "COMPLETE" | Text that signals completion |
| `mode` | string | "hybrid" | Execution mode: background, manual, hybrid |
| `archon_project_id` | string | null | Archon project for state management |
| `archon_task_id` | string | null | Specific task to work on |
| `timeout_minutes` | number | 0 | Timeout per iteration (0 = unlimited) |
| `pause_between_iterations` | number | 0 | Seconds to wait between iterations |
| `auto_commit` | boolean | true | Automatically commit after each iteration |
| `test_command` | string | null | Command to run tests |
| `build_command` | string | null | Command to build project |
| `validation_commands` | array | [] | Commands to validate completion |

### Configuration File

Create `.ralph/config.json`:

```json
{
  "defaults": {
    "max_iterations": 50,
    "mode": "hybrid",
    "completion_promise": "COMPLETE",
    "auto_commit": true,
    "pause_between_iterations": 5
  },
  "archon": {
    "default_project": null,
    "sync_interval_seconds": 30,
    "create_state_document": true
  },
  "integration": {
    "harness": {
      "enabled": true,
      "agent": "harness-coder",
      "use_session_notes": true
    },
    "speckit": {
      "enabled": true,
      "spec_directory": "specs",
      "checklist_validation": true
    },
    "prp": {
      "enabled": true,
      "plans_directory": "PRPs/plans",
      "auto_update_phases": true
    }
  },
  "validation": {
    "require_tests_pass": true,
    "require_build_success": true,
    "require_lint_clean": false
  },
  "safety": {
    "max_files_per_iteration": 20,
    "max_lines_changed_per_iteration": 500,
    "blocked_paths": ["node_modules", ".git", "dist"],
    "require_review_after": 10
  }
}
```

---

## Archon State Management

### State Document Structure

Ralph creates and maintains a state document in Archon:

```json
{
  "document_type": "note",
  "title": "Ralph Loop State: [LOOP_ID]",
  "content": {
    "loop_id": "ralph-20260122-150000",
    "status": "running",
    "started_at": "2026-01-22T15:00:00Z",
    "last_updated": "2026-01-22T15:35:00Z",
    "current_iteration": 7,
    "max_iterations": 50,
    "completion_promise": "COMPLETE",
    "prompt_hash": "sha256:abc123...",
    
    "progress": {
      "files_created": 12,
      "files_modified": 8,
      "tests_added": 15,
      "tests_passing": 14,
      "tests_failing": 1
    },
    
    "iterations": [
      {
        "n": 1,
        "started_at": "2026-01-22T15:00:00Z",
        "completed_at": "2026-01-22T15:05:00Z",
        "duration_seconds": 300,
        "summary": "Initial project setup and dependencies",
        "files_changed": ["package.json", "tsconfig.json", "src/index.ts"],
        "tests_run": 0,
        "tests_passed": 0,
        "commit_sha": "abc123"
      },
      {
        "n": 2,
        "started_at": "2026-01-22T15:05:00Z",
        "completed_at": "2026-01-22T15:12:00Z",
        "duration_seconds": 420,
        "summary": "Basic CRUD operations implemented",
        "files_changed": ["src/api.ts", "src/types.ts", "tests/api.test.ts"],
        "tests_run": 5,
        "tests_passed": 3,
        "tests_failed": 2,
        "failure_summary": "Validation errors on create/update"
      }
    ],
    
    "current_focus": "Fixing validation errors",
    "blockers": [],
    "decisions": [
      "Using Zod for validation",
      "REST API with Express"
    ]
  }
}
```

### Task Integration

Ralph can work on existing Archon tasks:

```python
# Ralph marks task as in-progress
manage_task("update",
    task_id=TASK_ID,
    status="doing",
    assignee="Ralph Agent"
)

# During iterations, Ralph updates description
manage_task("update",
    task_id=TASK_ID,
    description="""[ORIGINAL_DESCRIPTION]

---
## Ralph Progress (Iteration 7/50)

### Completed
- Project setup ✅
- Basic CRUD ✅
- Input validation 🔄 (in progress)

### Current Focus
Fixing validation errors in create/update endpoints

### Test Status
- Passing: 14/15
- Failing: 1 (validation test)

### Files Changed
- src/api.ts
- src/validators.ts
- tests/api.test.ts

---
Last Updated: 2026-01-22T15:35:00Z
"""
)

# On completion
manage_task("update",
    task_id=TASK_ID,
    status="done"
)
```

---

## Prompt Templates

### Standard Loop Prompt Template

```markdown
# Ralph Loop: [TASK_NAME]

## Objective
[Clear description of what needs to be accomplished]

## Requirements
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Self-Correction Loop

For each iteration:
1. Review previous work in files and git history
2. Run tests: `[TEST_COMMAND]`
3. If tests fail:
   - Analyze failure output
   - Fix the issue
   - Re-run tests
4. If tests pass:
   - Review against requirements
   - Continue with next requirement
5. When all requirements met:
   - Run full validation
   - Output: <promise>COMPLETE</promise>

## Validation Commands
```bash
[BUILD_COMMAND]
[TEST_COMMAND]
[LINT_COMMAND]
```

## Escape Hatch

After [N] iterations without progress:
1. Document blockers in Archon task
2. List what was attempted
3. Suggest alternative approaches
4. Output: <promise>BLOCKED</promise>

## Important Context
- Archon Project ID: [PROJECT_ID]
- Archon Task ID: [TASK_ID]
- Working Directory: [DIRECTORY]
```

### TDD-Focused Template

```markdown
# TDD Loop: [FEATURE_NAME]

## Test-Driven Development Protocol

### Phase 1: RED (Write Failing Tests)
Write tests that define expected behavior:
1. Unit tests for core logic
2. Integration tests for API endpoints
3. Edge case coverage

### Phase 2: GREEN (Make Tests Pass)
Implement minimal code to pass tests:
1. Focus on one test at a time
2. Simplest solution first
3. No premature optimization

### Phase 3: REFACTOR
Improve code quality:
1. Remove duplication
2. Improve naming
3. Simplify complexity
4. Maintain passing tests

## Iteration Loop

```
for each requirement:
    write_tests()    # RED
    while tests_fail:
        implement()  # GREEN
        run_tests()
    refactor()       # REFACTOR
    run_tests()      # Verify still green
```

## Completion Signal

When all requirements have passing tests:
```
<promise>TDD_COMPLETE</promise>
```
```

### Bug Fix Template

```markdown
# Bug Fix Loop: [BUG_DESCRIPTION]

## Issue Reference
- GitHub Issue: #[NUMBER]
- Archon Task: [TASK_ID]

## Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected vs Actual
- Expected: [What should happen]
- Actual: [What happens instead]

## Investigation Protocol

### Iteration Pattern
1. Review current understanding of bug
2. Add/run diagnostic tests or logging
3. Analyze output
4. Form hypothesis
5. Implement fix attempt
6. Test the fix
7. If not fixed, update understanding and repeat

### When Fixed
1. Verify original issue resolved
2. Add regression test
3. Remove diagnostic code
4. Clean up changes
5. Output: <promise>BUG_FIXED</promise>

### If Cannot Fix
After [N] iterations:
1. Document root cause findings
2. List attempted fixes
3. Suggest escalation path
4. Output: <promise>NEEDS_ESCALATION</promise>
```

---

## Framework Integration

### The Long Run Harness Integration

Ralph can wrap the harness-coder agent:

```yaml
# .ralph/integrations/harness.yaml
integration: harness
enabled: true

# Ralph wraps harness coding sessions
wrapper_mode: true

# Use harness session notes for context
use_session_notes: true

# Completion tied to task status
completion_trigger: archon_task_done

# Custom iteration prompt
iteration_prompt: |
  Continue the harness coding session.
  
  1. Check session notes for context
  2. Work on current task
  3. Update Archon state
  4. Commit progress
  
  Complete when task is done.
```

**Usage:**

```bash
# Start Ralph-powered harness session
/harness-ralph

# Equivalent to:
# /ralph-loop with harness-coder as the inner agent
```

### Spec Kit Integration

Ralph iterates until spec requirements are met:

```yaml
# .ralph/integrations/speckit.yaml
integration: speckit
enabled: true

# Spec location
spec_directory: specs

# Validate against checklist
checklist_validation: true

# Completion when checklist complete
completion_trigger: checklist_done

# Iteration prompt
iteration_prompt: |
  Implement the specification at: {SPEC_PATH}
  
  For each checklist item:
  1. Implement the requirement
  2. Run validation
  3. Update checklist
  
  Complete when all checklist items pass.
```

**Usage:**

```bash
# Ralph iterates on spec implementation
/speckit-ralph specs/123-auth-feature/spec.md

# Ralph tracks progress via checklist
# Completes when all items checked
```

### PRP Framework Integration

Ralph executes PRP plans with iteration:

```yaml
# .ralph/integrations/prp.yaml
integration: prp
enabled: true

# Plan location
plans_directory: PRPs/plans

# Auto-update phase status
auto_update_phases: true

# Completion when plan complete
completion_trigger: plan_done

# Iteration prompt
iteration_prompt: |
  Execute the PRP plan at: {PLAN_PATH}
  
  For each task in the plan:
  1. Implement the task
  2. Run validation commands
  3. Mark task complete
  
  Complete when all tasks done.
```

**Usage:**

```bash
# Ralph iterates through PRP plan
/prp-ralph PRPs/plans/feature.plan.md

# Ralph validates each step
# Updates plan status
# Completes when all tasks done
```

### Multi-Framework Mode

Enable all integrations:

```bash
/ralph-integrate all
```

Ralph automatically detects which framework applies:
- Has `.harness/config.json` → Use harness mode
- Has `specs/*/spec.md` → Use speckit mode
- Has `PRPs/plans/*.plan.md` → Use PRP mode

---

## Advanced Patterns

### Parallel Loops

Run multiple Ralph loops for independent features:

```bash
# Terminal 1: Auth feature
/ralph-loop "Implement authentication" --loop-id ralph-auth

# Terminal 2: API feature
/ralph-loop "Implement API endpoints" --loop-id ralph-api

# Both write to separate Archon documents
# No interference between loops
```

### Supervised Start, Autonomous Finish

```bash
# First iterations - supervised
/ralph-iterate  # Watch iteration 1
/ralph-iterate  # Watch iteration 2
/ralph-iterate  # Looks good!

# Confidence gained, go autonomous
& /ralph-continue --remaining
```

### Checkpointing

Enable checkpoints for long-running loops:

```json
{
  "checkpointing": {
    "enabled": true,
    "interval_iterations": 5,
    "checkpoint_directory": ".ralph/checkpoints",
    "git_tag_checkpoints": true
  }
}
```

Recover from checkpoint:

```bash
/ralph-resume --checkpoint ralph-checkpoint-5
```

### Progressive Timeout

Increase iteration timeout as task nears completion:

```json
{
  "progressive_timeout": {
    "enabled": true,
    "base_minutes": 5,
    "increment_per_iteration": 0.5,
    "max_minutes": 30
  }
}
```

---

## API Reference

### Wizard Agent

`@ralph-wizard` - Interactive setup wizard

**Collects:**
- Project/task from Archon
- Task description
- Completion criteria
- Max iterations
- Execution mode
- Framework integration options
- Validation commands

### Loop Agent

`@ralph-loop` - Main loop controller

**Parameters:**
```
@ralph-loop <prompt> [options]

Options:
  --max-iterations <n>      Maximum iterations (default: 50)
  --completion-promise <s>  Completion marker (default: COMPLETE)
  --mode <mode>             background|manual|hybrid
  --project <id>            Archon project ID
  --task <id>               Archon task ID
  --loop-id <id>            Custom loop identifier
```

### Monitor Agent

`@ralph-monitor` - Progress monitoring

**Features:**
- Real-time iteration progress
- Test status tracking
- File change summary
- Time estimates
- Blocker detection

### Integration Agent

`@ralph-integrator` - Framework integration

**Commands:**
```
@ralph-integrator harness   # Configure harness integration
@ralph-integrator speckit   # Configure speckit integration
@ralph-integrator prp       # Configure PRP integration
@ralph-integrator status    # Show integration status
```

---

## Archon Tool Reference

### For State Management

```python
# Create loop state document
manage_document("create",
    project_id=PROJECT_ID,
    title="Ralph Loop State: [LOOP_ID]",
    document_type="note",
    content={...}
)

# Update loop state
manage_document("update",
    project_id=PROJECT_ID,
    document_id=DOC_ID,
    content={...}
)

# Find loop state
find_documents(
    project_id=PROJECT_ID,
    query="Ralph Loop State"
)
```

### For Task Tracking

```python
# Get current task
find_tasks(task_id=TASK_ID)

# Update task progress
manage_task("update",
    task_id=TASK_ID,
    status="doing",
    description="Updated with Ralph progress"
)

# Complete task
manage_task("update",
    task_id=TASK_ID,
    status="done"
)
```

---

## Metrics & Monitoring

### Loop Metrics

Track across loops:

| Metric | Description |
|--------|-------------|
| `iterations_to_completion` | How many iterations needed |
| `success_rate` | Loops that complete vs blocked |
| `avg_iteration_duration` | Time per iteration |
| `files_changed_per_iteration` | Code velocity |
| `test_pass_rate_trend` | Quality over iterations |

### Dashboard Query

```python
# Get all Ralph loop documents
loops = find_documents(
    project_id=PROJECT_ID,
    query="Ralph Loop State"
)

# Aggregate metrics
total_loops = len(loops)
completed = sum(1 for l in loops if l["content"]["status"] == "complete")
avg_iterations = sum(l["content"]["current_iteration"] for l in loops) / total_loops
```

---

## Best Practices Checklist

### Before Starting a Loop

- [ ] Task has clear, testable completion criteria
- [ ] Max iterations set (safety net)
- [ ] Archon project/task configured
- [ ] Validation commands defined
- [ ] Escape hatch instructions in prompt
- [ ] Framework integration configured (if applicable)

### During Loop

- [ ] Monitor first few iterations
- [ ] Check iteration summaries
- [ ] Watch for stuck patterns
- [ ] Verify tests are actually running

### After Loop

- [ ] Verify completion criteria met
- [ ] Review all changes
- [ ] Run full test suite
- [ ] Check Archon state updated
- [ ] Archive loop state document
