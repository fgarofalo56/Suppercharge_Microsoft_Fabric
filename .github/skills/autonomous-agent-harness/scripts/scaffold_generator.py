#!/usr/bin/env python3
"""
Autonomous Agent Harness - Project Scaffold Generator

Generates complete project scaffolds for autonomous coding agent workflows.
Creates directory structure, configuration files, and agent prompts.

Usage:
    python scaffold_generator.py --name "my-project" --output ./projects
    python scaffold_generator.py --config project_config.json
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class ProjectConfig:
    """Configuration for autonomous agent project."""

    def __init__(
        self,
        name: str,
        description: str = "",
        project_type: str = "web",
        language: str = "typescript",
        framework: str = "",
        database: str = "none",
        package_manager: str = "npm",
        max_features: int = 30,
        max_iterations: int = 50,
        model: str = "claude-opus-4-5-20251101",
        testing_strategy: str = "full",
        browser_testing: str = "playwright",
        archon_project_id: Optional[str] = None,
        github_repo: Optional[str] = None,
        app_spec: str = "",
    ):
        self.name = name
        self.description = description
        self.project_type = project_type
        self.language = language
        self.framework = framework
        self.database = database
        self.package_manager = package_manager
        self.max_features = max_features
        self.max_iterations = max_iterations
        self.model = model
        self.testing_strategy = testing_strategy
        self.browser_testing = browser_testing
        self.archon_project_id = archon_project_id
        self.github_repo = github_repo
        self.app_spec = app_spec

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "project_type": self.project_type,
            "language": self.language,
            "framework": self.framework,
            "database": self.database,
            "package_manager": self.package_manager,
            "max_features": self.max_features,
            "max_iterations": self.max_iterations,
            "model": self.model,
            "testing_strategy": self.testing_strategy,
            "browser_testing": self.browser_testing,
            "archon_project_id": self.archon_project_id,
            "github_repo": self.github_repo,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectConfig":
        return cls(**data)

    @classmethod
    def from_json_file(cls, path: str) -> "ProjectConfig":
        with open(path, "r") as f:
            return cls.from_dict(json.load(f))


class ScaffoldGenerator:
    """Generates project scaffold for autonomous coding agent harness."""

    def __init__(self, config: ProjectConfig, output_dir: str = "."):
        self.config = config
        self.output_dir = Path(output_dir)
        self.project_dir = self.output_dir / config.name

    def generate(self) -> Path:
        """Generate complete project scaffold."""
        print(f"Generating scaffold for: {self.config.name}")

        # Create directory structure
        self._create_directories()

        # Generate configuration files
        self._generate_archon_project_json()
        self._generate_claude_settings_json()
        self._generate_features_json()

        # Generate prompts
        self._generate_initializer_prompt()
        self._generate_coding_prompt()

        # Generate support files
        self._generate_init_script()
        self._generate_progress_file()
        self._generate_app_spec()
        self._generate_gitignore()

        print(f"Scaffold created at: {self.project_dir}")
        return self.project_dir

    def _create_directories(self):
        """Create project directory structure."""
        dirs = [
            self.project_dir,
            self.project_dir / "prompts",
            self.project_dir / "src",
            self.project_dir / "tests",
            self.project_dir / "docs",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {d}")

    def _generate_archon_project_json(self):
        """Generate .archon_project.json file."""
        data = {
            "project_id": self.config.archon_project_id or "<ARCHON_PROJECT_ID>",
            "project_name": self.config.name,
            "created_at": datetime.now().isoformat(),
            "status": "initializing",
            "config": {
                "max_features": self.config.max_features,
                "max_iterations": self.config.max_iterations,
                "model": self.config.model,
                "testing_strategy": self.config.testing_strategy,
            },
        }
        path = self.project_dir / ".archon_project.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Created: {path}")

    def _generate_claude_settings_json(self):
        """Generate .claude_settings.json file."""
        # Build allowed commands based on language/package manager
        allowed = [
            "Read",
            "Write",
            "Edit",
            "MultiEdit",
            "Glob",
            "Grep",
            "Bash(git:*)",
        ]

        pm_commands = {
            "npm": ["Bash(npm:*)", "Bash(npx:*)"],
            "yarn": ["Bash(yarn:*)"],
            "pnpm": ["Bash(pnpm:*)"],
            "pip": ["Bash(pip:*)", "Bash(pip3:*)", "Bash(python:*)", "Bash(python3:*)"],
            "poetry": ["Bash(poetry:*)", "Bash(python:*)", "Bash(python3:*)"],
            "cargo": ["Bash(cargo:*)"],
            "go": ["Bash(go:*)"],
        }
        allowed.extend(pm_commands.get(self.config.package_manager, []))

        # Add language-specific commands
        if self.config.language in ["typescript", "javascript"]:
            allowed.extend(["Bash(node:*)", "Bash(tsc:*)"])
        elif self.config.language == "python":
            allowed.extend(["Bash(pytest:*)", "Bash(mypy:*)"])

        # Build MCP servers
        mcp_servers = ["archon"]
        if self.config.browser_testing:
            mcp_servers.append(f"{self.config.browser_testing}-mcp")
        if self.config.github_repo:
            mcp_servers.append("github")

        data = {
            "permissions": {
                "allow": allowed,
                "deny": [
                    "Bash(rm -rf /*)",
                    "Bash(sudo:*)",
                    "Bash(chmod 777:*)",
                    "Bash(dd:*)",
                ],
            },
            "mcp_servers": mcp_servers,
            "model": self.config.model,
            "max_iterations": self.config.max_iterations,
            "sandbox": {
                "enabled": True,
                "filesystem_restrictions": True,
                "network_restrictions": False,
            },
        }
        path = self.project_dir / ".claude_settings.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Created: {path}")

    def _generate_features_json(self):
        """Generate features.json file."""
        data = {
            "version": "1.0",
            "total_features": 0,
            "completed": 0,
            "passing": 0,
            "failing": 0,
            "in_progress": 0,
            "features": [],
        }
        path = self.project_dir / "features.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Created: {path}")

    def _generate_initializer_prompt(self):
        """Generate initializer agent prompt."""
        content = f"""# Initializer Agent Prompt

