# Microsoft 365 Agents Toolkit Reference

Comprehensive reference for the Microsoft 365 Agents Toolkit MCP tools.

## MCP Tool Specifications

### get_schema

**Full Name:** `get_schema`

**Description:** Retrieve JSON schemas for Microsoft 365 manifests and configuration files.

**Parameters:**

```typescript
{
  schema_name: SchemaTypeEnum;  // Required
  schema_version: string;       // Required
}
```

**SchemaTypeEnum Values:**
- `"App manifest"` - Teams app manifest schema
- `"Declarative agent manifest"` - Copilot declarative agent schema
- `"API plugin manifest"` - API plugin manifest schema
- `"M365 agents yaml"` - Teams Toolkit YAML configuration schema

**Version Format:**
- Semantic versioning: `"v1.4"`, `"v2.3"`, etc.
- Latest version: `"latest"`

**Schema URLs:**
- App manifest: `https://developer.microsoft.com/json-schemas/teams/{version}/MicrosoftTeams.schema.json`
- Declarative agent: `https://developer.microsoft.com/json-schemas/copilot/declarative-agent/{version}/schema.json`
- API plugin: `https://developer.microsoft.com/json-schemas/copilot/plugin/{version}/schema.json`
- M365 agents yaml: `https://developer.microsoft.com/json-schemas/teams-toolkit/teamsapp-yaml/{version}/yaml.schema.json`

**Current Versions:**
- App manifest: v1.23
- Declarative agent manifest: v1.4
- API plugin manifest: v2.3
- M365 agents yaml: v1.9

**Returns:** JSON schema object with structure definitions, required fields, and validation rules.

**Example Usage:**
```json
{
  "schema_name": "App manifest",
  "schema_version": "latest"
}
```

---

### get_knowledge

**Full Name:** `get_knowledge`

**Description:** Search Microsoft 365 and Copilot development documentation.

**Parameters:**

```typescript
{
  question: string;  // Required
}
```

**Question Parameter:**
- Natural language query
- Can be question or keyword search
- Supports concepts, how-tos, and best practices
- Max recommended length: 500 characters

**Knowledge Base Coverage:**
- Microsoft 365 platform concepts
- Teams app development
- Copilot extension development
- Declarative agents
- Message extensions
- Bot development
- Authentication (SSO, OAuth)
- Microsoft Graph API
- Adaptive Cards
- Deployment and distribution

**Returns:** Relevant documentation excerpts, explanations, and guidance.

**Example Queries:**
```
"What is a declarative agent?"
"How to implement SSO in Teams tabs?"
"Best practices for bot conversation design"
"Microsoft Graph API authentication"
"Adaptive Card design guidelines"
```

---

### get_code_snippets

**Full Name:** `get_code_snippets`

**Description:** Access implementation templates and SDK code examples.

**Parameters:**

```typescript
{
  question: string;  // Required
}
```

**Question Parameter:**
- Describe desired functionality or SDK usage
- Can include SDK name for targeted results
- Mention specific features or patterns

**SDK Coverage:**
- **@microsoft/teams-ai** v1.x
- **@microsoft/teams-js** v2.x
- **botbuilder** v4.x
- Related Microsoft SDKs

**Code Categories:**
- Bot initialization and configuration
- Tab application setup
- Message extension implementation
- Authentication flows (SSO)
- Adaptive Card templates
- AI action handlers
- Conversation management
- Graph API integration

**Returns:** Code snippets with explanations, import statements, and usage notes.

**Example Queries:**
```
"Teams AI bot basic setup"
"SSO authentication in Teams tab"
"Bot Builder dialog waterfall example"
"Message extension with search command"
"Adaptive Card with submit action"
```

---

### troubleshoot

**Full Name:** `troubleshoot`

**Description:** Get solutions for common Microsoft 365 development issues.

**Parameters:**

```typescript
{
  question: string;  // Required
}
```

**Question Parameter:**
- Description of the problem
- Error messages (include full text)
- Context of when error occurs
- Components involved

**Issue Categories:**
- Manifest validation errors
- Authentication failures
- Bot/tab loading issues
- Message extension problems
- Deployment errors
- Teams Toolkit issues
- Azure configuration
- Graph API errors
- SDK version conflicts
- Runtime errors

**Returns:** Troubleshooting steps, common causes, and solutions.

**Example Queries:**
```
"Manifest validation error: invalid bot ID"
"Bot returns 401 Unauthorized"
"Teams tab fails to load with CORS error"
"Cannot sideload app in Teams"
"Graph API permission denied"
```

---

## Manifest Schemas Deep Dive

### App Manifest Schema

**File:** `manifest.json`

**Purpose:** Defines Teams app package structure and capabilities.

**Root Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| $schema | string | Yes | Schema URL for validation |
| manifestVersion | string | Yes | Manifest format version |
| id | string (GUID) | Yes | Unique app identifier |
| version | string | Yes | App version (semver) |
| packageName | string | Yes | Reverse domain identifier |
| developer | object | Yes | Developer information |
| name | object | Yes | App display names |
| description | object | Yes | App descriptions |
| icons | object | Yes | App icon URLs |
| accentColor | string | Yes | Theme hex color |

**Capability Properties:**

| Property | Type | Description |
|----------|------|-------------|
| bots | array | Bot configurations |
| composeExtensions | array | Message extensions |
| staticTabs | array | Static tab definitions |
| configurableTabs | array | Configurable tabs |
| connectors | array | Office 365 connectors |
| permissions | array | Required permissions |
| validDomains | array | Allowed domains |
| webApplicationInfo | object | AAD app details (for SSO) |

