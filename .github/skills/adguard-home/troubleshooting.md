# AdGuard Home Troubleshooting Guide

Comprehensive troubleshooting guide for common AdGuard Home issues.

## Quick Diagnostics

Run full diagnostics via SSH:
```bash
python scripts/adguard_ssh.py diagnostics
```

Or check status via API:
```bash
python scripts/adguard_api.py status
```

---

## DNS Resolution Issues

### Problem: DNS queries not resolving

**Symptoms:**
- Websites not loading
- "DNS_PROBE_FINISHED_NXDOMAIN" errors
- Slow or no internet connectivity

**Diagnostic Steps:**

1. **Check service status:**
   ```bash
   python scripts/adguard_ssh.py status
   ```

2. **Test DNS resolution on the server:**
   ```bash
   python scripts/adguard_ssh.py check-dns --domain google.com
   ```

3. **Test upstream DNS servers:**
   ```bash
   python scripts/adguard_api.py test-upstream --upstreams 8.8.8.8 1.1.1.1
   ```

4. **Check query log for errors:**
   ```bash
   python scripts/adguard_api.py querylog --limit 50 --json
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| Upstream DNS unreachable | Change upstream DNS servers |
| Service not running | `python scripts/adguard_ssh.py restart` |
| Port 53 blocked | Check firewall rules |
| Rate limiting | Increase `ratelimit` in DNS settings |

---

### Problem: Clients not using AdGuard Home

**Symptoms:**
- Ads still appearing
- Query log shows no queries from specific devices
- DNS requests bypassing AdGuard Home

**Diagnostic Steps:**

1. **Check what DNS server a client is using:**
   ```bash
   # On Windows client:
   nslookup google.com

   # On Linux/Mac client:
   dig google.com
   ```

2. **Verify DHCP is distributing correct DNS:**
   ```bash
   python scripts/adguard_api.py dhcp --json
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| Router DNS override | Configure router to use AdGuard Home as DNS |
| Static DNS on device | Change device to use DHCP or set static DNS to AdGuard |
| IPv6 bypass | Disable IPv6 on router or configure IPv6 DNS |
| DoH/DoT bypass | Block port 853 and DoH endpoints on firewall |

**Router Configuration:**

Set these in your router's DHCP settings:
- Primary DNS: `<AdGuard Home IP>`
- Secondary DNS: `<AdGuard Home IP>` (same IP, or leave empty)

Do NOT set a public DNS as secondary - clients will bypass AdGuard Home.

---

### Problem: High DNS latency

**Symptoms:**
- Slow page loading
- High `avg_processing_time` in stats
- Query log shows long response times

**Diagnostic Steps:**

1. **Check statistics:**
   ```bash
   python scripts/adguard_api.py stats
   ```

2. **Test upstream latency:**
   ```bash
   python scripts/adguard_ssh.py test-upstream --server 8.8.8.8
   python scripts/adguard_ssh.py test-upstream --server 1.1.1.1
   ```

3. **Check system resources:**
   ```bash
   python scripts/adguard_ssh.py check-memory
   python scripts/adguard_ssh.py check-disk
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| Slow upstream DNS | Switch to faster upstream (Cloudflare, Quad9) |
| DoH/DoT overhead | Use plain DNS upstream if on local network |
| Large blocklists | Remove redundant filter lists |
| Low cache size | Increase DNS cache size |
| High query volume | Enable rate limiting |

**Recommended Upstream DNS (by speed):**

1. **Fastest (Plain DNS):** `8.8.8.8`, `1.1.1.1`
2. **Fast (DoH):** `https://dns.cloudflare.com/dns-query`
3. **Privacy-focused:** `https://dns.quad9.net/dns-query`

---

## Filter & Blocking Issues

### Problem: Legitimate site blocked (false positive)

**Diagnostic Steps:**

1. **Check if domain is blocked:**
   ```bash
   python scripts/adguard_api.py check-host --host example.com
   ```

2. **Find the blocking rule:**
   ```bash
   python scripts/adguard_api.py querylog --search "example.com" --response-status blocked
   ```

**Solution - Add whitelist rule:**

```bash
# Via API script
python scripts/adguard_api.py add-rule --rule "@@||example.com^"
```

Or add directly in UI: `@@||example.com^`

---

### Problem: Ads still getting through

**Diagnostic Steps:**

1. **Check filtering status:**
   ```bash
   python scripts/adguard_api.py filters
   ```

2. **Verify protection is enabled:**
   ```bash
   python scripts/adguard_api.py status
   ```

3. **Check if domain is being queried:**
   ```bash
   python scripts/adguard_api.py querylog --search "doubleclick"
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| Outdated filters | `python scripts/adguard_api.py refresh-filters` |
| Missing blocklist | Add comprehensive blocklist |
| Client-specific bypass | Check client settings |
| First-party ads | Add custom rules |

**Recommended Blocklists:**

```
# AdGuard DNS Filter (default)
https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt

# OISD Full (comprehensive)
https://big.oisd.nl/

# Steven Black's Hosts
https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts

