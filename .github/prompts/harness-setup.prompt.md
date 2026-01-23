---
name: harness-setup
description: Launch the autonomous agent harness setup wizard. Creates a fully-configured project for long-running autonomous development with Archon integration.
mode: agent
agent: harness-wizard
---

# 🚀 Autonomous Agent Harness Setup

Launch the interactive wizard to set up a new autonomous coding agent harness.

## What This Creates

- **Archon Project** with tasks, documents, and session tracking
- **Feature Tasks** generated from your application specification
- **Agent Pipeline** (Initializer → Coder → Tester → Reviewer)
- **Local Configuration** for harness management

## Setup Modes

Choose your preferred setup mode:

### 1. Full Setup (Default)
Complete interactive wizard with all configuration options.

```
I want to set up a new autonomous agent harness project.
```

### 2. Quick Setup
Minimal questions, smart defaults for existing codebases.

```
Quick setup for the current directory with these defaults:
- Project name: [infer from directory]
- Language: [detect from files]  
- Testing: unit + integration
- Features: 30
```

### 3. Resume Project
Continue an existing harness project.

```
Resume the existing harness project in this directory.
```

---

## Requirements

Before starting, ensure:

- [ ] **Archon MCP** is configured and running
- [ ] **Working directory** is where you want the project
- [ ] **Application specification** is ready (you'll provide this)

---

## Start the Wizard

Tell me about your project and I'll guide you through setup!
