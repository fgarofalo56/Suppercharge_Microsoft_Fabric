# Delegation Rules for Copilot Coding Agent

This document defines guidelines for delegating tasks to the GitHub Copilot coding agent. Following these rules ensures effective task completion and maintains code quality.

## When to Delegate

### ✅ Good Candidates for Delegation

| Task Type | Examples |
|-----------|----------|
| **Bug fixes** | Fix null reference, correct calculation, handle edge case |
| **Feature implementation** | Add new endpoint, create component, implement service |
| **Refactoring** | Extract method, rename variables, simplify logic |
| **Test coverage** | Add unit tests, integration tests |
| **Documentation** | Update README, add JSDoc, create guides |
| **Dependency updates** | Update package versions, fix deprecations |

### ❌ Avoid Delegating

| Task Type | Reason |
|-----------|--------|
| **Security-sensitive changes** | Requires human review |
| **Architecture decisions** | Needs team discussion |
| **Production deployments** | Needs human approval |
| **Database migrations** | High risk, needs review |
| **Credential/secret changes** | Security concern |
| **Breaking API changes** | Needs coordination |

## Writing Effective Task Descriptions

### Structure

```markdown
## Objective
[Clear, specific goal - what should be accomplished]

## Context
[Background information the agent needs to understand]

## Requirements
- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Constraints
- [Any limitations or restrictions]
- [Performance requirements]
- [Compatibility requirements]

## References
- [Link to related code]
- [Link to documentation]
- [Link to design doc]
```

### Good Example

```markdown
## Objective
Add email validation to the user registration form.

## Context
Currently, the registration form accepts any string as an email. 
We need proper validation to prevent invalid emails.

## Requirements
- Validate email format using a standard regex pattern
- Show error message "Please enter a valid email address"
- Validate on blur and on submit
- Clear error when user starts typing

## Acceptance Criteria
- [ ] Invalid emails show error message
- [ ] Valid emails pass validation
- [ ] Error clears on input change
- [ ] Unit tests cover validation logic
- [ ] Accessibility: error is announced to screen readers

## Constraints
- Use existing form validation library (react-hook-form)
- Must work with existing styling
- No new dependencies

## References
- Form component: src/components/RegisterForm.tsx
- Validation utils: src/utils/validation.ts
```

### Bad Example

```markdown
Fix the email thing on the form
```

*Why it's bad: No context, no requirements, no acceptance criteria*

## Task Size Guidelines

### Ideal Task Size
- **1-2 hours of work** for a human developer
- **5-15 files** modified
- **50-200 lines** changed
- **Single logical change**

### Too Large
- Multi-day features → Break into smaller tasks
- Multiple unrelated changes → Create separate tasks
- System-wide refactoring → Phase into incremental changes

### Too Small
- Single typo fix → Do it yourself
- One-line change → Faster to do manually

## Labels for Delegation

When creating issues for delegation, use these labels:

| Label | Purpose |
|-------|---------|
| `copilot-delegate` | Mark for agent processing |
| `priority:high` | Process before other tasks |
| `priority:low` | Process when queue is empty |
| `type:bug` | Bug fix task |
| `type:feature` | New feature |
| `type:refactor` | Code improvement |
| `type:test` | Test coverage |
| `type:docs` | Documentation |

## Review Process

### Before Merging Agent PRs

1. **Review all changes** - Agent code needs human review
2. **Run tests locally** - Verify tests pass
3. **Check for regressions** - Ensure nothing broke
4. **Verify acceptance criteria** - All requirements met
5. **Check security** - No credentials, vulnerabilities
6. **Approve and merge** - Or request changes

### Common Issues to Watch For

- Generated code that's too verbose
- Missing edge case handling
- Incorrect assumptions about existing code
- Tests that don't actually test behavior
- Over-engineering simple solutions

## Feedback Loop

### If Agent Did Well
- Approve the PR
- Note what worked in the issue

### If Agent Needs Improvement
- Request changes with specific feedback
- Agent will iterate based on comments
- Update task description if requirements were unclear

### If Agent Failed
- Close the PR
- Update the issue with more context
- Consider if task is appropriate for delegation

## Templates

Use delegation templates in `.github/copilot/delegate-templates/` for common task types:
- `bug-fix.md` - Bug fix template
- `feature.md` - New feature template
- `refactor.md` - Refactoring template
- `test-coverage.md` - Testing template
- `docs-update.md` - Documentation template

## Quick Reference

```
Good delegation = Clear goal + Context + Requirements + Acceptance criteria

Delegate: Bugs, features, refactoring, tests, docs
Avoid: Security, architecture, deployments, migrations

Task size: 1-2 hours, 5-15 files, single logical change

Always review agent PRs before merging!
```
