---
mode: agent
description: "Add documentation and comments to code"
---

# Document Code

Add comprehensive documentation to the code.

{{#if selection}}
## Code to Document

```
{{{ selection }}}
```
{{/if}}

## Documentation Standards

1. **File/Module Level** - Purpose and overview
2. **Function/Method Level** - JSDoc/docstring with params, returns, throws
3. **Inline Comments** - Complex logic explanation (sparingly)
4. **Type Annotations** - Clear type definitions
5. **Examples** - Usage examples where helpful

## Output Format

Match the project's existing documentation style. Include:
- Parameter descriptions
- Return value descriptions
- Exception/error documentation
- Usage examples for public APIs
