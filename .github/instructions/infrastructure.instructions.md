---
applyTo:
  - "**/terraform/**"
  - "**/*.tf"
  - "**/*.tfvars"
  - "**/bicep/**"
  - "**/*.bicep"
  - "**/pulumi/**"
  - "**/cdk/**"
  - "**/docker/**"
  - "**/Dockerfile*"
  - "**/docker-compose*.yml"
  - "**/kubernetes/**"
  - "**/*.yaml"
  - "**/*.yml"
  - "**/helm/**"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# Infrastructure as Code Standards

## Core Principles
- Infrastructure should be version controlled
- Environments should be reproducible
- Use immutable infrastructure patterns
- Separate configuration from code
- Document all infrastructure decisions

## Terraform

### File Organization
```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── database/
│   └── compute/
└── shared/
    └── backend.tf
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Resources | lowercase with underscores | `aws_instance.web_server` |
| Variables | lowercase with underscores | `instance_count` |
| Outputs | lowercase with underscores | `vpc_id` |
| Modules | lowercase with hyphens | `networking`, `database-cluster` |
| Tags | PascalCase or consistent style | `Name`, `Environment` |

### Resource Naming
```hcl
# Use consistent tagging
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = var.owner_team
  }
}

resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-web"
    Role = "web-server"
  })
}
```

### Use Modules for Reusability
```hcl
module "vpc" {
  source = "../../modules/networking"
  
  name             = "${var.project_name}-${var.environment}"
  cidr_block       = var.vpc_cidr
  azs              = var.availability_zones
  private_subnets  = var.private_subnet_cidrs
  public_subnets   = var.public_subnet_cidrs
  
  enable_nat_gateway = var.environment == "prod"
  
  tags = local.common_tags
}
```

### Variable Definitions
```hcl
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 2
  
  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
```

### State Management
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "projects/myapp/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

## Docker

### Dockerfile Best Practices
```dockerfile
# Use specific version tags
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy dependency files first (leverage cache)
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/

# Build application
RUN npm run build

# Production stage
FROM node:20-alpine AS production

# Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy built application
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules

USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### Docker Compose
```yaml
# docker-compose.yml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Kubernetes

### Resource Organization
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app: myapp
    component: api
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      component: api
  template:
    metadata:
      labels:
        app: myapp
        component: api
        version: v1
    spec:
      containers:
        - name: api
          image: myapp/api:1.0.0
          ports:
            - containerPort: 3000
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url
```

### ConfigMaps and Secrets
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  LOG_LEVEL: "info"
  CACHE_TTL: "3600"

---
# secret.yaml (use external secret management in production)
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
type: Opaque
stringData:
  database-url: "postgres://user:pass@host:5432/db"
```

### Helm Charts
```yaml
# Chart.yaml
apiVersion: v2
name: myapp
description: My application Helm chart
version: 1.0.0
appVersion: "1.0.0"

# values.yaml
replicaCount: 3

image:
  repository: myapp/api
  tag: "1.0.0"
  pullPolicy: IfNotPresent

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

ingress:
  enabled: true
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
```

## Azure Bicep

### Module Structure
```bicep
// main.bicep
targetScope = 'subscription'

param environment string
param location string = 'eastus'

resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: 'rg-myapp-${environment}'
  location: location
  tags: {
    Environment: environment
    ManagedBy: 'bicep'
  }
}

module networking 'modules/networking.bicep' = {
  name: 'networking'
  scope: rg
  params: {
    environment: environment
    location: location
  }
}

// modules/networking.bicep
param environment string
param location string

resource vnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: 'vnet-myapp-${environment}'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
  }
}

output vnetId string = vnet.id
```

## Security

### Secrets Management
- Never commit secrets to version control
- Use secret management tools (Vault, AWS Secrets Manager, Azure Key Vault)
- Rotate secrets regularly
- Use least-privilege access

```hcl
# Reference secrets from external store
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "myapp/db-password"
}

resource "aws_db_instance" "main" {
  # ...
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

### Network Security
- Use private subnets for databases and internal services
- Implement security groups with minimal required access
- Enable VPC flow logs
- Use WAF for public-facing applications

## CI/CD for Infrastructure

### Terraform Workflow
```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
    paths:
      - 'infrastructure/**'
  push:
    branches: [main]
    paths:
      - 'infrastructure/**'

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        
      - name: Terraform Init
        run: terraform init
        
      - name: Terraform Plan
        run: terraform plan -out=tfplan
        
      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: tfplan

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - uses: actions/download-artifact@v4
        with:
          name: tfplan
      - run: terraform apply tfplan
```

## Documentation

### Document infrastructure decisions
```markdown
# Infrastructure Decision Record

## ADR-001: Use Managed Kubernetes

### Context
We need container orchestration for our microservices.

### Decision
We will use AWS EKS for managed Kubernetes.

### Consequences
- Reduced operational burden
- Higher base cost than self-managed
- Vendor lock-in for some features
```