You are initializing a new autonomous coding project: **{self.config.name}**

## Project Details
- **Description**: {self.config.description}
- **Type**: {self.config.project_type}
- **Language**: {self.config.language}
- **Framework**: {self.config.framework or "None specified"}
- **Database**: {self.config.database}

## Your Tasks

### 1. Read Application Specification
Read `app_spec.txt` thoroughly to understand what needs to be built.

### 2. Connect to Archon MCP
Verify Archon project connection:
```python
find_projects(project_id="{self.config.archon_project_id or '<PROJECT_ID>'}")
```

### 3. Create Feature Tasks
Create {self.config.max_features} detailed task issues in Archon:

```python
# For each feature:
manage_task("create",
    project_id="{self.config.archon_project_id or '<PROJECT_ID>'}",
    title="<Feature Title>",
    description=\"\"\"
## Requirements
- What needs to be built
- Technical specifications

## Acceptance Criteria
- [ ] Testable criterion 1
- [ ] Testable criterion 2

## Test Steps
1. How to verify this works
2. Expected behavior
\"\"\",
    status="todo",
    task_order=<priority>,  # 100 = highest
    feature="<Feature Group>",
    assignee="Coding Agent"
)
```

### 4. Create META Task
Create a META task for session tracking:
```python
manage_task("create",
    project_id="{self.config.archon_project_id or '<PROJECT_ID>'}",
    title="META: Session Tracking & Handoffs",
    description="Track session summaries and handoff notes. Update after each session.",
    task_order=100,
    feature="Meta",
    assignee="Coding Agent"
)
```

