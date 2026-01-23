---
mode: agent
description: "Perform security review and fix vulnerabilities"
---

# Security Review

Analyze code for security vulnerabilities and provide fixes.

{{#if selection}}
## Code to Review

```
{{{ selection }}}
```
{{/if}}

## Security Checklist

1. **Injection** - SQL, XSS, command injection
2. **Authentication** - Proper auth checks, session handling
3. **Authorization** - Access control, privilege escalation
4. **Data Exposure** - Sensitive data in logs, responses, URLs
5. **Input Validation** - All user input validated and sanitized
6. **Dependencies** - Known vulnerabilities in packages
7. **Cryptography** - Secure algorithms, proper key management
8. **Error Handling** - No sensitive info in errors

## Output

For each issue found:
1. **Severity** - Critical/High/Medium/Low
2. **Description** - What's the vulnerability?
3. **Risk** - What could an attacker do?
4. **Fix** - Secure code replacement
