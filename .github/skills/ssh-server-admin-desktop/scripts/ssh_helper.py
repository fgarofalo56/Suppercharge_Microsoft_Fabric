#!/usr/bin/env python3
"""
Cross-Platform SSH Helper

A Python-based SSH client that works on Windows, macOS, and Linux.
Uses paramiko library for SSH connections with password authentication.

This script is designed to be used by Claude Code skills when native
SSH tools (sshpass) are not available, particularly on Windows.

Usage:
    # Execute command
    python ssh_helper.py --host 192.168.1.100 --user admin --password "secret" --command "df -h"

    # Upload file
    python ssh_helper.py --host 192.168.1.100 --user admin --password "secret" --upload ./local.txt --remote-path /tmp/remote.txt

    # Download file
    python ssh_helper.py --host 192.168.1.100 --user admin --password "secret" --download /var/log/syslog --local-path ./syslog.txt

    # Use SSH key instead of password
    python ssh_helper.py --host 192.168.1.100 --user admin --key ~/.ssh/id_rsa --command "df -h"

Requirements:
    pip install paramiko
"""

import argparse
import sys
import os
from pathlib import Path

try:
    import paramiko
except ImportError:
    print("Error: paramiko library not installed.")
    print("Install with: pip install paramiko")
    sys.exit(1)


class SSHClient:
    """Cross-platform SSH client using paramiko."""

    def __init__(self, host: str, username: str, password: str = None,
                 key_path: str = None, port: int = 22, timeout: int = 30):
        """
        Initialize SSH client.

        Args:
            host: Remote host IP or hostname
            username: SSH username
            password: SSH password (optional if using key)
            key_path: Path to SSH private key (optional)
            port: SSH port (default 22)
            timeout: Connection timeout in seconds
        """
        self.host = host
        self.username = username
        self.password = password
        self.key_path = key_path
        self.port = port
        self.timeout = timeout
        self.client = None

    def connect(self):
        """Establish SSH connection."""
        self.client = paramiko.SSHClient()

        # Auto-add host keys (equivalent to StrictHostKeyChecking=accept-new)
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            connect_kwargs = {
                'hostname': self.host,
                'port': self.port,
                'username': self.username,
                'timeout': self.timeout,
                'allow_agent': True,
                'look_for_keys': True,
            }

            # Use key authentication if key path provided
            if self.key_path:
                key_path = os.path.expanduser(self.key_path)
                if not os.path.exists(key_path):
                    raise FileNotFoundError(f"SSH key not found: {key_path}")

                # Try to load key (supports RSA, DSA, ECDSA, Ed25519)
                try:
                    key = paramiko.RSAKey.from_private_key_file(key_path)
                except:
                    try:
                        key = paramiko.Ed25519Key.from_private_key_file(key_path)
                    except:
                        try:
                            key = paramiko.ECDSAKey.from_private_key_file(key_path)
                        except:
                            key = paramiko.DSSKey.from_private_key_file(key_path)

                connect_kwargs['pkey'] = key
            elif self.password:
                connect_kwargs['password'] = self.password

            self.client.connect(**connect_kwargs)
            return True

        except paramiko.AuthenticationException:
            print(f"Error: Authentication failed for {self.username}@{self.host}")
            return False
        except paramiko.SSHException as e:
            print(f"Error: SSH connection failed: {e}")
            return False
        except Exception as e:
            print(f"Error: Connection failed: {e}")
            return False

    def disconnect(self):
        """Close SSH connection."""
        if self.client:
            self.client.close()
            self.client = None

    def execute(self, command: str, sudo: bool = False,
                sudo_password: str = None) -> tuple:
        """
        Execute a command on the remote host.

        Args:
            command: Command to execute
            sudo: Whether to run with sudo
            sudo_password: Password for sudo (uses SSH password if not provided)

        Returns:
            Tuple of (stdout, stderr, exit_code)
        """
        if not self.client:
            if not self.connect():
                return "", "Connection failed", 1

        try:
            if sudo:
                pwd = sudo_password or self.password
                if pwd:
                    command = f"echo '{pwd}' | sudo -S {command}"
                else:
                    command = f"sudo {command}"

            stdin, stdout, stderr = self.client.exec_command(
                command,
                timeout=self.timeout
            )

            # Get output
            stdout_str = stdout.read().decode('utf-8', errors='replace')
            stderr_str = stderr.read().decode('utf-8', errors='replace')
            exit_code = stdout.channel.recv_exit_status()

            return stdout_str, stderr_str, exit_code

        except Exception as e:
            return "", str(e), 1

    def upload(self, local_path: str, remote_path: str) -> bool:
        """
        Upload a file to the remote host.

        Args:
            local_path: Local file path
            remote_path: Remote destination path

        Returns:
            True if successful
        """
        if not self.client:
            if not self.connect():
                return False

        try:
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            print(f"Uploaded: {local_path} -> {remote_path}")
            return True
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False

    def download(self, remote_path: str, local_path: str) -> bool:
        """
        Download a file from the remote host.

        Args:
            remote_path: Remote file path
            local_path: Local destination path

        Returns:
            True if successful
        """
        if not self.client:
            if not self.connect():
                return False

        try:
            sftp = self.client.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            print(f"Downloaded: {remote_path} -> {local_path}")
            return True
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False

    def list_dir(self, remote_path: str = ".") -> list:
        """
        List directory contents on remote host.

        Args:
            remote_path: Remote directory path

        Returns:
            List of filenames
        """
        if not self.client:
            if not self.connect():
                return []

        try:
            sftp = self.client.open_sftp()
            files = sftp.listdir(remote_path)
            sftp.close()
            return files
        except Exception as e:
            print(f"Error listing directory: {e}")
            return []


