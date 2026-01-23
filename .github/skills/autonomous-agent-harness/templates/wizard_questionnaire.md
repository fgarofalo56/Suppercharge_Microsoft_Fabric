# Wizard Questionnaire Template

Use this questionnaire to gather all required information for harness setup.

---

## 📋 PHASE 1: PROJECT BASICS

### 1. Project Name
What should the project be called?
- Example: "saas-dashboard", "e-commerce-api", "task-manager"
- Requirements: lowercase, hyphens allowed, no spaces

**Your answer:** _______________

### 2. Project Description
Brief description of what you're building (1-3 sentences)

**Your answer:** _______________

### 3. Project Type
Select one:
- [ ] Web Application (Frontend + Backend)
- [ ] API/Backend Only
- [ ] CLI Application
- [ ] Full-Stack with Database
- [ ] Library/Package
- [ ] Mobile App Backend
- [ ] Other: _______________

### 4. Working Directory
Where should the project be created?
- Default: Current directory
- Or specify path: _______________

### 5. GitHub Repository
- [ ] Create new repository
- [ ] Use existing: (URL) _______________
- [ ] No GitHub integration

---

## 🔧 PHASE 2: TECHNICAL STACK

### 6. Primary Language
Select one:
- [ ] TypeScript/JavaScript
- [ ] Python
- [ ] Go
- [ ] Rust
- [ ] Java
- [ ] C#/.NET
- [ ] Other: _______________

### 7. Framework
**Frontend:** (if applicable)
- [ ] React
- [ ] Vue
- [ ] Svelte
- [ ] Next.js
- [ ] Angular
- [ ] None
- [ ] Other: _______________

**Backend:** (if applicable)
- [ ] Express
- [ ] FastAPI
- [ ] Gin
- [ ] Actix
- [ ] Spring
- [ ] ASP.NET
- [ ] None
- [ ] Other: _______________

### 8. Database
Select one:
- [ ] PostgreSQL
- [ ] MySQL/MariaDB
- [ ] MongoDB
- [ ] SQLite
- [ ] Supabase
- [ ] Firebase
- [ ] None/TBD
- [ ] Other: _______________

### 9. Package Manager
Select one:
- [ ] npm
- [ ] yarn
- [ ] pnpm
- [ ] pip/poetry
- [ ] go mod
- [ ] cargo
- [ ] nuget
- [ ] Other: _______________

---

## 🤖 PHASE 3: AGENT CONFIGURATION

### 10. Target Feature Count
How many features should be generated from the spec?
- Recommended: 20-50
- Default: 30

**Your answer:** _______ (number)

### 11. Session Iteration Limit
Max tool calls per coding session? (0 = unlimited)
- Default: 100

**Your answer:** _______ (number)

### 12. Claude Model Preference
Select one:
- [ ] claude-sonnet-4 (Recommended - good balance)
- [ ] claude-opus-4-5 (Complex reasoning, premium)
- [ ] claude-haiku-4.5 (Quick iterations, faster)

### 13. Execution Mode
How will you run the harness?
- [ ] Terminal only (manual prompt execution)
- [ ] Background agents (use & prefix)
- [ ] SDK (Python automation)
- [ ] All modes supported (Recommended)

---

## 🧪 PHASE 4: TESTING STRATEGY

### 14. Testing Requirements
Select one:
- [ ] Unit tests only
- [ ] Unit + Integration tests
- [ ] Full E2E with browser automation
- [ ] Manual testing only (no automation)

### 15. Browser Testing Tool
(If E2E selected)
- [ ] Playwright MCP (Recommended)
- [ ] Puppeteer MCP
- [ ] No browser testing

### 16. Test Framework
Based on language, confirm framework:
- [ ] Jest/Vitest (JS/TS)
- [ ] pytest (Python)
- [ ] go test (Go)
- [ ] cargo test (Rust)
- [ ] xUnit/NUnit (C#)
- [ ] Other: _______________

---

## 📋 PHASE 5: APPLICATION SPECIFICATION

### 17. Application Specification

Provide a detailed description of the application to build. Include:

**Core Features:**
- What are the main capabilities?
- What does the application do?

**User Flows:**
- How do users interact with the system?
- What are the key workflows?

**Data Models:**
- What entities exist?
- How are they related?

**Authentication/Authorization:**
- Is auth required?
- What type? (JWT, sessions, OAuth)

**Third-Party Integrations:**
- Any external services?
- APIs to integrate with?

**UI/UX Requirements:**
- Design requirements?
- Responsive? Theme? Accessibility?

---

**Write your specification below:**

```
[Your detailed application specification here]
```

---

## ✅ REVIEW & CONFIRM

Before proceeding, confirm:

| Setting | Value |
|---------|-------|
| Project Name | |
| Language | |
| Framework | |
| Database | |
| Features | |
| Testing | |
| Model | |

Ready to create the harness? Confirm to proceed.