### 5. Initialize Project Structure
- Create appropriate src/ structure for {self.config.language}
- Set up tests/ with test framework
- Initialize documentation in docs/

### 6. Run Environment Setup
```bash
chmod +x init.sh
./init.sh
```

### 7. Update Progress
Update `claude-progress.txt` with:
- Tasks created
- Initial setup completed
- Notes for first coding session

### 8. Commit Changes
```bash
git add .
git commit -m "Initialize {self.config.name} autonomous agent project

- Created {self.config.max_features} feature tasks in Archon
- Set up project structure
- Configured development environment"
```

## Feature Task Guidelines

### Task Granularity
Each task should represent 30 minutes to 4 hours of work.

### Feature Groups (suggested)
| Group | Priority Range | Examples |
|-------|----------------|----------|
| Setup | 95-100 | Environment, dependencies |
| Database | 85-94 | Schema, models, migrations |
| Authentication | 75-84 | Login, registration, sessions |
| Core API | 55-74 | Main business endpoints |
| Frontend | 35-54 | UI components, pages |
| Integration | 25-34 | Third-party services |
| Testing | 15-24 | Test suites, coverage |
| Documentation | 5-14 | API docs, guides |

## Session Handoff

Before ending this session:
1. Update `claude-progress.txt` with initialization summary
2. Update META task in Archon with handoff notes
3. Update `.archon_project.json` status to "active"
4. Commit all changes
"""
        path = self.project_dir / "prompts" / "initializer_prompt.md"
        with open(path, "w") as f:
            f.write(content)
        print(f"  Created: {path}")

    def _generate_coding_prompt(self):
        """Generate coding agent prompt."""
        content = f"""# Coding Agent Prompt

You are continuing work on: **{self.config.name}**

## Session Startup Protocol

### 1. Verify Environment
```bash
pwd  # Should be in project directory
git status  # Check for uncommitted changes
```

### 2. Review Progress
```bash
cat claude-progress.txt  # Previous session notes
git log --oneline -10    # Recent commits
```

### 3. Query Archon for Task Status
```python
# Get all project tasks
find_tasks(filter_by="project", filter_value="{self.config.archon_project_id or '<PROJECT_ID>'}")

# Check for in-progress task
find_tasks(filter_by="status", filter_value="doing")

# Get TODO tasks
find_tasks(filter_by="status", filter_value="todo")
```

### 4. Run Health Checks
```bash
{self._get_test_command()}  # Run test suite
```
If tests fail, fix them before starting new work.

### 5. Select Task
Choose the highest-priority TODO task (highest `task_order` value).

## Work Loop

For each task:

### Step 1: Start Task
```python
manage_task("update", task_id="<TASK_ID>", status="doing")
```

### Step 2: Implement
Follow the acceptance criteria in the task description.

### Step 3: Write Tests
- Unit tests for new functions/components
- Integration tests for API endpoints
- E2E tests for user flows (using {self.config.browser_testing or 'Playwright'} MCP)

### Step 4: Run Tests
```bash
{self._get_test_command()}
```

### Step 5: Browser Testing (if UI involved)
```python
mcp__playwright__browser_navigate(url="http://localhost:3000")
mcp__playwright__browser_snapshot()
# Test interactions...
```

### Step 6: Update Task
```python
manage_task("update",
    task_id="<TASK_ID>",
    status="review",
    description="<ORIGINAL_DESC>\\n\\n---\\n## Implementation Notes\\n<YOUR_NOTES>"
)
```

### Step 7: Update Features Registry
Update `features.json` with test results.

### Step 8: Commit
```bash
git add .
git commit -m "Implement: <Feature Title>

- <Change 1>
- <Change 2>

Task: <TASK_ID>"
```

### Step 9: Next Task
Query for next TODO task and repeat.

## Testing Requirements