def main():
    parser = argparse.ArgumentParser(
        description='Cross-platform SSH helper for Claude Code skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Run a command
  %(prog)s --host 192.168.1.100 --user admin --password "secret" --command "df -h"

  # Upload a file
  %(prog)s --host 192.168.1.100 --user admin --password "secret" --upload ./local.txt --remote-path /tmp/file.txt

  # Download a file
  %(prog)s --host 192.168.1.100 --user admin --password "secret" --download /var/log/syslog --local-path ./syslog.txt

  # Use SSH key
  %(prog)s --host 192.168.1.100 --user admin --key ~/.ssh/id_rsa --command "uptime"

  # Run command with sudo
  %(prog)s --host 192.168.1.100 --user admin --password "secret" --command "systemctl restart nginx" --sudo
'''
    )

    # Connection arguments
    parser.add_argument('--host', '-H', required=True, help='Remote host IP or hostname')
    parser.add_argument('--user', '-u', required=True, help='SSH username')
    parser.add_argument('--password', '-p', help='SSH password')
    parser.add_argument('--key', '-k', help='Path to SSH private key')
    parser.add_argument('--port', '-P', type=int, default=22, help='SSH port (default: 22)')
    parser.add_argument('--timeout', '-t', type=int, default=30, help='Connection timeout (default: 30)')

    # Operation arguments
    parser.add_argument('--command', '-c', help='Command to execute')
    parser.add_argument('--sudo', action='store_true', help='Run command with sudo')
    parser.add_argument('--upload', help='Local file to upload')
    parser.add_argument('--download', help='Remote file to download')
    parser.add_argument('--remote-path', help='Remote path for upload')
    parser.add_argument('--local-path', help='Local path for download')
    parser.add_argument('--list', '-l', help='List remote directory')

    args = parser.parse_args()

    # Validate arguments
    if not args.password and not args.key:
        # Try to find default SSH keys
        default_keys = [
            os.path.expanduser('~/.ssh/id_ed25519'),
            os.path.expanduser('~/.ssh/id_rsa'),
            os.path.expanduser('~/.ssh/id_ecdsa'),
        ]
        for key in default_keys:
            if os.path.exists(key):
                args.key = key
                break

        if not args.key:
            print("Error: Either --password or --key must be provided")
            print("       (No default SSH keys found in ~/.ssh/)")
            sys.exit(1)

    if not any([args.command, args.upload, args.download, args.list]):
        print("Error: Must specify --command, --upload, --download, or --list")
        sys.exit(1)

    if args.upload and not args.remote_path:
        print("Error: --remote-path required with --upload")
        sys.exit(1)

    if args.download and not args.local_path:
        print("Error: --local-path required with --download")
        sys.exit(1)

    # Create client
    client = SSHClient(
        host=args.host,
        username=args.user,
        password=args.password,
        key_path=args.key,
        port=args.port,
        timeout=args.timeout
    )

    try:
        # Execute operation
        if args.command:
            stdout, stderr, exit_code = client.execute(args.command, sudo=args.sudo)

            if stdout:
                print(stdout, end='')
            if stderr:
                print(stderr, end='', file=sys.stderr)

            sys.exit(exit_code)

        elif args.upload:
            success = client.upload(args.upload, args.remote_path)
            sys.exit(0 if success else 1)

        elif args.download:
            success = client.download(args.download, args.local_path)
            sys.exit(0 if success else 1)

        elif args.list:
            files = client.list_dir(args.list)
            for f in files:
                print(f)
            sys.exit(0 if files else 1)

    finally:
        client.disconnect()


if __name__ == '__main__':
    main()
