#!/bin/bash
# GitHub Batch Operations Helper for Claude Code
# Provides shell functions for common bulk GitHub operations via gh CLI

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check gh is installed and authenticated
check_gh() {
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}Error: gh CLI not found. Install from https://cli.github.com/${NC}"
        exit 1
    fi

    if ! gh auth status &> /dev/null; then
        echo -e "${RED}Error: Not authenticated. Run 'gh auth login'${NC}"
        exit 1
    fi
}

# Print colored message
log() {
    local color="$1"
    shift
    echo -e "${color}$*${NC}"
}

# ============================================
# Repository Operations
# ============================================

# Clone multiple repositories from an organization
clone_org_repos() {
    local org="$1"
    local dest="${2:-.}"
    local limit="${3:-100}"

    check_gh
    log "$BLUE" "Cloning repos from $org..."

    gh repo list "$org" --limit "$limit" --json name,sshUrl --jq '.[] | .sshUrl' | while read -r url; do
        local repo_name=$(basename "$url" .git)
        if [[ -d "$dest/$repo_name" ]]; then
            log "$YELLOW" "Skipping $repo_name (already exists)"
        else
            log "$GREEN" "Cloning $repo_name..."
            gh repo clone "$url" "$dest/$repo_name"
        fi
    done

    log "$GREEN" "Done!"
}

