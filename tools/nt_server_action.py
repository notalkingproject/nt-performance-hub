from __future__ import annotations

import argparse
import os
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

APP_NAME = "NT Performance Hub"
ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "app.py"
LOGS_DIR = ROOT / "logs"
DATA_DIR = ROOT / "data"
PID_PATH = DATA_DIR / "server.pid"
OUT_LOG = LOGS_DIR / "server.out.log"
ERR_LOG = LOGS_DIR / "server.err.log"


def ensure_dirs() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def read_pid() -> int | None:
    try:
        text = PID_PATH.read_text(encoding="ascii").strip()
        return int(text) if text else None
    except Exception:
        return None


def write_pid(pid: int) -> None:
    ensure_dirs()
    PID_PATH.write_text(str(pid), encoding="ascii")


def remove_pid() -> None:
    try:
        PID_PATH.unlink()
    except FileNotFoundError:
        pass


def process_alive(pid: int | None) -> bool:
    if not pid:
        return False
    if os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes

            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            STILL_ACTIVE = 259
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if not handle:
                return False
            exit_code = wintypes.DWORD()
            try:
                if not kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                    return False
                return exit_code.value == STILL_ACTIVE
            finally:
                kernel32.CloseHandle(handle)
        except Exception:
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def health_ok(port: int) -> bool:
    try:
        with urlopen(f"http://127.0.0.1:{port}/health", timeout=1.5) as response:
            return 200 <= response.status < 400
    except Exception:
        return False


def identity_ok(port: int) -> bool:
    try:
        with urlopen(f"http://127.0.0.1:{port}/api/identity", timeout=1.5) as response:
            return b"NT Performance Hub" in response.read(2048)
    except Exception:
        return False


def port_available(port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def lan_urls(port: int) -> list[str]:
    urls: list[str] = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if ip.startswith("127.") or ip.startswith("169.254."):
                continue
            url = f"http://{ip}:{port}/"
            if url not in urls:
                urls.append(url)
    except Exception:
        pass
    return urls


def print_status(port: int) -> None:
    pid = read_pid()
    alive = process_alive(pid)
    print(f"{APP_NAME} status")
    print(f"Local:     http://127.0.0.1:{port}/")
    print(f"Preflight: http://127.0.0.1:{port}/preflight")
    for url in lan_urls(port):
        print(f"Remote:    {url}")
    print(f"Health:    {'ok' if health_ok(port) else 'not responding'}")
    print(f"PID file:  {pid if pid else 'none'}")
    print(f"Managed:   {'running' if alive else 'not running'}")


def launch_server(host: str, port: int) -> int:
    ensure_dirs()
    flags = 0
    if os.name == "nt":
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    with OUT_LOG.open("ab") as stdout_file, ERR_LOG.open("ab") as stderr_file:
        process = subprocess.Popen(
            [sys.executable, str(APP_PATH), "--host", host, "--port", str(port)],
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stdout_file,
            stderr=stderr_file,
            creationflags=flags,
            close_fds=False,
        )
    write_pid(process.pid)
    return process.pid


def start_app(host: str, port: int, open_browser: bool) -> int:
    if identity_ok(port):
        print(f"{APP_NAME} is already running.")
        print_status(port)
        if open_browser:
            webbrowser.open(f"http://127.0.0.1:{port}/")
        return 0

    pid = read_pid()
    if pid and not process_alive(pid):
        remove_pid()

    if not port_available(port):
        print(f"Port {port} is already in use by another app.")
        print("Close that app, or run Start NT Performance Hub.bat with another port number.")
        return 1

    print(f"Starting {APP_NAME} on http://127.0.0.1:{port}/")
    print(f"Logs: {OUT_LOG}")
    pid = launch_server(host, port)
    for _ in range(30):
        if health_ok(port):
            print_status(port)
            if open_browser:
                webbrowser.open(f"http://127.0.0.1:{port}/")
            return 0
        if not process_alive(pid):
            break
        time.sleep(0.5)

    print("Server did not become healthy within 15 seconds.")
    print(f"Check logs: {OUT_LOG}")
    print(f"Check errors: {ERR_LOG}")
    return 1


def stop_app(port: int) -> int:
    pid = read_pid()
    if not pid:
        print(f"{APP_NAME} is not running from the managed launcher.")
        print("If it is open in a command window, close that window to stop it.")
        return 0

    if not process_alive(pid):
        remove_pid()
        print(f"{APP_NAME} was not running; cleared stale PID file.")
        return 0

    print(f"Stopping {APP_NAME} PID {pid}...")
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception:
        pass
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=False, timeout=3)
        except Exception:
            pass

    for _ in range(20):
        if not process_alive(pid):
            remove_pid()
            print("Stopped.")
            return 0
        time.sleep(0.25)

    print("Stop command was sent, but the process still appears to be running.")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=f"Manage {APP_NAME}.")
    parser.add_argument("action", choices=["start", "stop", "restart", "status"])
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--open", action="store_true")
    args = parser.parse_args()

    if args.action == "start":
        return start_app(args.host, args.port, args.open)
    if args.action == "stop":
        return stop_app(args.port)
    if args.action == "restart":
        stopped = stop_app(args.port)
        if stopped != 0:
            return stopped
        return start_app(args.host, args.port, args.open)
    print_status(args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

