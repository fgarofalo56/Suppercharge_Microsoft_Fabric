---
mode: agent
description: "Refactor code for better readability, performance, or maintainability"
---

# Code Refactoring

Analyze and refactor the selected code or specified file for improved quality.

## Focus Areas

1. **Readability** - Clear variable names, logical structure, comments where needed
2. **Performance** - Optimize loops, reduce complexity, improve efficiency
3. **Maintainability** - Extract functions, reduce duplication, improve modularity
4. **Best Practices** - Apply language idioms and modern patterns

## Instructions

{{#if selection}}
Refactor this code:

```
{{{ selection }}}
```
{{else}}
Please specify the file or code you want refactored.
{{/if}}

## Output

Provide:
1. Refactored code with improvements
2. Brief explanation of changes made
3. Any trade-offs or considerations
