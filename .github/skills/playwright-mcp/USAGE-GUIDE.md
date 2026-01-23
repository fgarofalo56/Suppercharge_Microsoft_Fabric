# Playwright MCP - Complete Usage Guide

Comprehensive guide to using the Playwright MCP skill with Claude Code, including detailed use cases, examples, and invocation patterns.

## Table of Contents

- [How to Invoke This Skill](#how-to-invoke-this-skill)
- [Complete Use Cases](#complete-use-cases)
- [Integration Patterns](#integration-patterns)
- [Common Workflows](#common-workflows)
- [Advanced Examples](#advanced-examples)

---

## How to Invoke This Skill

### Automatic Activation

Claude automatically activates this skill when you use these **trigger keywords**:

- `playwright`, `browser`, `web browser`
- `screenshot`, `capture`, `snapshot`
- `web scraping`, `scrape`, `extract data`
- `form automation`, `fill form`, `submit form`
- `test website`, `browser test`, `e2e test`
- `navigate to`, `visit website`
- `click`, `hover`, `interact`

### Explicit Requests

Be explicit about using Playwright for best results:

```
✅ GOOD: "Use Playwright to navigate to example.com and take a screenshot"
✅ GOOD: "With the Playwright skill, automate filling the contact form"
✅ GOOD: "Test the login flow using browser automation"

⚠️ VAGUE: "Take a picture of the website"
⚠️ VAGUE: "Fill out the form"
```

### Example Invocation Patterns

```bash
# Web scraping
"Use Playwright to scrape product information from this e-commerce site"

# Testing
"Test my web app's checkout flow with browser automation"

# Form automation
"Automate filling and submitting this registration form"

# Screenshots
"Capture full-page screenshots of all pages in this list"

# Monitoring
"Check if the website is loading correctly and capture any errors"
```

---

## Complete Use Cases

### Use Case 1: Web Scraping & Data Extraction

**Scenario**: Extract product information from an e-commerce website

**When to use**:
- Competitive analysis
- Price monitoring
- Content aggregation
- Market research

**Step-by-step workflow**:

1. **Request the task**:
```
"Use Playwright to scrape product names, prices, and descriptions from example-shop.com/products"
```

2. **Claude will**:
   - Navigate to the URL
   - Take a snapshot to understand page structure
   - Identify product elements
   - Extract data using selectors
   - Return structured data

3. **What you'll get**:
```json
{
  "products": [
    {
      "name": "Product Name",
      "price": "$29.99",
      "description": "Product description text",
      "url": "https://example-shop.com/products/123"
    }
  ]
}
```

**Advanced example**:
```
"Scrape the top 20 products from this category, including images, ratings, and availability status. Export to CSV."
```

**Tools used**:
- `browser_navigate` - Navigate to URL
- `browser_snapshot` - Capture page structure
- `browser_evaluate` - Extract data with JavaScript
- `browser_take_screenshot` - Visual verification (optional)

---

### Use Case 2: Form Automation

**Scenario**: Automate registration form filling and submission

**When to use**:
- Testing form validation
- Bulk data entry
- Automated account creation
- Form testing across browsers

**Step-by-step workflow**:

1. **Request the task**:
```
"Use Playwright to fill out the contact form at example.com/contact with test data and submit it"
```

2. **Provide form data** (if needed):
```
Name: John Doe
Email: john@example.com
Message: This is a test message
```

3. **Claude will**:
   - Navigate to the form
   - Analyze form structure
   - Fill all fields with provided data
   - Handle dropdowns, checkboxes, radio buttons
   - Submit the form
   - Verify submission success

4. **What you'll get**:
```
✓ Form filled successfully
✓ Submitted
✓ Confirmation: "Thank you for your message"
```

**Advanced example**:
```
"Fill out the multi-step registration form with these details, handle file upload, solve CAPTCHA if present, and verify email confirmation"
```

**Tools used**:
- `browser_navigate` - Go to form page
- `browser_snapshot` - Analyze form fields
- `browser_fill_form` - Fill multiple fields at once
- `browser_type` - Type into text fields
- `browser_click` - Submit button
- `browser_wait_for` - Wait for success message
- `browser_take_screenshot` - Capture result

---

### Use Case 3: End-to-End Testing

**Scenario**: Test a complete user workflow (login → dashboard → action → logout)

**When to use**:
- Pre-deployment testing
- Regression testing
- User acceptance testing
- Continuous integration

**Step-by-step workflow**:

1. **Request the task**:
```
"Use Playwright to test the following workflow on myapp.com:
1. Login with test credentials
2. Navigate to user dashboard
3. Create a new project
4. Verify project appears in list
5. Logout"
```

2. **Provide test data**:
```
Username: testuser@example.com
Password: TestPass123
Project name: Playwright Test Project
```

3. **Claude will**:
   - Execute each step systematically
   - Verify success at each stage
   - Take screenshots for documentation
   - Log any errors encountered
   - Provide detailed test results

4. **What you'll get**:
```
Test Results:
✓ Step 1: Login successful
✓ Step 2: Dashboard loaded
✓ Step 3: Project created
✓ Step 4: Project visible in list
✓ Step 5: Logout successful

Test Status: PASSED
Duration: 12.4 seconds
Screenshots: 5 captured
```

**Advanced example**:
```
"Run the checkout flow test 10 times with different payment methods and product combinations. Generate a test report with pass/fail rates."
```

**Tools used**:
- `browser_navigate` - Navigate between pages
- `browser_snapshot` - Verify page states
- `browser_fill_form` - Enter data
- `browser_click` - Interact with UI
- `browser_wait_for` - Wait for page loads
- `browser_take_screenshot` - Document test steps
- `browser_console_messages` - Check for errors
- `browser_network_requests` - Monitor API calls

---

### Use Case 4: Screenshot & Visual Documentation

**Scenario**: Capture screenshots for documentation, bug reports, or visual regression testing

**When to use**:
- Creating documentation
- Bug reporting
- Design review
- Visual regression testing
- Marketing materials

**Step-by-step workflow**:

1. **Request the task**:
```
"Use Playwright to capture full-page screenshots of all pages on mysite.com (homepage, about, services, contact)"
```

2. **Claude will**:
   - Navigate to each URL
   - Wait for page to fully load
   - Capture full-page screenshot
   - Save with descriptive filename
   - Organize screenshots

3. **What you'll get**:
```
Screenshots captured:
✓ homepage-2024-12-18.png (1920x3200)
✓ about-2024-12-18.png (1920x2400)
✓ services-2024-12-18.png (1920x2800)
✓ contact-2024-12-18.png (1920x1600)

Saved to: ./screenshots/
```

**Advanced examples**:

**Responsive screenshots**:
```
"Capture screenshots of the homepage at mobile (375px), tablet (768px), and desktop (1920px) widths"
```

**Element-specific screenshots**:
```
"Screenshot only the pricing table on the pricing page, excluding header and footer"
```

**Before/after comparison**:
```
"Take a screenshot before and after clicking the 'Dark Mode' toggle"
```

**Tools used**:
- `browser_navigate` - Go to pages
- `browser_resize` - Change viewport size
- `browser_take_screenshot` - Capture images (full-page or element-specific)
- `browser_wait_for` - Ensure content loaded

---

### Use Case 5: Website Monitoring & Health Checks

**Scenario**: Verify website functionality, check for errors, monitor performance

**When to use**:
- Production monitoring
- Uptime verification
- Error detection
- Performance tracking
- Post-deployment checks

**Step-by-step workflow**:

1. **Request the task**:
```
"Use Playwright to check myapp.com for:
- Page loads correctly
- No console errors
- Critical API calls succeed
- Login functionality works
- Response time under 3 seconds"
```

2. **Claude will**:
   - Navigate to the site
   - Monitor console for errors
   - Track network requests
   - Test key functionality
   - Measure performance
   - Generate health report

3. **What you'll get**:
```
Health Check Report - myapp.com
======================================

✓ Page Load: SUCCESS (2.1s)
✓ Console: No errors
✓ API Calls: 12/12 successful
✓ Login: WORKING
⚠ Warning: Slow API call /api/data (4.2s)

Status: HEALTHY
Recommendations:
- Optimize /api/data endpoint
```

**Advanced example**:
```
"Monitor these 5 critical pages every hour and alert me if:
- Page fails to load
- Console errors appear
- Response time > 5 seconds
- Any 404/500 errors
Generate a daily summary report"
```

**Tools used**:
- `browser_navigate` - Access pages
- `browser_console_messages` - Check for errors
- `browser_network_requests` - Monitor API calls
- `browser_snapshot` - Verify page structure
- `browser_evaluate` - Check page state
- `browser_take_screenshot` - Visual verification

---

### Use Case 6: Dynamic Content Interaction

**Scenario**: Interact with JavaScript-heavy single-page applications (SPAs)

**When to use**:
- Testing React/Vue/Angular apps
- Interacting with dynamic menus
- Handling infinite scroll
- Working with modal dialogs
- Testing real-time updates

**Step-by-step workflow**:

1. **Request the task**:
```
"Use Playwright to:
1. Click the 'Show More' button 5 times to load additional items
2. Open the user profile modal
3. Extract all loaded item titles"
```

2. **Claude will**:
   - Wait for JavaScript to initialize
   - Click the button multiple times
   - Wait for new content to load after each click
   - Handle dynamic elements
   - Extract data after all interactions

3. **What you'll get**:
```
Loaded 50 items (10 per page)
Extracted titles:
1. Item Title 1
2. Item Title 2
...
50. Item Title 50
```

**Advanced example**:
```
"Navigate through a multi-level dropdown menu to reach 'Settings > Account > Privacy', toggle all privacy options, and save changes"
```

**Tools used**:
- `browser_click` - Click dynamic elements
- `browser_wait_for` - Wait for content to appear/disappear
- `browser_hover` - Trigger hover menus
- `browser_evaluate` - Execute JavaScript
- `browser_snapshot` - Verify dynamic state changes

---

### Use Case 7: File Upload & Download Testing

**Scenario**: Test file upload functionality and download generated files

**When to use**:
- Testing document upload forms
- Verifying file processing
- Testing export features
- Downloading generated reports

**Step-by-step workflow**:

1. **Request the task**:
```
"Use Playwright to:
1. Navigate to the file upload page
2. Upload test-document.pdf
3. Verify upload success
4. Download the processed file"
```

2. **Claude will**:
   - Navigate to upload form
   - Select file from local system
   - Submit upload
   - Monitor upload progress
   - Verify success message
   - Download resulting file

3. **What you'll get**:
```
✓ File uploaded: test-document.pdf (2.3 MB)
✓ Processing completed in 4.2s
✓ Downloaded: test-document-processed.pdf (1.8 MB)
```

**Tools used**:
- `browser_navigate` - Go to upload page
- `browser_file_upload` - Select and upload files
- `browser_click` - Submit form
- `browser_wait_for` - Wait for processing
- `browser_network_requests` - Monitor upload/download

---

## Integration Patterns

### Pattern 1: Playwright + Testing Framework

Integrate Playwright skill with your test suite:

```python
# pytest example
def test_user_registration():
    """
    Request: "Use Playwright to test user registration with email user@test.com"
    """
    # Claude will execute the test using Playwright
    # You can verify results and assertions
    pass

def test_checkout_flow():
    """
    Request: "Test the complete checkout flow with test product ID 12345"
    """
    pass
```

### Pattern 2: Playwright + CI/CD

Use in continuous integration:

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run E2E tests
        run: |
          # Claude Code can be integrated here
          # Request: "Run all E2E tests using Playwright"
```

### Pattern 3: Playwright + Data Pipeline

Scraping as part of data workflow:

```python
# ETL pipeline example
def extract_data():
    """
    Request: "Use Playwright to scrape product data from competitor sites"
    Returns: JSON data for processing
    """
    pass

def transform_data(raw_data):
    # Your transformation logic
    pass

def load_data(transformed_data):
    # Load into database
    pass
```

### Pattern 4: Playwright + Monitoring

Automated health checks:

```python
# monitoring/health_check.py
def check_website_health():
    """
    Request: "Check website health including page load, API calls, and console errors"
    Returns: Health status report
    """
    pass

def alert_on_failure(report):
    if report['status'] != 'healthy':
        # Send alert
        pass
```

---

## Common Workflows

### Workflow 1: Competitive Analysis

```
Request to Claude:
"Use Playwright to:
1. Visit competitor websites A, B, C
2. Extract pricing information
3. Take screenshots of their pricing pages
4. Compare features against our product
5. Generate a competitive analysis report"
```

### Workflow 2: Automated Testing Suite

```
Request to Claude:
"Run the following test suite using Playwright:
1. Login/Logout tests
2. Form submission tests
3. Navigation tests
4. API integration tests
5. Error handling tests
Generate a summary report with pass/fail statistics"
```

### Workflow 3: Documentation Generation

```
Request to Claude:
"Use Playwright to:
1. Capture screenshots of all major features
2. Test and document the user journey
3. Extract help text and tooltips
4. Generate a visual user guide with screenshots and descriptions"
```

### Workflow 4: Performance Monitoring

```
Request to Claude:
"Use Playwright to measure:
1. Page load time for all critical pages
2. Time to interactive (TTI)
3. Network request count and sizes
4. JavaScript execution time
Generate a performance report with recommendations"
```

---

## Advanced Examples

### Example 1: Multi-Page Workflow with Data Extraction

**Request**:
```
"Use Playwright to scrape all job listings from jobs-site.com:
1. Start at the jobs listing page
2. Iterate through all pages (click 'Next' until no more pages)
3. For each job, extract: title, company, salary, location, description
4. Save results to jobs-data.json"
```

**Expected behavior**:
- Navigate to listing page
- Loop through pagination
- Extract structured data
- Handle potential errors
- Save to file

---

### Example 2: Complex Form with Conditional Logic

**Request**:
```
"Fill out the loan application form at bank.com/apply:
- If asked for employment type, select 'Full-time'
- If 'Full-time' is selected, fill annual income field
- Upload pay stub document
- Complete multi-step form (3 steps)
- Verify each step before proceeding
- Submit and capture confirmation number"
```

**Expected behavior**:
- Handle conditional form fields
- Navigate multi-step process
- Upload files
- Extract confirmation data

---

### Example 3: Authenticated Session with Data Operations

**Request**:
```
"Use Playwright to:
1. Login to admin dashboard with provided credentials
2. Navigate to Users section
3. Export user list to CSV
4. Search for user 'john@example.com'
5. Update user role to 'Administrator'
6. Verify change was saved
7. Logout"
```

**Expected behavior**:
- Maintain session throughout
- Handle authentication
- Perform CRUD operations
- Verify changes

---

### Example 4: Visual Regression Testing

**Request**:
```
"Perform visual regression testing:
1. Take baseline screenshots of homepage, product page, checkout
2. Switch to staging environment
3. Take comparison screenshots
4. Identify any visual differences
5. Generate a diff report with highlighted changes"
```

**Expected behavior**:
- Capture multiple screenshots
- Compare across environments
- Identify differences
- Create visual report

---

### Example 5: Real-Time Data Monitoring

**Request**:
```
"Monitor the live dashboard at metrics.myapp.com:
1. Capture initial state
2. Wait for real-time updates (observe for 2 minutes)
3. Capture any changes in metrics
4. Log all WebSocket messages
5. Alert if any metric drops below threshold"
```

**Expected behavior**:
- Monitor real-time updates
- Track WebSocket traffic
- Detect threshold violations
- Generate alerts

---

## Tips for Success

### 1. Be Specific with URLs
```
✅ GOOD: "Navigate to https://example.com/products/category/electronics"
❌ VAGUE: "Go to the electronics section"
```

### 2. Provide Test Data
```
✅ GOOD: "Fill form with: Name='John Doe', Email='john@test.com'"
❌ VAGUE: "Fill the form with test data"
```

### 3. Specify Success Criteria
```
✅ GOOD: "Verify the success message 'Registration complete' appears"
❌ VAGUE: "Make sure it worked"
```

### 4. Handle Edge Cases
```
✅ GOOD: "If CAPTCHA appears, skip and notify me"
❌ MISSING: Not mentioning how to handle CAPTCHAs
```

### 5. Request Screenshots for Verification
```
✅ GOOD: "Take a screenshot after each step for verification"
❌ MISSING: No visual confirmation of results
```

---

## Troubleshooting Common Issues

### Issue: "Element not found"
**Solution**: Ask Claude to take a snapshot first to identify correct selectors
```
"First take a snapshot of the page, then click the submit button"
```

### Issue: "Page loaded but content missing"
**Solution**: Add explicit wait conditions
```
"Wait for the product grid to load before extracting data"
```

### Issue: "Form submission failed"
**Solution**: Verify each step
```
"Fill the form, verify all fields are populated, then submit"
```

### Issue: "Session expired during workflow"
**Solution**: Check authentication
```
"Verify login status before each major operation"
```

---

## Additional Resources

- [SKILL.md](SKILL.md) - Main skill instructions
- [reference.md](reference.md) - Complete tool reference
- [workflows.md](workflows.md) - Workflow patterns
- [best-practices.md](best-practices.md) - Best practices guide
- [troubleshooting.md](troubleshooting.md) - Common issues and solutions

---

## Questions?

If you need help with a specific use case or run into issues:

1. Check the [troubleshooting guide](troubleshooting.md)
2. Review the [reference documentation](reference.md)
3. Try being more explicit in your request
4. Ask Claude to break down the task into smaller steps

**Example debug request**:
```
"I'm trying to scrape data from this site but getting errors. Can you:
1. Take a snapshot to see the page structure
2. Identify the correct selectors
3. Test extraction on one item first
4. Then scale to all items"
```
