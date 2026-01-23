# Playwright MCP Workflow Examples

Practical workflow examples for common browser automation tasks.

## Table of Contents

1. [Web Scraping Workflows](#web-scraping-workflows)
2. [Form Automation Workflows](#form-automation-workflows)
3. [Testing Workflows](#testing-workflows)
4. [Data Entry Workflows](#data-entry-workflows)
5. [Monitoring Workflows](#monitoring-workflows)
6. [Authentication Workflows](#authentication-workflows)

---

## Web Scraping Workflows

### Basic Page Scraping

**Goal:** Extract structured data from a webpage

**Steps:**
```
1. browser_navigate
   url: "https://example.com/products"

2. browser_wait_for
   text: "Products"  (or key content indicator)

3. browser_snapshot
   (analyze structure, identify data elements)

4. browser_evaluate
   function: "() => {
     return Array.from(document.querySelectorAll('.product-card')).map(card => ({
       name: card.querySelector('.product-name')?.textContent?.trim(),
       price: card.querySelector('.price')?.textContent?.trim(),
       image: card.querySelector('img')?.src,
       link: card.querySelector('a')?.href
     }))
   }"

5. (Process returned data)
```

### Paginated Content Scraping

**Goal:** Scrape data across multiple pages

**Steps:**
```
1. browser_navigate
   url: "https://example.com/listings?page=1"

2. browser_snapshot
   (identify pagination controls)

3. browser_evaluate
   function: "() => { /* extract current page data */ }"

4. browser_click
   element: "Next page button"
   ref: "link[Next]" (or "button[›]", etc.)

5. browser_wait_for
   textGone: "Loading"

6. Repeat steps 3-5 until no more pages

7. browser_close
```

### Dynamic Content Scraping (Infinite Scroll)

**Goal:** Scrape content that loads on scroll

**Steps:**
```
1. browser_navigate
   url: "https://example.com/feed"

2. browser_evaluate
   function: "() => window.scrollTo(0, document.body.scrollHeight)"

3. browser_wait_for
   time: 2  (wait for content to load)

4. browser_evaluate
   function: "() => document.querySelectorAll('.item').length"
   (check item count)

5. Repeat steps 2-4 until desired count or no new items

6. browser_evaluate
   function: "() => { /* extract all loaded data */ }"
```

### SPA (Single Page Application) Scraping

**Goal:** Scrape React/Vue/Angular apps

**Steps:**
```
1. browser_navigate
   url: "https://spa-app.example.com"

2. browser_wait_for
   text: "Dashboard"  (wait for app to render)

3. browser_snapshot
   (apps render accessibility tree even for virtual DOM)

4. browser_click
   element: "Data tab"
   ref: "tab[Data]"

5. browser_wait_for
   textGone: "Loading..."

6. browser_evaluate
   function: "() => {
     // For React apps, may need to access state
     return window.__REACT_DEVTOOLS_GLOBAL_HOOK__?.renderers?.get(1)?.getCurrentFiber()
   }"
   (or use DOM extraction)
```

---

## Form Automation Workflows

### Simple Contact Form

**Goal:** Fill and submit a contact form

**Steps:**
```
1. browser_navigate
   url: "https://example.com/contact"

2. browser_snapshot
   (identify form fields)

3. browser_fill_form
   fields: [
     {"name": "Name", "type": "textbox", "ref": "textbox[Name]", "value": "John Doe"},
     {"name": "Email", "type": "textbox", "ref": "textbox[Email]", "value": "john@example.com"},
     {"name": "Subject", "type": "combobox", "ref": "combobox[Subject]", "value": "General Inquiry"},
     {"name": "Message", "type": "textbox", "ref": "textbox[Message]", "value": "Hello, I have a question..."}
   ]

4. browser_click
   element: "Submit button"
   ref: "button[Submit]"

5. browser_wait_for
   text: "Thank you"

6. browser_snapshot
   (verify success state)
```

### Multi-Step Form (Wizard)

**Goal:** Complete a multi-step registration

**Steps:**
```
# Step 1: Personal Info
1. browser_navigate
   url: "https://example.com/register"

2. browser_snapshot

3. browser_fill_form
   fields: [
     {"name": "First Name", "type": "textbox", "ref": "textbox[First Name]", "value": "John"},
     {"name": "Last Name", "type": "textbox", "ref": "textbox[Last Name]", "value": "Doe"}
   ]

4. browser_click
   element: "Next button"
   ref: "button[Next]"

# Step 2: Contact Info
5. browser_wait_for
   text: "Contact Information"

6. browser_snapshot

7. browser_fill_form
   fields: [
     {"name": "Email", "type": "textbox", "ref": "textbox[Email]", "value": "john@example.com"},
     {"name": "Phone", "type": "textbox", "ref": "textbox[Phone]", "value": "555-1234"}
   ]

8. browser_click
   element: "Next button"
   ref: "button[Next]"

# Step 3: Preferences
9. browser_wait_for
   text: "Preferences"

10. browser_snapshot

11. browser_fill_form
    fields: [
      {"name": "Newsletter", "type": "checkbox", "ref": "checkbox[Newsletter]", "value": "true"}
    ]

12. browser_click
    element: "Complete Registration"
    ref: "button[Complete]"

13. browser_wait_for
    text: "Registration Complete"
```

### Form with File Upload

**Goal:** Submit application with documents

**Steps:**
```
1. browser_navigate
   url: "https://jobs.example.com/apply"

2. browser_snapshot

3. browser_fill_form
   fields: [
     {"name": "Name", "type": "textbox", "ref": "textbox[Name]", "value": "John Doe"},
     {"name": "Email", "type": "textbox", "ref": "textbox[Email]", "value": "john@example.com"},
     {"name": "Position", "type": "combobox", "ref": "combobox[Position]", "value": "Software Engineer"}
   ]

4. browser_click
   element: "Upload Resume button"
   ref: "button[Upload Resume]"

5. browser_file_upload
   paths: ["C:/Users/john/Documents/resume.pdf"]

6. browser_wait_for
   text: "resume.pdf"  (confirm upload)

7. browser_click
   element: "Upload Cover Letter"
   ref: "button[Upload Cover Letter]"

8. browser_file_upload
   paths: ["C:/Users/john/Documents/cover-letter.pdf"]

9. browser_click
   element: "Submit Application"
   ref: "button[Submit]"

10. browser_wait_for
    text: "Application Submitted"
```

---

## Testing Workflows

### Login Flow Testing

**Goal:** Verify login functionality

**Steps:**
```
# Test 1: Valid Login
1. browser_navigate
   url: "https://app.example.com/login"

2. browser_snapshot

3. browser_type
   element: "Username"
   ref: "textbox[Username]"
   text: "testuser"

4. browser_type
   element: "Password"
   ref: "textbox[Password]"
   text: "validpassword"
   submit: true

5. browser_wait_for
   text: "Dashboard"

6. browser_take_screenshot
   filename: "login-success.png"

# Test 2: Invalid Login
7. browser_navigate
   url: "https://app.example.com/login"

8. browser_type
   element: "Username"
   ref: "textbox[Username]"
   text: "testuser"

9. browser_type
   element: "Password"
   ref: "textbox[Password]"
   text: "wrongpassword"
   submit: true

10. browser_wait_for
    text: "Invalid credentials"

11. browser_take_screenshot
    filename: "login-failure.png"
```

### E2E Checkout Testing

**Goal:** Test complete purchase flow

**Steps:**
```
1. browser_navigate
   url: "https://shop.example.com"

2. browser_snapshot

3. browser_click
   element: "Product"
   ref: "link[Blue Widget]"

4. browser_wait_for
   text: "Blue Widget"

5. browser_click
   element: "Add to Cart"
   ref: "button[Add to Cart]"

6. browser_wait_for
   text: "Added to cart"

7. browser_click
   element: "View Cart"
   ref: "link[Cart (1)]"

8. browser_wait_for
   text: "Shopping Cart"

9. browser_snapshot
   (verify cart contents)

10. browser_click
    element: "Checkout"
    ref: "button[Checkout]"

11. browser_fill_form
    fields: [
      {"name": "Address", "type": "textbox", "ref": "textbox[Address]", "value": "123 Test St"},
      {"name": "City", "type": "textbox", "ref": "textbox[City]", "value": "Test City"},
      {"name": "Zip", "type": "textbox", "ref": "textbox[Zip]", "value": "12345"}
    ]

12. browser_click
    element: "Continue to Payment"
    ref: "button[Continue]"

# (Continue with payment flow...)
```

### Visual Regression Testing

**Goal:** Capture screenshots for visual comparison

**Steps:**
```
1. browser_navigate
   url: "https://example.com"

2. browser_resize
   width: 1920
   height: 1080

3. browser_wait_for
   time: 2

4. browser_take_screenshot
   fullPage: true
   filename: "homepage-desktop-1920.png"

5. browser_resize
   width: 768
   height: 1024

6. browser_take_screenshot
   fullPage: true
   filename: "homepage-tablet-768.png"

7. browser_resize
   width: 375
   height: 812

8. browser_take_screenshot
   fullPage: true
   filename: "homepage-mobile-375.png"
```

---

## Data Entry Workflows

### Bulk Data Entry

**Goal:** Enter multiple records efficiently

**Steps:**
```
# For each record in dataset:

1. browser_navigate
   url: "https://admin.example.com/new-record"

2. browser_snapshot
   (first time only, cache field refs)

3. browser_fill_form
   fields: [
     {"name": "Title", "type": "textbox", "ref": "textbox[Title]", "value": "{record.title}"},
     {"name": "Description", "type": "textbox", "ref": "textbox[Description]", "value": "{record.description}"},
     {"name": "Category", "type": "combobox", "ref": "combobox[Category]", "value": "{record.category}"}
   ]

4. browser_click
   element: "Save"
   ref: "button[Save]"

5. browser_wait_for
   text: "Saved successfully"

# Repeat for next record
```

### Copy Data Between Systems

**Goal:** Transfer data from one app to another

**Steps:**
```
# Tab 1: Source System
1. browser_navigate
   url: "https://source-system.com/data"

2. browser_snapshot

3. browser_evaluate
   function: "() => {
     // Extract data to transfer
     return Array.from(document.querySelectorAll('.record')).map(r => ({
       name: r.querySelector('.name').textContent,
       email: r.querySelector('.email').textContent
     }))
   }"

# Tab 2: Target System
4. browser_tabs
   action: "new"

5. browser_navigate
   url: "https://target-system.com/import"

6. browser_snapshot

# For each extracted record:
7. browser_fill_form
   fields: [
     {"name": "Name", "type": "textbox", "ref": "textbox[Name]", "value": "{record.name}"},
     {"name": "Email", "type": "textbox", "ref": "textbox[Email]", "value": "{record.email}"}
   ]

8. browser_click
   element: "Add Record"
   ref: "button[Add]"

9. browser_wait_for
   text: "Record added"
```

---

## Monitoring Workflows

### Page Status Monitoring

**Goal:** Check if page loads correctly

**Steps:**
```
1. browser_navigate
   url: "https://example.com"

2. browser_console_messages
   level: "error"
   (check for JavaScript errors)

3. browser_network_requests
   includeStatic: false
   (check for failed API calls)

4. browser_snapshot
   (verify expected content present)

5. browser_take_screenshot
   filename: "status-check-{timestamp}.png"
```

### Performance Monitoring

**Goal:** Capture performance metrics

**Steps:**
```
1. browser_navigate
   url: "https://example.com"

2. browser_evaluate
   function: "() => {
     const timing = performance.timing;
     return {
       dns: timing.domainLookupEnd - timing.domainLookupStart,
       connection: timing.connectEnd - timing.connectStart,
       ttfb: timing.responseStart - timing.requestStart,
       domLoad: timing.domContentLoadedEventEnd - timing.navigationStart,
       fullLoad: timing.loadEventEnd - timing.navigationStart
     }
   }"

3. browser_evaluate
   function: "() => {
     return performance.getEntriesByType('resource').map(r => ({
       name: r.name,
       duration: r.duration,
       size: r.transferSize
     }))
   }"
```

---

## Authentication Workflows

### Basic Login

**Steps:**
```
1. browser_navigate
   url: "https://app.example.com/login"

2. browser_snapshot

3. browser_fill_form
   fields: [
     {"name": "Email", "type": "textbox", "ref": "textbox[Email]", "value": "user@example.com"},
     {"name": "Password", "type": "textbox", "ref": "textbox[Password]", "value": "securepassword"}
   ]

4. browser_click
   element: "Sign In"
   ref: "button[Sign In]"

5. browser_wait_for
   text: "Welcome"
```

### OAuth Login (Google/GitHub)

**Steps:**
```
1. browser_navigate
   url: "https://app.example.com/login"

2. browser_snapshot

3. browser_click
   element: "Sign in with Google"
   ref: "button[Sign in with Google]"

4. browser_wait_for
   text: "Sign in with Google"

5. browser_snapshot
   (Google auth page)

6. browser_type
   element: "Email"
   ref: "textbox[Email or phone]"
   text: "user@gmail.com"
   submit: true

7. browser_wait_for
   text: "Enter your password"

8. browser_type
   element: "Password"
   ref: "textbox[Enter your password]"
   text: "password"
   submit: true

9. browser_wait_for
   text: "Welcome"  (back on original app)
```

### Two-Factor Authentication

**Steps:**
```
# After initial login...

1. browser_wait_for
   text: "Enter verification code"

2. browser_snapshot

# If TOTP (app-based):
3. (Get code from authenticator app externally)

4. browser_type
   element: "Verification code"
   ref: "textbox[Enter code]"
   text: "123456"
   submit: true

# If SMS:
# Wait for user to provide code

5. browser_wait_for
   text: "Dashboard"
```

---

## Tips for All Workflows

### Error Recovery

Always include error handling:
```
1. After critical actions, verify success
2. Take screenshots on failure
3. Check console for errors
4. Retry transient failures
```

### Performance Optimization

- Use `browser_fill_form` for multiple fields (single request)
- Avoid unnecessary `browser_snapshot` calls
- Use `browser_wait_for` with specific text rather than fixed delays
- Close browser when done

### Reliability

- Always wait for page state before interactions
- Use unique element identifiers when possible
- Handle dynamic content with appropriate waits
- Check for and dismiss unexpected dialogs