### Critical Rules
- Run existing tests BEFORE starting new work
- If tests fail, fix them FIRST
- NEVER remove or modify tests to make them pass artificially
- NEVER mark a feature complete without testing

### Test Commands
```bash
# Run all tests
{self._get_test_command()}

# Run specific test file
{self._get_test_command(specific=True)}
```

## Session Handoff

Before ending:

### 1. Update Progress File
```markdown
## Session: <DATE>

### Completed:
- [x] Task: <Description> (DONE)
- [ ] Task: <Description> (IN PROGRESS - X%)

### Test Results:
- Unit: X/Y passing
- Integration: X/Y passing
- E2E: X/Y passing

### Blockers:
- None / <List blockers>

### Next Steps:
1. <Priority 1>
2. <Priority 2>

### Notes:
<Important context for next session>
```

### 2. Update META Task
```python
manage_task("update",
    task_id="<META_TASK_ID>",
    description="Session <DATE>:\\n\\n<SUMMARY>"
)
```

### 3. Final Commit
```bash
git add .
git commit -m "Session end: <Brief summary>

Completed: <Tasks>
Next: <Next task>"
```

### 4. Clean State
Leave codebase in clean, runnable state with no failing tests.

## Archon Quick Reference

```python
# Get task by ID
find_tasks(task_id="uuid")

# List project tasks
find_tasks(filter_by="project", filter_value="{self.config.archon_project_id or '<PROJECT_ID>'}")

# Filter by status
find_tasks(filter_by="status", filter_value="todo")  # or doing, review, done

# Update task status
manage_task("update", task_id="uuid", status="doing")

# Add notes to task
manage_task("update", task_id="uuid", description="Updated description...")
```

## CRITICAL RULES

1. **Never declare complete prematurely** - Verify all features with E2E testing
2. **Never skip testing** - All features must have tests
3. **Never modify tests to pass** - Fix the code, not the tests
4. **Always update Archon** - Keep task status accurate
5. **Always commit incrementally** - Small, meaningful commits
6. **Always document** - Update progress file and task notes
"""
        path = self.project_dir / "prompts" / "coding_prompt.md"
        with open(path, "w") as f:
            f.write(content)
        print(f"  Created: {path}")

    def _generate_init_script(self):
        """Generate init.sh script."""
        # Build init commands based on language/framework
        init_commands = ["#!/bin/bash", "set -e", "", f'echo "Initializing {self.config.name}..."', ""]

        # Git initialization
        init_commands.extend([
            "# Initialize git if needed",
            'if [ ! -d ".git" ]; then',
            "    git init",
            '    echo "node_modules/" >> .gitignore',
            '    echo ".env" >> .gitignore',
            '    echo ".env.local" >> .gitignore',
            '    echo "__pycache__/" >> .gitignore',
            '    echo "*.pyc" >> .gitignore',
            '    echo ".venv/" >> .gitignore',
            '    echo "dist/" >> .gitignore',
            '    echo "build/" >> .gitignore',
            "fi",
            "",
        ])

        # Language-specific initialization
        if self.config.language in ["typescript", "javascript"]:
            if self.config.package_manager == "npm":
                init_commands.extend([
                    "# Initialize Node.js project",
                    'if [ ! -f "package.json" ]; then',
                    "    npm init -y",
                    "fi",
                    "",
                    "# Install dependencies",
                    "npm install",
                    "",
                ])
            elif self.config.package_manager == "yarn":
                init_commands.extend([
                    "# Initialize Node.js project",
                    'if [ ! -f "package.json" ]; then',
                    "    yarn init -y",
                    "fi",
                    "yarn install",
                    "",
                ])
        elif self.config.language == "python":
            init_commands.extend([
                "# Set up Python virtual environment",
                'if [ ! -d ".venv" ]; then',
                "    python3 -m venv .venv",
                "fi",
                "source .venv/bin/activate",
                "",
                "# Install dependencies",
                'if [ -f "requirements.txt" ]; then',
                "    pip install -r requirements.txt",
                "fi",
                "",
            ])

        init_commands.extend([
            'echo ""',
            'echo "Environment setup complete!"',
            f'echo "Project: {self.config.name}"',
            'echo "Ready for development."',
        ])

        content = "\n".join(init_commands)
        path = self.project_dir / "init.sh"
        with open(path, "w") as f:
            f.write(content)
        os.chmod(path, 0o755)  # Make executable
        print(f"  Created: {path}")

    def _generate_progress_file(self):
        """Generate initial claude-progress.txt file."""
        content = f"""# Project Progress: {self.config.name}

