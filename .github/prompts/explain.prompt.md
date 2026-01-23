---
mode: agent
description: "Explain code in detail with documentation"
---

# Explain Code

Provide a detailed explanation of the code.

{{#if selection}}
## Code to Explain

```
{{{ selection }}}
```
{{/if}}

## Explanation Format

1. **Overview** - What does this code do at a high level?
2. **Step-by-Step** - Walk through the logic
3. **Key Concepts** - Explain any patterns, algorithms, or techniques used
4. **Dependencies** - What does it rely on?
5. **Usage** - How would you use this code?

Keep explanations clear and accessible for developers of varying experience levels.
