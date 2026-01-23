# Microsoft 365 Agents Toolkit - Complete Usage Guide

Comprehensive guide to using the Microsoft 365 Agents Toolkit skill with Claude Code for building Teams apps, declarative agents, and M365 integrations.

## Table of Contents

- [How to Invoke This Skill](#how-to-invoke-this-skill)
- [Tools Overview](#tools-overview)
- [Complete Use Cases](#complete-use-cases)
- [Workflow Examples](#workflow-examples)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Best Practices](#best-practices)

---

## How to Invoke This Skill

### Automatic Activation

Claude automatically activates this skill when you use these **trigger keywords**:

- `Teams app`, `Microsoft Teams`, `Teams bot`
- `M365 agent`, `Microsoft 365 agent`, `declarative agent`
- `Teams manifest`, `app manifest`, `API plugin`
- `Teams Toolkit`, `bot framework`, `message extension`
- `copilot extension`, `Teams extension`
- `schema`, `manifest validation`, `SDK`

### Explicit Requests

Be clear about what you're trying to build or troubleshoot:

```
✅ GOOD: "Show me the Teams app manifest schema for version 1.17"
✅ GOOD: "Get code snippets for implementing SSO in a Teams tab"
✅ GOOD: "Help me troubleshoot why my Teams bot isn't responding"
✅ GOOD: "Create a declarative agent for Microsoft 365 Copilot"

⚠️ VAGUE: "Help me with Teams"
⚠️ VAGUE: "Show me some code"
```

### Example Invocation Patterns

```bash
# Schema exploration
"Show me the complete Teams app manifest schema"
"What's in the declarative agent manifest schema version 1.4?"

# Code snippets
"Get code examples for Teams SSO authentication"
"Show me how to implement message extensions"

# Troubleshooting
"My Teams bot returns 401 errors, help me debug"
"Troubleshoot Teams tab authentication issues"

# Building from scratch
"Walk me through building a Teams message extension"
"Create a declarative agent that answers HR questions"
```

---

## Tools Overview

The skill provides 4 MCP tools for M365/Teams development:

### 1. get_schema

**Purpose**: Retrieve official manifest schemas

**Parameters**:
- `schema_name`: "App manifest" | "Declarative agent manifest" | "API plugin manifest" | "M365 agents yaml"
- `schema_version`: Specific version (e.g., "v1.17") or "latest"

**Use when**:
- Creating new manifests
- Validating existing manifests
- Understanding available properties
- Upgrading to new versions

---

### 2. get_knowledge

**Purpose**: Access comprehensive knowledge base articles

**Parameters**:
- `topic`: "Teams Toolkit" | "Declarative Agents" | "API plugins" | etc.

**Use when**:
- Learning concepts
- Understanding workflows
- Planning implementation
- Researching best practices

---

### 3. get_code_snippets

**Purpose**: Get working code examples

**Parameters**:
- `snippet_type`: "Auth" | "Graph API" | "Bot" | "Tab" | "Message extension" | etc.
- `language`: "TypeScript" | "JavaScript" | "C#" | "Python"

**Use when**:
- Implementing features
- Need working examples
- Learning syntax
- Debugging issues

---

### 4. troubleshoot

**Purpose**: Get solutions to common problems

**Parameters**:
- `issue`: Description of the problem
- `context`: "Teams app" | "Bot" | "Tab" | "API plugin" | "Manifest"

**Use when**:
- Errors occur
- Features not working
- Authentication fails
- Deployment issues

---

## Complete Use Cases

### Use Case 1: Creating a Teams Message Extension from Scratch

**Scenario**: Build a message extension that searches a knowledge base

**Step-by-step workflow**:

1. **Get the manifest schema**:
```
Request: "Show me the Teams app manifest schema latest version"

Claude retrieves schema showing:
- Required properties
- Message extension configuration
- Compose extensions structure
- Available command types
```

2. **Learn about message extensions**:
```
Request: "Get knowledge about Teams message extensions"

Claude provides:
- What message extensions are
- Types (search vs. action)
- Implementation patterns
- Best practices
```

3. **Get code examples**:
```
Request: "Get TypeScript code snippets for implementing a search message extension"

Claude returns:
- Bot handler code
- Search query handling
- Result formatting
- Adaptive card templates
```

4. **Create manifest**:
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/teams/v1.17/MicrosoftTeams.schema.json",
  "manifestVersion": "1.17",
  "id": "{{APP_ID}}",
  "version": "1.0.0",
  "developer": {
    "name": "Your Company",
    "websiteUrl": "https://example.com",
    "privacyUrl": "https://example.com/privacy",
    "termsOfUseUrl": "https://example.com/terms"
  },
  "name": {
    "short": "Knowledge Search",
    "full": "Knowledge Base Search Extension"
  },
  "description": {
    "short": "Search company knowledge base",
    "full": "Search and insert content from your company knowledge base directly in Teams conversations"
  },
  "icons": {
    "outline": "outline.png",
    "color": "color.png"
  },
  "accentColor": "#FFFFFF",
  "composeExtensions": [
    {
      "botId": "{{BOT_ID}}",
      "commands": [
        {
          "id": "searchKB",
          "type": "query",
          "title": "Search Knowledge Base",
          "description": "Search company knowledge base",
          "initialRun": false,
          "parameters": [
            {
              "name": "searchQuery",
              "title": "Search",
              "description": "Enter search terms"
            }
          ]
        }
      ]
    }
  ],
  "permissions": [
    "identity",
    "messageTeamMembers"
  ],
  "validDomains": [
    "api.example.com"
  ]
}
```

5. **Implement bot logic** (from code snippets):
```typescript
// bot.ts
import {
  TeamsActivityHandler,
  TurnContext,
  MessagingExtensionQuery,
  MessagingExtensionResponse
} from 'botbuilder';

export class SearchBot extends TeamsActivityHandler {
  async handleTeamsMessagingExtensionQuery(
    context: TurnContext,
    query: MessagingExtensionQuery
  ): Promise<MessagingExtensionResponse> {
    const searchQuery = query.parameters[0].value;

    // Search knowledge base
    const results = await this.searchKnowledgeBase(searchQuery);

    // Format results as adaptive cards
    const attachments = results.map(result => ({
      contentType: 'application/vnd.microsoft.card.adaptive',
      content: {
        type: 'AdaptiveCard',
        version: '1.4',
        body: [
          {
            type: 'TextBlock',
            text: result.title,
            weight: 'bolder',
            size: 'medium'
          },
          {
            type: 'TextBlock',
            text: result.description,
            wrap: true
          }
        ],
        actions: [
          {
            type: 'Action.OpenUrl',
            title: 'View Article',
            url: result.url
          }
        ]
      },
      preview: {
        contentType: 'application/vnd.microsoft.card.hero',
        content: {
          title: result.title,
          text: result.description
        }
      }
    }));

    return {
      composeExtension: {
        type: 'result',
        attachmentLayout: 'list',
        attachments
      }
    };
  }

  private async searchKnowledgeBase(query: string) {
    // Your search implementation
    return [];
  }
}
```

6. **Test and troubleshoot**:
```
Request: "My message extension shows no results. Help troubleshoot"

Claude provides:
- Check bot endpoint is registered
- Verify bot ID matches manifest
- Test search function directly
- Check network requests in dev tools
- Validate adaptive card schema
```

**Expected outcome**:
- Working message extension
- Proper manifest configuration
- Implemented search functionality
- Deployed to Teams

---

### Use Case 2: Building a Declarative Agent for M365 Copilot

**Scenario**: Create an HR assistant agent for Microsoft 365 Copilot

**Step-by-step workflow**:

1. **Get declarative agent schema**:
```
Request: "Show me the declarative agent manifest schema version 1.4"

Claude returns complete schema with:
- Required fields (name, description, instructions)
- Capabilities configuration
- Conversation starters
- Actions and API plugins
```

2. **Learn about declarative agents**:
```
Request: "Get knowledge about M365 declarative agents"

Claude explains:
- What declarative agents are
- How they extend Copilot
- Capabilities and limitations
- Best practices for instructions
```

3. **Create declarative agent manifest**:
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.4/schema.json",
  "version": "v1.4",
  "name": "HR Assistant",
  "description": "Get help with HR policies, benefits, and time-off requests",
  "instructions": "You are an HR assistant that helps employees with:\n- Company policies and procedures\n- Benefits information\n- Time-off request processes\n- Contact information for HR team\n\nAlways maintain a helpful and professional tone. If you don't have specific information, direct users to contact HR directly at hr@company.com.",
  "conversation_starters": [
    {
      "title": "Time Off",
      "text": "How do I request time off?"
    },
    {
      "title": "Benefits",
      "text": "What health insurance options are available?"
    },
    {
      "title": "Policies",
      "text": "What's the remote work policy?"
    }
  ],
  "capabilities": {
    "web_search": {
      "enabled": false
    },
    "actions": [
      {
        "id": "getPolicyAction",
        "file": "hr-policies-plugin.json"
      }
    ]
  }
}
```

4. **Create API plugin for HR data** (if needed):
```
Request: "Show me the API plugin manifest schema"

Claude returns schema for connecting to HR APIs
```

**API Plugin example**:
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/copilot/plugin/v2.3/schema.json",
  "schema_version": "v2.3",
  "name": "HR Policies",
  "description": "Access company HR policies and information",
  "api": {
    "type": "openapi",
    "url": "https://api.company.com/hr/openapi.json",
    "auth": {
      "type": "oauth",
      "client_id": "{{CLIENT_ID}}",
      "authorization_url": "https://login.company.com/oauth/authorize",
      "token_url": "https://api.company.com/oauth/token",
      "scope": "hr.read"
    }
  },
  "functions": [
    {
      "name": "getPolicy",
      "description": "Retrieve company policy by category",
      "parameters": {
        "type": "object",
        "properties": {
          "category": {
            "type": "string",
            "description": "Policy category (benefits, timeoff, remote, etc.)"
          }
        },
        "required": ["category"]
      }
    }
  ]
}
```

5. **Deploy and test**:
```
Request: "How do I deploy a declarative agent to M365?"

Claude provides deployment steps:
1. Package manifest and plugin files
2. Upload to Teams admin center
3. Assign to users/groups
4. Test in Copilot
```

**Expected outcome**:
- Deployed HR assistant agent
- Working in M365 Copilot
- Can answer HR questions
- Integrated with HR APIs

---

### Use Case 3: Implementing SSO Authentication in Teams Tab

**Scenario**: Add single sign-on to a Teams personal tab app

**Step-by-step workflow**:

1. **Get Teams manifest schema**:
```
Request: "Show me Teams app manifest schema focusing on authentication"

Claude highlights auth-related properties:
- webApplicationInfo section
- resource URLs
- validDomains
```

2. **Get SSO knowledge**:
```
Request: "Get knowledge about Teams SSO authentication"

Claude explains:
- How Teams SSO works
- OAuth flow
- Token exchange
- Azure AD configuration
```

3. **Get code snippets**:
```
Request: "Get TypeScript code snippets for Teams tab SSO"

Claude provides complete implementation:
```

**Manifest configuration**:
```json
{
  "webApplicationInfo": {
    "id": "{{CLIENT_ID}}",
    "resource": "api://{{TAB_DOMAIN}}/{{CLIENT_ID}}"
  },
  "validDomains": [
    "{{TAB_DOMAIN}}",
    "token.botframework.com"
  ]
}
```

**Client-side code**:
```typescript
// auth.ts
import * as microsoftTeams from '@microsoft/teams-js';

export async function getAuthToken(): Promise<string> {
  return new Promise((resolve, reject) => {
    microsoftTeams.authentication.getAuthToken({
      successCallback: (token) => resolve(token),
      failureCallback: (error) => reject(error)
    });
  });
}

export async function getUserProfile() {
  try {
    const token = await getAuthToken();

    // Exchange for Graph token if needed
    const graphToken = await exchangeTokenForGraph(token);

    // Call Graph API
    const response = await fetch('https://graph.microsoft.com/v1.0/me', {
      headers: {
        'Authorization': `Bearer ${graphToken}`
      }
    });

    return await response.json();
  } catch (error) {
    console.error('Auth error:', error);
    throw error;
  }
}

async function exchangeTokenForGraph(token: string): Promise<string> {
  const response = await fetch('/api/auth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ token })
  });

  const data = await response.json();
  return data.access_token;
}
```

**Server-side token exchange**:
```typescript
// api/auth/token.ts
import { ConfidentialClientApplication } from '@azure/msal-node';

const msalClient = new ConfidentialClientApplication({
  auth: {
    clientId: process.env.CLIENT_ID!,
    clientSecret: process.env.CLIENT_SECRET!,
    authority: `https://login.microsoftonline.com/${process.env.TENANT_ID}`
  }
});

export async function exchangeToken(teamsToken: string): Promise<string> {
  const result = await msalClient.acquireTokenOnBehalfOf({
    oboAssertion: teamsToken,
    scopes: ['https://graph.microsoft.com/.default']
  });

  return result.accessToken;
}
```

4. **Troubleshoot if issues**:
```
Request: "Getting 401 error when calling Graph API, help troubleshoot"

Claude provides:
- Check Azure AD app registration
- Verify API permissions granted
- Ensure admin consent given
- Test token with jwt.ms
- Check resource URL matches
```

**Expected outcome**:
- SSO working in Teams tab
- Users automatically signed in
- Can call Graph API with user context
- No separate login required

---

### Use Case 4: Creating a Teams Bot with Adaptive Cards

**Scenario**: Build a bot that sends interactive adaptive cards

**Step-by-step workflow**:

1. **Get bot knowledge**:
```
Request: "Get knowledge about Teams bots and adaptive cards"

Claude explains:
- Bot Framework basics
- Adaptive card structure
- User interactions
- Action handling
```

2. **Get code snippets**:
```
Request: "Get TypeScript code for Teams bot with adaptive cards"

Claude provides bot implementation:
```

```typescript
// bot.ts
import {
  TeamsActivityHandler,
  TurnContext,
  CardFactory,
  MessageFactory
} from 'botbuilder';

export class TaskBot extends TeamsActivityHandler {
  constructor() {
    super();

    this.onMessage(async (context, next) => {
      const text = context.activity.text.toLowerCase();

      if (text.includes('create task')) {
        await this.sendTaskCard(context);
      } else if (text.includes('help')) {
        await context.sendActivity('I can help you create tasks. Just say "create task"');
      }

      await next();
    });

    this.onMembersAdded(async (context, next) => {
      const welcomeText = 'Welcome! I\'m your task management bot. Say "create task" to get started.';
      for (const member of context.activity.membersAdded) {
        if (member.id !== context.activity.recipient.id) {
          await context.sendActivity(MessageFactory.text(welcomeText));
        }
      }
      await next();
    });
  }

  private async sendTaskCard(context: TurnContext) {
    const card = {
      type: 'AdaptiveCard',
      version: '1.4',
      body: [
        {
          type: 'TextBlock',
          text: 'Create New Task',
          size: 'large',
          weight: 'bolder'
        },
        {
          type: 'Input.Text',
          id: 'taskTitle',
          placeholder: 'Task title',
          isRequired: true,
          errorMessage: 'Title is required'
        },
        {
          type: 'Input.Text',
          id: 'taskDescription',
          placeholder: 'Description',
          isMultiline: true
        },
        {
          type: 'Input.ChoiceSet',
          id: 'priority',
          label: 'Priority',
          choices: [
            { title: 'High', value: 'high' },
            { title: 'Medium', value: 'medium' },
            { title: 'Low', value: 'low' }
          ],
          value: 'medium'
        },
        {
          type: 'Input.Date',
          id: 'dueDate',
          label: 'Due Date'
        }
      ],
      actions: [
        {
          type: 'Action.Submit',
          title: 'Create Task',
          data: {
            action: 'createTask'
          }
        },
        {
          type: 'Action.Submit',
          title: 'Cancel',
          data: {
            action: 'cancel'
          }
        }
      ]
    };

    await context.sendActivity({
      attachments: [CardFactory.adaptiveCard(card)]
    });
  }

  async onAdaptiveCardInvoke(context: TurnContext) {
    const action = context.activity.value.action;
    const data = context.activity.value.data;

    if (action === 'createTask') {
      // Create task with data
      const task = {
        title: data.taskTitle,
        description: data.taskDescription,
        priority: data.priority,
        dueDate: data.dueDate
      };

      // Save task (your implementation)
      await this.saveTask(task);

      // Send confirmation
      const confirmCard = {
        type: 'AdaptiveCard',
        version: '1.4',
        body: [
          {
            type: 'TextBlock',
            text: '✅ Task Created',
            size: 'large',
            weight: 'bolder',
            color: 'good'
          },
          {
            type: 'FactSet',
            facts: [
              { title: 'Title', value: task.title },
              { title: 'Priority', value: task.priority },
              { title: 'Due Date', value: task.dueDate || 'Not set' }
            ]
          }
        ]
      };

      return {
        statusCode: 200,
        type: 'application/vnd.microsoft.card.adaptive',
        value: confirmCard
      };
    }

    return { statusCode: 200 };
  }

  private async saveTask(task: any) {
    // Your implementation
  }
}
```

3. **Update manifest for bot**:
```json
{
  "bots": [
    {
      "botId": "{{BOT_ID}}",
      "scopes": ["personal", "team", "groupchat"],
      "supportsFiles": false,
      "isNotificationOnly": false,
      "supportsCalling": false,
      "supportsVideo": false
    }
  ]
}
```

**Expected outcome**:
- Interactive bot in Teams
- Sends adaptive cards
- Handles user input
- Creates tasks from card data

---

## Workflow Examples

### Workflow 1: Complete Teams App Development

```
1. "Show me the latest Teams app manifest schema"
   → Understand structure

2. "Get knowledge about Teams Toolkit"
   → Learn development workflow

3. "Get TypeScript code snippets for Teams tab with Graph API"
   → Implement features

4. "Troubleshoot: My tab shows blank page in Teams"
   → Debug issues

5. Deploy and test
```

---

### Workflow 2: Upgrading Manifest Version

```
1. "Show me Teams app manifest schema v1.17"
   → Review new features

2. "Get knowledge about Teams manifest version changes"
   → Understand breaking changes

3. Update manifest with new properties

4. "Troubleshoot: Manifest validation fails after upgrade"
   → Fix issues
```

---

### Workflow 3: Adding Graph API Integration

```
1. "Get code snippets for Microsoft Graph authentication in Teams"
   → Auth implementation

2. "Get TypeScript code for calling Graph API"
   → API calls

3. "Troubleshoot: Graph API returns 403 forbidden"
   → Permission issues

4. Update Azure AD app permissions
```

---

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: "Manifest validation failed"

**Request**: `"Troubleshoot Teams manifest validation errors"`

**Claude will check**:
- Schema version compatibility
- Required fields present
- Valid URLs and domains
- Correct property types
- Icon file requirements

**Common fixes**:
- Ensure `manifestVersion` matches schema
- Check all URLs are HTTPS
- Verify icon files exist and are correct size
- Validate JSON syntax

---

#### Issue: "Bot not responding in Teams"

**Request**: `"My Teams bot doesn't respond to messages, help debug"`

**Claude will troubleshoot**:
- Bot endpoint registered correctly
- Bot ID matches manifest
- Messaging endpoint accessible
- Bot authentication configured
- Handler methods implemented

**Common fixes**:
- Check Azure Bot Service configuration
- Verify endpoint URL is public
- Test endpoint with Bot Framework Emulator
- Check bot is added to conversation

---

#### Issue: "SSO authentication fails"

**Request**: `"Teams tab SSO returns 401 error, help troubleshoot"`

**Claude will check**:
- Azure AD app registration
- API permissions configured
- Admin consent granted
- Resource URL correct
- Token exchange implementation

**Common fixes**:
- Grant admin consent for API permissions
- Verify resource URL matches: `api://{{domain}}/{{clientId}}`
- Check Azure AD app has correct redirect URIs
- Test token at jwt.ms to verify claims

---

#### Issue: "Message extension shows no results"

**Request**: `"Message extension search returns empty, troubleshoot"`

**Claude will verify**:
- Query handler implementation
- Results formatting correct
- Bot endpoint accessible
- Command parameters match manifest
- Adaptive card schema valid

**Common fixes**:
- Add logging to query handler
- Test search function independently
- Validate adaptive card JSON
- Check bot ID in manifest

---

## Best Practices

### 1. Manifest Management

```
✅ GOOD:
- Use latest schema version
- Include all required fields
- Provide clear descriptions
- Use valid domains
- Keep icons optimized

❌ BAD:
- Missing schema version
- Empty descriptions
- HTTP URLs (must be HTTPS)
- Large icon files
```

---

### 2. Authentication

```
✅ GOOD:
- Use SSO when possible
- Implement token caching
- Handle token refresh
- Validate tokens server-side
- Use least privilege scopes

❌ BAD:
- Storing tokens in localStorage
- Not handling token expiration
- Requesting unnecessary permissions
- Exposing client secrets
```

---

### 3. Bot Development

```
✅ GOOD:
- Handle all message types
- Provide help commands
- Use adaptive cards for rich UI
- Implement proactive messaging carefully
- Log errors for debugging

❌ BAD:
- Only handling text messages
- No error handling
- Spamming users with notifications
- Not testing in different contexts (1:1, group, channel)
```

---

### 4. Code Organization

```
✅ GOOD:
project/
├── src/
│   ├── bot/
│   │   ├── bot.ts
│   │   └── cards/
│   ├── tabs/
│   │   ├── auth.ts
│   │   └── api.ts
│   └── manifest/
│       └── manifest.json
└── tests/

❌ BAD:
- All code in one file
- No separation of concerns
- Hardcoded values
- No tests
```

---

### 5. Testing

```
✅ GOOD:
- Test in Teams desktop and web
- Test all user contexts (1:1, group, channel)
- Test with different permissions
- Test error scenarios
- Use Bot Framework Emulator for bots

❌ BAD:
- Only testing in web
- Not testing error cases
- Skipping validation
- No local testing
```

---

## Additional Resources

- [SKILL.md](SKILL.md) - Main skill instructions
- [reference.md](reference.md) - Complete API reference
- [Microsoft Teams Developer Documentation](https://learn.microsoft.com/microsoftteams/platform/)
- [Teams Toolkit](https://learn.microsoft.com/microsoftteams/platform/toolkit/teams-toolkit-fundamentals)
- [Declarative Agents](https://learn.microsoft.com/microsoft-365-copilot/extensibility/overview-declarative-agent)

---

## Quick Reference

### Common Commands

```bash
# Get schema
"Show me Teams app manifest schema latest"
"Get declarative agent schema v1.4"
"Show API plugin manifest schema"

# Get code
"Get TypeScript code for Teams SSO"
"Get bot code with adaptive cards"
"Get message extension implementation"

# Troubleshoot
"Troubleshoot Teams manifest validation"
"Debug bot not responding"
"Fix SSO authentication error"

# Learn
"Get knowledge about Teams Toolkit"
"Learn about declarative agents"
"Understand API plugins"
```

---

## Questions?

**Q: Which schema version should I use?**
A: Always use the latest version unless you need to support older Teams clients. Check the schema for deprecations.

**Q: How do I test locally?**
A: Use ngrok or similar to expose localhost, then configure in Azure Bot Service or Teams Toolkit.

**Q: Can declarative agents call external APIs?**
A: Yes, via API plugins. Create an OpenAPI spec and reference it in the declarative agent manifest.

**Q: How do I deploy to production?**
A: Package your app, upload to Teams admin center or Partner Center, and submit for approval if distributing publicly.

**Q: Where do I get CLIENT_ID and other values?**
A: Register your app in Azure AD (for Teams apps) or Teams Developer Portal, which generates these values.
