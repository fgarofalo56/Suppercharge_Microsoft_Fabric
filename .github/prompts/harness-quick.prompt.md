---
name: harness-quick
description: Quick setup for autonomous agent harness with smart defaults. Minimal questions, fast initialization.
mode: agent
agent: harness-wizard
---

# ⚡ Quick Harness Setup

Fast-track harness setup with smart defaults.

## Automatic Detection

I'll automatically detect:
- **Project name** from directory
- **Language/Framework** from package.json, requirements.txt, go.mod, etc.
- **Testing framework** based on existing test files
- **Git status** from repository

## You Only Need to Provide

1. **Project Description** (1-2 sentences)
2. **Application Specification** (features to build)

## Defaults Applied

| Setting | Default Value |
|---------|---------------|
| Max Features | 30 |
| Max Iterations | 100 |
| Model | claude-sonnet-4 |
| Testing | unit + integration |
| Execution Mode | all (terminal, background, SDK) |

---

## Quick Start

Provide your project description and application specification:

```
Quick setup:

Description: [Brief description of what you're building]

Specification:
[Detailed features, user flows, and requirements]
```

Example:

```
Quick setup:

Description: A task management API with real-time updates

Specification:
Build a REST API for task management with:
- User authentication (JWT)
- CRUD operations for tasks
- Real-time updates via WebSocket
- Task assignment and collaboration
- Due date reminders
- Task categories and tags
```