# HaGeZi Pro
https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt
```

---

### Problem: Filter update failing

**Symptoms:**
- `last_updated` not changing
- Error messages in logs

**Diagnostic Steps:**

1. **Check filter status:**
   ```bash
   python scripts/adguard_api.py filters --json
   ```

2. **Check logs for errors:**
   ```bash
   python scripts/adguard_ssh.py logs --lines 100 | grep -i filter
   ```

3. **Test URL accessibility:**
   ```bash
   ssh user@adguard "curl -I https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt"
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| URL unreachable | Check internet connectivity, update URL |
| SSL certificate error | Verify system certificates are updated |
| Rate limited | Increase update interval |
| Disk full | Free up disk space |

---

## Service & System Issues

### Problem: AdGuard Home service won't start

**Diagnostic Steps:**

1. **Check service status:**
   ```bash
   python scripts/adguard_ssh.py status
   ```

2. **Check logs:**
   ```bash
   python scripts/adguard_ssh.py logs-errors --lines 50
   ```

3. **Check port conflicts:**
   ```bash
   python scripts/adguard_ssh.py check-ports
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| Port 53 in use | Stop conflicting service (systemd-resolved) |
| Permission denied | Check file permissions |
| Config syntax error | Restore backup config |
| Corrupt database | Delete data directory, restart |

**Disable systemd-resolved (common conflict):**

```bash
sudo systemctl disable systemd-resolved
sudo systemctl stop systemd-resolved
sudo rm /etc/resolv.conf
echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf
```

---

### Problem: High memory usage

**Diagnostic Steps:**

1. **Check memory:**
   ```bash
   python scripts/adguard_ssh.py check-memory
   ```

2. **Check stats config:**
   ```bash
   python scripts/adguard_api.py stats --json | grep interval
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| Large query log | Reduce retention period |
| Large stats retention | Reduce stats interval |
| Too many filters | Remove redundant blocklists |
| Memory leak | Update AdGuard Home |

---

### Problem: Web UI not accessible

**Diagnostic Steps:**

1. **Check if service is running:**
   ```bash
   python scripts/adguard_ssh.py status
   ```

2. **Check HTTP port:**
   ```bash
   python scripts/adguard_ssh.py check-ports
   ```

3. **Check firewall:**
   ```bash
   ssh user@adguard "sudo ufw status"
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| Wrong port | Check config for `http.address` |
| Firewall blocking | Allow port in firewall |
| Binding to localhost | Change bind address to 0.0.0.0 |
| TLS certificate issue | Check/renew TLS certificate |

---

## DHCP Issues

### Problem: DHCP not assigning addresses

**Diagnostic Steps:**

1. **Check DHCP status:**
   ```bash
   python scripts/adguard_api.py dhcp --json
   ```

2. **Check for other DHCP servers:**
   ```bash
   # Via API
   curl -u user:pass https://adguard.local/control/dhcp/find_active_dhcp -X POST
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| Multiple DHCP servers | Disable router's DHCP |
| Wrong interface | Select correct network interface |
| IP range conflict | Adjust DHCP range |
| Lease exhaustion | Expand IP range or reduce lease time |

---

## TLS/Encryption Issues

### Problem: DNS-over-HTTPS not working

**Diagnostic Steps:**

1. **Check TLS status:**
   ```bash
   python scripts/adguard_api.py tls --json
   ```

2. **Test certificate:**
   ```bash
   openssl s_client -connect adguard.local:443 -servername adguard.local
   ```

**Common Solutions:**

| Issue | Solution |
|-------|----------|
| Certificate expired | Renew certificate |
| Wrong server name | Update server_name in TLS config |
| Self-signed cert | Install CA on clients or use Let's Encrypt |
| Port blocked | Open port 443 (HTTPS) and 853 (DoT) |

---

## Recovery Procedures

### Restore from backup

```bash
# List available backups
python scripts/adguard_ssh.py list-backups

# Restore specific backup
python scripts/adguard_ssh.py restore --backup-path /opt/AdGuardHome/AdGuardHome.yaml.backup_20240115

# Restart service
python scripts/adguard_ssh.py restart
```

### Factory reset

```bash
# Stop service
python scripts/adguard_ssh.py stop

# Backup current config
python scripts/adguard_ssh.py backup

# Reset (via SSH)
ssh user@adguard "sudo rm -rf /opt/AdGuardHome/data/*"

# Start service (will reinitialize)
python scripts/adguard_ssh.py start
```

### Force update

```bash
python scripts/adguard_ssh.py update
```

---

## Log Analysis

### View recent errors
```bash
python scripts/adguard_ssh.py logs-errors --lines 100
```

### View logs since specific time
```bash
python scripts/adguard_ssh.py logs-since --since "1 hour ago"
```

### Search for specific issues
```bash
ssh user@adguard "sudo journalctl -u AdGuardHome | grep -i error"
```

---

## Getting Help

If issues persist:

1. **Check official docs:** https://adguard-dns.io/kb/adguard-home/
2. **GitHub issues:** https://github.com/AdguardTeam/AdGuardHome/issues
3. **Reddit community:** r/AdGuardHome

When reporting issues, include:
- AdGuard Home version
- Operating system
- Relevant log entries
- Steps to reproduce
