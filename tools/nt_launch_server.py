from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch NT Performance Hub server in the background.")
    parser.add_argument("--app", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True)
    parser.add_argument("--stdout", required=True)
    parser.add_argument("--stderr", required=True)
    parser.add_argument("--pid", required=True)
    args = parser.parse_args()

    stdout_path = Path(args.stdout)
    stderr_path = Path(args.stderr)
    pid_path = Path(args.pid)
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    pid_path.parent.mkdir(parents=True, exist_ok=True)

    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    stdout_file = stdout_path.open("ab")
    stderr_file = stderr_path.open("ab")
    try:
        process = subprocess.Popen(
            [sys.executable, args.app, "--host", args.host, "--port", str(args.port)],
            cwd=args.cwd,
            stdin=subprocess.DEVNULL,
            stdout=stdout_file,
            stderr=stderr_file,
            creationflags=creationflags,
            close_fds=False,
        )
    finally:
        stdout_file.close()
        stderr_file.close()

    pid_path.write_text(str(process.pid), encoding="ascii")
    print(process.pid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())