**Bot Configuration:**
```json
{
  "botId": "{{BOT_ID}}",
  "scopes": ["personal", "team", "groupchat"],
  "supportsFiles": false,
  "isNotificationOnly": false,
  "commandLists": [
    {
      "scopes": ["personal"],
      "commands": [
        {
          "title": "Command",
          "description": "Description"
        }
      ]
    }
  ]
}
```

---

### Declarative Agent Manifest Schema

**File:** `declarativeAgent.json`

**Purpose:** Configure Copilot declarative agents.

**Root Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| $schema | string | Yes | Schema URL |
| id | string | Yes | Unique agent ID |
| version | string | Yes | Agent version |
| name | string | Yes | Agent name |
| description | string | Yes | Agent purpose |
| instructions | string | Yes | System prompt |

**Advanced Properties:**

| Property | Type | Description |
|----------|------|-------------|
| conversation_starters | array | Suggested prompts |
| actions | array | API actions |
| capabilities | object | Agent capabilities |

**Instructions Field:**
- Defines agent behavior and personality
- Sets scope and limitations
- Provides context and expertise areas
- Max length: 8000 characters

**Conversation Starters:**
```json
{
  "conversation_starters": [
    {
      "title": "Starter Title",
      "text": "Suggested prompt text"
    }
  ]
}
```

**Actions:**
```json
{
  "actions": [
    {
      "id": "action-id",
      "file": "./plugin-manifest.json"
    }
  ]
}
```

---

### API Plugin Manifest Schema

**File:** `apiPlugin.json`

**Purpose:** Define API plugins for Copilot.

**Root Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| $schema | string | Yes | Schema URL |
| schema_version | string | Yes | Schema version |
| name_for_human | string | Yes | Display name |
| name_for_model | string | Yes | Model identifier |
| description_for_human | string | Yes | User description |
| description_for_model | string | Yes | Model instruction |
| api | object | Yes | API specification |
| auth | object | Yes | Authentication config |

**API Property:**
```json
{
  "api": {
    "type": "openapi",
    "url": "./openapi.json"
  }
}
```

**Auth Property:**
```json
{
  "auth": {
    "type": "none" | "api_key" | "oauth"
  }
}
```

---

### M365 Agents YAML Schema

**File:** `teamsapp.yml` or `teamsapp.local.yml`

**Purpose:** Teams Toolkit project configuration.

**Root Properties:**

| Property | Type | Description |
|----------|------|-------------|
| version | string | YAML schema version |
| environmentFolderPath | string | Path to env configs |
| provision | array | Provisioning actions |
| deploy | array | Deployment actions |
| publish | array | Publishing actions |
| projectId | string | Unique project ID |

**Action Types:**

| Action | Purpose |
|--------|---------|
| `aadApp/create` | Create AAD app |
| `teamsApp/create` | Create Teams app |
| `botAadApp/create` | Create bot AAD app |
| `botFramework/create` | Register bot |
| `arm/deploy` | Deploy to Azure |
| `azureStorage/enableStaticWebsite` | Enable static hosting |
| `file/createOrUpdateJsonFile` | Update config files |
| `script` | Run custom scripts |

---

## SDK Integration Examples

### Teams AI SDK

**Package:** `@microsoft/teams-ai`

**Installation:**
```bash
npm install @microsoft/teams-ai
```

**Basic Bot Setup:**
```typescript
import { Application, ActionPlanner, OpenAIModel } from '@microsoft/teams-ai';

const app = new Application({
  storage: new MemoryStorage(),
  ai: {
    planner: new ActionPlanner({
      model: new OpenAIModel({
        apiKey: process.env.OPENAI_KEY,
        defaultModel: 'gpt-4'
      }),
      prompts: './prompts'
    })
  }
});

app.message('/hello', async (context, state) => {
  await context.sendActivity('Hello!');
});
```

**Use get_code_snippets for more examples.**

---

### Teams JS SDK

**Package:** `@microsoft/teams-js`

**Installation:**
```bash
npm install @microsoft/teams-js
```

**Initialize in Tab:**
```typescript
import * as microsoftTeams from '@microsoft/teams-js';

microsoftTeams.app.initialize().then(() => {
  microsoftTeams.app.getContext().then((context) => {
    console.log('User ID:', context.user?.id);
    console.log('Team ID:', context.team?.groupId);
  });
});
```

**SSO Authentication:**
```typescript
microsoftTeams.authentication.getAuthToken().then((token) => {
  // Use token to call APIs
}).catch((error) => {
  // Handle auth failure
});
```

**Use get_code_snippets for more examples.**

---

### Bot Builder SDK

**Package:** `botbuilder`

**Installation:**
```bash
npm install botbuilder
```

**Basic Bot:**
```typescript
import { ActivityHandler } from 'botbuilder';

export class MyBot extends ActivityHandler {
  constructor() {
    super();

    this.onMessage(async (context, next) => {
      await context.sendActivity(`You said: ${context.activity.text}`);
      await next();
    });

    this.onMembersAdded(async (context, next) => {
      await context.sendActivity('Welcome!');
      await next();
    });
  }
}
```

**Use get_code_snippets for more examples.**

---

## Additional Resources

- [Teams Toolkit Documentation](https://learn.microsoft.com/microsoftteams/platform/toolkit/teams-toolkit-fundamentals)
- [Teams Platform Docs](https://learn.microsoft.com/microsoftteams/platform/)
- [Copilot Extensibility](https://learn.microsoft.com/microsoft-365-copilot/extensibility/)
- [Bot Framework SDK](https://learn.microsoft.com/azure/bot-service/)
- [Microsoft Graph API](https://learn.microsoft.com/graph/)
