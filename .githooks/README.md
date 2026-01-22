# 🔒 Git Hooks for Security

This directory contains Git hooks to prevent accidental commits of sensitive data.

## Available Hooks

| Hook | Purpose |
|------|---------|
| `pre-commit` | Scans staged files for secrets, credentials, API keys, and PII |

## Installation

To enable these hooks, run one of the following commands from the repository root:

### Option 1: Configure Git to use this hooks directory (Recommended)

```bash
git config core.hooksPath .githooks
```

### Option 2: Copy hooks to .git/hooks

```bash
cp .githooks/* .git/hooks/
chmod +x .git/hooks/*
```

## What the Pre-Commit Hook Detects

### 🚫 Blocked (High-Risk Secrets)

These patterns will **block the commit**:

| Category | Examples |
|----------|----------|
| Azure Storage Keys | `AccountKey=...`, `SharedAccessSignature=sv=...` |
| AWS Credentials | `AKIA...`, `aws_secret_access_key=...` |
| API Keys | `api_key=...`, `apikey:...` |
| Private Keys | `-----BEGIN PRIVATE KEY-----` |
| Connection Strings | `Password=...` in connection strings |
| JWT Tokens | `eyJ...` format tokens |
| GitHub Tokens | `ghp_...`, `gho_...`, etc. |
| Slack Tokens | `xox[baprs]-...` |
| Client Secrets | `client_secret=...` |

### ⚠️ Warnings (Potential PII)

These patterns will **warn but not block**:

| Category | Pattern |
|----------|---------|
| SSN | `XXX-XX-XXXX` format (raw, not masked) |
| Credit Cards | 16-digit card numbers |
| Email Addresses | In code files (not documentation) |

### ✅ Automatically Skipped

These files are not scanned:

- Markdown files (`*.md`)
- Sample/example files (`*.sample`, `*.example`)
- Test files (`test_*.py`, `*_test.py`, `conftest.py`)
- Sample data (`sample-data/*.csv`)
- Environment templates (`.env.sample`, `.env.example`)

## Bypassing the Hook

If you're certain a detection is a false positive:

```bash
git commit --no-verify -m "Your commit message"
```

> ⚠️ **Use with caution!** Only bypass after confirming the flagged content is not sensitive.

## Troubleshooting

### Hook not running?

1. Ensure the hook is executable:
   ```bash
   chmod +x .githooks/pre-commit
   ```

2. Verify Git is configured to use the hooks:
   ```bash
   git config --get core.hooksPath
   ```

### False positives?

If a legitimate pattern is being flagged:

1. Check if the file should be added to `SKIP_PATTERNS` in the hook
2. Consider if the pattern can be refactored (e.g., use environment variables)
3. As a last resort, use `--no-verify`

## Best Practices

1. **Never commit real credentials** - Use environment variables or Key Vault
2. **Use `.env.sample`** - Document required variables without real values
3. **Mask PII in sample data** - Hash SSNs, mask names and emails
4. **Review before bypassing** - Always verify false positives manually
5. **Enable hooks for all team members** - Include setup in onboarding docs