# Archive multiple repositories
archive_repos() {
    local repos_file="$1"  # File with repo names, one per line

    check_gh

    while IFS= read -r repo; do
        [[ -z "$repo" || "$repo" =~ ^# ]] && continue
        log "$YELLOW" "Archiving $repo..."
        gh repo archive "$repo" --yes || log "$RED" "Failed to archive $repo"
    done < "$repos_file"
}

# ============================================
# Issue Operations
# ============================================

# Close all issues with a specific label
close_issues_by_label() {
    local repo="$1"
    local label="$2"
    local reason="${3:-completed}"

    check_gh
    log "$BLUE" "Closing issues with label '$label' in $repo..."

    gh issue list -R "$repo" --label "$label" --state open --json number --jq '.[].number' | while read -r num; do
        log "$YELLOW" "Closing issue #$num..."
        gh issue close "$num" -R "$repo" --reason "$reason"
    done

    log "$GREEN" "Done!"
}

# Transfer issues to another repository
transfer_issues() {
    local source_repo="$1"
    local target_repo="$2"
    local label="${3:-}"

    check_gh

    local jq_filter='.[].number'
    local gh_args=("-R" "$source_repo" "--state" "open" "--json" "number")

    if [[ -n "$label" ]]; then
        gh_args+=("--label" "$label")
    fi

    gh issue list "${gh_args[@]}" --jq "$jq_filter" | while read -r num; do
        log "$YELLOW" "Transferring issue #$num..."
        gh issue transfer "$num" "$target_repo" -R "$source_repo" || log "$RED" "Failed to transfer #$num"
    done

    log "$GREEN" "Done!"
}

# Add label to all open issues
label_all_open_issues() {
    local repo="$1"
    local label="$2"

    check_gh
    log "$BLUE" "Adding label '$label' to all open issues in $repo..."

    gh issue list -R "$repo" --state open --json number --jq '.[].number' | while read -r num; do
        log "$YELLOW" "Labeling issue #$num..."
        gh issue edit "$num" -R "$repo" --add-label "$label"
    done

    log "$GREEN" "Done!"
}

# ============================================
# Pull Request Operations
# ============================================

# Close all stale PRs (no activity in N days)
close_stale_prs() {
    local repo="$1"
    local days="${2:-90}"
    local comment="${3:-Closing due to inactivity. Please reopen if still needed.}"

    check_gh

    local cutoff_date=$(date -d "$days days ago" +%Y-%m-%d 2>/dev/null || date -v-${days}d +%Y-%m-%d)
    log "$BLUE" "Closing PRs with no activity since $cutoff_date in $repo..."

    gh pr list -R "$repo" --state open --json number,updatedAt --jq ".[] | select(.updatedAt < \"$cutoff_date\") | .number" | while read -r num; do
        log "$YELLOW" "Closing PR #$num..."
        gh pr close "$num" -R "$repo" --comment "$comment"
    done

    log "$GREEN" "Done!"
}

# Approve all PRs from a trusted user
approve_prs_from_user() {
    local repo="$1"
    local author="$2"

    check_gh
    log "$BLUE" "Approving PRs from $author in $repo..."

    gh pr list -R "$repo" --author "$author" --state open --json number --jq '.[].number' | while read -r num; do
        log "$YELLOW" "Approving PR #$num..."
        gh pr review "$num" -R "$repo" --approve
    done

    log "$GREEN" "Done!"
}

# Request reviews on all open PRs without reviewers
request_reviews() {
    local repo="$1"
    local reviewers="$2"  # Comma-separated

    check_gh
    log "$BLUE" "Requesting reviews from $reviewers..."

    gh pr list -R "$repo" --state open --json number,reviewRequests --jq '.[] | select(.reviewRequests | length == 0) | .number' | while read -r num; do
        log "$YELLOW" "Requesting review on PR #$num..."
        gh pr edit "$num" -R "$repo" --add-reviewer "$reviewers"
    done

    log "$GREEN" "Done!"
}

# ============================================
# Workflow Operations
# ============================================

# Cancel all running workflows
cancel_running_workflows() {
    local repo="$1"

    check_gh
    log "$BLUE" "Cancelling running workflows in $repo..."

    gh run list -R "$repo" --status in_progress --json databaseId --jq '.[].databaseId' | while read -r run_id; do
        log "$YELLOW" "Cancelling run $run_id..."
        gh run cancel "$run_id" -R "$repo" || log "$RED" "Failed to cancel $run_id"
    done

    log "$GREEN" "Done!"
}

# Rerun all failed workflows
rerun_failed_workflows() {
    local repo="$1"
    local limit="${2:-10}"

    check_gh
    log "$BLUE" "Rerunning failed workflows in $repo..."

    gh run list -R "$repo" --status failure --limit "$limit" --json databaseId --jq '.[].databaseId' | while read -r run_id; do
        log "$YELLOW" "Rerunning $run_id..."
        gh run rerun "$run_id" -R "$repo" --failed || log "$RED" "Failed to rerun $run_id"
    done

    log "$GREEN" "Done!"
}

# Download artifacts from latest successful run
download_latest_artifacts() {
    local repo="$1"
    local workflow="${2:-}"
    local dest="${3:-.}"

    check_gh

    local gh_args=("-R" "$repo" "--status" "success" "--limit" "1" "--json" "databaseId")
    if [[ -n "$workflow" ]]; then
        gh_args+=("-w" "$workflow")
    fi

    local run_id=$(gh run list "${gh_args[@]}" --jq '.[0].databaseId')

    if [[ -n "$run_id" ]]; then
        log "$BLUE" "Downloading artifacts from run $run_id..."
        gh run download "$run_id" -R "$repo" --dir "$dest"
        log "$GREEN" "Artifacts downloaded to $dest"
    else
        log "$RED" "No successful runs found"
    fi
}

# ============================================
# Release Operations
# ============================================

# Delete all pre-releases
delete_prereleases() {
    local repo="$1"

    check_gh
    log "$BLUE" "Deleting pre-releases in $repo..."

    gh release list -R "$repo" --json tagName,isPrerelease --jq '.[] | select(.isPrerelease) | .tagName' | while read -r tag; do
        log "$YELLOW" "Deleting pre-release $tag..."
        gh release delete "$tag" -R "$repo" --yes || log "$RED" "Failed to delete $tag"
    done

    log "$GREEN" "Done!"
}

# Create release from changelog
create_release_from_changelog() {
    local repo="$1"
    local tag="$2"
    local changelog_file="${3:-CHANGELOG.md}"

    check_gh

    if [[ ! -f "$changelog_file" ]]; then
        log "$RED" "Changelog file not found: $changelog_file"
        exit 1
    fi

    # Extract notes for this version (assumes standard changelog format)
    local notes=$(awk "/^## \[?$tag/,/^## \[?[0-9]/" "$changelog_file" | head -n -1)

    log "$BLUE" "Creating release $tag..."
    gh release create "$tag" -R "$repo" --title "$tag" --notes "$notes"
    log "$GREEN" "Release $tag created!"
}

# ============================================
# Security Operations
# ============================================

# Export all security alerts to JSON
export_security_alerts() {
    local repo="$1"
    local output="${2:-security-alerts.json}"

    check_gh
    log "$BLUE" "Exporting security alerts from $repo..."

    local owner="${repo%/*}"
    local repo_name="${repo#*/}"

    {
        echo '{'
        echo '"code_scanning":'
        gh api "repos/$owner/$repo_name/code-scanning/alerts" 2>/dev/null || echo '[]'
        echo ','
        echo '"dependabot":'
        gh api "repos/$owner/$repo_name/dependabot/alerts" 2>/dev/null || echo '[]'
        echo ','
        echo '"secret_scanning":'
        gh api "repos/$owner/$repo_name/secret-scanning/alerts" 2>/dev/null || echo '[]'
        echo '}'
    } > "$output"

    log "$GREEN" "Security alerts exported to $output"
}

# ============================================
# Utility Functions
# ============================================

# Generate repository activity report
activity_report() {
    local repo="$1"
    local days="${2:-30}"

    check_gh

    log "$BLUE" "=== Activity Report for $repo (last $days days) ==="

    echo ""
    log "$YELLOW" "Issues created:"
    gh issue list -R "$repo" --state all --json createdAt --jq "[.[] | select(.createdAt > \"$(date -d "$days days ago" +%Y-%m-%d 2>/dev/null || date -v-${days}d +%Y-%m-%d)\")] | length"

    echo ""
    log "$YELLOW" "PRs created:"
    gh pr list -R "$repo" --state all --json createdAt --jq "[.[] | select(.createdAt > \"$(date -d "$days days ago" +%Y-%m-%d 2>/dev/null || date -v-${days}d +%Y-%m-%d)\")] | length"

    echo ""
    log "$YELLOW" "PRs merged:"
    gh pr list -R "$repo" --state merged --json mergedAt --jq "[.[] | select(.mergedAt > \"$(date -d "$days days ago" +%Y-%m-%d 2>/dev/null || date -v-${days}d +%Y-%m-%d)\")] | length"

    echo ""
    log "$YELLOW" "Commits to main:"
    gh api "repos/${repo}/commits?since=$(date -d "$days days ago" +%Y-%m-%dT00:00:00Z 2>/dev/null || date -v-${days}d +%Y-%m-%dT00:00:00Z)" --jq 'length'

    echo ""
    log "$GREEN" "=== End Report ==="
}

# Show help
show_help() {
    cat << EOF
GitHub Batch Operations Helper

Usage: source batch_operations.sh && function_name args

Available Functions:

Repository Operations:
  clone_org_repos <org> [dest] [limit]     Clone all repos from an organization
  archive_repos <repos_file>               Archive repos listed in file

Issue Operations:
  close_issues_by_label <repo> <label> [reason]  Close issues with label
  transfer_issues <source> <target> [label]      Transfer issues between repos
  label_all_open_issues <repo> <label>           Add label to all open issues

Pull Request Operations:
  close_stale_prs <repo> [days] [comment]        Close PRs with no activity
  approve_prs_from_user <repo> <author>          Approve PRs from trusted user
  request_reviews <repo> <reviewers>             Request reviews on PRs

Workflow Operations:
  cancel_running_workflows <repo>                Cancel all running workflows
  rerun_failed_workflows <repo> [limit]          Rerun failed workflows
  download_latest_artifacts <repo> [workflow] [dest]  Download artifacts

Release Operations:
  delete_prereleases <repo>                      Delete all pre-releases
  create_release_from_changelog <repo> <tag> [changelog]  Create release

Security Operations:
  export_security_alerts <repo> [output]         Export security alerts to JSON

Utility:
  activity_report <repo> [days]                  Generate activity report

Examples:
  clone_org_repos microsoft ./repos 50
  close_issues_by_label owner/repo "wontfix" "not planned"
  close_stale_prs owner/repo 90
  cancel_running_workflows owner/repo
  activity_report owner/repo 7

EOF
}

# If script is run directly, show help
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    show_help
fi
