#!/usr/bin/env python3
"""
AdGuard Home SSH Management Script

Provides server-side management capabilities via SSH including:
- Service management (start, stop, restart, status)
- Configuration file operations
- Log viewing
- Updates
- System diagnostics

Usage:
    python adguard_ssh.py <command> [options]

Environment Variables:
    ADGUARD_SSH_HOST  - SSH host (IP or hostname)
    ADGUARD_SSH_USER  - SSH username
    ADGUARD_SSH_PORT  - SSH port (default: 22)
    ADGUARD_SSH_KEY   - Path to SSH private key (optional)
"""

import argparse
import os
import sys
from typing import Optional, Tuple

try:
    import paramiko
except ImportError:
    print("Error: 'paramiko' package required. Install with: pip install paramiko")
    sys.exit(1)


class AdGuardSSHClient:
    """SSH client for AdGuard Home server management."""

    # Default paths for AdGuard Home installation
    DEFAULT_INSTALL_PATH = "/opt/AdGuardHome"
    DEFAULT_CONFIG_PATH = "/opt/AdGuardHome/AdGuardHome.yaml"
    DEFAULT_BINARY_PATH = "/opt/AdGuardHome/AdGuardHome"

    def __init__(self, host: str, user: str, port: int = 22,
                 key_path: Optional[str] = None, password: Optional[str] = None):
        self.host = host
        self.user = user
        self.port = port
        self.key_path = key_path
        self.password = password
        self.client = None

    def connect(self) -> None:
        """Establish SSH connection."""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs = {
            "hostname": self.host,
            "port": self.port,
            "username": self.user,
        }

        if self.key_path:
            connect_kwargs["key_filename"] = self.key_path
        elif self.password:
            connect_kwargs["password"] = self.password

        try:
            self.client.connect(**connect_kwargs)
        except paramiko.AuthenticationException:
            print("Authentication failed. Check credentials or SSH key.")
            sys.exit(1)
        except paramiko.SSHException as e:
            print(f"SSH connection failed: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Connection error: {e}")
            sys.exit(1)

    def disconnect(self) -> None:
        """Close SSH connection."""
        if self.client:
            self.client.close()

    def execute(self, command: str, sudo: bool = False) -> Tuple[str, str, int]:
        """Execute a command via SSH."""
        if not self.client:
            self.connect()

        if sudo:
            command = f"sudo {command}"

        stdin, stdout, stderr = self.client.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()

        return stdout.read().decode(), stderr.read().decode(), exit_code

    def read_file(self, path: str, sudo: bool = True) -> str:
        """Read a file from the server."""
        stdout, stderr, code = self.execute(f"cat {path}", sudo=sudo)
        if code != 0:
            raise Exception(f"Failed to read {path}: {stderr}")
        return stdout

    def write_file(self, path: str, content: str, sudo: bool = True) -> None:
        """Write content to a file on the server."""
        # Use heredoc for safe content transfer
        escaped_content = content.replace("'", "'\\''")
        cmd = f"cat > {path} << 'EOFADGUARD'\n{content}\nEOFADGUARD"
        if sudo:
            # Write to temp file then move with sudo
            temp_path = f"/tmp/adguard_temp_{os.getpid()}"
            self.execute(f"cat > {temp_path} << 'EOFADGUARD'\n{content}\nEOFADGUARD")
            self.execute(f"mv {temp_path} {path}", sudo=True)
        else:
            self.execute(cmd)

    # ==================== Service Management ====================

    def service_status(self) -> str:
        """Get AdGuard Home service status."""
        stdout, stderr, code = self.execute("systemctl status AdGuardHome", sudo=True)
        return stdout if code == 0 else f"Service check failed: {stderr}"

    def service_start(self) -> str:
        """Start AdGuard Home service."""
        stdout, stderr, code = self.execute("systemctl start AdGuardHome", sudo=True)
        if code != 0:
            return f"Failed to start: {stderr}"
        return "Service started successfully"

    def service_stop(self) -> str:
        """Stop AdGuard Home service."""
        stdout, stderr, code = self.execute("systemctl stop AdGuardHome", sudo=True)
        if code != 0:
            return f"Failed to stop: {stderr}"
        return "Service stopped successfully"

    def service_restart(self) -> str:
        """Restart AdGuard Home service."""
        stdout, stderr, code = self.execute("systemctl restart AdGuardHome", sudo=True)
        if code != 0:
            return f"Failed to restart: {stderr}"
        return "Service restarted successfully"

    def service_enable(self) -> str:
        """Enable AdGuard Home service at boot."""
        stdout, stderr, code = self.execute("systemctl enable AdGuardHome", sudo=True)
        if code != 0:
            return f"Failed to enable: {stderr}"
        return "Service enabled for auto-start"

    def service_disable(self) -> str:
        """Disable AdGuard Home service at boot."""
        stdout, stderr, code = self.execute("systemctl disable AdGuardHome", sudo=True)
        if code != 0:
            return f"Failed to disable: {stderr}"
        return "Service disabled from auto-start"

    # ==================== Logs ====================

    def get_logs(self, lines: int = 100, follow: bool = False) -> str:
        """Get AdGuard Home logs."""
        cmd = f"journalctl -u AdGuardHome -n {lines}"
        if follow:
            cmd += " -f"
        stdout, stderr, code = self.execute(cmd, sudo=True)
        return stdout if code == 0 else f"Failed to get logs: {stderr}"

    def get_logs_since(self, since: str = "1 hour ago") -> str:
        """Get logs since a specific time."""
        cmd = f'journalctl -u AdGuardHome --since "{since}"'
        stdout, stderr, code = self.execute(cmd, sudo=True)
        return stdout if code == 0 else f"Failed to get logs: {stderr}"

    def get_error_logs(self, lines: int = 50) -> str:
        """Get only error-level logs."""
        cmd = f"journalctl -u AdGuardHome -p err -n {lines}"
        stdout, stderr, code = self.execute(cmd, sudo=True)
        return stdout if code == 0 else f"Failed to get logs: {stderr}"

    # ==================== Configuration ====================

    def get_config(self) -> str:
        """Get current AdGuard Home configuration."""
        return self.read_file(self.DEFAULT_CONFIG_PATH)

    def backup_config(self, backup_path: Optional[str] = None) -> str:
        """Backup current configuration."""
        if not backup_path:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.DEFAULT_CONFIG_PATH}.backup_{timestamp}"

        stdout, stderr, code = self.execute(
            f"cp {self.DEFAULT_CONFIG_PATH} {backup_path}", sudo=True
        )
        if code != 0:
            return f"Backup failed: {stderr}"
        return f"Configuration backed up to: {backup_path}"

    def list_backups(self) -> str:
        """List configuration backups."""
        stdout, stderr, code = self.execute(
            f"ls -la {self.DEFAULT_INSTALL_PATH}/*.backup* 2>/dev/null || echo 'No backups found'"
        )
        return stdout

    def restore_config(self, backup_path: str) -> str:
        """Restore configuration from backup."""
        # Verify backup exists
        stdout, stderr, code = self.execute(f"test -f {backup_path} && echo 'exists'")
        if "exists" not in stdout:
            return f"Backup file not found: {backup_path}"

        # Create current backup first
        self.backup_config()

        # Restore
        stdout, stderr, code = self.execute(
            f"cp {backup_path} {self.DEFAULT_CONFIG_PATH}", sudo=True
        )
        if code != 0:
            return f"Restore failed: {stderr}"

        return f"Configuration restored from: {backup_path}\nRestart service to apply changes."

    # ==================== Updates ====================

    def check_version(self) -> str:
        """Check current AdGuard Home version."""
        stdout, stderr, code = self.execute(f"{self.DEFAULT_BINARY_PATH} --version")
        return stdout if code == 0 else f"Version check failed: {stderr}"

    def update_adguard(self) -> str:
        """Update AdGuard Home to latest version."""
        commands = [
            f"cd {self.DEFAULT_INSTALL_PATH}",
            f"{self.DEFAULT_BINARY_PATH} -s stop",
            f"{self.DEFAULT_BINARY_PATH} --update",
            f"{self.DEFAULT_BINARY_PATH} -s start"
        ]
        full_cmd = " && ".join(commands)
        stdout, stderr, code = self.execute(full_cmd, sudo=True)
        if code != 0:
            return f"Update failed: {stderr}\n{stdout}"
        return f"Update completed:\n{stdout}"

    # ==================== Diagnostics ====================

    def check_ports(self) -> str:
        """Check if AdGuard Home ports are in use."""
        stdout, stderr, code = self.execute(
            "ss -tlnp | grep -E ':(53|80|443|3000|853)'"
        )
        return stdout if stdout else "No AdGuard Home ports detected"

    def check_dns_resolution(self, domain: str = "google.com") -> str:
        """Test DNS resolution through AdGuard Home."""
        stdout, stderr, code = self.execute(f"dig @127.0.0.1 {domain} +short")
        return stdout if code == 0 else f"DNS test failed: {stderr}"

    def check_disk_space(self) -> str:
        """Check disk space for AdGuard Home directory."""
        stdout, stderr, code = self.execute(f"df -h {self.DEFAULT_INSTALL_PATH}")
        return stdout

    def check_memory(self) -> str:
        """Check AdGuard Home memory usage."""
        stdout, stderr, code = self.execute(
            "ps aux | grep -E 'AdGuardHome|PID' | grep -v grep"
        )
        return stdout

    def check_system_dns(self) -> str:
        """Check system DNS configuration."""
        stdout, stderr, code = self.execute("cat /etc/resolv.conf")
        return stdout

    def run_diagnostics(self) -> str:
        """Run comprehensive diagnostics."""
        results = []

        results.append("=== AdGuard Home Diagnostics ===\n")

        results.append("--- Service Status ---")
        results.append(self.service_status())

        results.append("\n--- Version ---")
        results.append(self.check_version())

        results.append("\n--- Port Usage ---")
        results.append(self.check_ports())

        results.append("\n--- Memory Usage ---")
        results.append(self.check_memory())

        results.append("\n--- Disk Space ---")
        results.append(self.check_disk_space())

        results.append("\n--- System DNS ---")
        results.append(self.check_system_dns())

        results.append("\n--- DNS Resolution Test ---")
        results.append(self.check_dns_resolution())

        results.append("\n--- Recent Errors ---")
        results.append(self.get_error_logs(20))

        return "\n".join(results)

    # ==================== Network ====================

    def get_network_info(self) -> str:
        """Get network interface information."""
        stdout, stderr, code = self.execute("ip addr show")
        return stdout

    def get_listening_ports(self) -> str:
        """Get all listening ports."""
        stdout, stderr, code = self.execute("ss -tlnp", sudo=True)
        return stdout

    def test_upstream(self, server: str) -> str:
        """Test connectivity to upstream DNS server."""
        stdout, stderr, code = self.execute(f"dig @{server} google.com +short +time=5")
        if code != 0 or not stdout.strip():
            return f"FAILED: Cannot reach {server}"
        return f"OK: {server} responded with {stdout.strip()}"


