#!/usr/bin/env python3
"""
GitHub Helper Script for Claude Code
Provides utility functions for complex GitHub operations via gh CLI.

Usage:
    python github_helper.py <command> [options]

Commands:
    batch-label         Add/remove labels from multiple issues
    batch-assign        Assign users to multiple issues
    bulk-close          Close multiple issues
    clone-issues        Clone issues from one repo to another
    pr-stats            Get PR statistics for a repo
    workflow-summary    Summarize recent workflow runs
    security-report     Generate security alerts report
    search-and-export   Search and export results to JSON
    file-tree           Get repo file tree with filters
    compare-branches    Compare two branches
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from typing import Any


def run_gh(args: list[str], capture: bool = True) -> str | None:
    """Run gh CLI command and return output."""
    cmd = ["gh"] + args
    try:
        if capture:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error running gh: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: gh CLI not found. Install from https://cli.github.com/", file=sys.stderr)
        sys.exit(1)


def run_gh_api(endpoint: str, method: str = "GET", fields: dict = None, jq: str = None) -> Any:
    """Run gh api command and return parsed JSON."""
    args = ["api", endpoint]
    if method != "GET":
        args.extend(["-X", method])
    if fields:
        for key, value in fields.items():
            args.extend(["-f", f"{key}={value}"])
    if jq:
        args.extend(["--jq", jq])

    result = run_gh(args)
    if result:
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result
    return None


def batch_label(repo: str, issues: list[int], add_labels: list[str] = None, remove_labels: list[str] = None):
    """Add or remove labels from multiple issues."""
    for issue in issues:
        args = ["issue", "edit", str(issue), "-R", repo]
        if add_labels:
            args.extend(["--add-label", ",".join(add_labels)])
        if remove_labels:
            args.extend(["--remove-label", ",".join(remove_labels)])

        print(f"Updating issue #{issue}...")
        run_gh(args, capture=False)

    print(f"Updated {len(issues)} issues.")


def batch_assign(repo: str, issues: list[int], assignees: list[str]):
    """Assign users to multiple issues."""
    for issue in issues:
        args = ["issue", "edit", str(issue), "-R", repo, "--add-assignee", ",".join(assignees)]
        print(f"Assigning issue #{issue}...")
        run_gh(args, capture=False)

    print(f"Assigned {len(issues)} issues to {', '.join(assignees)}.")


def bulk_close(repo: str, issues: list[int], comment: str = None, reason: str = None):
    """Close multiple issues."""
    for issue in issues:
        args = ["issue", "close", str(issue), "-R", repo]
        if comment:
            args.extend(["--comment", comment])
        if reason:
            args.extend(["--reason", reason])

        print(f"Closing issue #{issue}...")
        run_gh(args, capture=False)

    print(f"Closed {len(issues)} issues.")


def clone_issues(source_repo: str, target_repo: str, issue_numbers: list[int] = None, labels: list[str] = None):
    """Clone issues from one repository to another."""
    # Get issues from source
    args = ["issue", "list", "-R", source_repo, "--json", "number,title,body,labels", "--limit", "1000"]
    result = run_gh(args)
    issues = json.loads(result)

    if issue_numbers:
        issues = [i for i in issues if i["number"] in issue_numbers]

    if labels:
        issues = [i for i in issues if any(l["name"] in labels for l in i.get("labels", []))]

    created = 0
    for issue in issues:
        issue_labels = ",".join(l["name"] for l in issue.get("labels", []))
        args = ["issue", "create", "-R", target_repo,
                "--title", f"[Cloned #{issue['number']}] {issue['title']}",
                "--body", issue.get("body", "") or "No description"]
        if issue_labels:
            args.extend(["--label", issue_labels])

        print(f"Creating issue from #{issue['number']}: {issue['title'][:50]}...")
        run_gh(args, capture=False)
        created += 1

    print(f"Created {created} issues in {target_repo}.")


def pr_stats(repo: str, days: int = 30):
    """Get pull request statistics for a repository."""
    # Get PRs
    result = run_gh(["pr", "list", "-R", repo, "--state", "all", "--json",
                     "number,state,createdAt,mergedAt,closedAt,additions,deletions",
                     "--limit", "500"])
    prs = json.loads(result)

    stats = {
        "total": len(prs),
        "open": sum(1 for p in prs if p["state"] == "OPEN"),
        "merged": sum(1 for p in prs if p["state"] == "MERGED"),
        "closed": sum(1 for p in prs if p["state"] == "CLOSED"),
        "total_additions": sum(p.get("additions", 0) for p in prs),
        "total_deletions": sum(p.get("deletions", 0) for p in prs),
    }

    print(f"\n{'='*50}")
    print(f"Pull Request Statistics for {repo}")
    print(f"{'='*50}")
    print(f"Total PRs:      {stats['total']}")
    print(f"Open:           {stats['open']}")
    print(f"Merged:         {stats['merged']}")
    print(f"Closed:         {stats['closed']}")
    print(f"Total Lines +   {stats['total_additions']:,}")
    print(f"Total Lines -   {stats['total_deletions']:,}")
    print(f"{'='*50}\n")

    return stats


def workflow_summary(repo: str, limit: int = 20):
    """Summarize recent workflow runs."""
    result = run_gh(["run", "list", "-R", repo, "--json",
                     "databaseId,name,status,conclusion,createdAt,updatedAt",
                     "--limit", str(limit)])
    runs = json.loads(result)

    summary = {}
    for run in runs:
        name = run["name"]
        if name not in summary:
            summary[name] = {"success": 0, "failure": 0, "cancelled": 0, "in_progress": 0}

        conclusion = run.get("conclusion", "")
        status = run.get("status", "")

        if status == "in_progress":
            summary[name]["in_progress"] += 1
        elif conclusion == "success":
            summary[name]["success"] += 1
        elif conclusion == "failure":
            summary[name]["failure"] += 1
        elif conclusion == "cancelled":
            summary[name]["cancelled"] += 1

    print(f"\n{'='*60}")
    print(f"Workflow Summary for {repo} (last {limit} runs)")
    print(f"{'='*60}")
    print(f"{'Workflow':<30} {'Pass':>8} {'Fail':>8} {'Cancel':>8} {'Active':>8}")
    print(f"{'-'*60}")

    for name, stats in summary.items():
        print(f"{name[:30]:<30} {stats['success']:>8} {stats['failure']:>8} {stats['cancelled']:>8} {stats['in_progress']:>8}")

    print(f"{'='*60}\n")

    return summary


def security_report(repo: str, output_file: str = None):
    """Generate a security alerts report."""
    owner, repo_name = repo.split("/")

    report = {
        "repository": repo,
        "generated_at": datetime.now().isoformat(),
        "code_scanning": [],
        "dependabot": [],
        "secret_scanning": []
    }

    # Code scanning alerts
    try:
        code_alerts = run_gh_api(f"repos/{owner}/{repo_name}/code-scanning/alerts")
        if code_alerts:
            report["code_scanning"] = [
                {
                    "number": a["number"],
                    "rule": a["rule"]["id"],
                    "severity": a["rule"]["severity"],
                    "state": a["state"],
                    "file": a.get("most_recent_instance", {}).get("location", {}).get("path", "N/A")
                }
                for a in code_alerts
            ]
    except Exception:
        report["code_scanning"] = "No access or not enabled"

    # Dependabot alerts
    try:
        dependabot = run_gh_api(f"repos/{owner}/{repo_name}/dependabot/alerts")
        if dependabot:
            report["dependabot"] = [
                {
                    "number": a["number"],
                    "package": a["dependency"]["package"]["name"],
                    "severity": a["security_advisory"]["severity"],
                    "state": a["state"]
                }
                for a in dependabot
            ]
    except Exception:
        report["dependabot"] = "No access or not enabled"

    # Secret scanning alerts
    try:
        secrets = run_gh_api(f"repos/{owner}/{repo_name}/secret-scanning/alerts")
        if secrets:
            report["secret_scanning"] = [
                {
                    "number": a["number"],
                    "secret_type": a["secret_type"],
                    "state": a["state"]
                }
                for a in secrets
            ]
    except Exception:
        report["secret_scanning"] = "No access or not enabled"

    # Output
    if output_file:
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Security report saved to {output_file}")
    else:
        print(json.dumps(report, indent=2))

    return report


def search_and_export(query: str, search_type: str = "repos", output_file: str = None, limit: int = 100):
    """Search GitHub and export results to JSON."""
    type_map = {
        "repos": "repos",
        "issues": "issues",
        "prs": "prs",
        "code": "code",
        "users": "users"
    }

    if search_type not in type_map:
        print(f"Invalid search type. Use one of: {list(type_map.keys())}")
        sys.exit(1)

    result = run_gh(["search", type_map[search_type], query, "--json",
                     "repository,url,title,description" if search_type != "repos" else "fullName,url,description,stargazersCount",
                     "--limit", str(limit)])

    results = json.loads(result)

    if output_file:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Exported {len(results)} results to {output_file}")
    else:
        print(json.dumps(results, indent=2))

    return results


def file_tree(repo: str, path: str = "", extensions: list[str] = None, max_depth: int = None):
    """Get repository file tree with optional filters."""
    owner, repo_name = repo.split("/")

    tree = run_gh_api(f"repos/{owner}/{repo_name}/git/trees/HEAD?recursive=1")

    if not tree or "tree" not in tree:
        print("Failed to get repository tree")
        return

    files = []
    for item in tree["tree"]:
        if item["type"] != "blob":
            continue

        file_path = item["path"]

        # Filter by path prefix
        if path and not file_path.startswith(path):
            continue

        # Filter by extension
        if extensions:
            ext = "." + file_path.split(".")[-1] if "." in file_path else ""
            if ext not in extensions:
                continue

        # Filter by depth
        if max_depth:
            depth = file_path.count("/")
            if depth > max_depth:
                continue

        files.append(file_path)

    for f in sorted(files):
        print(f)

    print(f"\nTotal: {len(files)} files")
    return files


def compare_branches(repo: str, base: str, head: str):
    """Compare two branches and show summary."""
    owner, repo_name = repo.split("/")

    comparison = run_gh_api(f"repos/{owner}/{repo_name}/compare/{base}...{head}")

    if not comparison:
        print("Failed to compare branches")
        return

    print(f"\n{'='*60}")
    print(f"Comparing {base}...{head} in {repo}")
    print(f"{'='*60}")
    print(f"Status:           {comparison['status']}")
    print(f"Ahead by:         {comparison['ahead_by']} commits")
    print(f"Behind by:        {comparison['behind_by']} commits")
    print(f"Total commits:    {comparison['total_commits']}")
    print(f"\nFiles changed:    {len(comparison['files'])}")

    if comparison['files']:
        print(f"\n{'File':<50} {'Status':<12} {'+':>8} {'-':>8}")
        print(f"{'-'*80}")
        for f in comparison['files'][:20]:  # Show first 20
            print(f"{f['filename'][:50]:<50} {f['status']:<12} {f['additions']:>8} {f['deletions']:>8}")

        if len(comparison['files']) > 20:
            print(f"... and {len(comparison['files']) - 20} more files")

    print(f"{'='*60}\n")

    return comparison


def main():
    parser = argparse.ArgumentParser(description="GitHub Helper for Claude Code")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # batch-label
    p = subparsers.add_parser("batch-label", help="Add/remove labels from multiple issues")
    p.add_argument("repo", help="Repository (owner/repo)")
    p.add_argument("--issues", required=True, help="Comma-separated issue numbers")
    p.add_argument("--add", help="Labels to add (comma-separated)")
    p.add_argument("--remove", help="Labels to remove (comma-separated)")

    # batch-assign
    p = subparsers.add_parser("batch-assign", help="Assign users to multiple issues")
    p.add_argument("repo", help="Repository (owner/repo)")
    p.add_argument("--issues", required=True, help="Comma-separated issue numbers")
    p.add_argument("--assignees", required=True, help="Comma-separated usernames")

    # bulk-close
    p = subparsers.add_parser("bulk-close", help="Close multiple issues")
    p.add_argument("repo", help="Repository (owner/repo)")
    p.add_argument("--issues", required=True, help="Comma-separated issue numbers")
    p.add_argument("--comment", help="Comment to add when closing")
    p.add_argument("--reason", choices=["completed", "not planned"], help="Close reason")

    # clone-issues
    p = subparsers.add_parser("clone-issues", help="Clone issues from one repo to another")
    p.add_argument("source", help="Source repository (owner/repo)")
    p.add_argument("target", help="Target repository (owner/repo)")
    p.add_argument("--issues", help="Specific issue numbers (comma-separated)")
    p.add_argument("--labels", help="Filter by labels (comma-separated)")

    # pr-stats
    p = subparsers.add_parser("pr-stats", help="Get PR statistics")
    p.add_argument("repo", help="Repository (owner/repo)")
    p.add_argument("--days", type=int, default=30, help="Days to analyze")

    # workflow-summary
    p = subparsers.add_parser("workflow-summary", help="Summarize workflow runs")
    p.add_argument("repo", help="Repository (owner/repo)")
    p.add_argument("--limit", type=int, default=20, help="Number of runs to analyze")

    # security-report
    p = subparsers.add_parser("security-report", help="Generate security alerts report")
    p.add_argument("repo", help="Repository (owner/repo)")
    p.add_argument("--output", help="Output file (JSON)")

    # search-and-export
    p = subparsers.add_parser("search-and-export", help="Search and export results")
    p.add_argument("query", help="Search query")
    p.add_argument("--type", choices=["repos", "issues", "prs", "code", "users"], default="repos")
    p.add_argument("--output", help="Output file (JSON)")
    p.add_argument("--limit", type=int, default=100, help="Max results")

    # file-tree
    p = subparsers.add_parser("file-tree", help="Get repo file tree")
    p.add_argument("repo", help="Repository (owner/repo)")
    p.add_argument("--path", default="", help="Path prefix filter")
    p.add_argument("--ext", help="Extensions to include (comma-separated, e.g., .py,.js)")
    p.add_argument("--depth", type=int, help="Max directory depth")

    # compare-branches
    p = subparsers.add_parser("compare-branches", help="Compare two branches")
    p.add_argument("repo", help="Repository (owner/repo)")
    p.add_argument("base", help="Base branch")
    p.add_argument("head", help="Head branch")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "batch-label":
        issues = [int(x) for x in args.issues.split(",")]
        add = args.add.split(",") if args.add else None
        remove = args.remove.split(",") if args.remove else None
        batch_label(args.repo, issues, add, remove)

    elif args.command == "batch-assign":
        issues = [int(x) for x in args.issues.split(",")]
        assignees = args.assignees.split(",")
        batch_assign(args.repo, issues, assignees)

    elif args.command == "bulk-close":
        issues = [int(x) for x in args.issues.split(",")]
        bulk_close(args.repo, issues, args.comment, args.reason)

    elif args.command == "clone-issues":
        issues = [int(x) for x in args.issues.split(",")] if args.issues else None
        labels = args.labels.split(",") if args.labels else None
        clone_issues(args.source, args.target, issues, labels)

    elif args.command == "pr-stats":
        pr_stats(args.repo, args.days)

    elif args.command == "workflow-summary":
        workflow_summary(args.repo, args.limit)

    elif args.command == "security-report":
        security_report(args.repo, args.output)

    elif args.command == "search-and-export":
        search_and_export(args.query, args.type, args.output, args.limit)

    elif args.command == "file-tree":
        extensions = args.ext.split(",") if args.ext else None
        file_tree(args.repo, args.path, extensions, args.depth)

    elif args.command == "compare-branches":
        compare_branches(args.repo, args.base, args.head)


if __name__ == "__main__":
    main()
