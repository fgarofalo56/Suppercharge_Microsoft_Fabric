# AdGuard Home API Reference

Complete REST API documentation for AdGuard Home. All endpoints use HTTP Basic Authentication and are prefixed with `/control/`.

## Authentication

All API requests require HTTP Basic Auth:

```bash
curl -u "username:password" https://adguard.local/control/status
```

## Status & Server Information

### GET /status
Retrieve DNS server status and general settings.

**Response:**
```json
{
  "version": "v0.107.43",
  "running": true,
  "protection_enabled": true,
  "dns_port": 53,
  "http_port": 80,
  "language": "en"
}
```

### GET /dns_info
Get DNS server configuration.

**Response:**
```json
{
  "upstream_dns": ["https://dns.cloudflare.com/dns-query"],
  "upstream_dns_file": "",
  "bootstrap_dns": ["1.1.1.1"],
  "protection_enabled": true,
  "ratelimit": 20,
  "blocking_mode": "default",
  "blocking_ipv4": "",
  "blocking_ipv6": "",
  "edns_cs_enabled": false,
  "dnssec_enabled": false,
  "disable_ipv6": false,
  "upstream_mode": "load_balance",
  "cache_size": 4194304,
  "cache_ttl_min": 0,
  "cache_ttl_max": 0
}
```

### POST /dns_config
Configure DNS settings.

**Request Body:**
```json
{
  "upstream_dns": ["https://dns.cloudflare.com/dns-query", "https://dns.google/dns-query"],
  "bootstrap_dns": ["1.1.1.1", "8.8.8.8"],
  "ratelimit": 20,
  "blocking_mode": "default",
  "cache_size": 4194304
}
```

### POST /protection
Enable or disable DNS protection.

**Request Body:**
```json
{
  "enabled": true,
  "duration": 0
}
```
- `duration`: Milliseconds (0 = permanent)

### POST /cache_clear
Clear DNS cache. No request body required.

### POST /test_upstream_dns
Test upstream DNS servers.

**Request Body:**
```json
{
  "upstream_dns": ["8.8.8.8", "https://dns.google/dns-query"],
  "bootstrap_dns": ["1.1.1.1"]
}
```

---

## Query Log

### GET /querylog
Get DNS query log entries.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `older_than` | string | Return entries older than this timestamp |
| `offset` | int | Pagination offset |
| `limit` | int | Max entries to return (default: 500) |
| `search` | string | Filter by domain/client |
| `response_status` | string | Filter by status |

**Response Status Values:**
- `all` - All queries
- `filtered` - Blocked queries
- `blocked` - Blocked by filters
- `blocked_safebrowsing` - Blocked by safebrowsing
- `blocked_parental` - Blocked by parental control
- `whitelisted` - Allowed by whitelist
- `rewritten` - DNS rewrites
- `safe_search` - Modified by safe search
- `processed` - Allowed queries

**Response:**
```json
{
  "data": [
    {
      "time": "2024-01-15T10:30:00.000Z",
      "question": {
        "name": "example.com",
        "type": "A",
        "class": "IN"
      },
      "answer": [
        {"value": "93.184.216.34", "type": "A", "ttl": 300}
      ],
      "client": "192.168.1.100",
      "client_proto": "dns",
      "upstream": "https://dns.cloudflare.com/dns-query",
      "elapsed_ms": "15",
      "reason": "NotFilteredNotFound",
      "rules": []
    }
  ],
  "oldest": "2024-01-14T10:30:00.000Z"
}
```

### POST /querylog_clear
Clear all query log entries.

### GET /querylog/config
Get query log configuration.

**Response:**
```json
{
  "enabled": true,
  "interval": 24,
  "anonymize_client_ip": false
}
```

### PUT /querylog/config/update
Update query log configuration.

**Request Body:**
```json
{
  "enabled": true,
  "interval": 24,
  "anonymize_client_ip": false
}
```

---

## Statistics

### GET /stats
Get server statistics.