## Project Overview
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **Type**: {self.config.project_type}
- **Language**: {self.config.language}
- **Archon Project**: {self.config.archon_project_id or '<PENDING>'}

---

## Session: INITIALIZATION PENDING

This project is waiting for the Initializer Agent to:
1. Read app_spec.txt
2. Create feature tasks in Archon
3. Set up project structure
4. Initialize development environment

### Status: NOT STARTED

---

## Next Steps
1. Run Initializer Agent with prompts/initializer_prompt.md
2. Review created tasks in Archon
3. Begin Coding Agent sessions with prompts/coding_prompt.md
"""
        path = self.project_dir / "claude-progress.txt"
        with open(path, "w") as f:
            f.write(content)
        print(f"  Created: {path}")

    def _generate_app_spec(self):
        """Generate app_spec.txt file."""
        if self.config.app_spec:
            content = self.config.app_spec
        else:
            content = f"""# Application Specification: {self.config.name}

## Overview
{self.config.description or '<Describe your application here>'}

## Project Type
{self.config.project_type}

## Technical Stack
- **Language**: {self.config.language}
- **Framework**: {self.config.framework or 'TBD'}
- **Database**: {self.config.database}

---

## Core Features

### Feature 1: <Name>
**Description**: <What this feature does>

**User Stories**:
- As a <user type>, I want to <action> so that <benefit>

**Acceptance Criteria**:
- [ ] <Testable criterion 1>
- [ ] <Testable criterion 2>

---

### Feature 2: <Name>
**Description**: <What this feature does>

**User Stories**:
- As a <user type>, I want to <action> so that <benefit>

**Acceptance Criteria**:
- [ ] <Testable criterion 1>
- [ ] <Testable criterion 2>

---

## Data Models

### Model 1: <Name>
```
- field1: type
- field2: type
- relationship: Model2
```

---

## API Endpoints (if applicable)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/resource | List resources |
| POST | /api/resource | Create resource |
| GET | /api/resource/:id | Get resource |
| PUT | /api/resource/:id | Update resource |
| DELETE | /api/resource/:id | Delete resource |

---

## Authentication Requirements
<Describe authentication needs: none, basic, OAuth, JWT, etc.>

---

## Third-Party Integrations
<List any external services/APIs to integrate>

---

## UI/UX Requirements
<Describe interface requirements, key screens, user flows>

---

