# AdGuard Home Best Practices Guide

Recommendations for optimal AdGuard Home configuration, security, and performance.

## Upstream DNS Configuration

### Recommended Upstream DNS Servers

Choose based on your priorities:

#### Privacy-Focused (Recommended)

```
# Quad9 (Malware blocking + Privacy)
https://dns.quad9.net/dns-query

# Cloudflare (Fast + Privacy)
https://cloudflare-dns.com/dns-query

# Mullvad (No logging)
https://doh.mullvad.net/dns-query
```

#### Speed-Optimized

```
# Cloudflare (Fastest)
https://cloudflare-dns.com/dns-query

# Google (Fast, but logs queries)
https://dns.google/dns-query

# NextDNS (Configurable)
https://dns.nextdns.io
```

#### Security-Focused

```
# Quad9 with ECS (Blocks malware)
https://dns11.quad9.net/dns-query

# CleanBrowsing Security Filter
https://doh.cleanbrowsing.org/doh/security-filter/
```

### Upstream Configuration Tips

1. **Use multiple upstreams** for redundancy:
   ```
   https://dns.quad9.net/dns-query
   https://cloudflare-dns.com/dns-query
   ```

2. **Use load balancing** (default) for best performance

3. **Bootstrap DNS** should be plain IP addresses:
   ```
   9.9.9.9
   1.1.1.1
   ```

4. **For local network**, consider using your ISP DNS as fallback for local resolution

---

## Filter Lists Recommendations

### Minimal Setup (Low false positives)

```
# AdGuard DNS Filter (default)
https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt
```

### Balanced Setup (Recommended)

```
# AdGuard DNS Filter
https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt

# OISD Small
https://small.oisd.nl/

# OR HaGeZi Light
https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/light.txt
```

### Comprehensive Setup

```
# HaGeZi Pro (Comprehensive)
https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt

# 1Hosts Lite (Additional coverage)
https://o0.pages.dev/Lite/adblock.txt
```

### Avoid These Mistakes

- **Don't add too many lists** - Causes redundancy and slowdown
- **Don't use hosts-format files** when AdBlock format available
- **Don't use outdated lists** - Check last update date
- **Avoid overlapping lists** - OISD already includes many other lists

### Filter Update Interval

- **Recommended:** 24 hours (default)
- **Minimum:** 12 hours
- **Don't set too frequent** - wastes bandwidth, may trigger rate limits

---

## Security Hardening

### Network Security

1. **Limit access to local network only:**
   ```yaml
   # In AdGuardHome.yaml
   http:
     address: 192.168.1.100:80  # Not 0.0.0.0
   ```

2. **Enable access control:**
   ```bash
   python scripts/adguard_api.py access-set \
     --allowed "192.168.1.0/24" \
     --disallowed "0.0.0.0/0"
   ```

3. **Block external DNS bypass:**
   - Block outbound port 53 on firewall (except from AdGuard Home)
   - Block known DoH endpoints

4. **Use strong admin password:**
   - Minimum 16 characters
   - Use password manager
   - Don't reuse passwords

### TLS/Encryption

1. **Enable DNS-over-HTTPS (DoH)** for remote access:
   ```json
   {
     "enabled": true,
     "server_name": "adguard.yourdomain.com",
     "port_https": 443,
     "port_dns_over_tls": 853
   }
   ```

2. **Use Let's Encrypt** for free, auto-renewing certificates

3. **Force HTTPS** for web interface in production

### Rate Limiting

1. **Enable rate limiting** to prevent abuse:
   ```json
   {
     "ratelimit": 20
   }
   ```

2. **Recommended values:**
   - Home network: 20-50 requests/second
   - Small office: 50-100 requests/second
   - Public server: 10-20 requests/second

---

## Performance Optimization

### DNS Cache Settings

1. **Increase cache size** for better performance:
   ```json
   {
     "cache_size": 10485760,  // 10MB (default 4MB)
     "cache_ttl_min": 60,     // Minimum 1 minute
     "cache_ttl_max": 86400   // Maximum 24 hours
   }
   ```

2. **Cache optimistic** - Enable for faster responses (may serve slightly stale data)

### Query Log Settings

1. **Reduce retention** if not needed:
   - 24 hours for most users
   - 7 days for troubleshooting
   - Disable if not using dashboard

2. **Enable anonymization** for privacy:
   ```json
   {
     "anonymize_client_ip": true
   }
   ```

### Statistics Settings

1. **Set appropriate retention:**
   - 24 hours for basic monitoring
   - 7 days for trend analysis
   - Longer periods use more memory

### Hardware Recommendations

| Network Size | RAM | Storage | CPU |
|--------------|-----|---------|-----|
| Home (1-10 devices) | 512MB | 1GB | Any |
| Home (10-50 devices) | 1GB | 2GB | Dual-core |
| Small Office | 2GB | 4GB | Quad-core |
| Large Network | 4GB+ | 8GB+ | Multi-core |

---

## Client Configuration

### Per-Client Settings

1. **Create client profiles** for different device types:

   **IoT Devices:**
   ```json
   {
     "name": "IoT Devices",
     "filtering_enabled": true,
     "safebrowsing_enabled": true,
     "blocked_services": ["facebook", "tiktok", "instagram"]
   }
   ```

   **Kids Devices:**
   ```json
   {
     "name": "Kids Tablet",
     "filtering_enabled": true,
     "parental_enabled": true,
     "safesearch": {"enabled": true},
     "blocked_services": ["youtube", "tiktok", "discord"]
   }
   ```

   **Work Devices:**
   ```json
   {
     "name": "Work Laptop",
     "filtering_enabled": true,
     "use_global_settings": true
   }
   ```

