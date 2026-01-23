# Playwright MCP Reference Documentation

Comprehensive reference for all Playwright MCP tools, parameters, and advanced usage patterns.

## Table of Contents

1. [Setup & Installation](#setup--installation)
2. [Core Tools - Navigation](#core-tools---navigation)
3. [Core Tools - Interaction](#core-tools---interaction)
4. [Core Tools - Information Retrieval](#core-tools---information-retrieval)
5. [Core Tools - Utilities](#core-tools---utilities)
6. [Optional Tools - Vision](#optional-tools---vision)
7. [Optional Tools - PDF](#optional-tools---pdf)
8. [Optional Tools - Testing](#optional-tools---testing)
9. [Optional Tools - Tracing](#optional-tools---tracing)
10. [Advanced Patterns](#advanced-patterns)
11. [Troubleshooting](#troubleshooting)

---

## Setup & Installation

### Prerequisites

The Playwright MCP server must be installed and configured. Common setup methods:

**NPX (Recommended):**
```bash
npx @anthropic-ai/claude-code@latest mcp add playwright -- npx @playwright/mcp@latest
```

**Manual Configuration:**

Add to your MCP settings (usually `~/.claude/settings.json` or VS Code settings):

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

### Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `--browser` | Browser to use | `--browser=chrome`, `firefox`, `webkit`, `msedge` |
| `--headless` | Run without UI | `--headless` (default) or `--no-headless` |
| `--device` | Emulate device | `--device="iPhone 15"` |
| `--user-agent` | Custom user agent | `--user-agent="CustomBot/1.0"` |
| `--viewport` | Set viewport size | `--viewport="1920x1080"` |
| `--caps` | Enable capabilities | `--caps=vision,pdf,testing,tracing` |

**Full Configuration Example:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser=chrome",
        "--no-headless",
        "--caps=vision,pdf,testing,tracing"
      ]
    }
  }
}
```

### Installing Browsers

If you encounter "browser not installed" errors:

```
Use browser_install tool to install the configured browser
```

---

## Core Tools - Navigation

### browser_navigate

Navigate to a specified URL.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| url | string | Yes | The URL to navigate to |

**Example:**
```json
{
  "url": "https://example.com/page"
}
```

**Notes:**
- Waits for page load to complete
- Follows redirects automatically
- Supports all URL schemes (http, https, file, etc.)

---

### browser_navigate_back

Navigate to the previous page in browser history.

**Parameters:** None

**Example:**
```json
{}
```

**Notes:**
- Equivalent to clicking browser back button
- No effect if no previous page in history

---

### browser_tabs

Manage browser tabs.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| action | string | Yes | "list", "new", "close", or "select" |
| index | number | No | Tab index for close/select operations |

**Actions:**

**List tabs:**
```json
{
  "action": "list"
}
```
Returns array of open tabs with titles and URLs.

**Create new tab:**
```json
{
  "action": "new"
}
```
Creates empty tab and switches to it.

**Close tab:**
```json
{
  "action": "close",
  "index": 2
}
```
Closes tab at index. If omitted, closes current tab.

**Select tab:**
```json
{
  "action": "select",
  "index": 0
}
```
Switches to tab at specified index.

---

### browser_close

Close the current page/browser.

**Parameters:** None

**Example:**
```json
{}
```

---

### browser_resize

Resize the browser window.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| width | number | Yes | Width in pixels |
| height | number | Yes | Height in pixels |

**Example:**
```json
{
  "width": 1920,
  "height": 1080
}
```

---

## Core Tools - Interaction

### browser_click

Click on a web page element.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| element | string | Yes | Human-readable description |
| ref | string | Yes | Element reference from snapshot |
| button | string | No | "left" (default), "right", "middle" |
| doubleClick | boolean | No | Perform double-click |
| modifiers | array | No | Key modifiers to hold |

**Modifiers:** `["Alt", "Control", "ControlOrMeta", "Meta", "Shift"]`

**Examples:**

Simple click:
```json
{
  "element": "Login button",
  "ref": "button[Login]"
}
```

Right-click:
```json
{
  "element": "Context menu target",
  "ref": "div[Item]",
  "button": "right"
}
```

Ctrl+Click (open in new tab):
```json
{
  "element": "Link to open in new tab",
  "ref": "link[Products]",
  "modifiers": ["Control"]
}
```

Double-click:
```json
{
  "element": "Editable cell",
  "ref": "cell[Data]",
  "doubleClick": true
}
```

---

### browser_type

Type text into an editable element.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| element | string | Yes | Human-readable description |
| ref | string | Yes | Element reference from snapshot |
| text | string | Yes | Text to type |
| submit | boolean | No | Press Enter after typing |
| slowly | boolean | No | Type character by character |

**Examples:**

Simple typing:
```json
{
  "element": "Email input",
  "ref": "textbox[Email]",
  "text": "user@example.com"
}
```

Type and submit:
```json
{
  "element": "Search box",
  "ref": "searchbox[Search]",
  "text": "playwright automation",
  "submit": true
}
```

Slow typing (for sites with key handlers):
```json
{
  "element": "Autocomplete input",
  "ref": "combobox[City]",
  "text": "New York",
  "slowly": true
}
```

---

### browser_fill_form

Fill multiple form fields at once.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| fields | array | Yes | Array of field objects |

**Field Object Structure:**
| Property | Type | Description |
|----------|------|-------------|
| name | string | Human-readable field name |
| type | string | Field type |
| ref | string | Element reference |
| value | string | Value to set |

**Field Types:** `textbox`, `checkbox`, `radio`, `combobox`, `slider`

**Example:**
```json
{
  "fields": [
    {
      "name": "First Name",
      "type": "textbox",
      "ref": "textbox[First Name]",
      "value": "John"
    },
    {
      "name": "Last Name",
      "type": "textbox",
      "ref": "textbox[Last Name]",
      "value": "Doe"
    },
    {
      "name": "Country",
      "type": "combobox",
      "ref": "combobox[Country]",
      "value": "United States"
    },
    {
      "name": "Subscribe to newsletter",
      "type": "checkbox",
      "ref": "checkbox[Subscribe]",
      "value": "true"
    },
    {
      "name": "Gender",
      "type": "radio",
      "ref": "radio[Male]",
      "value": "male"
    }
  ]
}
```

---

### browser_select_option

Select an option in a dropdown.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| element | string | Yes | Human-readable description |
| ref | string | Yes | Element reference |
| values | array | Yes | Values to select |

**Example:**

Single selection:
```json
{
  "element": "Country dropdown",
  "ref": "combobox[Country]",
  "values": ["United States"]
}
```

Multiple selection:
```json
{
  "element": "Skills multi-select",
  "ref": "listbox[Skills]",
  "values": ["JavaScript", "Python", "TypeScript"]
}
```

---

### browser_hover

Hover over an element.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| element | string | Yes | Human-readable description |
| ref | string | Yes | Element reference |

**Example:**
```json
{
  "element": "Menu item to reveal submenu",
  "ref": "menuitem[Products]"
}
```

---

### browser_drag

Drag and drop between elements.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| startElement | string | Yes | Source element description |
| startRef | string | Yes | Source element reference |
| endElement | string | Yes | Target element description |
| endRef | string | Yes | Target element reference |

**Example:**
```json
{
  "startElement": "Draggable item",
  "startRef": "listitem[Task 1]",
  "endElement": "Drop zone",
  "endRef": "region[Done Column]"
}
```

---

### browser_press_key

Press a keyboard key.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| key | string | Yes | Key name or character |

**Common Keys:**
- Letters: `a`, `b`, `c`, etc.
- Numbers: `0`, `1`, `2`, etc.
- Special: `Enter`, `Tab`, `Escape`, `Backspace`, `Delete`
- Navigation: `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`
- Modifiers: `Shift`, `Control`, `Alt`, `Meta`
- Function: `F1` through `F12`
- Other: `Home`, `End`, `PageUp`, `PageDown`, `Space`

**Examples:**

Press Enter:
```json
{
  "key": "Enter"
}
```

Press Escape:
```json
{
  "key": "Escape"
}
```

Arrow navigation:
```json
{
  "key": "ArrowDown"
}
```

---

### browser_file_upload

Upload files to a file input.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| paths | array | No | Absolute file paths to upload |

**Example:**

Upload single file:
```json
{
  "paths": ["C:/Users/john/Documents/resume.pdf"]
}
```

Upload multiple files:
```json
{
  "paths": [
    "C:/Users/john/Photos/photo1.jpg",
    "C:/Users/john/Photos/photo2.jpg"
  ]
}
```

Cancel file chooser:
```json
{}
```

**Notes:**
- Paths must be absolute
- Triggered after clicking a file input that opens file chooser
- Omit paths to cancel the file chooser dialog

---

### browser_handle_dialog

Handle JavaScript dialogs (alert, confirm, prompt).

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| accept | boolean | Yes | Accept or dismiss dialog |
| promptText | string | No | Text for prompt dialogs |

**Examples:**

Accept alert:
```json
{
  "accept": true
}
```

Dismiss confirm:
```json
{
  "accept": false
}
```

Fill and accept prompt:
```json
{
  "accept": true,
  "promptText": "My response"
}
```

---

## Core Tools - Information Retrieval

### browser_snapshot

Capture accessibility snapshot of the page. **This is the preferred method for understanding page structure.**

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| filename | string | No | Save snapshot to file |

**Example:**

Return snapshot:
```json
{}
```

Save to file:
```json
{
  "filename": "page-snapshot.md"
}
```

**Output Format:**
The snapshot returns a structured representation of the page including:
- Element types (button, link, textbox, etc.)
- Element references (ref) for interactions
- Accessible names and descriptions
- Hierarchical structure

**Sample Output:**
```
- document "Page Title"
  - navigation "Main Navigation"
    - link "Home" [ref: link[Home]]
    - link "Products" [ref: link[Products]]
    - link "Contact" [ref: link[Contact]]
  - main
    - heading "Welcome" [level: 1]
    - textbox "Email" [ref: textbox[Email]]
    - textbox "Password" [ref: textbox[Password]]
    - button "Login" [ref: button[Login]]
```

---

### browser_take_screenshot

Capture a visual screenshot.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| type | string | No | "png" (default) or "jpeg" |
| filename | string | No | Save filename |
| fullPage | boolean | No | Capture full scrollable page |
| element | string | No | Element description (for element screenshot) |
| ref | string | No | Element reference (for element screenshot) |

**Examples:**

Viewport screenshot:
```json
{}
```

Full page screenshot:
```json
{
  "fullPage": true,
  "filename": "full-page.png"
}
```

Element screenshot:
```json
{
  "element": "Header section",
  "ref": "banner[Main Header]",
  "filename": "header.png"
}
```

JPEG with custom name:
```json
{
  "type": "jpeg",
  "filename": "screenshot.jpg"
}
```

---

### browser_console_messages

Get browser console messages.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| level | string | No | Minimum log level |

**Log Levels (each includes higher severity):**
- `debug` - All messages
- `info` - Info, warnings, errors
- `warning` - Warnings and errors
- `error` - Only errors

**Example:**
```json
{
  "level": "warning"
}
```

---

### browser_network_requests

Get all network requests since page load.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| includeStatic | boolean | No | Include static resources (images, fonts, etc.) |

**Examples:**

API requests only:
```json
{
  "includeStatic": false
}
```

All requests:
```json
{
  "includeStatic": true
}
```

---

## Core Tools - Utilities

### browser_wait_for

Wait for conditions.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| text | string | No | Wait for text to appear |
| textGone | string | No | Wait for text to disappear |
| time | number | No | Wait for N seconds |

**Examples:**

Wait for text:
```json
{
  "text": "Welcome back"
}
```

Wait for loading to finish:
```json
{
  "textGone": "Loading..."
}
```

Wait fixed time:
```json
{
  "time": 3
}
```

---

### browser_evaluate

Execute JavaScript in page context.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| function | string | Yes | JavaScript function to execute |
| element | string | No | Element description (if targeting element) |
| ref | string | No | Element reference (if targeting element) |

**Examples:**

Get page title:
```json
{
  "function": "() => document.title"
}
```

Extract data:
```json
{
  "function": "() => { return Array.from(document.querySelectorAll('.product')).map(el => ({ name: el.querySelector('.name').textContent, price: el.querySelector('.price').textContent })) }"
}
```

Execute on element:
```json
{
  "element": "Product list",
  "ref": "list[Products]",
  "function": "(element) => element.children.length"
}
```

Scroll page:
```json
{
  "function": "() => window.scrollTo(0, document.body.scrollHeight)"
}
```

---

### browser_run_code

Run Playwright code snippets directly.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| code | string | Yes | Playwright code as async function |

**Examples:**

Complex interaction:
```json
{
  "code": "async (page) => { await page.getByRole('button', { name: 'Submit' }).click(); return await page.title(); }"
}
```

Wait for specific element:
```json
{
  "code": "async (page) => { await page.waitForSelector('.result-item', { timeout: 10000 }); return 'Results loaded'; }"
}
```

Extract with Playwright locators:
```json
{
  "code": "async (page) => { const items = await page.locator('.item').all(); return Promise.all(items.map(item => item.textContent())); }"
}
```

---

### browser_install

Install the configured browser.

**Parameters:** None

**Example:**
```json
{}
```

**Notes:**
- Call this if you get "browser not installed" errors
- Downloads and installs the browser configured in MCP settings

---

## Optional Tools - Vision

These tools require `--caps=vision` flag.

### browser_mouse_click_xy

Click at specific coordinates.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| element | string | Yes | Description of target |
| x | number | Yes | X coordinate |
| y | number | Yes | Y coordinate |

**Example:**
```json
{
  "element": "Canvas drawing area",
  "x": 150,
  "y": 200
}
```

---

### browser_mouse_drag_xy

Drag from one position to another.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| element | string | Yes | Description of action |
| startX | number | Yes | Start X coordinate |
| startY | number | Yes | Start Y coordinate |
| endX | number | Yes | End X coordinate |
| endY | number | Yes | End Y coordinate |

**Example:**
```json
{
  "element": "Drag slider",
  "startX": 100,
  "startY": 200,
  "endX": 300,
  "endY": 200
}
```

---

### browser_mouse_move_xy

Move mouse to position.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| element | string | Yes | Description of target |
| x | number | Yes | X coordinate |
| y | number | Yes | Y coordinate |

**Example:**
```json
{
  "element": "Hover target",
  "x": 250,
  "y": 150
}
```

---

## Optional Tools - PDF

Requires `--caps=pdf` flag.

### browser_pdf_save

Save current page as PDF.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| filename | string | No | Output filename |

**Example:**
```json
{
  "filename": "page-export.pdf"
}
```

---

## Optional Tools - Testing

These tools require `--caps=testing` flag.

### browser_generate_locator

Generate Playwright locator for use in tests.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| element | string | Yes | Element description |
| ref | string | Yes | Element reference |

**Example:**
```json
{
  "element": "Submit button",
  "ref": "button[Submit]"
}
```

Returns Playwright locator code like:
```javascript
page.getByRole('button', { name: 'Submit' })
```

---

### browser_verify_element_visible

Verify element is visible on page.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| role | string | Yes | ARIA role |
| accessibleName | string | Yes | Accessible name |

**Example:**
```json
{
  "role": "button",
  "accessibleName": "Submit"
}
```

---

### browser_verify_text_visible

Verify text is visible on page.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| text | string | Yes | Text to verify |

**Example:**
```json
{
  "text": "Welcome to our site"
}
```

---

### browser_verify_value

Verify element value.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| type | string | Yes | Verification type |
| element | string | Yes | Element description |
| ref | string | Yes | Element reference |
| value | string | Yes | Expected value |

**Example:**
```json
{
  "type": "value",
  "element": "Email input",
  "ref": "textbox[Email]",
  "value": "test@example.com"
}
```

---

### browser_verify_list_visible

Verify list with specific items is visible.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| element | string | Yes | List element description |
| ref | string | Yes | Element reference |
| items | array | Yes | Expected items |

**Example:**
```json
{
  "element": "Navigation menu",
  "ref": "navigation[Main]",
  "items": ["Home", "Products", "About", "Contact"]
}
```

---

## Optional Tools - Tracing

Requires `--caps=tracing` flag.

### browser_start_tracing

Start recording a trace.

**Parameters:** None

**Example:**
```json
{}
```

---

### browser_stop_tracing

Stop trace recording and save.

**Parameters:** None

**Example:**
```json
{}
```

**Notes:**
- Trace files can be viewed at https://trace.playwright.dev
- Useful for debugging complex automation sequences

---

## Advanced Patterns

### Handling Dynamic Content

```
1. browser_navigate to page
2. browser_wait_for text that indicates content loaded
3. browser_snapshot to capture current state
4. Proceed with interactions
```

### Multi-Page Workflows

```
1. browser_navigate to start page
2. Perform actions
3. browser_tabs action="list" to see all tabs
4. browser_tabs action="select" index=N to switch
5. Continue workflow in new tab
```

### Authentication Flows

```
1. browser_navigate to login page
2. browser_snapshot to find form fields
3. browser_fill_form with credentials
4. browser_click on submit button
5. browser_wait_for dashboard element
6. browser_snapshot to verify login success
```

### Data Extraction Pattern

```
1. browser_navigate to data page
2. browser_snapshot for structure
3. browser_evaluate with extraction function
4. If paginated:
   a. browser_click on next page
   b. browser_wait_for new content
   c. Repeat extraction
5. Aggregate results
```

### Error Handling Pattern

```
1. Attempt action
2. browser_snapshot to check state
3. If error dialog: browser_handle_dialog
4. If unexpected state: browser_console_messages for clues
5. browser_take_screenshot for evidence
6. Retry or report error
```

---

## Troubleshooting

### Browser Not Installed

**Error:** "Browser is not installed"

**Solution:** Use `browser_install` tool

---

### Element Not Found

**Error:** Cannot find element with ref

**Solutions:**
1. Take fresh `browser_snapshot`
2. Verify page has loaded (`browser_wait_for`)
3. Check if element is in iframe
4. Element may be hidden - use `browser_evaluate` to check visibility

---

### Timeout Errors

**Error:** Operation timed out

**Solutions:**
1. Increase wait time with `browser_wait_for`
2. Check network connectivity
3. Page may be slow - use `browser_network_requests` to diagnose
4. Check `browser_console_messages` for JavaScript errors

---

### Dialog Blocking

**Error:** Action blocked by dialog

**Solution:** Use `browser_handle_dialog` to dismiss/accept before proceeding

---

### Stale Element Reference

**Error:** Element no longer attached to DOM

**Solutions:**
1. Page may have reloaded - take new `browser_snapshot`
2. Dynamic content updated - wait and re-snapshot
3. Use `browser_wait_for` before interactions

---

## Additional Resources

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Accessibility Tree](https://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree)
- [ARIA Roles Reference](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)