def main():
    parser = argparse.ArgumentParser(
        description="AdGuard Home SSH Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  Service Management:
    status              Show service status
    start               Start service
    stop                Stop service
    restart             Restart service
    enable              Enable service at boot
    disable             Disable service at boot

  Logs:
    logs                Show recent logs
    logs-errors         Show error logs only
    logs-since          Show logs since time (e.g., "1 hour ago")

  Configuration:
    config              Show current configuration
    backup              Backup configuration
    list-backups        List available backups
    restore             Restore from backup

  Updates:
    version             Show current version
    update              Update to latest version

  Diagnostics:
    diagnostics         Run full diagnostics
    check-ports         Check port usage
    check-dns           Test DNS resolution
    check-memory        Check memory usage
    check-disk          Check disk space
    network-info        Show network interfaces
    test-upstream       Test upstream DNS server

Examples:
  python adguard_ssh.py status
  python adguard_ssh.py logs --lines 200
  python adguard_ssh.py logs-since --since "2 hours ago"
  python adguard_ssh.py backup
  python adguard_ssh.py diagnostics
  python adguard_ssh.py test-upstream --server 8.8.8.8
"""
    )

    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--host", default=os.environ.get("ADGUARD_SSH_HOST"),
                        help="SSH host")
    parser.add_argument("--user", default=os.environ.get("ADGUARD_SSH_USER"),
                        help="SSH username")
    parser.add_argument("--port", type=int,
                        default=int(os.environ.get("ADGUARD_SSH_PORT", "22")),
                        help="SSH port")
    parser.add_argument("--key", default=os.environ.get("ADGUARD_SSH_KEY"),
                        help="Path to SSH private key")
    parser.add_argument("--password", default=os.environ.get("ADGUARD_SSH_PASS"),
                        help="SSH password (not recommended)")

    # Log options
    parser.add_argument("--lines", type=int, default=100, help="Number of log lines")
    parser.add_argument("--since", default="1 hour ago", help="Time range for logs")

    # Test options
    parser.add_argument("--server", help="Upstream server to test")
    parser.add_argument("--domain", default="google.com", help="Domain for DNS test")

    # Restore options
    parser.add_argument("--backup-path", help="Backup file path for restore")

    args = parser.parse_args()

    # Validate required parameters
    if not args.host:
        print("Error: ADGUARD_SSH_HOST environment variable or --host required")
        sys.exit(1)
    if not args.user:
        print("Error: ADGUARD_SSH_USER environment variable or --user required")
        sys.exit(1)

    # Create client
    client = AdGuardSSHClient(
        host=args.host,
        user=args.user,
        port=args.port,
        key_path=args.key,
        password=args.password
    )

    try:
        # Execute command
        command = args.command.lower().replace("-", "_")

        if command == "status":
            print(client.service_status())

        elif command == "start":
            print(client.service_start())

        elif command == "stop":
            print(client.service_stop())

        elif command == "restart":
            print(client.service_restart())

        elif command == "enable":
            print(client.service_enable())

        elif command == "disable":
            print(client.service_disable())

        elif command == "logs":
            print(client.get_logs(lines=args.lines))

        elif command == "logs_errors":
            print(client.get_error_logs(lines=args.lines))

        elif command == "logs_since":
            print(client.get_logs_since(args.since))

        elif command == "config":
            print(client.get_config())

        elif command == "backup":
            print(client.backup_config())

        elif command == "list_backups":
            print(client.list_backups())

        elif command == "restore":
            if not args.backup_path:
                print("Error: --backup-path required")
                sys.exit(1)
            print(client.restore_config(args.backup_path))

        elif command == "version":
            print(client.check_version())

        elif command == "update":
            print("Starting update... This may take a few minutes.")
            print(client.update_adguard())

        elif command == "diagnostics":
            print(client.run_diagnostics())

        elif command == "check_ports":
            print(client.check_ports())

        elif command == "check_dns":
            print(client.check_dns_resolution(args.domain))

        elif command == "check_memory":
            print(client.check_memory())

        elif command == "check_disk":
            print(client.check_disk_space())

        elif command == "network_info":
            print(client.get_network_info())

        elif command == "test_upstream":
            if not args.server:
                print("Error: --server required")
                sys.exit(1)
            print(client.test_upstream(args.server))

        else:
            print(f"Unknown command: {args.command}")
            parser.print_help()
            sys.exit(1)

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
