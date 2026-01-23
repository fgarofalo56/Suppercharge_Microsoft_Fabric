# GitHub Codespaces Reference

> Complete CLI reference and API documentation for Codespaces

---

## Table of Contents

- [CLI Commands](#cli-commands)
- [DevContainer Schema](#devcontainer-schema)
- [Features Registry](#features-registry)
- [Extensions Configuration](#extensions-configuration)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)

---

## CLI Commands

### Codespace Management

#### Create Codespace

```bash
# Basic creation
gh codespace create -r owner/repo

# With specific branch
gh codespace create -r owner/repo -b feature-branch

# With machine type
gh codespace create -r owner/repo -m largePremiumLinux

# With display name
gh codespace create -r owner/repo --display-name "My Feature Work"

# With devcontainer path
gh codespace create -r owner/repo --devcontainer-path .devcontainer/backend-api/devcontainer.json

# With idle timeout
gh codespace create -r owner/repo --idle-timeout 60m

# With retention period
gh codespace create -r owner/repo --retention-period 168h
```

**Machine type options:**
- `basicLinux` - 2 cores, 8GB RAM
- `standardLinux` - 4 cores, 16GB RAM
- `premiumLinux` - 8 cores, 32GB RAM
- `largePremiumLinux` - 16 cores, 64GB RAM

#### List Codespaces

```bash
# Basic list
gh codespace list

# JSON output
gh codespace list --json name,state,repository,machinetype

# Filter by repo
gh codespace list -r owner/repo

# Include organization codespaces
gh codespace list --org my-org
```

#### View Codespace Details

```bash
# View in terminal
gh codespace view -c <codespace-name>

# Open in browser
gh codespace view -c <codespace-name> -w
```

#### Open Codespace

```bash
# Open in VS Code Desktop
gh codespace code -c <codespace-name>

# Open in VS Code Insiders
gh codespace code -c <codespace-name> --insiders

# Open in JupyterLab
gh codespace jupyter -c <codespace-name>

# Open in web editor
gh codespace view -c <codespace-name> -w
```

#### SSH Access

```bash
# Interactive SSH
gh codespace ssh -c <codespace-name>

# Run command via SSH
gh codespace ssh -c <codespace-name> -- ls -la

# Get SSH config
gh codespace ssh --config
```

#### Stop/Start Codespace

```bash
# Stop codespace
gh codespace stop -c <codespace-name>

# Codespace will auto-start on next access
gh codespace code -c <codespace-name>
```

#### Delete Codespace

```bash
# Delete specific codespace
gh codespace delete -c <codespace-name>

# Delete with confirmation skip
gh codespace delete -c <codespace-name> --force

# Delete all codespaces for repo
gh codespace delete -r owner/repo --all

# Delete codespaces older than 7 days
gh codespace list --json name,createdAt | jq -r '.[] | select(.createdAt < (now - 604800 | todate)) | .name' | xargs -I {} gh codespace delete -c {}
```

#### Edit Codespace

```bash
# Change machine type
gh codespace edit -c <codespace-name> -m largePremiumLinux

# Change display name
gh codespace edit -c <codespace-name> --display-name "New Name"
```

### Port Forwarding

```bash
# List forwarded ports
gh codespace ports -c <codespace-name>

# Forward specific port
gh codespace ports forward 3000:3000 -c <codespace-name>

# Change port visibility
gh codespace ports visibility 3000:public -c <codespace-name>
gh codespace ports visibility 3000:private -c <codespace-name>
gh codespace ports visibility 3000:org -c <codespace-name>
```

### File Operations

```bash
# Copy file to codespace
gh codespace cp ./local-file.txt remote:/workspaces/project/ -c <codespace-name>

# Copy file from codespace
gh codespace cp remote:/workspaces/project/file.txt ./local/ -c <codespace-name>

# Recursive copy
gh codespace cp -r ./local-dir remote:/workspaces/project/ -c <codespace-name>
```

### Logs and Debugging

```bash
# View creation logs
gh codespace logs -c <codespace-name>

# Follow logs
gh codespace logs -c <codespace-name> --follow
```

---

## DevContainer Schema

### Complete Schema Reference

```json
{
  // Identity
  "name": "Development Environment",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  
  // Or use Dockerfile
  "build": {
    "dockerfile": "Dockerfile",
    "context": "..",
    "args": {
      "NODE_VERSION": "20"
    }
  },
  
  // Or use Docker Compose
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspaces/${localWorkspaceFolderBasename}",
  
  // Features (modular additions)
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  
  // Lifecycle scripts
  "initializeCommand": "echo 'Starting...'",
  "onCreateCommand": "npm ci",
  "updateContentCommand": "npm run build",
  "postCreateCommand": "npm run setup",
  "postStartCommand": "npm run dev:services",
  "postAttachCommand": "echo 'Ready!'",
  
  // Environment
  "containerEnv": {
    "NODE_ENV": "development",
    "DATABASE_URL": "${localEnv:DATABASE_URL}"
  },
  "remoteEnv": {
    "PATH": "${containerEnv:PATH}:/custom/path"
  },
  
  // User configuration
  "containerUser": "vscode",
  "remoteUser": "vscode",
  "updateRemoteUserUID": true,
  
  // Mounts
  "mounts": [
    "source=${localWorkspaceFolder}/.cache,target=/home/vscode/.cache,type=bind,consistency=cached"
  ],
  
  // Ports
  "forwardPorts": [3000, 5000, 5432],
  "portsAttributes": {
    "3000": {
      "label": "Frontend",
      "onAutoForward": "openBrowser",
      "protocol": "http"
    },
    "5000": {
      "label": "API",
      "onAutoForward": "notify"
    },
    "5432": {
      "label": "PostgreSQL",
      "onAutoForward": "silent"
    }
  },
  "otherPortsAttributes": {
    "onAutoForward": "notify"
  },
  
  // VS Code customizations
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "terminal.integrated.defaultProfile.linux": "bash"
      }
    },
    "codespaces": {
      "openFiles": ["README.md", "src/index.ts"]
    }
  },
  
  // Host requirements
  "hostRequirements": {
    "cpus": 4,
    "memory": "16gb",
    "storage": "64gb",
    "gpu": "optional"
  },
  
  // Secrets
  "secrets": {
    "API_KEY": {
      "description": "API key for external service",
      "documentationUrl": "https://example.com/docs"
    }
  },
  
  // Run arguments
  "runArgs": ["--cap-add=SYS_PTRACE", "--security-opt", "seccomp=unconfined"],
  "privileged": false,
  
  // Shutdown action
  "shutdownAction": "stopContainer",
  "waitFor": "postCreateCommand"
}
```

---

## Features Registry

### Official Features

| Feature | ID | Description |
|---------|-------|-------------|
| Node.js | `ghcr.io/devcontainers/features/node:1` | Node.js and npm |
| Python | `ghcr.io/devcontainers/features/python:1` | Python and pip |
| Go | `ghcr.io/devcontainers/features/go:1` | Go language |
| Rust | `ghcr.io/devcontainers/features/rust:1` | Rust and Cargo |
| Java | `ghcr.io/devcontainers/features/java:1` | JDK and Maven |
| .NET | `ghcr.io/devcontainers/features/dotnet:1` | .NET SDK |
| Docker-in-Docker | `ghcr.io/devcontainers/features/docker-in-docker:2` | Docker inside container |
| kubectl | `ghcr.io/devcontainers/features/kubectl-helm-minikube:1` | Kubernetes tools |
| AWS CLI | `ghcr.io/devcontainers/features/aws-cli:1` | AWS command line |
| Azure CLI | `ghcr.io/devcontainers/features/azure-cli:1` | Azure command line |
| GitHub CLI | `ghcr.io/devcontainers/features/github-cli:1` | gh CLI |
| Terraform | `ghcr.io/devcontainers/features/terraform:1` | Terraform IaC |
| PostgreSQL | `ghcr.io/devcontainers-contrib/features/postgres-asdf:1` | PostgreSQL |
| Redis | `ghcr.io/devcontainers-contrib/features/redis-asdf:1` | Redis |

### Feature Configuration

```json
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20",
      "nodeGypDependencies": true,
      "nvmInstallPath": "/usr/local/share/nvm"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11",
      "installTools": true,
      "optimize": true
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "version": "latest",
      "moby": true,
      "dockerDashComposeVersion": "v2"
    }
  }
}
```

---

## Extensions Configuration

### Common Extension Sets

#### Web Development
```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint",
        "bradlc.vscode-tailwindcss",
        "formulahendry.auto-rename-tag",
        "christian-kohler.path-intellisense",
        "naumovs.color-highlight"
      ]
    }
  }
}
```

#### Python Development
```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "ms-toolsai.jupyter",
        "charliermarsh.ruff"
      ]
    }
  }
}
```

#### Backend/API Development
```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "humao.rest-client",
        "mtxr.sqltools",
        "ckolkman.vscode-postgres",
        "ms-azuretools.vscode-docker"
      ]
    }
  }
}
```

---

## Environment Variables

### Setting Methods

#### 1. In devcontainer.json
```json
{
  "containerEnv": {
    "NODE_ENV": "development",
    "LOG_LEVEL": "debug"
  }
}
```

#### 2. Repository Secrets (GitHub Settings)
```bash
gh secret set API_KEY --repo owner/repo --app codespaces
```

#### 3. User Secrets (GitHub Settings > Codespaces)
```bash
gh secret set NPM_TOKEN --user
```

#### 4. In Dockerfile
```dockerfile
ENV NODE_ENV=development
```

### Variable Precedence (highest to lowest)
1. `remoteEnv` in devcontainer.json
2. User secrets
3. Repository secrets
4. `containerEnv` in devcontainer.json
5. Dockerfile ENV

---

## API Reference

### REST API Endpoints

#### List Codespaces
```bash
gh api user/codespaces --jq '.codespaces[] | {name: .name, state: .state, repo: .repository.full_name}'
```

#### Create Codespace
```bash
gh api user/codespaces \
  -X POST \
  -f repository_id=12345 \
  -f ref="main" \
  -f machine="standardLinux"
```

#### Get Codespace
```bash
gh api user/codespaces/{codespace_name}
```

#### Start Codespace
```bash
gh api user/codespaces/{codespace_name}/start -X POST
```

#### Stop Codespace
```bash
gh api user/codespaces/{codespace_name}/stop -X POST
```

#### Delete Codespace
```bash
gh api user/codespaces/{codespace_name} -X DELETE
```

#### Export to Branch
```bash
gh api user/codespaces/{codespace_name}/exports \
  -X POST \
  -f branch="exported-changes"
```

---

## Related Resources

- [SKILL.md](./SKILL.md) - Main skill documentation
- [Codespaces Workflow Guide](../../../docs/guides/codespaces-workflow.md)
- [DevContainer Configurations](../../../.devcontainer/)