**Response:**
```json
{
  "time_units": "hours",
  "num_dns_queries": 15234,
  "num_blocked_filtering": 1523,
  "num_replaced_safebrowsing": 12,
  "num_replaced_safesearch": 45,
  "num_replaced_parental": 8,
  "avg_processing_time": 15.5,
  "top_queried_domains": [
    {"name": "google.com", "count": 500}
  ],
  "top_blocked_domains": [
    {"name": "ads.example.com", "count": 100}
  ],
  "top_clients": [
    {"name": "192.168.1.100", "count": 5000}
  ],
  "dns_queries": [100, 150, 200, ...]
}
```

### POST /stats_reset
Reset all statistics.

### GET /stats/config
Get statistics configuration.

### PUT /stats/config/update
Update statistics configuration.

**Request Body:**
```json
{
  "interval": 24
}
```

---

## Filtering

### GET /filtering/status
Get filtering configuration.

**Response:**
```json
{
  "enabled": true,
  "interval": 24,
  "filters": [
    {
      "id": 1,
      "url": "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt",
      "name": "AdGuard DNS filter",
      "enabled": true,
      "last_updated": "2024-01-15T00:00:00Z",
      "rules_count": 50000
    }
  ],
  "whitelist_filters": [],
  "user_rules": [
    "||ads.example.com^",
    "@@||allowed.example.com^"
  ]
}
```

### POST /filtering/config
Configure filtering settings.

**Request Body:**
```json
{
  "enabled": true,
  "interval": 24
}
```

### POST /filtering/add_url
Add a filter list.

**Request Body:**
```json
{
  "name": "My Filter List",
  "url": "https://example.com/blocklist.txt",
  "whitelist": false
}
```

### POST /filtering/remove_url
Remove a filter list.

**Request Body:**
```json
{
  "url": "https://example.com/blocklist.txt",
  "whitelist": false
}
```

### POST /filtering/set_url
Update filter settings.

**Request Body:**
```json
{
  "url": "https://example.com/blocklist.txt",
  "data": {
    "name": "Updated Name",
    "url": "https://example.com/blocklist.txt",
    "enabled": true
  },
  "whitelist": false
}
```

### POST /filtering/refresh
Force refresh filters.

**Request Body:**
```json
{
  "whitelist": false
}
```

### POST /filtering/set_rules
Set custom filtering rules.

**Request Body:**
```json
{
  "rules": [
    "||ads.example.com^",
    "@@||allowed.example.com^",
    "/tracking.*\\.js/"
  ]
}
```

### GET /filtering/check_host
Check if a host is filtered.

**Query Parameters:**
- `name` (required): Hostname to check
- `client`: Client IP (optional)
- `qtype`: Query type (optional)

**Response:**
```json
{
  "reason": "FilteredBlackList",
  "filter_id": 1,
  "rule": "||ads.example.com^",
  "cname": "",
  "ip_addrs": []
}
```

---

## Clients

### GET /clients
List all configured clients.

**Response:**
```json
{
  "clients": [
    {
      "name": "My PC",
      "ids": ["192.168.1.100", "aa:bb:cc:dd:ee:ff"],
      "use_global_settings": false,
      "filtering_enabled": true,
      "parental_enabled": false,
      "safebrowsing_enabled": true,
      "safesearch": {"enabled": false},
      "use_global_blocked_services": true,
      "blocked_services": [],
      "upstreams": [],
      "tags": ["user_device"]
    }
  ],
  "auto_clients": [
    {
      "name": "192.168.1.101",
      "ip": "192.168.1.101",
      "source": "dhcp"
    }
  ]
}
```

### POST /clients/add
Add a new client.

**Request Body:**
```json
{
  "name": "Living Room TV",
  "ids": ["192.168.1.50"],
  "use_global_settings": false,
  "filtering_enabled": true,
  "parental_enabled": true,
  "safebrowsing_enabled": true,
  "safesearch": {"enabled": true},
  "blocked_services": ["facebook", "tiktok"],
  "upstreams": [],
  "tags": ["iot_device"]
}
```