2. **Use tags** to organize clients:
   - `user_device` - Personal devices
   - `iot_device` - Smart home devices
   - `kids_device` - Children's devices
   - `guest_device` - Guest network

### Blocked Services

Recommended services to block for security:
- `cryptomining` - Prevent crypto mining
- `gambling` - Block gambling sites
- `pornography` - Adult content (if using parental controls)

---

## DHCP Configuration

### When to Use AdGuard Home DHCP

**Use it when:**
- Router DHCP doesn't allow setting custom DNS
- You want static leases managed in one place
- You need hostname resolution for local devices

**Don't use it when:**
- Router DHCP works fine with custom DNS
- You have complex networking (VLANs, etc.)
- Another device already handles DHCP well

### DHCP Best Practices

1. **Reserve IP range** for static assignments:
   ```
   DHCP Range: 192.168.1.100 - 192.168.1.200
   Static IPs: 192.168.1.2 - 192.168.1.99
   ```

2. **Set appropriate lease time:**
   - Home: 24 hours (86400 seconds)
   - Office: 8 hours
   - Guest network: 2-4 hours

3. **Create static leases** for important devices:
   - Servers
   - Printers
   - Smart home hubs

---

## Backup Strategy

### What to Backup

1. **Configuration file:** `/opt/AdGuardHome/AdGuardHome.yaml`
2. **Data directory:** `/opt/AdGuardHome/data/`
3. **TLS certificates** (if using custom)

### Backup Schedule

```bash
# Daily backup via cron
0 2 * * * /usr/local/bin/backup-adguard.sh
```

### Backup Script

```bash
#!/bin/bash
BACKUP_DIR="/backup/adguard"
DATE=$(date +%Y%m%d)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup config
cp /opt/AdGuardHome/AdGuardHome.yaml $BACKUP_DIR/config_$DATE.yaml

# Backup data (optional - can be large)
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /opt/AdGuardHome/data/

# Keep only last 7 backups
find $BACKUP_DIR -name "config_*.yaml" -mtime +7 -delete
find $BACKUP_DIR -name "data_*.tar.gz" -mtime +7 -delete
```

### Automated Backup via Skill

```bash
# Manual backup
python scripts/adguard_ssh.py backup

# List backups
python scripts/adguard_ssh.py list-backups
```

---

## Monitoring

### Key Metrics to Monitor

1. **Query statistics:**
   - Total queries per day
   - Block rate percentage
   - Average response time

2. **System health:**
   - Service uptime
   - Memory usage
   - Disk usage

3. **Security events:**
   - Blocked malware domains
   - Unusual query patterns
   - New client connections

### Query Log Analysis

Regular analysis helps identify:
- Compromised devices (unusual query patterns)
- Tracking domains to block
- False positives to whitelist

```bash
# Generate analysis report
python scripts/query_analyzer.py report --limit 5000
```

### Alerting

Set up alerts for:
- Service down
- High memory usage (>80%)
- Unusual spike in blocked queries
- New unknown clients

---

## Common Custom Rules

### Block Tracking

```
# Facebook tracking
||facebook.com^$important
||fbcdn.net^
||facebook.net^

# Google tracking (careful - may break services)
||googleadservices.com^
||googlesyndication.com^
||doubleclick.net^
```

### Allow Specific Services

```
# Allow specific CDN
@@||cdn.example.com^

# Allow specific tracking for functionality
@@||analytics.example.com^$client=192.168.1.100
```

### Block by Pattern

```
# Block all subdomains of tracking domain
||*.tracker.com^

# Block domains containing "ads"
/^ads\./
```

---

## Updates and Maintenance

### Update Schedule

- **AdGuard Home:** Monthly (check changelog for security updates)
- **Filter lists:** Automatic (24-hour interval)
- **OS/System:** Regular security patches

### Pre-Update Checklist

1. Backup configuration
2. Check changelog for breaking changes
3. Schedule maintenance window
4. Have rollback plan ready

### Update Process

```bash
# 1. Backup
python scripts/adguard_ssh.py backup

# 2. Update
python scripts/adguard_ssh.py update

# 3. Verify
python scripts/adguard_api.py status
```

---

## Checklist: Initial Setup

- [ ] Install AdGuard Home on dedicated device/VM
- [ ] Configure upstream DNS (DoH/DoT recommended)
- [ ] Add 1-2 quality filter lists
- [ ] Enable safebrowsing protection
- [ ] Set up strong admin password
- [ ] Configure HTTPS for web interface
- [ ] Point router DNS to AdGuard Home
- [ ] Test from multiple devices
- [ ] Set up backup schedule
- [ ] Create client profiles for different device types
- [ ] Document your configuration

## Checklist: Security Audit

- [ ] Admin password is strong and unique
- [ ] Web interface uses HTTPS
- [ ] Access restricted to local network
- [ ] Rate limiting enabled
- [ ] Query log anonymization (if needed)
- [ ] No unnecessary ports exposed
- [ ] Regular backups configured
- [ ] Updates applied promptly
- [ ] Filter lists up to date
- [ ] No unknown clients in query log
