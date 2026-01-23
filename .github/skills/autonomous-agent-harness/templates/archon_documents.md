# Archon Document Templates

Templates for storing harness data in Archon documents.

---

## Document Types Used

| Document Type | Purpose | Template |
|---------------|---------|----------|
| `spec` | Application Specification | Below |
| `guide` | Harness Configuration | Below |
| `note` | Session Notes | See session_handoff.md |
| `prp` | Feature Registry | Below |

---

## Application Specification Document

**Document Type**: `spec`
**Title**: "Application Specification"

```json
{
  "version": "1.0",
  "last_updated": "2024-01-22T10:00:00Z",
  
  "specification": {
    "overview": "Brief description of the application",
    
    "core_features": [
      {
        "name": "Feature Name",
        "description": "What this feature does",
        "priority": "high | medium | low",
        "dependencies": ["other feature names"]
      }
    ],
    
    "user_flows": [
      {
        "name": "Flow Name",
        "description": "Description of the user journey",
        "steps": [
          "Step 1",
          "Step 2",
          "Step 3"
        ]
      }
    ],
    
    "data_models": [
      {
        "name": "Entity Name",
        "fields": [
          { "name": "id", "type": "uuid", "required": true },
          { "name": "name", "type": "string", "required": true }
        ],
        "relationships": [
          { "type": "hasMany", "target": "OtherEntity" }
        ]
      }
    ],
    
    "authentication": {
      "type": "jwt | session | oauth | none",
      "providers": ["email", "google", "github"],
      "requirements": [
        "Requirement 1",
        "Requirement 2"
      ]
    },
    
    "integrations": [
      {
        "name": "Service Name",
        "type": "api | webhook | sdk",
        "purpose": "Why it's used"
      }
    ],
    
    "ui_requirements": {
      "responsive": true,
      "theme": "light | dark | system",
      "accessibility": "WCAG AA",
      "components": [
        "Component list"
      ]
    }
  },
  
  "raw_specification": "Original text specification provided by user"
}
```

### Creating in Archon

```python
manage_document("create",
    project_id=PROJECT_ID,
    title="Application Specification",
    document_type="spec",
    content={
        "version": "1.0",
        "last_updated": datetime.now().isoformat(),
        "specification": parsed_spec,
        "raw_specification": raw_user_input
    },
    tags=["harness", "spec", "requirements"]
)
```

---

## Harness Configuration Document

**Document Type**: `guide`
**Title**: "Harness Configuration"

```json
{
  "harness_version": "2.0",
  "created_at": "2024-01-22T10:00:00Z",
  "status": "initializing | active | paused | completed",
  
  "project": {
    "name": "project-name",
    "type": "web-app | api | cli | library",
    "directory": "/path/to/project"
  },
  
  "technical_stack": {
    "language": "typescript",
    "frontend_framework": "react",
    "backend_framework": "express",
    "database": "postgresql",
    "package_manager": "npm"
  },
  
  "agent_config": {
    "max_features": 30,
    "max_iterations": 100,
    "model": "claude-sonnet-4",
    "execution_modes": ["terminal", "background", "sdk"]
  },
  
  "testing": {
    "strategy": "unit | unit+integration | full-e2e | manual",
    "browser_tool": "playwright-mcp | puppeteer-mcp | none",
    "framework": "jest | pytest | go-test | cargo-test"
  },
  
  "mcp_servers": {
    "archon": {
      "required": true,
      "status": "connected"
    },
    "playwright-mcp": {
      "required": false,
      "enabled": true
    },
    "github": {
      "required": false,
      "enabled": true
    }
  },
  
  "permissions": {
    "allowed_commands": [
      "npm:*", "node:*", "git:*",
      "python:*", "pip:*", "pytest:*"
    ],
    "denied_commands": [
      "rm -rf /*", "sudo:*", "curl|wget *://"
    ],
    "filesystem_restricted": true
  }
}
```

### Creating in Archon

```python
manage_document("create",
    project_id=PROJECT_ID,
    title="Harness Configuration",
    document_type="guide",
    content={
        "harness_version": "2.0",
        "created_at": datetime.now().isoformat(),
        "status": "initializing",
        "project": project_config,
        "technical_stack": stack_config,
        "agent_config": agent_config,
        "testing": testing_config,
        "mcp_servers": mcp_config,
        "permissions": permissions_config
    },
    tags=["harness", "config"]
)
```

