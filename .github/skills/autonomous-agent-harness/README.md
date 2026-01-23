# Autonomous Agent Harness - Complete Guide

> A comprehensive system for long-running autonomous coding agents based on Anthropic's ["Effective Harnesses for Long-Running Agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) architecture.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Setup Wizard](#setup-wizard)
- [Agent Pipeline](#agent-pipeline)
- [Archon Integration](#archon-integration)
- [Execution Modes](#execution-modes)
- [Session Management](#session-management)
- [Testing Integration](#testing-integration)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

### The Challenge

AI agents face a fundamental problem: **context windows are limited**. Complex projects cannot be completed in a single session, and each new session starts with no memory of previous work.

### The Solution

This harness implements a **multi-agent pipeline** with:

1. **Archon-based State Management**: All state persists across sessions
2. **Specialized Agents**: Each agent has a focused role
3. **Clean Handoffs**: Structured notes for seamless continuation
4. **Incremental Progress**: One feature per session
5. **Quality Assurance**: Built-in testing and code review

### Key Benefits

| Benefit | Description |
|---------|-------------|
| 🔄 **Multi-Session** | Work spans many context windows |
| 📋 **Task-Driven** | Features tracked as Archon tasks |
| 🧪 **Quality Built-In** | Testing and review agents |
| 📝 **Clean Handoffs** | Context preserved between sessions |
| ⚡ **Parallel Execution** | Testing can run in background |

---

## Quick Start

### 1. Prerequisites

Ensure you have:
- Archon MCP server configured and running
- GitHub Copilot with agent mode
- A project idea with detailed specification

### 2. Initial Setup

```bash
# Start the setup wizard
/harness-setup
```

The wizard will guide you through:
- Project configuration
- Technical stack selection
- Agent settings
- Application specification

### 3. Initialize Project

```bash
# Run the initializer (first session only)
/harness-init
```

This creates feature tasks from your specification.

### 4. Start Coding

```bash
# Begin coding sessions
/harness-next
```

Repeat this for each feature until complete.

### 5. Check Progress

```bash
# View status anytime
/harness-status
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                       HARNESS SYSTEM                                 │
│                                                                      │
│   ┌───────────────────────────────────────────────────────────────┐ │
│   │                     USER INTERFACE                             │ │
│   │                                                                │ │
│   │   /harness-setup   /harness-init   /harness-next              │ │
│   │   /harness-status  /harness-resume                            │ │
│   └───────────────────────────────────────────────────────────────┘ │
│                              │                                       │
│                              ▼                                       │
│   ┌───────────────────────────────────────────────────────────────┐ │
│   │                    AGENT PIPELINE                              │ │
│   │                                                                │ │
│   │   @harness-wizard ──► @harness-initializer ──► @harness-coder │ │
│   │                                                    │           │ │
│   │                              ┌─────────────────────┤           │ │
│   │                              ▼                     ▼           │ │
│   │                      @harness-tester    @harness-reviewer     │ │
│   └───────────────────────────────────────────────────────────────┘ │
│                              │                                       │
│                              ▼                                       │
│   ┌───────────────────────────────────────────────────────────────┐ │
│   │                   ARCHON STATE LAYER                           │ │
│   │                                                                │ │
│   │   ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │ │
│   │   │  Projects   │  │    Tasks     │  │    Documents      │   │ │
│   │   │             │  │              │  │                   │   │ │
│   │   │ • Metadata  │  │ • Features   │  │ • App Spec        │   │ │
│   │   │ • Status    │  │ • Status     │  │ • Session Notes   │   │ │
│   │   │ • Config    │  │ • Priority   │  │ • Config          │   │ │
│   │   └─────────────┘  └──────────────┘  └───────────────────┘   │ │
│   └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Setup Wizard

### Full Setup Mode

Interactive wizard for new projects:

```bash
/harness-setup
```

Collects information in 5 phases:
1. **Project Basics**: Name, description, type
2. **Technical Stack**: Language, framework, database
3. **Agent Configuration**: Features, iterations, model
4. **Testing Strategy**: Unit, integration, E2E
5. **Application Specification**: Detailed requirements

### Quick Setup Mode

Minimal questions with smart defaults:

```bash
/harness-quick
```

Auto-detects from existing files:
- Language from package.json, requirements.txt, etc.
- Framework from dependencies
- Testing from existing test files

### Resume Mode

Continue existing project:

```bash
/harness-resume
```

Reads `.harness/config.json` and queries Archon.

---

## Agent Pipeline

### @harness-wizard

**Purpose**: Interactive setup and configuration

**Responsibilities**:
- Gather project requirements
- Create Archon project and documents
- Generate local configuration files
- Guide user through setup process

### @harness-initializer

**Purpose**: First session initialization

**Responsibilities**:
- Read application specification
- Generate feature tasks in Archon
- Set up project structure
- Initialize git repository
- Create clean handoff for coder

### @harness-coder

**Purpose**: Main development workhorse

**Responsibilities**:
- Read session context from Archon
- Verify existing features work
- Select and implement one feature
- Coordinate with tester and reviewer
- Create clean handoff for next session

### @harness-tester

**Purpose**: Testing and verification

**Responsibilities**:
- Run unit, integration, and E2E tests
- Use browser automation for UI testing
- Report results to Archon
- Identify issues for fixing

**Invocation**:
```bash
& @harness-tester verify "Feature Name" --task-id "task-123"
```

### @harness-reviewer

**Purpose**: Code quality and review

**Responsibilities**:
- Review code changes
- Check architecture consistency
- Identify security issues
- Provide actionable feedback

**Invocation**:
```bash
& @harness-reviewer check "Feature Name" --task-id "task-123"
```

---

## Archon Integration

### Data Model

```
Archon Project: "my-project"
├── Documents:
│   ├── "Application Specification" (type: spec)
│   ├── "Harness Configuration" (type: guide)
│   ├── "Session Notes" (type: note)
│   └── "Feature Registry" (type: prp)
│
└── Tasks:
    ├── META: "Session Tracking" (task_order: 100)
    ├── Setup: "Initialize environment" (task_order: 99)
    ├── Feature 1: "..." (task_order: 85)
    ├── Feature 2: "..." (task_order: 75)
    └── ...
```

### Task Status Flow

```
todo ──► doing ──► review ──► done
  ▲         │         │
  │         │         │
  └─────────┴─────────┘
     (if issues found)
```

### Key Archon Commands

```python
# Find tasks
find_tasks(filter_by="project", filter_value=PROJECT_ID)
find_tasks(filter_by="status", filter_value="todo")

# Update task
manage_task("update", task_id="...", status="doing")
manage_task("update", task_id="...", status="done")

# Get documents
find_documents(project_id=PROJECT_ID, query="Session Notes")

# Update documents
manage_document("update", project_id=PROJECT_ID, document_id="...", content={...})
```

---

## Execution Modes

### Terminal Mode

Manual prompt execution:

```bash
/harness-setup    # Setup wizard
/harness-init     # Initialize project
/harness-next     # Start coding session
/harness-status   # Check progress
```

### Background Mode

Parallel execution with `&` prefix:

```bash
# Run coding session in background
& /harness-next

# Run testing in parallel
& @harness-tester verify "User Auth"

# Run review in parallel
& @harness-reviewer check "User Auth"
```

### SDK Mode (Python)

For automated pipelines:

```python
# harness_runner.py
import asyncio
from pathlib import Path

async def run_harness():
    """Run harness sessions automatically"""
    # Read configuration
    config = load_config(".harness/config.json")
    
    # Run sessions until complete
    while has_remaining_tasks():
        await run_coding_session(config)
        await asyncio.sleep(3)  # Brief pause between sessions

if __name__ == "__main__":
    asyncio.run(run_harness())
```

---

## Session Management

### Session Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                             │
│                                                                  │
│   1. ORIENT          2. VERIFY          3. SELECT               │
│   ┌─────────┐       ┌─────────┐       ┌─────────┐              │
│   │ Read    │──────►│ Run     │──────►│ Pick    │              │
│   │ Archon  │       │ Tests   │       │ Task    │              │
│   └─────────┘       └─────────┘       └─────────┘              │
│                                              │                   │
│   6. HANDOFF         5. UPDATE         4. IMPLEMENT             │
│   ┌─────────┐       ┌─────────┐       ┌─────────┐              │
│   │ Commit  │◄──────│ Update  │◄──────│ Code &  │◄─────────────┘│
│   │ & Note  │       │ Archon  │       │ Test    │              │
│   └─────────┘       └─────────┘       └─────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Handoff Protocol

At the end of each session:

1. **Update Session Notes** in Archon
2. **Update META Task** with progress
3. **Commit to Git** with descriptive message
4. **Leave Clean State** - no broken tests

### Session Notes Structure

```json
{
  "sessions": [...],
  "current_focus": "Next task title",
  "blockers": [...],
  "next_steps": [...],
  "decisions": [...]
}
```

---

## Testing Integration

### Testing Strategy Options

| Strategy | Tests Included |
|----------|----------------|
| Unit Only | Unit tests |
| Unit + Integration | Unit + Integration tests |
| Full E2E | Unit + Integration + Browser tests |
| Manual | No automated tests |

### Browser Testing

Using Playwright MCP:

```python
# Navigate and interact
mcp__playwright__browser_navigate(url="http://localhost:3000")
mcp__playwright__browser_type(element="Email", ref="#email", text="test@example.com")
mcp__playwright__browser_click(element="Submit", ref="button[type='submit']")
mcp__playwright__browser_snapshot()  # Verify results
```

### Test Result Reporting

Test results are stored in Archon task descriptions:

```markdown
## Test Results (Verified by harness-tester)
**Status**: ✅ PASSING

| Type | Passed | Failed | Total |
|------|--------|--------|-------|
| Unit | 15 | 0 | 15 |
| Integration | 8 | 0 | 8 |
| E2E | 3 | 0 | 3 |
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Archon not accessible | Check MCP configuration and server status |
| Task stuck in "doing" | Reset to "todo" with note about issue |
| Tests failing | Fix before starting new features |
| Lost context | Read session notes and git log |
| Agent skips testing | Check testing configuration |

### Recovery Commands

```python
# Find stuck tasks
find_tasks(filter_by="status", filter_value="doing")

# Reset stuck task
manage_task("update", task_id="...", status="todo")

# View session history
find_documents(project_id=PROJECT_ID, query="Session Notes")

# Check git history
git log --oneline -20
```

### Debug Checklist

- [ ] Archon MCP is running and accessible
- [ ] `.harness/config.json` exists with valid project ID
- [ ] Session notes document exists in Archon
- [ ] Git repository is initialized
- [ ] Development environment works (`init.sh`)

---

## Best Practices

### 1. Detailed Specifications

The more detail in your app specification, the better the generated tasks.

**Good**:
```
User authentication with JWT tokens:
- Registration with email/password
- Email validation with regex
- Password hashing with bcrypt (cost 12)
- JWT with 7-day expiry and refresh tokens
- Rate limiting: 5 attempts per minute
```

**Bad**:
```
Add user authentication
```

### 2. Incremental Progress

- Work on ONE feature per session
- Complete and test before moving on
- Don't try to do too much at once

### 3. Clean Handoffs

- Always update Archon session notes
- Always commit with descriptive messages
- Never leave tests failing
- Document any blockers or decisions

### 4. Trust the Pipeline

- Let testing agent verify features
- Use review agent for complex changes
- Address feedback before marking complete

### 5. Fix Issues First

- Failing tests before new features
- Blockers before new work
- Technical debt before new features

---

## Related Files

### Agents
- `.github/agents/harness-wizard.agent.md`
- `.github/agents/harness-initializer.agent.md`
- `.github/agents/harness-coder.agent.md`
- `.github/agents/harness-tester.agent.md`
- `.github/agents/harness-reviewer.agent.md`

### Prompts
- `.github/prompts/harness-setup.prompt.md`
- `.github/prompts/harness-quick.prompt.md`
- `.github/prompts/harness-init.prompt.md`
- `.github/prompts/harness-next.prompt.md`
- `.github/prompts/harness-status.prompt.md`
- `.github/prompts/harness-resume.prompt.md`

### Templates
- `templates/wizard_questionnaire.md`
- `templates/session_handoff.md`
- `templates/archon_documents.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-22 | Multi-agent pipeline, enhanced Archon integration |
| 1.0.0 | 2024-12-22 | Initial release |
