#!/usr/bin/env python3
"""
AdGuard Home API Client

A comprehensive CLI tool for managing AdGuard Home via REST API.
Supports all major operations: status, query logs, filtering, clients, rewrites, and more.

Usage:
    python adguard_api.py <command> [options]

Environment Variables:
    ADGUARD_URL   - AdGuard Home URL (e.g., https://adguard.local)
    ADGUARD_USER  - Admin username
    ADGUARD_PASS  - Admin password
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Optional

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("Error: 'requests' package required. Install with: pip install requests")
    sys.exit(1)


class AdGuardHomeClient:
    """Client for interacting with AdGuard Home REST API."""

    def __init__(self, url: str, username: str, password: str, verify_ssl: bool = True):
        self.base_url = url.rstrip("/")
        self.auth = HTTPBasicAuth(username, password)
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.verify = verify_ssl

    def _request(self, method: str, endpoint: str, data: Any = None, params: dict = None) -> dict:
        """Make an API request."""
        url = f"{self.base_url}/control/{endpoint.lstrip('/')}"
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()

            if response.content:
                return response.json()
            return {"success": True}
        except requests.exceptions.SSLError as e:
            print(f"SSL Error: {e}")
            print("Tip: If using self-signed cert, set ADGUARD_VERIFY_SSL=false")
            sys.exit(1)
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: Cannot reach {url}")
            print(f"Details: {e}")
            sys.exit(1)
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            if response.status_code == 401:
                print("Authentication failed. Check ADGUARD_USER and ADGUARD_PASS")
            sys.exit(1)

    # ==================== Status & Info ====================

    def get_status(self) -> dict:
        """Get AdGuard Home status and general settings."""
        return self._request("GET", "status")

    def get_dns_info(self) -> dict:
        """Get DNS server configuration."""
        return self._request("GET", "dns_info")

    def get_version(self) -> dict:
        """Check for available updates."""
        return self._request("POST", "version.json", {})

    # ==================== Query Log ====================

    def get_querylog(self, limit: int = 100, offset: int = 0,
                     search: str = None, response_status: str = None) -> dict:
        """Get DNS query log entries."""
        params = {"limit": limit, "offset": offset}
        if search:
            params["search"] = search
        if response_status:
            params["response_status"] = response_status
        return self._request("GET", "querylog", params=params)

    def clear_querylog(self) -> dict:
        """Clear all query log entries."""
        return self._request("POST", "querylog_clear")

    def get_querylog_config(self) -> dict:
        """Get query log configuration."""
        return self._request("GET", "querylog/config")

    # ==================== Statistics ====================

    def get_stats(self) -> dict:
        """Get server statistics."""
        return self._request("GET", "stats")

    def reset_stats(self) -> dict:
        """Reset all statistics."""
        return self._request("POST", "stats_reset")

    def get_stats_config(self) -> dict:
        """Get statistics configuration."""
        return self._request("GET", "stats/config")

    # ==================== Filtering ====================

    def get_filtering_status(self) -> dict:
        """Get filtering configuration and status."""
        return self._request("GET", "filtering/status")

    def add_filter(self, name: str, url: str, whitelist: bool = False) -> dict:
        """Add a filter URL."""
        return self._request("POST", "filtering/add_url", {
            "name": name,
            "url": url,
            "whitelist": whitelist
        })

    def remove_filter(self, url: str, whitelist: bool = False) -> dict:
        """Remove a filter URL."""
        return self._request("POST", "filtering/remove_url", {
            "url": url,
            "whitelist": whitelist
        })

    def refresh_filters(self, whitelist: bool = False) -> dict:
        """Force refresh all filters."""
        return self._request("POST", "filtering/refresh", {"whitelist": whitelist})

    def set_custom_rules(self, rules: list) -> dict:
        """Set custom filtering rules."""
        return self._request("POST", "filtering/set_rules", {"rules": rules})

    def check_host(self, host: str) -> dict:
        """Check if a host is filtered."""
        return self._request("GET", "filtering/check_host", params={"name": host})

    # ==================== Clients ====================

    def get_clients(self) -> dict:
        """Get all configured clients."""
        return self._request("GET", "clients")

    def add_client(self, name: str, ids: list, tags: list = None,
                   use_global_settings: bool = True, filtering_enabled: bool = True,
                   parental_enabled: bool = False, safebrowsing_enabled: bool = False,
                   safesearch_enabled: bool = False, blocked_services: list = None,
                   upstreams: list = None) -> dict:
        """Add a new client configuration."""
        client_data = {
            "name": name,
            "ids": ids if isinstance(ids, list) else [ids],
            "tags": tags or [],
            "use_global_settings": use_global_settings,
            "filtering_enabled": filtering_enabled,
            "parental_enabled": parental_enabled,
            "safebrowsing_enabled": safebrowsing_enabled,
            "safesearch": {"enabled": safesearch_enabled},
            "blocked_services": blocked_services or [],
            "upstreams": upstreams or []
        }
        return self._request("POST", "clients/add", client_data)

    def update_client(self, name: str, data: dict) -> dict:
        """Update an existing client."""
        return self._request("POST", "clients/update", {"name": name, "data": data})

    def delete_client(self, name: str) -> dict:
        """Delete a client configuration."""
        return self._request("POST", "clients/delete", {"name": name})

    # ==================== DNS Rewrites ====================

    def get_rewrites(self) -> dict:
        """Get all DNS rewrite rules."""
        return self._request("GET", "rewrite/list")

    def add_rewrite(self, domain: str, answer: str) -> dict:
        """Add a DNS rewrite rule."""
        return self._request("POST", "rewrite/add", {"domain": domain, "answer": answer})

    def delete_rewrite(self, domain: str, answer: str) -> dict:
        """Delete a DNS rewrite rule."""
        return self._request("POST", "rewrite/delete", {"domain": domain, "answer": answer})

    # ==================== DHCP ====================

    def get_dhcp_status(self) -> dict:
        """Get DHCP server status and configuration."""
        return self._request("GET", "dhcp/status")

    def get_dhcp_interfaces(self) -> dict:
        """Get available network interfaces for DHCP."""
        return self._request("GET", "dhcp/interfaces")

    def add_static_lease(self, mac: str, ip: str, hostname: str) -> dict:
        """Add a static DHCP lease."""
        return self._request("POST", "dhcp/add_static_lease", {
            "mac": mac,
            "ip": ip,
            "hostname": hostname
        })

    def remove_static_lease(self, mac: str, ip: str, hostname: str) -> dict:
        """Remove a static DHCP lease."""
        return self._request("POST", "dhcp/remove_static_lease", {
            "mac": mac,
            "ip": ip,
            "hostname": hostname
        })

    # ==================== Protection ====================

    def set_protection(self, enabled: bool, duration: int = 0) -> dict:
        """Enable or disable protection."""
        return self._request("POST", "protection", {
            "enabled": enabled,
            "duration": duration
        })

    def get_safebrowsing_status(self) -> dict:
        """Get safebrowsing status."""
        return self._request("GET", "safebrowsing/status")

    def get_parental_status(self) -> dict:
        """Get parental control status."""
        return self._request("GET", "parental/status")

    # ==================== Blocked Services ====================

    def get_blocked_services(self) -> dict:
        """Get list of blocked services."""
        return self._request("GET", "blocked_services/get")

    def get_available_services(self) -> dict:
        """Get all available services that can be blocked."""
        return self._request("GET", "blocked_services/all")

    # ==================== TLS ====================

    def get_tls_status(self) -> dict:
        """Get TLS configuration status."""
        return self._request("GET", "tls/status")

    # ==================== Cache ====================

    def clear_cache(self) -> dict:
        """Clear DNS cache."""
        return self._request("POST", "cache_clear")

    def test_upstream_dns(self, upstreams: list, bootstrap_dns: list = None) -> dict:
        """Test upstream DNS servers."""
        data = {"upstream_dns": upstreams}
        if bootstrap_dns:
            data["bootstrap_dns"] = bootstrap_dns
        return self._request("POST", "test_upstream_dns", data)


def format_output(data: Any, format_type: str = "json") -> str:
    """Format output data."""
    if format_type == "json":
        return json.dumps(data, indent=2, default=str)
    return str(data)


def print_status(client: AdGuardHomeClient):
    """Print status summary."""
    status = client.get_status()
    dns_info = client.get_dns_info()

    print("=" * 50)
    print("AdGuard Home Status")
    print("=" * 50)
    print(f"Version: {status.get('version', 'Unknown')}")
    print(f"Running: {status.get('running', False)}")
    print(f"Protection Enabled: {status.get('protection_enabled', False)}")
    print(f"DNS Port: {status.get('dns_port', 'Unknown')}")
    print(f"HTTP Port: {status.get('http_port', 'Unknown')}")
    print()
    print("DNS Configuration:")
    print(f"  Upstream DNS: {dns_info.get('upstream_dns', [])}")
    print(f"  Bootstrap DNS: {dns_info.get('bootstrap_dns', [])}")
    print(f"  Rate Limit: {dns_info.get('ratelimit', 'Unknown')} req/s")
    print(f"  Blocking Mode: {dns_info.get('blocking_mode', 'Unknown')}")


def print_stats(client: AdGuardHomeClient):
    """Print statistics summary."""
    stats = client.get_stats()

    print("=" * 50)
    print("AdGuard Home Statistics")
    print("=" * 50)
    print(f"Total Queries: {stats.get('num_dns_queries', 0):,}")
    print(f"Blocked Queries: {stats.get('num_blocked_filtering', 0):,}")
    print(f"Safebrowsing Blocked: {stats.get('num_replaced_safebrowsing', 0):,}")
    print(f"Parental Blocked: {stats.get('num_replaced_parental', 0):,}")
    print(f"Average Processing Time: {stats.get('avg_processing_time', 0):.2f}ms")

    if stats.get('num_dns_queries', 0) > 0:
        block_rate = (stats.get('num_blocked_filtering', 0) / stats.get('num_dns_queries', 1)) * 100
        print(f"Block Rate: {block_rate:.1f}%")

    print()
    print("Top Blocked Domains:")
    for domain, count in list(stats.get('top_blocked_domains', {}).items())[:10]:
        print(f"  {domain}: {count:,}")

    print()
    print("Top Clients:")
    for client_ip, count in list(stats.get('top_clients', {}).items())[:10]:
        print(f"  {client_ip}: {count:,}")


def print_querylog(client: AdGuardHomeClient, limit: int, search: str, response_status: str):
    """Print query log entries."""
    result = client.get_querylog(limit=limit, search=search, response_status=response_status)
    entries = result.get('data', [])

    print(f"Query Log ({len(entries)} entries)")
    print("=" * 80)

    for entry in entries:
        timestamp = entry.get('time', '')
        question = entry.get('question', {})
        domain = question.get('name', 'Unknown')
        qtype = question.get('type', 'Unknown')
        client_ip = entry.get('client', 'Unknown')
        reason = entry.get('reason', 'Processed')

        # Color code based on reason
        status_icon = "+" if reason == "NotFilteredNotFound" else "-"

        print(f"{status_icon} [{timestamp[:19]}] {domain} ({qtype}) from {client_ip}")
        if reason != "NotFilteredNotFound":
            print(f"    Reason: {reason}")
            if entry.get('rules'):
                for rule in entry['rules']:
                    print(f"    Rule: {rule.get('text', '')} (Filter: {rule.get('filter_list_id', '')})")


def print_clients(client: AdGuardHomeClient):
    """Print client list."""
    result = client.get_clients()
    clients = result.get('clients', [])
    auto_clients = result.get('auto_clients', [])

    print("=" * 50)
    print("Configured Clients")
    print("=" * 50)

    for c in clients:
        print(f"\n{c.get('name', 'Unknown')}")
        print(f"  IDs: {', '.join(c.get('ids', []))}")
        print(f"  Filtering: {'Enabled' if c.get('filtering_enabled') else 'Disabled'}")
        print(f"  Safebrowsing: {'Enabled' if c.get('safebrowsing_enabled') else 'Disabled'}")
        print(f"  Parental: {'Enabled' if c.get('parental_enabled') else 'Disabled'}")
        if c.get('blocked_services'):
            print(f"  Blocked Services: {', '.join(c['blocked_services'])}")

    print()
    print("=" * 50)
    print("Auto-detected Clients")
    print("=" * 50)

    for c in auto_clients:
        name = c.get('name', c.get('ip', 'Unknown'))
        ip = c.get('ip', 'Unknown')
        source = c.get('source', 'Unknown')
        print(f"  {name} ({ip}) - {source}")


def print_filters(client: AdGuardHomeClient):
    """Print filter list."""
    result = client.get_filtering_status()
    filters = result.get('filters', [])
    user_rules = result.get('user_rules', [])

    print("=" * 50)
    print("Filter Lists")
    print("=" * 50)

    for f in filters:
        status = "Enabled" if f.get('enabled') else "Disabled"
        rules_count = f.get('rules_count', 0)
        print(f"\n{f.get('name', 'Unknown')} [{status}]")
        print(f"  URL: {f.get('url', 'Unknown')}")
        print(f"  Rules: {rules_count:,}")
        print(f"  Last Updated: {f.get('last_updated', 'Never')}")

    print()
    print("=" * 50)
    print(f"Custom Rules ({len(user_rules)} rules)")
    print("=" * 50)
    for rule in user_rules[:20]:  # Show first 20
        print(f"  {rule}")
    if len(user_rules) > 20:
        print(f"  ... and {len(user_rules) - 20} more")


def print_rewrites(client: AdGuardHomeClient):
    """Print DNS rewrites."""
    result = client.get_rewrites()

    print("=" * 50)
    print("DNS Rewrites")
    print("=" * 50)

    if not result:
        print("No rewrites configured")
        return

    for r in result:
        print(f"  {r.get('domain', 'Unknown')} -> {r.get('answer', 'Unknown')}")


def main():
    parser = argparse.ArgumentParser(
        description="AdGuard Home API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  status              Show server status and configuration
  stats               Show statistics summary
  querylog            Show DNS query log
  clients             List all clients
  filters             Show filter lists
  rewrites            Show DNS rewrites
  dhcp                Show DHCP status

  add-filter          Add a filter list
  remove-filter       Remove a filter list
  refresh-filters     Force refresh all filters
  add-rule            Add custom filtering rule
  check-host          Check if host is filtered

  add-client          Add a client configuration
  delete-client       Delete a client

  add-rewrite         Add DNS rewrite
  delete-rewrite      Delete DNS rewrite

  enable-protection   Enable DNS protection
  disable-protection  Disable DNS protection
  clear-cache         Clear DNS cache
  reset-stats         Reset statistics

  test-upstream       Test upstream DNS servers
  version             Check for updates

Examples:
  python adguard_api.py status
  python adguard_api.py querylog --limit 50 --search "google"
  python adguard_api.py add-filter --name "EasyList" --url "https://..."
  python adguard_api.py check-host --host "ads.example.com"
"""
    )

    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--url", default=os.environ.get("ADGUARD_URL"), help="AdGuard Home URL")
    parser.add_argument("--user", default=os.environ.get("ADGUARD_USER"), help="Username")
    parser.add_argument("--password", default=os.environ.get("ADGUARD_PASS"), help="Password")
    parser.add_argument("--no-verify-ssl", action="store_true",
                        default=os.environ.get("ADGUARD_VERIFY_SSL", "true").lower() == "false",
                        help="Disable SSL verification")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Query log options
    parser.add_argument("--limit", type=int, default=100, help="Number of entries to return")
    parser.add_argument("--search", help="Search string for query log")
    parser.add_argument("--response-status", choices=[
        "all", "filtered", "blocked", "blocked_safebrowsing",
        "blocked_parental", "whitelisted", "rewritten", "safe_search", "processed"
    ], help="Filter by response status")

    # Filter options
    parser.add_argument("--name", help="Filter/client name")
    parser.add_argument("--filter-url", help="Filter URL")
    parser.add_argument("--whitelist", action="store_true", help="Add as whitelist")
    parser.add_argument("--rule", help="Custom filtering rule")

    # Client options
    parser.add_argument("--ids", nargs="+", help="Client identifiers (IP, MAC, ClientID)")

    # Host check options
    parser.add_argument("--host", help="Hostname to check")

    # Rewrite options
    parser.add_argument("--domain", help="Domain for rewrite")
    parser.add_argument("--answer", help="Answer for rewrite (IP or domain)")

    # Protection options
    parser.add_argument("--duration", type=int, default=0, help="Duration in milliseconds (0 = permanent)")

    # Upstream test options
    parser.add_argument("--upstreams", nargs="+", help="Upstream DNS servers to test")

    args = parser.parse_args()

    # Validate required parameters
    if not args.url:
        print("Error: ADGUARD_URL environment variable or --url required")
        sys.exit(1)
    if not args.user:
        print("Error: ADGUARD_USER environment variable or --user required")
        sys.exit(1)
    if not args.password:
        print("Error: ADGUARD_PASS environment variable or --password required")
        sys.exit(1)

    # Create client
    client = AdGuardHomeClient(
        url=args.url,
        username=args.user,
        password=args.password,
        verify_ssl=not args.no_verify_ssl
    )

    # Execute command
    command = args.command.lower().replace("-", "_")

    if command == "status":
        if args.json:
            print(format_output(client.get_status()))
        else:
            print_status(client)

    elif command == "stats":
        if args.json:
            print(format_output(client.get_stats()))
        else:
            print_stats(client)

    elif command == "querylog":
        if args.json:
            print(format_output(client.get_querylog(
                limit=args.limit,
                search=args.search,
                response_status=args.response_status
            )))
        else:
            print_querylog(client, args.limit, args.search, args.response_status)

    elif command == "clients":
        if args.json:
            print(format_output(client.get_clients()))
        else:
            print_clients(client)

    elif command == "filters":
        if args.json:
            print(format_output(client.get_filtering_status()))
        else:
            print_filters(client)

    elif command == "rewrites":
        if args.json:
            print(format_output(client.get_rewrites()))
        else:
            print_rewrites(client)

    elif command == "dhcp":
        print(format_output(client.get_dhcp_status()))

    elif command == "add_filter":
        if not args.name or not args.filter_url:
            print("Error: --name and --filter-url required")
            sys.exit(1)
        result = client.add_filter(args.name, args.filter_url, args.whitelist)
        print(f"Filter added: {args.name}")

    elif command == "remove_filter":
        if not args.filter_url:
            print("Error: --filter-url required")
            sys.exit(1)
        result = client.remove_filter(args.filter_url, args.whitelist)
        print(f"Filter removed: {args.filter_url}")

    elif command == "refresh_filters":
        result = client.refresh_filters(args.whitelist)
        print("Filters refreshed")

    elif command == "add_rule":
        if not args.rule:
            print("Error: --rule required")
            sys.exit(1)
        # Get existing rules first
        status = client.get_filtering_status()
        rules = status.get("user_rules", [])
        rules.append(args.rule)
        result = client.set_custom_rules(rules)
        print(f"Rule added: {args.rule}")

    elif command == "check_host":
        if not args.host:
            print("Error: --host required")
            sys.exit(1)
        result = client.check_host(args.host)
        print(format_output(result))

    elif command == "add_client":
        if not args.name or not args.ids:
            print("Error: --name and --ids required")
            sys.exit(1)
        result = client.add_client(args.name, args.ids)
        print(f"Client added: {args.name}")

    elif command == "delete_client":
        if not args.name:
            print("Error: --name required")
            sys.exit(1)
        result = client.delete_client(args.name)
        print(f"Client deleted: {args.name}")

    elif command == "add_rewrite":
        if not args.domain or not args.answer:
            print("Error: --domain and --answer required")
            sys.exit(1)
        result = client.add_rewrite(args.domain, args.answer)
        print(f"Rewrite added: {args.domain} -> {args.answer}")

    elif command == "delete_rewrite":
        if not args.domain or not args.answer:
            print("Error: --domain and --answer required")
            sys.exit(1)
        result = client.delete_rewrite(args.domain, args.answer)
        print(f"Rewrite deleted: {args.domain}")

    elif command == "enable_protection":
        result = client.set_protection(True, args.duration)
        print("Protection enabled")

    elif command == "disable_protection":
        result = client.set_protection(False, args.duration)
        msg = f"Protection disabled"
        if args.duration > 0:
            print(f"{msg} for {args.duration}ms")
        else:
            print(msg)

    elif command == "clear_cache":
        result = client.clear_cache()
        print("DNS cache cleared")

    elif command == "reset_stats":
        result = client.reset_stats()
        print("Statistics reset")

    elif command == "test_upstream":
        if not args.upstreams:
            print("Error: --upstreams required")
            sys.exit(1)
        result = client.test_upstream_dns(args.upstreams)
        print(format_output(result))

    elif command == "version":
        result = client.get_version()
        print(format_output(result))

    elif command == "tls":
        print(format_output(client.get_tls_status()))

    elif command == "blocked_services":
        print(format_output(client.get_blocked_services()))

    elif command == "available_services":
        print(format_output(client.get_available_services()))

    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