### POST /clients/update
Update an existing client.

**Request Body:**
```json
{
  "name": "Living Room TV",
  "data": {
    "name": "Living Room TV",
    "ids": ["192.168.1.50"],
    "filtering_enabled": true
  }
}
```

### POST /clients/delete
Delete a client.

**Request Body:**
```json
{
  "name": "Living Room TV"
}
```

### POST /clients/search
Search for clients.

**Request Body:**
```json
{
  "clients": [
    {"ip": "192.168.1.100"},
    {"id": "aa:bb:cc:dd:ee:ff"}
  ]
}
```

### GET /access/list
Get access control lists.

**Response:**
```json
{
  "allowed_clients": [],
  "disallowed_clients": [],
  "blocked_hosts": []
}
```

### POST /access/set
Configure access control.

**Request Body:**
```json
{
  "allowed_clients": ["192.168.1.0/24"],
  "disallowed_clients": ["192.168.1.200"],
  "blocked_hosts": ["malware.example.com"]
}
```

---

## DNS Rewrites

### GET /rewrite/list
List all DNS rewrite rules.

**Response:**
```json
[
  {"domain": "myserver.local", "answer": "192.168.1.100"},
  {"domain": "*.local", "answer": "192.168.1.1"}
]
```

### POST /rewrite/add
Add a DNS rewrite rule.

**Request Body:**
```json
{
  "domain": "myserver.local",
  "answer": "192.168.1.100"
}
```

Supported answer types:
- IP address: `192.168.1.100`
- Domain: `actual-server.example.com`
- CNAME: Point to another domain
- Special values: `A` (return nothing)

### POST /rewrite/delete
Delete a DNS rewrite rule.

**Request Body:**
```json
{
  "domain": "myserver.local",
  "answer": "192.168.1.100"
}
```

### PUT /rewrite/update
Update an existing rewrite rule.

**Request Body:**
```json
{
  "target": {
    "domain": "old.local",
    "answer": "192.168.1.100"
  },
  "update": {
    "domain": "new.local",
    "answer": "192.168.1.200"
  }
}
```

---

## DHCP Server

### GET /dhcp/status
Get DHCP server status.

**Response:**
```json
{
  "enabled": true,
  "interface_name": "eth0",
  "v4": {
    "gateway_ip": "192.168.1.1",
    "subnet_mask": "255.255.255.0",
    "range_start": "192.168.1.100",
    "range_end": "192.168.1.200",
    "lease_duration": 86400
  },
  "leases": [
    {
      "mac": "aa:bb:cc:dd:ee:ff",
      "ip": "192.168.1.150",
      "hostname": "mydevice",
      "expires": "2024-01-16T10:30:00Z"
    }
  ],
  "static_leases": []
}
```

### GET /dhcp/interfaces
List available network interfaces.

### POST /dhcp/set_config
Configure DHCP server.

**Request Body:**
```json
{
  "enabled": true,
  "interface_name": "eth0",
  "v4": {
    "gateway_ip": "192.168.1.1",
    "subnet_mask": "255.255.255.0",
    "range_start": "192.168.1.100",
    "range_end": "192.168.1.200",
    "lease_duration": 86400
  }
}
```

### POST /dhcp/add_static_lease
Add a static DHCP lease.

**Request Body:**
```json
{
  "mac": "aa:bb:cc:dd:ee:ff",
  "ip": "192.168.1.50",
  "hostname": "myserver"
}
```

### POST /dhcp/remove_static_lease
Remove a static DHCP lease.

**Request Body:**
```json
{
  "mac": "aa:bb:cc:dd:ee:ff",
  "ip": "192.168.1.50",
  "hostname": "myserver"
}
```

### POST /dhcp/find_active_dhcp
Scan for active DHCP servers on the network.

### POST /dhcp/reset
Reset DHCP configuration.

### POST /dhcp/reset_leases
Clear all DHCP leases.

---

## Blocked Services

### GET /blocked_services/all
Get all services that can be blocked.

