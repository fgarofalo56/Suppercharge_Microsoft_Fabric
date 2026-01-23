---
mode: agent
description: Configure a devcontainer.json for optimal Codespaces experience
tools: []
---

# Configure Codespace

Create or update a devcontainer.json configuration for GitHub Codespaces.

## Context

You are helping the user configure a devcontainer.json file for their project. This configuration defines the development environment in GitHub Codespaces.

## Instructions

1. **Understand Requirements**:
   - What languages/frameworks are used?
   - What database/services are needed?
   - Any specific VS Code extensions required?
   - Any special tools or CLIs needed?

2. **Generate Configuration**:
   Create a complete devcontainer.json with:
   - Appropriate base image
   - Required features
   - VS Code extensions
   - Port forwarding
   - Lifecycle scripts

3. **Explain Key Sections**:
   Briefly explain important configuration choices.

## Configuration Template

```json
{
  "name": "[Project Name]",
  "image": "[base-image]",
  
  "features": {
    // Language runtimes, tools, services
  },
  
  "customizations": {
    "vscode": {
      "extensions": [/* Required extensions */],
      "settings": {/* Editor settings */}
    }
  },
  
  "forwardPorts": [/* Exposed ports */],
  "portsAttributes": {/* Port labels and behaviors */},
  
  "postCreateCommand": "/* Initial setup */",
  
  "hostRequirements": {
    "cpus": 4,
    "memory": "16gb"
  }
}
```

## Example

**User Input**: "Configure a devcontainer for a Python FastAPI project with PostgreSQL"

**Response**:

### devcontainer.json for FastAPI + PostgreSQL

```json
{
  "name": "FastAPI Development",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11",
      "installTools": true
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "humao.rest-client",
        "mtxr.sqltools",
        "mtxr.sqltools-driver-pg"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "[python]": {
          "editor.defaultFormatter": "ms-python.black-formatter",
          "editor.tabSize": 4
        },
        "python.analysis.typeCheckingMode": "basic"
      }
    }
  },
  
  "forwardPorts": [8000, 5432],
  "portsAttributes": {
    "8000": {
      "label": "FastAPI",
      "onAutoForward": "openBrowser"
    },
    "5432": {
      "label": "PostgreSQL",
      "onAutoForward": "silent"
    }
  },
  
  "postCreateCommand": "pip install -r requirements.txt && docker-compose up -d postgres",
  
  "containerEnv": {
    "DATABASE_URL": "postgresql://postgres:postgres@localhost:5432/appdb"
  },
  
  "hostRequirements": {
    "cpus": 4,
    "memory": "16gb"
  }
}
```

### Key Configuration Choices:

1. **Python 3.11 image**: Latest stable Python with dev tools
2. **Docker-in-Docker**: For running PostgreSQL in a container
3. **Black + Ruff**: Modern Python formatting and linting
4. **SQLTools**: Database management in VS Code
5. **Port 8000**: FastAPI default, opens browser automatically

### Required docker-compose.yml:

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
```

### Usage:
1. Place `devcontainer.json` in `.devcontainer/` folder
2. Add `docker-compose.yml` to project root
3. Create Codespace: `gh codespace create -r owner/repo`
4. Run API: `uvicorn main:app --reload`

Would you like me to add any additional configuration?

## User Request

{{{ input }}}
