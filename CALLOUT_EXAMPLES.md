# Visual Callout Examples - Before and After

## Example 1: Important Setup Information

### BEFORE ❌
\\\markdown
> ℹ️ **Note:** Ensure all required values in .env are populated before proceeding.
\\\

### AFTER ✅
\\\markdown
> 📝 **Note:** Ensure all required values in .env are populated before proceeding.
\\\

**Why better:** 📝 emoji provides clearer visual hierarchy than generic ℹ️

---

## Example 2: Critical Warning

### BEFORE ❌
\\\markdown
> ⚠️ **Warning:** If your capacity is paused, notebooks and data processing will not work.
\\\

### AFTER ✅
\\\markdown
> ⚠️ **Warning:** If your capacity is paused, notebooks and data processing will not work. 
> Ensure the capacity is in "Active" state before proceeding. Resume can take 2-3 minutes.
\\\

**Why better:** Added actionable context and time expectations

---

## Example 3: Helpful Pro Tip (NEW)

### BEFORE ❌
\\\markdown
> ℹ️ **Note:** Always run what-if analysis before deployment to review changes.
\\\

### AFTER ✅
\\\markdown
> 💡 **Pro Tip:** Always run what-if analysis before deployment to preview resource changes 
> and catch potential issues early.
\\\

**Why better:** 
- Changed from generic "Note" to actionable "Pro Tip"
- Added specific benefits (preview changes, catch issues)
- 💡 emoji indicates this is helpful advice

---

## Example 4: Prerequisites Context

### BEFORE ❌
\\\markdown
Before starting, ensure you have:
- [ ] Azure subscription with Fabric enabled
\\\

### AFTER ✅
\\\markdown
Before starting, ensure you have:
- [ ] Azure subscription with Fabric enabled

> 📋 **Prerequisites:** If you don't have a Fabric capacity, you can start a free trial 
> at app.fabric.microsoft.com. Trial capacity provides 60 days of limited compute units.
\\\

**Why better:** Provides alternative path for users without capacity

---

## Callout Pattern Reference

### 💡 Pro Tip
**Use for:**
- Performance optimizations
- Time-saving techniques  
- Best practices
- Expert insights

**Example:**
\\\markdown
> 💡 **Pro Tip:** Enable auto-pause on dev environments to reduce costs by up to 76%.
\\\

---

### ⚠️ Warning
**Use for:**
- Potential pitfalls
- Security concerns
- Destructive operations
- Time-sensitive issues

**Example:**
\\\markdown
> ⚠️ **Warning:** Resource deletion is irreversible. Ensure backups exist before cleanup.
\\\

---

### 📝 Note
**Use for:**
- Additional context
- Clarifications
- Design decisions
- Important details

**Example:**
\\\markdown
> 📝 **Note:** This architecture is designed for POC. Production requires additional 
> security controls and compliance certifications.
\\\

---

### 📋 Prerequisites
**Use for:**
- Required items
- Dependencies
- Preparation steps
- Access requirements

**Example:**
\\\markdown
> 📋 **Prerequisites:** Complete the full Prerequisites Guide before starting deployment. 
> This includes Azure subscription setup, tool installation, and resource provider registration.
\\\

---

## Markdown Rendering

All callouts use standard Markdown blockquote syntax:

\\\markdown
> [emoji] **[Label]:** [Message text]
\\\

**Benefits:**
✅ Renders in GitHub, Azure DevOps, GitLab, Bitbucket
✅ Works in VS Code preview
✅ Accessible to screen readers
✅ No custom CSS required
✅ Easy to search and maintain

---

## Accessibility Considerations

- **Emoji + Text Label:** Screen readers announce both the emoji description and text label
- **Bold Labels:** Clearly distinguish the callout type
- **Blockquote Syntax:** Standard semantic HTML makes it accessible
- **Consistent Pattern:** Users learn to recognize callout types quickly

---

Generated: 2026-01-27 23:54:38
