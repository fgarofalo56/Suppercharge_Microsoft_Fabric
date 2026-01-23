---
description: Determine what to work on next based on Archon tasks and priorities
---

# What's Next?

Analyze current state and provide options for what to work on next.

## Check Current Context

### 1. In-Progress Work

```
find_tasks(filter_by="status", filter_value="doing")
```

### 2. Pending Tasks

```
find_tasks(filter_by="status", filter_value="todo")
```

### 3. Blockers

```
find_tasks(filter_by="status", filter_value="blocked")
```

### 4. Recent Session Memory

```
find_documents(project_id="[PROJECT_ID]", query="Session Memory")
```

## Provide Options

```markdown
## 🎯 What Should I Work On Next?

### Option A: Continue Previous Work

**Task**: [In-progress task title]
**Status**: [Current progress]
**Next Action**: [Specific next step]
**Estimated Time**: [X minutes/hours]

---

### Option B: New Priority Items

**Ranked by importance:**

1. **[Task Title]** (Priority: X/100)
   - Why: [Reason for priority]
   - Action: [First step]
   - Time: [Estimate]

2. **[Task Title]** (Priority: X/100)
   - Why: [Reason]
   - Action: [First step]
   - Time: [Estimate]

3. **[Task Title]** (Priority: X/100)
   - Why: [Reason]
   - Action: [First step]
   - Time: [Estimate]

---

### Option C: Maintenance Tasks

- [ ] Documentation updates needed
- [ ] Test coverage improvements
- [ ] Refactoring opportunities
- [ ] Dependency updates

---

### ⚠️ Blockers to Resolve First

- [Any blockers that should be addressed]

---

**My Recommendation**: [Option X] because [reason]
```

Be specific about what the next action would be for each option.

{input}
