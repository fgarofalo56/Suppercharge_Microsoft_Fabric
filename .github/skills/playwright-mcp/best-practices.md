# Playwright MCP Best Practices

Guidelines for reliable, efficient, and maintainable browser automation.

## Table of Contents

1. [Page Interaction](#page-interaction)
2. [Element Selection](#element-selection)
3. [Waiting Strategies](#waiting-strategies)
4. [Error Handling](#error-handling)
5. [Performance Optimization](#performance-optimization)
6. [Security Considerations](#security-considerations)
7. [Debugging Tips](#debugging-tips)
8. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## Page Interaction

### Always Snapshot First

**DO:**
```
1. browser_navigate to page
2. browser_snapshot to understand structure
3. Use refs from snapshot for interactions
```

**DON'T:**
```
1. browser_navigate to page
2. Immediately try browser_click with guessed ref
```

### Use Semantic Descriptions

**DO:**
```json
{
  "element": "Submit order button",
  "ref": "button[Submit Order]"
}
```

**DON'T:**
```json
{
  "element": "btn",
  "ref": "button[btn-primary-123]"
}
```

### Verify State After Actions

**DO:**
```
1. browser_click on submit
2. browser_wait_for success message
3. browser_snapshot to verify new state
```

**DON'T:**
```
1. browser_click on submit
2. Assume success without verification
```

---

## Element Selection

### Prefer Accessible Names Over IDs/Classes

Accessibility tree references are more stable than DOM selectors:

**Good refs:**
- `button[Submit]`
- `textbox[Email address]`
- `link[Home]`
- `checkbox[Remember me]`

**Fragile refs (avoid when possible):**
- `button[btn-xyz-123]`
- `div[container-wrapper]`

### Use the Most Specific Reference

When multiple elements match, add context:

**Ambiguous:**
```
button[Submit]  (might match multiple buttons)
```

**Specific:**
```
button[Submit Order]  (unique on checkout page)
```

### Handle Dynamic References

For elements with dynamic IDs:

```
1. browser_snapshot to get current refs
2. Use refs immediately (don't cache for later pages)
3. Re-snapshot after navigation or major state changes
```

---

## Waiting Strategies

### Use Explicit Waits Over Fixed Delays

**DO:**
```json
{
  "text": "Order confirmed"
}
```
Waits for specific content to appear.

**DON'T:**
```json
{
  "time": 5
}
```
Fixed delays are unreliable and slow.

### Wait for the Right Indicator

**Page Load:**
```json
{
  "text": "Welcome"  // Key content that appears when loaded
}
```

**After Form Submit:**
```json
{
  "text": "Thank you"  // Success message
}
```

**Loading Spinner Gone:**
```json
{
  "textGone": "Loading..."
}
```

### Combine Wait Strategies When Needed

For complex state changes:
```
1. browser_wait_for textGone="Loading"
2. browser_wait_for text="Results"
3. browser_snapshot
```

---

## Error Handling

### Check for Dialogs

Before interactions, handle any blocking dialogs:

```
1. Attempt action
2. If blocked, use browser_handle_dialog
3. Retry action
```

### Verify Expected State

After critical actions:

```
1. browser_snapshot
2. Check for expected elements/text
3. If unexpected state:
   - browser_console_messages for errors
   - browser_take_screenshot for evidence
```

### Handle Common Failure Cases

**Element not found:**
- Take fresh snapshot
- Verify page loaded correctly
- Check for redirects

**Timeout:**
- Increase wait time
- Check network issues
- Verify page is responding

**Unexpected dialog:**
- Use browser_handle_dialog
- Check console for JavaScript errors

---

## Performance Optimization

### Minimize Tool Calls

**DO:**
```
browser_fill_form with all fields at once
```

**DON'T:**
```
browser_type for field 1
browser_type for field 2
browser_type for field 3
...
```

### Use Snapshots Efficiently

- Take one snapshot after page load
- Re-use refs from snapshot for multiple interactions
- Only re-snapshot after major state changes

### Avoid Redundant Screenshots

**DO:**
- Screenshot on errors
- Screenshot for final verification
- Screenshot for visual regression tests

**DON'T:**
- Screenshot after every action
- Screenshot as a substitute for snapshots

### Close Browser When Done

Always clean up:
```
browser_close
```

---

## Security Considerations

### Credential Handling

**DO:**
- Use environment variables for secrets
- Clear sensitive data after use
- Use secure connections (HTTPS)

**DON'T:**
- Hardcode passwords in automation scripts
- Log sensitive data
- Store credentials in screenshots

### Input Validation

When filling forms with external data:
- Validate input before entry
- Escape special characters if needed
- Watch for injection vulnerabilities

### Session Management

- Don't share browser sessions between contexts
- Clear cookies/storage when switching users
- Use isolated browser profiles for sensitive operations

### File Upload Safety

- Validate file paths before upload
- Don't upload files from untrusted sources
- Check file types and sizes

---

## Debugging Tips

### Use Console Messages

```json
{
  "level": "error"
}
```
Check for JavaScript errors that might indicate issues.

### Capture Network Requests

```json
{
  "includeStatic": false
}
```
See API calls and their responses.

### Take Strategic Screenshots

- Before and after problematic steps
- When errors occur
- At key checkpoints

### Use Tracing (if enabled)

```
1. browser_start_tracing
2. Perform actions
3. browser_stop_tracing
4. Review trace at trace.playwright.dev
```

### Inspect Accessibility Snapshot

The snapshot reveals:
- Actual element names (vs. visual labels)
- Element hierarchy
- Interactive element types
- Current values/states

---

## Anti-Patterns to Avoid

### Fixed Sleep Delays

**Bad:**
```json
{
  "time": 10
}
```

**Good:**
```json
{
  "text": "Content loaded"
}
```

### Ignoring Return Values

**Bad:**
```
browser_evaluate (ignore result)
browser_click
```

**Good:**
```
result = browser_evaluate
Use result to inform next action
```

### Hardcoded References

**Bad:**
```
Always use "button[btn-123]" everywhere
```

**Good:**
```
Snapshot each page, use returned refs
```

### No Error Recovery

**Bad:**
```
Click -> Click -> Click (hope for the best)
```

**Good:**
```
Click -> Verify -> Handle errors -> Retry if needed
```

### Over-Engineering

**Bad:**
```
Complex retry logic for simple one-time tasks
```

**Good:**
```
Simple, readable automation for straightforward tasks
```

### Screenshot-First Approach

**Bad:**
```
Take screenshot -> Analyze visually -> Interact
```

**Good:**
```
Take snapshot -> Parse structure -> Interact
```

Snapshots are faster, more reliable, and don't require vision capabilities.

---

## Checklist for Reliable Automation

### Before Starting
- [ ] Clear goal defined
- [ ] Target URLs accessible
- [ ] Test credentials ready (if needed)
- [ ] Error handling planned

### During Development
- [ ] Snapshot taken first
- [ ] Explicit waits used
- [ ] State verified after actions
- [ ] Errors handled gracefully

### Before Production
- [ ] Tested on target environment
- [ ] Edge cases handled
- [ ] Credentials secured
- [ ] Logging appropriate
- [ ] Clean-up implemented

### Maintenance
- [ ] Monitor for failures
- [ ] Update when UI changes
- [ ] Review performance
- [ ] Rotate credentials regularly
