# Playwright MCP Troubleshooting Guide

Common issues and solutions when using Playwright MCP tools.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Browser Issues](#browser-issues)
3. [Element Interaction Issues](#element-interaction-issues)
4. [Timeout Issues](#timeout-issues)
5. [Dialog and Popup Issues](#dialog-and-popup-issues)
6. [Network Issues](#network-issues)
7. [Authentication Issues](#authentication-issues)
8. [Performance Issues](#performance-issues)
9. [Tool-Specific Issues](#tool-specific-issues)

---

## Installation Issues

### Browser Not Installed

**Symptoms:**
- Error: "Browser is not installed"
- Tool calls fail immediately

**Solution:**
```
Use browser_install tool

This will download and install the configured browser.
```

### MCP Server Not Connected

**Symptoms:**
- Playwright tools not available
- "Tool not found" errors

**Solutions:**

1. **Verify MCP configuration:**
   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       }
     }
   }
   ```

2. **Check npx is available:**
   ```bash
   npx --version
   ```

3. **Restart Claude Code** after configuration changes

4. **Check for port conflicts** if using custom ports

### Package Not Found

**Symptoms:**
- "Cannot find package @playwright/mcp"
- npm/npx errors

**Solutions:**

1. **Update npm:**
   ```bash
   npm install -g npm@latest
   ```

2. **Clear npm cache:**
   ```bash
   npm cache clean --force
   ```

3. **Install globally:**
   ```bash
   npm install -g @playwright/mcp
   ```

---

## Browser Issues

### Browser Crashes on Launch

**Symptoms:**
- Browser window appears briefly then closes
- "Browser closed unexpectedly"

**Solutions:**

1. **Try headless mode:**
   ```json
   {
     "args": ["@playwright/mcp@latest", "--headless"]
   }
   ```

2. **Disable sandbox (if in container):**
   ```json
   {
     "args": ["@playwright/mcp@latest", "--no-sandbox"]
   }
   ```

3. **Check system resources:**
   - Ensure sufficient RAM (4GB+ recommended)
   - Check disk space

### Wrong Browser Version

**Symptoms:**
- Features not working as expected
- Compatibility issues

**Solution:**
```
browser_install to get compatible browser version
```

### Cannot Start Headed Browser

**Symptoms:**
- "Cannot open display"
- Browser window doesn't appear

**Solutions:**

1. **Use headless mode** (recommended for automation)

2. **If display needed:**
   - Ensure X server running (Linux)
   - Check DISPLAY environment variable
   - Use virtual display (Xvfb)

---

## Element Interaction Issues

### Element Not Found

**Symptoms:**
- "Cannot find element with ref"
- Click/type fails

**Solutions:**

1. **Take fresh snapshot:**
   ```
   browser_snapshot
   ```
   Element refs change after navigation or DOM updates.

2. **Wait for page to load:**
   ```
   browser_wait_for text="Expected content"
   ```

3. **Check if in iframe:**
   - Elements in iframes have different context
   - May need to switch context

4. **Element may be hidden:**
   - Use browser_evaluate to check visibility
   - Scroll element into view first

### Click Not Registering

**Symptoms:**
- Click executes but nothing happens
- No visible change

**Solutions:**

1. **Element might be covered:**
   - Wait for overlays to disappear
   - Scroll to element

2. **Need double-click:**
   ```json
   {
     "element": "Editable cell",
     "ref": "cell[Data]",
     "doubleClick": true
   }
   ```

3. **Wrong element targeted:**
   - Take snapshot and verify ref
   - Some elements have clickable children

4. **Page not ready:**
   ```
   browser_wait_for text="Ready"
   ```

### Type Not Working

**Symptoms:**
- Text doesn't appear in field
- Partial text entry

**Solutions:**

1. **Element not focused:**
   - Click element first
   - Then type

2. **Field has restrictions:**
   - Check for max length
   - Check for input masks

3. **Use slowly mode:**
   ```json
   {
     "slowly": true
   }
   ```
   For fields with input handlers.

4. **Clear existing content:**
   - Select all (Ctrl+A) then type
   - Use browser_evaluate to clear

### Hover Not Revealing Menu

**Symptoms:**
- Menu doesn't appear on hover
- Dropdown stays closed

**Solutions:**

1. **Add wait after hover:**
   ```
   browser_hover element="Menu" ref="menuitem[Products]"
   browser_wait_for text="Submenu item"
   browser_snapshot
   ```

2. **Element requires click instead:**
   - Some "dropdown" menus are click-triggered
   - Try browser_click instead

---

## Timeout Issues

### Page Load Timeout

**Symptoms:**
- Navigation takes too long
- "Timeout waiting for page load"

**Solutions:**

1. **Check URL accessibility:**
   - Verify URL is correct
   - Check if site is up

2. **Increase wait time:**
   ```
   browser_wait_for time=10
   ```

3. **Wait for specific content instead:**
   ```
   browser_wait_for text="Page loaded indicator"
   ```

4. **Check network:**
   - Slow connection
   - Firewall blocking

### Wait Timeout

**Symptoms:**
- "Timeout waiting for text"
- Expected content never appears

**Solutions:**

1. **Verify text exists:**
   - Take screenshot to see actual page
   - Text might be slightly different

2. **Check for typos:**
   - Exact text match required
   - Case sensitivity matters

3. **Content may be dynamic:**
   - Try different wait target
   - Use textGone for loading indicators

4. **Page might have error:**
   ```
   browser_console_messages level="error"
   ```

### Action Timeout

**Symptoms:**
- Click/type times out
- Element "not interactable"

**Solutions:**

1. **Element not ready:**
   - Wait for page to stabilize
   - Element might be animating

2. **Element covered:**
   - Wait for overlays to disappear
   - Cookie banners, modals, etc.

3. **Element off-screen:**
   - Scroll to element
   - Use browser_evaluate to scroll

---

## Dialog and Popup Issues

### Unexpected Dialog

**Symptoms:**
- Actions blocked by alert/confirm
- "Dialog already open"

**Solution:**
```
browser_handle_dialog accept=true
```
Or with prompt text:
```json
{
  "accept": true,
  "promptText": "response"
}
```

### Popup Window

**Symptoms:**
- New window opened
- Can't interact with popup

**Solution:**
```
browser_tabs action="list"
browser_tabs action="select" index=1
```

### Auth Popup (Basic Auth)

**Symptoms:**
- Browser login dialog
- Can't interact with dialog

**Solution:**

Include credentials in URL:
```
https://username:password@example.com
```

Or use browser_handle_dialog for some auth popups.

---

## Network Issues

### Page Not Loading

**Symptoms:**
- Blank page
- Network error

**Solutions:**

1. **Check URL format:**
   - Include protocol (https://)
   - URL encode special characters

2. **Check connectivity:**
   ```
   browser_network_requests
   ```

3. **Proxy issues:**
   - Configure proxy in MCP settings
   - Check proxy authentication

### CORS Errors

**Symptoms:**
- API calls fail
- Cross-origin errors in console

**Solution:**
```
browser_console_messages level="error"
```
CORS is a browser security feature. If scraping, this shouldn't affect page interaction.

### SSL/TLS Errors

**Symptoms:**
- Certificate errors
- "Your connection is not private"

**Solutions:**

1. **Ignore HTTPS errors (if appropriate):**
   ```json
   {
     "args": ["@playwright/mcp@latest", "--ignore-https-errors"]
   }
   ```

2. **Check system certificates**

---

## Authentication Issues

### Login Not Persisting

**Symptoms:**
- Have to login every time
- Session lost between navigations

**Solutions:**

1. **Check for cookie consent:**
   - Accept cookie banners
   - Some sites require explicit consent

2. **Browser context resetting:**
   - Use persistent profile in config
   - Check storage state settings

3. **Session timeout:**
   - Site may have short session timeout
   - Refresh session as needed

### OAuth/SSO Issues

**Symptoms:**
- Redirect loops
- Can't complete OAuth flow

**Solutions:**

1. **Follow all redirects:**
   - Wait for final destination
   - Handle multiple page loads

2. **May need manual intervention:**
   - Some OAuth requires user interaction
   - CAPTCHA, device verification, etc.

3. **Check all tabs:**
   ```
   browser_tabs action="list"
   ```
   Auth may open in new tab.

---

## Performance Issues

### Slow Automation

**Symptoms:**
- Actions take long time
- Browser unresponsive

**Solutions:**

1. **Use headless mode:**
   Rendering UI is slower.

2. **Minimize snapshots:**
   Only snapshot when needed.

3. **Use bulk operations:**
   ```
   browser_fill_form (single call for multiple fields)
   ```

4. **Close unused tabs:**
   ```
   browser_tabs action="close"
   ```

5. **Avoid fixed delays:**
   Use explicit waits instead.

### High Memory Usage

**Symptoms:**
- System slowdown
- Out of memory errors

**Solutions:**

1. **Close browser when done:**
   ```
   browser_close
   ```

2. **Limit concurrent tabs**

3. **Clear browser data periodically**

4. **Use appropriate viewport size**

---

## Tool-Specific Issues

### browser_snapshot Returns Empty

**Symptoms:**
- Empty or minimal snapshot
- Missing expected elements

**Solutions:**

1. **Page not loaded:**
   ```
   browser_wait_for text="Key content"
   ```

2. **Content in iframe:**
   - Iframes have separate accessibility trees
   - May need to focus iframe

3. **JavaScript rendering:**
   - Wait for client-side rendering
   - Some SPAs take time to render

### browser_evaluate Fails

**Symptoms:**
- JavaScript error
- Unexpected return value

**Solutions:**

1. **Syntax error:**
   - Check JavaScript syntax
   - Use arrow function format: `() => { ... }`

2. **Element not found:**
   - Verify selector
   - Element may not exist yet

3. **Serialize return value:**
   - Can't return DOM nodes
   - Extract data into plain objects

### browser_file_upload Not Working

**Symptoms:**
- File chooser not triggered
- Upload fails

**Solutions:**

1. **Use absolute paths:**
   ```json
   {
     "paths": ["C:/Users/user/file.pdf"]
   }
   ```

2. **File chooser must be open:**
   - Click upload button first
   - Then use browser_file_upload

3. **Check file exists:**
   - Verify path is correct
   - Check file permissions

### browser_take_screenshot Black/Blank

**Symptoms:**
- Screenshot is black
- Screenshot is blank

**Solutions:**

1. **Page not loaded:**
   - Wait for content
   - Check for errors

2. **Element off-screen:**
   - Scroll to element
   - Use fullPage option

3. **Canvas/WebGL content:**
   - Some content can't be screenshotted
   - May appear black

---

## Getting Help

If issues persist:

1. **Check console messages:**
   ```
   browser_console_messages level="debug"
   ```

2. **Check network:**
   ```
   browser_network_requests includeStatic=true
   ```

3. **Take screenshot:**
   ```
   browser_take_screenshot fullPage=true
   ```

4. **Enable tracing (if available):**
   ```
   browser_start_tracing
   (perform actions)
   browser_stop_tracing
   ```

5. **Review Playwright docs:**
   - https://playwright.dev/docs/intro

6. **Check Playwright MCP issues:**
   - https://github.com/microsoft/playwright-mcp/issues