**Response:**
```json
{
  "blocked_services": [
    {"id": "facebook", "name": "Facebook", "icon_svg": "..."},
    {"id": "youtube", "name": "YouTube", "icon_svg": "..."},
    {"id": "tiktok", "name": "TikTok", "icon_svg": "..."}
  ]
}
```

### GET /blocked_services/get
Get currently blocked services.

**Response:**
```json
{
  "ids": ["facebook", "tiktok"],
  "schedule": {
    "time_zone": "Local",
    "mon": {"start": 0, "end": 86400},
    "tue": {"start": 0, "end": 86400}
  }
}
```

### PUT /blocked_services/update
Update blocked services.

**Request Body:**
```json
{
  "ids": ["facebook", "tiktok", "instagram"],
  "schedule": {
    "time_zone": "America/New_York",
    "mon": {"start": 28800, "end": 64800}
  }
}
```

---

## Safebrowsing & Parental

### GET /safebrowsing/status
Get safebrowsing status.

### POST /safebrowsing/enable
Enable safebrowsing protection.

### POST /safebrowsing/disable
Disable safebrowsing protection.

### GET /parental/status
Get parental control status.

### POST /parental/enable
Enable parental controls.

### POST /parental/disable
Disable parental controls.

### GET /safesearch/status
Get safe search status.

### PUT /safesearch/settings
Update safe search settings.

**Request Body:**
```json
{
  "enabled": true,
  "bing": true,
  "duckduckgo": true,
  "google": true,
  "pixabay": true,
  "yandex": true,
  "youtube": true
}
```

---

## TLS/Encryption

### GET /tls/status
Get TLS configuration.

**Response:**
```json
{
  "enabled": true,
  "server_name": "adguard.example.com",
  "force_https": true,
  "port_https": 443,
  "port_dns_over_tls": 853,
  "port_dns_over_quic": 853,
  "certificate_chain": "...",
  "private_key": "...",
  "valid_cert": true,
  "valid_key": true,
  "key_type": "RSA"
}
```

### POST /tls/configure
Configure TLS settings.

**Request Body:**
```json
{
  "enabled": true,
  "server_name": "adguard.example.com",
  "force_https": true,
  "port_https": 443,
  "port_dns_over_tls": 853,
  "certificate_chain": "-----BEGIN CERTIFICATE-----...",
  "private_key": "-----BEGIN PRIVATE KEY-----..."
}
```

### POST /tls/validate
Validate TLS configuration before applying.

---

## Version & Updates

### POST /version.json
Check for updates.

**Response:**
```json
{
  "new_version": "v0.107.44",
  "announcement": "Bug fixes and improvements",
  "announcement_url": "https://github.com/AdguardTeam/AdGuardHome/releases",
  "can_autoupdate": true
}
```

### POST /update
Start auto-update process.

---

## Apple Configuration Profiles

### GET /apple/doh.mobileconfig
Generate DNS-over-HTTPS configuration profile.

**Query Parameters:**
- `host` (required): Server hostname
- `client_id`: Client identifier

### GET /apple/dot.mobileconfig
Generate DNS-over-TLS configuration profile.

**Query Parameters:**
- `host` (required): Server hostname
- `client_id`: Client identifier

---

## Filtering Rule Syntax

### Basic Rules

```
# Block domain and subdomains
||ads.example.com^

# Block exact domain only
|http://ads.example.com|

# Block pattern in URL
/ads.*\.js/

# Whitelist (exception)
@@||allowed.example.com^

# Comment
! This is a comment
# This is also a comment
```

### Advanced Modifiers

```
# Block with specific content type
||example.com^$script

# Block for specific client
||example.com^$client=192.168.1.100

# Important rule (overrides whitelists)
||malware.com^$important

# Block DNS type
||example.com^$dnstype=AAAA
```

### CNAME/Rewrite Rules

```
# Rewrite to IP
||myserver.local^$dnsrewrite=192.168.1.100

# Rewrite to CNAME
||alias.local^$dnsrewrite=CNAME;real-server.local
```
