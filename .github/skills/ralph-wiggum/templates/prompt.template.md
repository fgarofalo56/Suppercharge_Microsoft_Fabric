# Ralph Loop: {{TASK_TITLE}}

## Objective

{{TASK_DESCRIPTION}}

## Requirements

{{#each REQUIREMENTS}}
{{@index}}. {{this}}
{{/each}}

## Acceptance Criteria

{{#each ACCEPTANCE_CRITERIA}}
- [ ] {{this}}
{{/each}}

## Self-Correction Loop

For each iteration:

1. **Review Previous Work**
   - Check git log for recent changes
   - Read modified files
   - Understand current state

2. **Run Validation**
   ```bash
   {{BUILD_CMD}}
   {{TEST_CMD}}
   ```

3. **If Validation Fails**
   - Analyze error output
   - Identify root cause
   - Implement fix
   - Return to step 2

4. **If Validation Passes**
   - Check against acceptance criteria
   - If criteria remaining, implement next one
   - If all criteria met, go to step 5

5. **Completion Check**
   - Run full validation suite
   - Verify all acceptance criteria
   - Update Archon task status
   - Output: `<promise>COMPLETE</promise>`

## Validation Commands

```bash
# Build
{{BUILD_CMD}}

# Test
{{TEST_CMD}}

# Lint (optional)
{{LINT_CMD}}
```

## Archon Context

- **Project ID**: {{ARCHON_PROJECT_ID}}
- **Task ID**: {{ARCHON_TASK_ID}}
- **Loop ID**: {{LOOP_ID}}

## State Management

After each iteration, update Archon:

```python
manage_task("update",
    task_id="{{ARCHON_TASK_ID}}",
    description="""[Original description]

---
## Ralph Progress (Iteration N/{{MAX_ITERATIONS}})

### Status
[Current progress summary]

### Files Changed
[List of files]

### Test Results
[Pass/fail status]
"""
)
```

## Escape Hatch

After {{ESCAPE_ITERATIONS}} iterations without progress:

1. **Document the Blocker**
   - What's preventing completion
   - What has been tried
   - What might work

2. **Update Archon Task**
   ```python
   manage_task("update",
       task_id="{{ARCHON_TASK_ID}}",
       status="todo",
       description="BLOCKED: [reason]"
   )
   ```

3. **Signal Blocked State**
   ```
   <promise>BLOCKED</promise>
   ```

## Important Rules

1. **ONE THING AT A TIME** - Focus on one requirement per iteration
2. **ALWAYS VALIDATE** - Run tests after every change
3. **ALWAYS UPDATE STATE** - Keep Archon current
4. **COMMIT INCREMENTALLY** - Commit after each successful iteration
5. **DON'T GIVE UP** - Iterate until completion or blocked

## Commit Message Format

```
Ralph iteration [N]: [Brief summary]

- [Change 1]
- [Change 2]

Loop: {{LOOP_ID}}
Task: {{ARCHON_TASK_ID}}
```

---

**Start now. Review current state and begin iteration.**
