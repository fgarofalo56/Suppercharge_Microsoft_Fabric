# GitHub Skill Reference Documentation

Complete reference for all GitHub operations available through this Claude Code skill.

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Authentication](#authentication)
3. [Helper Scripts](#helper-scripts)
4. [API Reference by Category](#api-reference-by-category)
5. [GraphQL Operations](#graphql-operations)
6. [Troubleshooting](#troubleshooting)
7. [Rate Limits](#rate-limits)
8. [Common Patterns](#common-patterns)

---

## Installation & Setup

### Prerequisites

1. **Install gh CLI**:
   - Windows: `winget install GitHub.cli` or `choco install gh`
   - macOS: `brew install gh`
   - Linux: `sudo apt install gh` or see https://cli.github.com/

2. **Authenticate**:
   ```bash
   gh auth login
   ```

3. **Verify Installation**:
   ```bash
   gh --version
   gh auth status
   ```

### Deploying This Skill

```bash
# Copy to personal skills folder
cp -r skills/github ~/.claude/skills/

# Or copy to project
cp -r skills/github /path/to/project/.claude/skills/
```

---

## Authentication

### Login Methods

```bash
# Interactive login (recommended)
gh auth login

# Login with token
gh auth login --with-token < token.txt

# Login to GitHub Enterprise
gh auth login --hostname github.mycompany.com
```

### Managing Auth

```bash
# Check status
gh auth status

# Show token (be careful!)
gh auth token

# Refresh credentials
gh auth refresh

# Add scopes
gh auth refresh --scopes repo,read:org

# Switch accounts
gh auth switch

# Logout
gh auth logout
```

### Required Scopes by Operation

| Operation | Required Scopes |
|-----------|-----------------|
| Public repos | `public_repo` |
| Private repos | `repo` |
| Workflows | `workflow` |
| Packages | `read:packages`, `write:packages` |
| Organizations | `read:org` |
| Users | `read:user` |
| Gists | `gist` |
| Notifications | `notifications` |
| Code scanning | `security_events` |
| Dependabot | `security_events` |
| Secret scanning | `security_events` |

---

## Helper Scripts

### Python Helper (`github_helper.py`)

Located at `scripts/github_helper.py`.

#### Commands

```bash
# Batch labeling
python github_helper.py batch-label owner/repo --issues 1,2,3 --add bug,urgent

# Batch assignment
python github_helper.py batch-assign owner/repo --issues 1,2,3 --assignees user1,user2

# Bulk close issues
python github_helper.py bulk-close owner/repo --issues 1,2,3 --comment "Closing as duplicate"

# Clone issues between repos
python github_helper.py clone-issues source/repo target/repo --labels enhancement

# PR statistics
python github_helper.py pr-stats owner/repo --days 30

# Workflow summary
python github_helper.py workflow-summary owner/repo --limit 50

# Security report
python github_helper.py security-report owner/repo --output report.json

# Search and export
python github_helper.py search-and-export "language:python stars:>1000" --type repos --output results.json

# File tree with filters
python github_helper.py file-tree owner/repo --path src --ext .py,.js --depth 3

# Compare branches
python github_helper.py compare-branches owner/repo main feature-branch
```

### Bash Helper (`batch_operations.sh`)

Located at `scripts/batch_operations.sh`.

```bash
# Source the script
source scripts/batch_operations.sh

# Clone all repos from org
clone_org_repos microsoft ./repos 50

# Close issues by label
close_issues_by_label owner/repo "wontfix" "not planned"

# Close stale PRs
close_stale_prs owner/repo 90 "Closing due to inactivity"

# Approve PRs from trusted user
approve_prs_from_user owner/repo dependabot

# Cancel running workflows
cancel_running_workflows owner/repo

# Rerun failed workflows
rerun_failed_workflows owner/repo 10

# Download latest artifacts
download_latest_artifacts owner/repo ci.yml ./artifacts

# Delete pre-releases
delete_prereleases owner/repo

# Export security alerts
export_security_alerts owner/repo security-report.json

# Activity report
activity_report owner/repo 7
```

---

## API Reference by Category

### Repositories

#### Get Repository Info
```bash
gh repo view owner/repo
gh repo view owner/repo --json name,description,url,stargazersCount
```

#### Create Repository
```bash
# Public
gh repo create my-repo --public --description "My repo"

# Private with README
gh repo create my-repo --private --add-readme

# From template
gh repo create my-repo --template owner/template

# Clone after create
gh repo create my-repo --clone
```

#### Fork Repository
```bash
gh repo fork owner/repo
gh repo fork owner/repo --clone
gh repo fork owner/repo --org my-org
```

#### Delete Repository
```bash
gh repo delete owner/repo --yes
```

#### Repository Settings (via API)
```bash
# Update description
gh api repos/{owner}/{repo} -X PATCH -f description="New description"

# Make private
gh api repos/{owner}/{repo} -X PATCH -F private=true

# Enable/disable features
gh api repos/{owner}/{repo} -X PATCH -F has_wiki=false -F has_issues=true
```

### Files & Content

#### Read File
```bash
# Get decoded content
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 --decode

# Get raw content via URL
gh api repos/{owner}/{repo}/contents/{path} --jq '.download_url' | xargs curl -sL
```

#### Create/Update File
```bash
# Create new file
gh api repos/{owner}/{repo}/contents/{path} \
  -X PUT \
  -f message="Add file" \
  -f content="$(echo -n 'content' | base64)"

# Update existing (needs SHA)
SHA=$(gh api repos/{owner}/{repo}/contents/{path} --jq '.sha')
gh api repos/{owner}/{repo}/contents/{path} \
  -X PUT \
  -f message="Update" \
  -f content="$(echo -n 'new content' | base64)" \
  -f sha="$SHA"
```

#### Delete File
```bash
SHA=$(gh api repos/{owner}/{repo}/contents/{path} --jq '.sha')
gh api repos/{owner}/{repo}/contents/{path} \
  -X DELETE \
  -f message="Delete file" \
  -f sha="$SHA"
```

#### List Directory
```bash
gh api repos/{owner}/{repo}/contents/{path} --jq '.[] | "\(.type)\t\(.name)"'
```

### Branches

#### List Branches
```bash
gh api repos/{owner}/{repo}/branches --jq '.[].name'

# With protection status
gh api repos/{owner}/{repo}/branches --jq '.[] | "\(.name)\t\(.protected)"'
```

#### Create Branch
```bash
# Get SHA of source branch
SHA=$(gh api repos/{owner}/{repo}/git/ref/heads/main --jq '.object.sha')

# Create new branch
gh api repos/{owner}/{repo}/git/refs \
  -X POST \
  -f ref="refs/heads/new-branch" \
  -f sha="$SHA"
```

#### Delete Branch
```bash
gh api repos/{owner}/{repo}/git/refs/heads/{branch} -X DELETE
```

#### Branch Protection
```bash
# Get protection rules
gh api repos/{owner}/{repo}/branches/{branch}/protection

# Set protection
gh api repos/{owner}/{repo}/branches/{branch}/protection \
  -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["ci"]}' \
  -F enforce_admins=true
```

### Commits

#### List Commits
```bash
gh api repos/{owner}/{repo}/commits --jq '.[] | "\(.sha[:7]) \(.commit.message | split("\n")[0])"'

# On specific branch
gh api "repos/{owner}/{repo}/commits?sha=develop" --jq '.[:10] | .[].sha[:7]'

# By author
gh api "repos/{owner}/{repo}/commits?author=username" --jq '.[].sha[:7]'
```

#### Get Commit Details
```bash
gh api repos/{owner}/{repo}/commits/{sha}

# Get diff
gh api repos/{owner}/{repo}/commits/{sha} --jq '.files[] | "\(.filename): +\(.additions) -\(.deletions)"'
```

#### Compare Commits
```bash
gh api repos/{owner}/{repo}/compare/{base}...{head} \
  --jq '{ahead: .ahead_by, behind: .behind_by, commits: .total_commits}'
```

### Issues

#### Create Issue
```bash
gh issue create -R owner/repo \
  --title "Bug: Something broken" \
  --body "Description" \
  --label bug,urgent \
  --assignee @me \
  --milestone "v1.0"
```

#### List Issues
```bash
# Basic list
gh issue list -R owner/repo

# With filters
gh issue list -R owner/repo \
  --state open \
  --label bug \
  --assignee @me \
  --limit 50

# JSON output
gh issue list -R owner/repo --json number,title,state,labels
```

#### Update Issue
```bash
gh issue edit 123 -R owner/repo \
  --title "New title" \
  --body "New body" \
  --add-label priority:high \
  --remove-label needs-triage \
  --add-assignee user1
```

#### Close Issue
```bash
gh issue close 123 -R owner/repo
gh issue close 123 -R owner/repo --comment "Fixed in #456"
gh issue close 123 -R owner/repo --reason "not planned"
```

#### Issue Comments
```bash
# Add comment
gh issue comment 123 -R owner/repo --body "Comment text"

# List comments via API
gh api repos/{owner}/{repo}/issues/123/comments --jq '.[] | "\(.user.login): \(.body | split("\n")[0])"'
```

### Pull Requests

#### Create PR
```bash
gh pr create -R owner/repo \
  --title "Add feature" \
  --body "Description" \
  --base main \
  --head feature-branch \
  --reviewer user1,user2 \
  --label enhancement
```

#### List PRs
```bash
gh pr list -R owner/repo
gh pr list -R owner/repo --state all --base main --author @me

# JSON output
gh pr list -R owner/repo --json number,title,state,reviewDecision
```

#### Review PR
```bash
# Approve
gh pr review 123 -R owner/repo --approve

# Request changes
gh pr review 123 -R owner/repo --request-changes --body "Please fix X"

# Comment
gh pr review 123 -R owner/repo --comment --body "Looks good"
```

#### Merge PR
```bash
# Merge commit
gh pr merge 123 -R owner/repo --merge

# Squash
gh pr merge 123 -R owner/repo --squash

# Rebase
gh pr merge 123 -R owner/repo --rebase

# Auto-merge
gh pr merge 123 -R owner/repo --auto --squash
```

#### PR Diff
```bash
gh pr diff 123 -R owner/repo
gh pr diff 123 -R owner/repo -- path/to/file
```

### GitHub Actions

#### Workflows
```bash
# List workflows
gh workflow list -R owner/repo

# Run workflow
gh workflow run ci.yml -R owner/repo
gh workflow run ci.yml -R owner/repo -f param=value --ref develop

# Enable/disable
gh workflow enable ci.yml -R owner/repo
gh workflow disable ci.yml -R owner/repo
```

#### Workflow Runs
```bash
# List runs
gh run list -R owner/repo
gh run list -R owner/repo --workflow ci.yml --status failure

# View run
gh run view 123456 -R owner/repo
gh run view 123456 -R owner/repo --verbose

# Watch run
gh run watch 123456 -R owner/repo

# Cancel run
gh run cancel 123456 -R owner/repo

# Rerun
gh run rerun 123456 -R owner/repo
gh run rerun 123456 -R owner/repo --failed
```

#### Artifacts
```bash
# List artifacts
gh run view 123456 -R owner/repo --json artifacts

# Download all
gh run download 123456 -R owner/repo

# Download specific
gh run download 123456 -R owner/repo --name artifact-name --dir ./output
```

#### Logs
```bash
gh run view 123456 -R owner/repo --log
gh run view 123456 -R owner/repo --log-failed
```

### Releases

#### Create Release
```bash
gh release create v1.0.0 -R owner/repo \
  --title "Version 1.0.0" \
  --notes "Release notes here"

# With assets
gh release create v1.0.0 -R owner/repo ./dist/*.zip

# Draft
gh release create v1.0.0 -R owner/repo --draft

# Pre-release
gh release create v1.0.0-beta -R owner/repo --prerelease

# Generate notes
gh release create v1.0.0 -R owner/repo --generate-notes
```

#### List Releases
```bash
gh release list -R owner/repo
```

#### Download Release Assets
```bash
gh release download v1.0.0 -R owner/repo
gh release download v1.0.0 -R owner/repo --pattern "*.zip"
```

#### Delete Release
```bash
gh release delete v1.0.0 -R owner/repo --yes
```

### Gists

```bash
# Create
gh gist create file.py --public --desc "My gist"

# List
gh gist list

# View
gh gist view abc123

# Edit
gh gist edit abc123

# Clone
gh gist clone abc123

# Delete
gh gist delete abc123
```

### Projects (v2)

```bash
# List projects
gh project list
gh project list --owner org-name

# View project
gh project view 1

# Create project
gh project create --title "My Project"

# Add item
gh project item-add 1 --url https://github.com/owner/repo/issues/123

# List items
gh project item-list 1

# Fields
gh project field-list 1
```

---

## GraphQL Operations

For features not available via REST API, use GraphQL:

### Basic Query
```bash
gh api graphql -f query='
query {
  viewer {
    login
    name
  }
}'
```

### Query with Variables
```bash
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    name
    stargazerCount
    issues(states: OPEN) {
      totalCount
    }
  }
}' -f owner="microsoft" -f repo="vscode"
```

### Discussions (GraphQL only)
```bash
# List discussions
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    discussions(first: 10) {
      nodes {
        number
        title
        author { login }
      }
    }
  }
}' -f owner="owner" -f repo="repo"
```

### Get Node ID (for mutations)
```bash
# Get repository ID
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    id
  }
}' -f owner="owner" -f repo="repo"
```

---

## Troubleshooting

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| `gh: command not found` | gh not installed | Install gh CLI |
| `not logged in` | No authentication | Run `gh auth login` |
| `HTTP 401` | Bad/expired token | Run `gh auth refresh` |
| `HTTP 403` | Insufficient permissions | Check scopes, refresh auth |
| `HTTP 404` | Resource not found | Verify repo/resource exists |
| `HTTP 422` | Invalid request | Check parameters |
| `rate limit exceeded` | Too many requests | Wait or authenticate |

### Debug Mode

```bash
# Verbose output
GH_DEBUG=1 gh api repos/owner/repo

# See HTTP requests
GH_DEBUG=api gh pr list
```

### Check Rate Limits

```bash
gh api rate_limit --jq '.resources | to_entries[] | "\(.key): \(.value.remaining)/\(.value.limit)"'
```

### Reset Authentication

```bash
gh auth logout
gh auth login
```

---

## Rate Limits

| Type | Limit (authenticated) | Limit (unauthenticated) |
|------|----------------------|------------------------|
| REST API | 5,000/hour | 60/hour |
| Search API | 30/minute | 10/minute |
| GraphQL | 5,000 points/hour | N/A |
| Secondary | Varies | Varies |

### Handling Rate Limits

```bash
# Check remaining
gh api rate_limit --jq '.resources.core.remaining'

# Wait for reset
RESET=$(gh api rate_limit --jq '.resources.core.reset')
echo "Reset at: $(date -d @$RESET)"
```

---

## Common Patterns

### Pagination

```bash
# Manual pagination
gh api "repos/{owner}/{repo}/issues?per_page=100&page=1"
gh api "repos/{owner}/{repo}/issues?per_page=100&page=2"

# Auto-paginate with --paginate
gh api repos/{owner}/{repo}/issues --paginate --jq '.[].number'
```

### JSON Processing

```bash
# Filter with jq
gh issue list --json number,title --jq '.[] | select(.title | contains("bug"))'

# Format output
gh pr list --json number,title,author --jq '.[] | "#\(.number) \(.title) by \(.author.login)"'
```

### Conditional Logic

```bash
# Check if PR is mergeable
MERGEABLE=$(gh pr view 123 --json mergeable --jq '.mergeable')
if [[ "$MERGEABLE" == "MERGEABLE" ]]; then
  gh pr merge 123
fi
```

### Error Handling

```bash
# Check exit code
if gh issue view 123 &>/dev/null; then
  echo "Issue exists"
else
  echo "Issue not found"
fi
```

### Environment Variables

```bash
# Set default repo
export GH_REPO=owner/repo
gh issue list  # Uses GH_REPO

# Set token
export GH_TOKEN=ghp_xxxx
gh api user

# Set enterprise host
export GH_HOST=github.mycompany.com
gh auth login
```

---

## Additional Resources

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [GitHub API Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
