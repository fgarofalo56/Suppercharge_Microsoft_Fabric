# SSH Server Administration - Reference Guide

Complete reference documentation for all SSH operations supported by this skill.

## Table of Contents

1. [SSH Connection Options](#ssh-connection-options)
2. [Command Execution](#command-execution)
3. [File Transfer - SCP](#file-transfer---scp)
4. [File Transfer - SFTP](#file-transfer---sftp)
5. [Port Forwarding](#port-forwarding)
6. [SSH Tunneling](#ssh-tunneling)
7. [Server Administration Commands](#server-administration-commands)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting Guide](#troubleshooting-guide)

---

## SSH Connection Options

### Basic Connection Syntax
```bash
ssh [options] [username]@[host]
```

### Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `-p [port]` | Specify port (default: 22) | `ssh -p 2222 user@host` |
| `-i [key]` | Use identity file (SSH key) | `ssh -i ~/.ssh/id_rsa user@host` |
| `-o [option]` | Set SSH option | `ssh -o ConnectTimeout=10 user@host` |
| `-v` | Verbose mode (debug) | `ssh -v user@host` |
| `-vv` | More verbose | `ssh -vv user@host` |
| `-vvv` | Maximum verbosity | `ssh -vvv user@host` |
| `-C` | Enable compression | `ssh -C user@host` |
| `-N` | No remote command (for tunnels) | `ssh -N -L 8080:localhost:80 user@host` |
| `-f` | Go to background | `ssh -f -N -L 8080:localhost:80 user@host` |
| `-T` | Disable pseudo-terminal | `ssh -T user@host` |
| `-t` | Force pseudo-terminal | `ssh -t user@host "sudo command"` |

### Useful SSH Options (-o)

| Option | Description | Default |
|--------|-------------|---------|
| `StrictHostKeyChecking=accept-new` | Auto-accept new keys | ask |
| `ConnectTimeout=[seconds]` | Connection timeout | none |
| `ServerAliveInterval=[seconds]` | Keep-alive interval | 0 |
| `ServerAliveCountMax=[count]` | Max keep-alive failures | 3 |
| `BatchMode=yes` | Non-interactive mode | no |
| `LogLevel=ERROR` | Reduce output noise | INFO |

### Connection String Formats

```bash
# Standard
ssh username@hostname

# With port
ssh -p 2222 username@hostname

# With options
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new username@hostname

# Multiple options
ssh -o "ConnectTimeout=10" -o "ServerAliveInterval=60" username@hostname
```

---

## Command Execution

### Single Command
```bash
ssh user@host "command"
```

### Multiple Commands
```bash
# Using semicolons
ssh user@host "command1; command2; command3"

# Using && (stop on failure)
ssh user@host "command1 && command2 && command3"

# Using heredoc for complex scripts
ssh user@host << 'EOF'
cd /var/log
grep -i error syslog | tail -20
df -h
EOF
```

### Commands Requiring sudo
```bash
# Interactive sudo (requires -t for pseudo-terminal)
ssh -t user@host "sudo systemctl restart nginx"

# Multiple sudo commands
ssh -t user@host "sudo bash -c 'systemctl restart nginx && systemctl status nginx'"
```

### Handling Output
```bash
# Capture output to local file
ssh user@host "cat /var/log/syslog" > local_syslog.txt

# Pipe remote output to local command
ssh user@host "cat /var/log/syslog" | grep ERROR

# Suppress stderr
ssh user@host "command 2>/dev/null"
```

---

## File Transfer - SCP

### Basic Syntax
```bash
scp [options] [source] [destination]
```

### Upload to Server
```bash
# Single file
scp localfile.txt user@host:/remote/path/

# With different name
scp localfile.txt user@host:/remote/path/newname.txt

# Multiple files
scp file1.txt file2.txt user@host:/remote/path/

# Directory (recursive)
scp -r local_directory/ user@host:/remote/path/
```

### Download from Server
```bash
# Single file
scp user@host:/remote/file.txt ./local_path/

# Directory (recursive)
scp -r user@host:/remote/directory/ ./local_path/

# All files matching pattern
scp user@host:/remote/path/*.log ./local_logs/
```

### SCP Options

| Option | Description |
|--------|-------------|
| `-r` | Recursive (for directories) |
| `-P [port]` | Specify port (note: capital P, unlike ssh -p) |
| `-C` | Enable compression |
| `-p` | Preserve modification times and modes |
| `-q` | Quiet mode (no progress) |
| `-v` | Verbose mode |
| `-l [limit]` | Limit bandwidth (Kbit/s) |

### Examples
```bash
# Upload with compression and preserve times
scp -Cp large_file.tar.gz user@host:/backup/

# Download from non-standard port
scp -P 2222 user@host:/var/log/app.log ./

# Bandwidth limited transfer
scp -l 1000 huge_file.iso user@host:/data/
```

---

## File Transfer - SFTP

### Starting SFTP Session
```bash
sftp user@host
sftp -P 2222 user@host  # Custom port
```

### SFTP Commands Reference

#### Navigation
| Command | Description |
|---------|-------------|
| `pwd` | Print remote working directory |
| `lpwd` | Print local working directory |
| `cd [path]` | Change remote directory |
| `lcd [path]` | Change local directory |
| `ls [path]` | List remote directory |
| `lls [path]` | List local directory |

#### File Operations
| Command | Description |
|---------|-------------|
| `get [remote] [local]` | Download file |
| `get -r [remote]` | Download directory recursively |
| `put [local] [remote]` | Upload file |
| `put -r [local]` | Upload directory recursively |
| `rm [file]` | Delete remote file |
| `rmdir [dir]` | Delete remote directory |
| `mkdir [dir]` | Create remote directory |
| `rename [old] [new]` | Rename remote file |
| `chmod [mode] [file]` | Change remote file permissions |
| `chown [owner] [file]` | Change remote file owner |

#### Session Control
| Command | Description |
|---------|-------------|
| `bye` / `exit` / `quit` | Exit SFTP |
| `!command` | Execute local shell command |
| `?` / `help` | Show help |

### Batch SFTP
```bash
# Execute commands from file
sftp -b commands.txt user@host

# Commands file example:
cd /var/log
get app.log
get error.log
bye
```

---

## Port Forwarding

### Local Port Forwarding (-L)

Access a remote service through a local port.

**Syntax:**
```bash
ssh -L [local_addr:]local_port:remote_host:remote_port user@ssh_server
```

**Use Cases:**
```bash
# Access remote MySQL (port 3306) on local port 3307
ssh -L 3307:localhost:3306 user@host

# Access service on internal network through SSH server
ssh -L 8080:internal.server:80 user@gateway

# Bind to all interfaces (accessible from network)
ssh -L 0.0.0.0:8080:localhost:80 user@host
```

### Remote Port Forwarding (-R)

Expose a local service to the remote network.

**Syntax:**
```bash
ssh -R [remote_addr:]remote_port:local_host:local_port user@ssh_server
```

**Use Cases:**
```bash
# Expose local web server to remote
ssh -R 8080:localhost:80 user@host

# Make local dev server accessible from remote
ssh -R 3000:localhost:3000 user@host
```

### Dynamic Port Forwarding (-D)

Create a SOCKS proxy.

**Syntax:**
```bash
ssh -D [local_addr:]local_port user@ssh_server
```

**Use Cases:**
```bash
# Create SOCKS5 proxy on port 1080
ssh -D 1080 user@host

# Configure browser/apps to use localhost:1080 as SOCKS proxy
```

### Persistent Tunnels
```bash
# Background tunnel that stays open
ssh -f -N -L 3307:localhost:3306 user@host

# With keep-alive to prevent timeout
ssh -f -N -o ServerAliveInterval=60 -L 3307:localhost:3306 user@host
```

---

## SSH Tunneling

### Jump Hosts / Bastion Servers
```bash
# Connect through jump host
ssh -J jumpuser@jumphost targetuser@targethost

# Multiple jumps
ssh -J jump1@host1,jump2@host2 user@finalhost

# With ProxyJump option
ssh -o ProxyJump=jumpuser@jumphost targetuser@targethost
```

### Tunnel to Internal Resources
```bash
# Access internal web server through bastion
ssh -L 8080:internal.server:80 user@bastion

# Then access http://localhost:8080 in browser
```

### Reverse Tunnels
```bash
# Allow remote server to access local service
ssh -R 9000:localhost:22 user@remote

# Remote can now: ssh -p 9000 localuser@localhost
```

---

## Server Administration Commands

### System Information
```bash
# Full system info
ssh user@host "uname -a"

# OS release info
ssh user@host "cat /etc/os-release"

# Kernel version
ssh user@host "uname -r"

# Hostname
ssh user@host "hostname -f"

# System uptime
ssh user@host "uptime"
```

### Resource Monitoring
```bash
# CPU info
ssh user@host "lscpu"
ssh user@host "cat /proc/cpuinfo | grep 'model name' | head -1"

# Memory usage
ssh user@host "free -h"
ssh user@host "cat /proc/meminfo | head -5"

# Disk usage
ssh user@host "df -h"
ssh user@host "df -i"  # inode usage

# Disk I/O
ssh user@host "iostat -x 1 3"

# Top processes by CPU
ssh user@host "ps aux --sort=-%cpu | head -10"

# Top processes by memory
ssh user@host "ps aux --sort=-%mem | head -10"

# Real-time monitoring (single snapshot)
ssh user@host "top -bn1 | head -20"
```

### Service Management (systemd)
```bash
# List all services
ssh user@host "systemctl list-units --type=service"

# Service status
ssh -t user@host "sudo systemctl status nginx"

# Start/stop/restart
ssh -t user@host "sudo systemctl start nginx"
ssh -t user@host "sudo systemctl stop nginx"
ssh -t user@host "sudo systemctl restart nginx"

# Enable/disable at boot
ssh -t user@host "sudo systemctl enable nginx"
ssh -t user@host "sudo systemctl disable nginx"

# Reload configuration
ssh -t user@host "sudo systemctl reload nginx"

# View service logs
ssh user@host "journalctl -u nginx -n 100 --no-pager"
ssh user@host "journalctl -u nginx --since '1 hour ago' --no-pager"
```

### Log Management
```bash
# System logs
ssh user@host "sudo tail -100 /var/log/syslog"
ssh user@host "sudo tail -f /var/log/syslog"  # Follow mode

# Auth logs
ssh user@host "sudo tail -50 /var/log/auth.log"

# Kernel logs
ssh user@host "dmesg | tail -50"

# Search logs
ssh user@host "sudo grep -i error /var/log/syslog | tail -20"
ssh user@host "sudo grep -i 'failed\|error' /var/log/auth.log"

# Journalctl
ssh user@host "journalctl -p err --since today --no-pager"
ssh user@host "journalctl --disk-usage"
```

### Network Diagnostics
```bash
# Network interfaces
ssh user@host "ip addr"
ssh user@host "ifconfig -a"

# Routing table
ssh user@host "ip route"
ssh user@host "netstat -rn"

# Listening ports
ssh user@host "ss -tulpn"
ssh user@host "netstat -tulpn"

# Active connections
ssh user@host "ss -tn state established"
ssh user@host "netstat -an | grep ESTABLISHED"

# DNS resolution
ssh user@host "dig google.com"
ssh user@host "nslookup google.com"

# Connectivity tests
ssh user@host "ping -c 3 8.8.8.8"
ssh user@host "traceroute google.com"
ssh user@host "mtr -c 10 --report google.com"

# Firewall rules
ssh -t user@host "sudo iptables -L -n"
ssh -t user@host "sudo ufw status verbose"
```

### User Management
```bash
# List users
ssh user@host "cat /etc/passwd"
ssh user@host "getent passwd"

# Current logged in users
ssh user@host "who"
ssh user@host "w"

# User info
ssh user@host "id username"

# Recent logins
ssh user@host "last -20"

# Failed login attempts
ssh user@host "sudo lastb -20"
```

### Package Management

**Debian/Ubuntu (apt):**
```bash
ssh -t user@host "sudo apt update"
ssh -t user@host "sudo apt upgrade -y"
ssh user@host "apt list --installed | wc -l"
ssh user@host "apt list --upgradable"
```

**RHEL/CentOS (yum/dnf):**
```bash
ssh -t user@host "sudo yum update -y"
ssh user@host "yum list installed | wc -l"
ssh -t user@host "sudo dnf update -y"
```

---

## Security Considerations

### Password Handling
- Never store passwords in files or scripts
- Use password only in memory during session
- Clear credentials when session ends
- Consider SSH keys for production environments

### Host Key Verification
```bash
# Accept new keys automatically (first connection)
ssh -o StrictHostKeyChecking=accept-new user@host

# Always verify (most secure)
ssh -o StrictHostKeyChecking=yes user@host

# Skip verification (NOT recommended)
ssh -o StrictHostKeyChecking=no user@host
```

### Connection Security
```bash
# Use specific ciphers
ssh -c aes256-ctr user@host

# Use specific key exchange
ssh -o KexAlgorithms=curve25519-sha256 user@host

# Disable agent forwarding
ssh -o ForwardAgent=no user@host
```

### Best Practices
1. Use non-standard ports when possible
2. Disable root login on servers
3. Use strong passwords or SSH keys
4. Keep SSH software updated
5. Monitor authentication logs
6. Use fail2ban or similar protection
7. Limit SSH access by IP when possible

---

## Troubleshooting Guide

### Connection Issues

**"Connection refused"**
- Check if SSH service is running: `systemctl status sshd`
- Verify port number: default is 22
- Check firewall rules

**"Connection timed out"**
- Check network connectivity
- Verify hostname/IP is correct
- Check firewall on both ends

**"Permission denied"**
- Verify username and password
- Check if user is allowed SSH access
- Verify account is not locked

**"Host key verification failed"**
- Server may have been reinstalled
- Remove old key: `ssh-keygen -R hostname`
- Verify with admin before accepting new key

### Transfer Issues

**"Permission denied" during SCP**
- Check remote directory permissions
- Use sudo if writing to protected areas
- Verify user has write access

**"No such file or directory"**
- Verify path exists on remote
- Check for typos in path
- Use absolute paths

**Slow transfers**
- Enable compression: `scp -C`
- Check network bandwidth
- Consider rsync for large transfers

### Tunnel Issues

**"Channel open failed"**
- Check if port is already in use
- Verify target service is running
- Check firewall allows forwarded connections

**"Address already in use"**
- Local port is taken
- Use different local port
- Kill existing tunnel: `pkill -f "ssh.*-L.*port"`

### Debug Mode

For detailed troubleshooting:
```bash
# Verbose mode
ssh -v user@host

# More verbose
ssh -vv user@host

# Maximum verbosity
ssh -vvv user@host
```
