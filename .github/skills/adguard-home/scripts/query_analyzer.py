#!/usr/bin/env python3
"""
AdGuard Home Query Log Analyzer

Advanced analysis tool for DNS query logs including:
- Traffic pattern analysis
- Blocked domain reports
- Client activity analysis
- Time-based statistics
- Anomaly detection

Usage:
    python query_analyzer.py <command> [options]
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("Error: 'requests' package required. Install with: pip install requests")
    sys.exit(1)


class QueryAnalyzer:
    """Analyze AdGuard Home query logs."""

    def __init__(self, url: str, username: str, password: str, verify_ssl: bool = True):
        self.base_url = url.rstrip("/")
        self.auth = HTTPBasicAuth(username, password)
        self.verify_ssl = verify_ssl

    def fetch_queries(self, limit: int = 1000, response_status: str = None) -> List[Dict]:
        """Fetch query log entries."""
        url = f"{self.base_url}/control/querylog"
        params = {"limit": limit}
        if response_status:
            params["response_status"] = response_status

        response = requests.get(url, auth=self.auth, params=params, verify=self.verify_ssl)
        response.raise_for_status()
        return response.json().get("data", [])

    def analyze_blocked(self, limit: int = 1000) -> Dict[str, Any]:
        """Analyze blocked queries."""
        queries = self.fetch_queries(limit=limit, response_status="filtered")

        blocked_domains = Counter()
        blocked_by_filter = Counter()
        blocked_by_client = Counter()
        rules_triggered = Counter()

        for q in queries:
            domain = q.get("question", {}).get("name", "unknown")
            client = q.get("client", "unknown")

            blocked_domains[domain] += 1
            blocked_by_client[client] += 1

            for rule in q.get("rules", []):
                filter_id = rule.get("filter_list_id", "custom")
                rule_text = rule.get("text", "unknown")
                blocked_by_filter[filter_id] += 1
                rules_triggered[rule_text] += 1

        return {
            "total_blocked": len(queries),
            "unique_blocked_domains": len(blocked_domains),
            "top_blocked_domains": blocked_domains.most_common(20),
            "blocks_by_client": blocked_by_client.most_common(20),
            "blocks_by_filter": blocked_by_filter.most_common(10),
            "top_rules_triggered": rules_triggered.most_common(10)
        }

    def analyze_clients(self, limit: int = 1000) -> Dict[str, Any]:
        """Analyze client activity."""
        queries = self.fetch_queries(limit=limit)

        client_queries = Counter()
        client_blocked = Counter()
        client_domains = defaultdict(set)
        client_types = defaultdict(Counter)

        for q in queries:
            client = q.get("client", "unknown")
            domain = q.get("question", {}).get("name", "unknown")
            qtype = q.get("question", {}).get("type", "unknown")
            reason = q.get("reason", "")

            client_queries[client] += 1
            client_domains[client].add(domain)
            client_types[client][qtype] += 1

            if "Filtered" in reason or "Blocked" in reason:
                client_blocked[client] += 1

        client_stats = []
        for client, count in client_queries.most_common(50):
            blocked = client_blocked.get(client, 0)
            unique_domains = len(client_domains[client])
            block_rate = (blocked / count * 100) if count > 0 else 0

            client_stats.append({
                "client": client,
                "total_queries": count,
                "blocked_queries": blocked,
                "block_rate": f"{block_rate:.1f}%",
                "unique_domains": unique_domains,
                "query_types": dict(client_types[client].most_common(5))
            })

        return {
            "total_clients": len(client_queries),
            "client_statistics": client_stats
        }

    def analyze_domains(self, limit: int = 1000) -> Dict[str, Any]:
        """Analyze domain request patterns."""
        queries = self.fetch_queries(limit=limit)

        domain_counts = Counter()
        domain_clients = defaultdict(set)
        tld_counts = Counter()
        subdomain_depth = Counter()

        for q in queries:
            domain = q.get("question", {}).get("name", "unknown")
            client = q.get("client", "unknown")

            domain_counts[domain] += 1
            domain_clients[domain].add(client)

            # Extract TLD
            parts = domain.rstrip(".").split(".")
            if len(parts) >= 2:
                tld = parts[-1]
                tld_counts[tld] += 1

            # Count subdomain depth
            subdomain_depth[len(parts)] += 1

        # Identify potential tracking domains
        potential_trackers = []
        for domain, count in domain_counts.items():
            if any(kw in domain.lower() for kw in
                   ["track", "analytics", "telemetry", "metric", "pixel", "beacon"]):
                potential_trackers.append((domain, count))

        return {
            "total_unique_domains": len(domain_counts),
            "top_domains": domain_counts.most_common(30),
            "top_tlds": tld_counts.most_common(10),
            "subdomain_depth_distribution": dict(subdomain_depth),
            "potential_trackers": potential_trackers[:20],
            "domains_by_client_count": [
                (domain, len(clients))
                for domain, clients in sorted(
                    domain_clients.items(),
                    key=lambda x: len(x[1]),
                    reverse=True
                )[:20]
            ]
        }

    def analyze_time_patterns(self, limit: int = 1000) -> Dict[str, Any]:
        """Analyze query patterns over time."""
        queries = self.fetch_queries(limit=limit)

        hourly_counts = Counter()
        daily_counts = Counter()
        hourly_blocked = Counter()

        for q in queries:
            timestamp = q.get("time", "")
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                hour = dt.hour
                day = dt.strftime("%Y-%m-%d")

                hourly_counts[hour] += 1
                daily_counts[day] += 1

                reason = q.get("reason", "")
                if "Filtered" in reason or "Blocked" in reason:
                    hourly_blocked[hour] += 1
            except (ValueError, AttributeError):
                continue

        # Calculate hourly block rates
        hourly_stats = []
        for hour in range(24):
            total = hourly_counts.get(hour, 0)
            blocked = hourly_blocked.get(hour, 0)
            rate = (blocked / total * 100) if total > 0 else 0
            hourly_stats.append({
                "hour": f"{hour:02d}:00",
                "queries": total,
                "blocked": blocked,
                "block_rate": f"{rate:.1f}%"
            })

        return {
            "hourly_distribution": hourly_stats,
            "daily_counts": dict(sorted(daily_counts.items())),
            "peak_hour": max(hourly_counts.items(), key=lambda x: x[1]) if hourly_counts else None,
            "quietest_hour": min(hourly_counts.items(), key=lambda x: x[1]) if hourly_counts else None
        }

    def detect_anomalies(self, limit: int = 1000) -> Dict[str, Any]:
        """Detect potential anomalies in query patterns."""
        queries = self.fetch_queries(limit=limit)

        anomalies = []

        # Check for high-frequency domains (potential DDoS or malware)
        domain_counts = Counter()
        client_domain_counts = defaultdict(Counter)

        for q in queries:
            domain = q.get("question", {}).get("name", "unknown")
            client = q.get("client", "unknown")
            domain_counts[domain] += 1
            client_domain_counts[client][domain] += 1

        # Domains with unusually high query counts
        avg_count = sum(domain_counts.values()) / len(domain_counts) if domain_counts else 0
        for domain, count in domain_counts.items():
            if count > avg_count * 10 and count > 50:
                anomalies.append({
                    "type": "high_frequency_domain",
                    "domain": domain,
                    "count": count,
                    "severity": "warning" if count < avg_count * 50 else "critical"
                })

        # Clients querying many unique domains (potential malware/exfiltration)
        client_unique_domains = {
            client: len(domains)
            for client, domains in client_domain_counts.items()
        }
        avg_unique = sum(client_unique_domains.values()) / len(client_unique_domains) if client_unique_domains else 0

        for client, unique_count in client_unique_domains.items():
            if unique_count > avg_unique * 5 and unique_count > 100:
                anomalies.append({
                    "type": "high_domain_diversity",
                    "client": client,
                    "unique_domains": unique_count,
                    "severity": "warning"
                })

        # Check for suspicious patterns
        suspicious_patterns = [
            r"[a-z0-9]{20,}\.",  # Very long random subdomains
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",  # IP in domain
        ]

        for q in queries:
            domain = q.get("question", {}).get("name", "unknown")
            # Check for encoded/base64-like subdomains (data exfiltration)
            parts = domain.split(".")
            if len(parts) > 2:
                subdomain = parts[0]
                if len(subdomain) > 30 and subdomain.isalnum():
                    anomalies.append({
                        "type": "suspicious_subdomain",
                        "domain": domain,
                        "client": q.get("client", "unknown"),
                        "severity": "warning"
                    })

        # Deduplicate anomalies
        seen = set()
        unique_anomalies = []
        for a in anomalies:
            key = (a["type"], a.get("domain", a.get("client", "")))
            if key not in seen:
                seen.add(key)
                unique_anomalies.append(a)

        return {
            "anomaly_count": len(unique_anomalies),
            "anomalies": unique_anomalies[:50],
            "critical_count": sum(1 for a in unique_anomalies if a.get("severity") == "critical"),
            "warning_count": sum(1 for a in unique_anomalies if a.get("severity") == "warning")
        }

    def generate_report(self, limit: int = 1000) -> str:
        """Generate a comprehensive analysis report."""
        lines = []
        lines.append("=" * 60)
        lines.append("AdGuard Home Query Analysis Report")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Sample Size: {limit} queries")
        lines.append("=" * 60)

        # Blocked Analysis
        lines.append("\n## Blocked Queries Analysis")
        lines.append("-" * 40)
        blocked = self.analyze_blocked(limit)
        lines.append(f"Total Blocked: {blocked['total_blocked']}")
        lines.append(f"Unique Blocked Domains: {blocked['unique_blocked_domains']}")
        lines.append("\nTop Blocked Domains:")
        for domain, count in blocked['top_blocked_domains'][:10]:
            lines.append(f"  {domain}: {count}")

        # Client Analysis
        lines.append("\n## Client Activity Analysis")
        lines.append("-" * 40)
        clients = self.analyze_clients(limit)
        lines.append(f"Total Clients: {clients['total_clients']}")
        lines.append("\nTop Clients by Activity:")
        for c in clients['client_statistics'][:10]:
            lines.append(f"  {c['client']}: {c['total_queries']} queries "
                         f"({c['blocked_queries']} blocked, {c['block_rate']})")

        # Domain Analysis
        lines.append("\n## Domain Analysis")
        lines.append("-" * 40)
        domains = self.analyze_domains(limit)
        lines.append(f"Unique Domains: {domains['total_unique_domains']}")
        lines.append("\nTop Queried Domains:")
        for domain, count in domains['top_domains'][:10]:
            lines.append(f"  {domain}: {count}")

        if domains['potential_trackers']:
            lines.append("\nPotential Tracking Domains Detected:")
            for domain, count in domains['potential_trackers'][:5]:
                lines.append(f"  {domain}: {count}")

        # Time Patterns
        lines.append("\n## Time-Based Patterns")
        lines.append("-" * 40)
        time_data = self.analyze_time_patterns(limit)
        if time_data['peak_hour']:
            lines.append(f"Peak Hour: {time_data['peak_hour'][0]}:00 "
                         f"({time_data['peak_hour'][1]} queries)")
        if time_data['quietest_hour']:
            lines.append(f"Quietest Hour: {time_data['quietest_hour'][0]}:00 "
                         f"({time_data['quietest_hour'][1]} queries)")

        # Anomalies
        lines.append("\n## Anomaly Detection")
        lines.append("-" * 40)
        anomalies = self.detect_anomalies(limit)
        lines.append(f"Total Anomalies: {anomalies['anomaly_count']}")
        lines.append(f"Critical: {anomalies['critical_count']}")
        lines.append(f"Warnings: {anomalies['warning_count']}")

        if anomalies['anomalies']:
            lines.append("\nDetected Anomalies:")
            for a in anomalies['anomalies'][:10]:
                lines.append(f"  [{a['severity'].upper()}] {a['type']}: "
                             f"{a.get('domain', a.get('client', 'unknown'))}")

        lines.append("\n" + "=" * 60)
        lines.append("End of Report")
        lines.append("=" * 60)

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="AdGuard Home Query Log Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  blocked         Analyze blocked queries
  clients         Analyze client activity
  domains         Analyze domain patterns
  time            Analyze time-based patterns
  anomalies       Detect anomalies
  report          Generate comprehensive report

Examples:
  python query_analyzer.py report --limit 5000
  python query_analyzer.py blocked --limit 1000 --json
  python query_analyzer.py anomalies
"""
    )

    parser.add_argument("command", help="Analysis command")
    parser.add_argument("--url", default=os.environ.get("ADGUARD_URL"))
    parser.add_argument("--user", default=os.environ.get("ADGUARD_USER"))
    parser.add_argument("--password", default=os.environ.get("ADGUARD_PASS"))
    parser.add_argument("--no-verify-ssl", action="store_true",
                        default=os.environ.get("ADGUARD_VERIFY_SSL", "true").lower() == "false")
    parser.add_argument("--limit", type=int, default=1000,
                        help="Number of queries to analyze")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not all([args.url, args.user, args.password]):
        print("Error: ADGUARD_URL, ADGUARD_USER, ADGUARD_PASS required")
        sys.exit(1)

    analyzer = QueryAnalyzer(
        url=args.url,
        username=args.user,
        password=args.password,
        verify_ssl=not args.no_verify_ssl
    )

    command = args.command.lower()

    if command == "blocked":
        result = analyzer.analyze_blocked(args.limit)
    elif command == "clients":
        result = analyzer.analyze_clients(args.limit)
    elif command == "domains":
        result = analyzer.analyze_domains(args.limit)
    elif command == "time":
        result = analyzer.analyze_time_patterns(args.limit)
    elif command == "anomalies":
        result = analyzer.detect_anomalies(args.limit)
    elif command == "report":
        print(analyzer.generate_report(args.limit))
        return
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