## Non-Functional Requirements
- Performance: <requirements>
- Security: <requirements>
- Scalability: <requirements>
"""
        path = self.project_dir / "app_spec.txt"
        with open(path, "w") as f:
            f.write(content)
        print(f"  Created: {path}")

    def _generate_gitignore(self):
        """Generate .gitignore file."""
        ignores = [
            "# Dependencies",
            "node_modules/",
            ".venv/",
            "venv/",
            "__pycache__/",
            "*.pyc",
            "",
            "# Build outputs",
            "dist/",
            "build/",
            "*.egg-info/",
            "",
            "# Environment",
            ".env",
            ".env.local",
            ".env.*.local",
            "",
            "# IDE",
            ".idea/",
            ".vscode/",
            "*.swp",
            "*.swo",
            "",
            "# OS",
            ".DS_Store",
            "Thumbs.db",
            "",
            "# Logs",
            "*.log",
            "logs/",
            "",
            "# Testing",
            "coverage/",
            ".coverage",
            "htmlcov/",
            ".pytest_cache/",
            "",
        ]
        content = "\n".join(ignores)
        path = self.project_dir / ".gitignore"
        with open(path, "w") as f:
            f.write(content)
        print(f"  Created: {path}")

    def _get_test_command(self, specific: bool = False) -> str:
        """Get appropriate test command for the language."""
        if self.config.language in ["typescript", "javascript"]:
            if specific:
                return "npm test -- path/to/test.spec.ts"
            return "npm test"
        elif self.config.language == "python":
            if specific:
                return "pytest tests/test_specific.py -v"
            return "pytest tests/ -v"
        elif self.config.language == "go":
            if specific:
                return "go test ./path/to/package -v"
            return "go test ./... -v"
        elif self.config.language == "rust":
            if specific:
                return "cargo test test_name -- --nocapture"
            return "cargo test"
        return "# Add test command for your language"


def main():
    parser = argparse.ArgumentParser(
        description="Generate autonomous agent harness project scaffold"
    )
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--description", help="Project description", default="")
    parser.add_argument("--output", help="Output directory", default=".")
    parser.add_argument("--config", help="JSON configuration file")
    parser.add_argument(
        "--type",
        dest="project_type",
        help="Project type",
        default="web",
        choices=["web", "api", "cli", "fullstack", "mobile-backend"],
    )
    parser.add_argument(
        "--language",
        help="Primary language",
        default="typescript",
        choices=["typescript", "javascript", "python", "go", "rust", "java"],
    )
    parser.add_argument("--framework", help="Framework to use", default="")
    parser.add_argument(
        "--database",
        help="Database",
        default="none",
        choices=["postgresql", "mysql", "mongodb", "sqlite", "supabase", "firebase", "none"],
    )
    parser.add_argument(
        "--package-manager",
        help="Package manager",
        default="npm",
        choices=["npm", "yarn", "pnpm", "pip", "poetry", "cargo", "go"],
    )
    parser.add_argument("--max-features", type=int, help="Max features", default=30)
    parser.add_argument("--max-iterations", type=int, help="Max iterations", default=50)
    parser.add_argument(
        "--model",
        help="Claude model",
        default="claude-opus-4-5-20251101",
    )
    parser.add_argument("--archon-project-id", help="Existing Archon project ID")
    parser.add_argument("--github-repo", help="GitHub repository URL")
    parser.add_argument("--app-spec-file", help="Path to app specification file")

    args = parser.parse_args()

    # Load config from file or arguments
    if args.config:
        config = ProjectConfig.from_json_file(args.config)
    else:
        if not args.name:
            parser.error("--name is required when not using --config")

        app_spec = ""
        if args.app_spec_file:
            with open(args.app_spec_file) as f:
                app_spec = f.read()

        config = ProjectConfig(
            name=args.name,
            description=args.description,
            project_type=args.project_type,
            language=args.language,
            framework=args.framework,
            database=args.database,
            package_manager=args.package_manager,
            max_features=args.max_features,
            max_iterations=args.max_iterations,
            model=args.model,
            archon_project_id=args.archon_project_id,
            github_repo=args.github_repo,
            app_spec=app_spec,
        )

    # Generate scaffold
    generator = ScaffoldGenerator(config, args.output)
    project_path = generator.generate()

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print(f"1. cd {project_path}")
    print("2. Update app_spec.txt with your application requirements")
    print("3. Create Archon project and update .archon_project.json:")
    print('   manage_project("create", title="<NAME>", description="...")')
    print("4. Run initializer agent:")
    print('   claude --prompt "$(cat prompts/initializer_prompt.md)"')
    print("5. Continue with coding agent sessions:")
    print('   claude --prompt "$(cat prompts/coding_prompt.md)"')
    print("=" * 60)


if __name__ == "__main__":
    main()