---

## Feature Registry Document

**Document Type**: `prp`
**Title**: "Feature Registry"

```json
{
  "version": "1.0",
  "last_updated": "2024-01-22T10:00:00Z",
  
  "summary": {
    "total_features": 30,
    "completed": 12,
    "in_progress": 1,
    "pending": 17,
    "passing": 11,
    "failing": 1
  },
  
  "features": [
    {
      "id": 1,
      "archon_task_id": "task-uuid-here",
      "name": "User Authentication",
      "description": "JWT-based user authentication",
      "feature_group": "Authentication",
      
      "status": "pending | in_progress | completed | failing",
      "priority": 85,
      
      "acceptance_criteria": [
        "Users can register with email/password",
        "Users can login and receive JWT",
        "Invalid credentials return 401"
      ],
      
      "test_steps": [
        "POST /api/auth/register with valid data",
        "Verify user in database",
        "POST /api/auth/login",
        "Verify JWT is valid"
      ],
      
      "implementation": {
        "completed_at": "2024-01-22",
        "session_number": 3,
        "files_created": [
          "src/services/auth.ts",
          "src/api/auth.ts"
        ]
      },
      
      "test_results": {
        "last_run": "2024-01-22T15:00:00Z",
        "unit": { "status": "pass", "count": 12, "passing": 12 },
        "integration": { "status": "pass", "count": 5, "passing": 5 },
        "e2e": { "status": "pass", "count": 3, "passing": 3 }
      },
      
      "dependencies": [],
      "notes": []
    }
  ]
}
```

### Creating in Archon

```python
manage_document("create",
    project_id=PROJECT_ID,
    title="Feature Registry",
    document_type="prp",
    content={
        "version": "1.0",
        "last_updated": datetime.now().isoformat(),
        "summary": {
            "total_features": 0,
            "completed": 0,
            "in_progress": 0,
            "pending": 0,
            "passing": 0,
            "failing": 0
        },
        "features": []
    },
    tags=["harness", "features", "registry"]
)
```

### Updating Feature Status

```python
# Get feature registry
registry = find_documents(
    project_id=PROJECT_ID,
    document_type="prp",
    query="Feature Registry"
)

# Find and update feature
for feature in registry["content"]["features"]:
    if feature["archon_task_id"] == completed_task_id:
        feature["status"] = "completed"
        feature["implementation"] = {
            "completed_at": datetime.now().isoformat(),
            "session_number": current_session,
            "files_created": changed_files
        }
        break

# Update summary counts
registry["content"]["summary"]["completed"] += 1
registry["content"]["summary"]["pending"] -= 1

# Save back
manage_document("update",
    project_id=PROJECT_ID,
    document_id=registry["id"],
    content=registry["content"]
)
```

---

## Document Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                      ARCHON PROJECT                              │
│                                                                  │
│   ┌─────────────┐    ┌──────────────────────────────────────┐  │
│   │   Tasks     │◄───│     Feature Registry (prp)           │  │
│   │             │    │     - Links tasks to features        │  │
│   │ • Feature 1 │    │     - Tracks test results            │  │
│   │ • Feature 2 │    └──────────────────────────────────────┘  │
│   │ • Feature 3 │                                               │
│   │ • META      │    ┌──────────────────────────────────────┐  │
│   └─────────────┘    │     App Specification (spec)          │  │
│                      │     - Source for task generation      │  │
│                      │     - Reference during implementation │  │
│   ┌─────────────┐    └──────────────────────────────────────┘  │
│   │  Documents  │                                               │
│   │             │    ┌──────────────────────────────────────┐  │
│   │ • Spec      │    │     Session Notes (note)              │  │
│   │ • Config    │    │     - Handoff between sessions       │  │
│   │ • Notes     │    │     - Context for agents             │  │
│   │ • Registry  │    └──────────────────────────────────────┘  │
│   └─────────────┘                                               │
│                      ┌──────────────────────────────────────┐  │
│                      │     Harness Configuration (guide)     │  │
│                      │     - Agent settings                  │  │
│                      │     - Testing configuration           │  │
│                      └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```
