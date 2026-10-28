#!/usr/bin/env python3
"""Prepare a separate Paper 26.2 + EaglerXPaper server directory.

This intentionally does not modify the legacy Bungee/Paper 1.8.8 files.
Run from any directory with Python 3 and Java 25+ installed.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
MANIFEST = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
SERVER = REPO_ROOT / "server-26.2"
PLUGINS = SERVER / "plugins"


def java_major() -> int | None:
    try:
        output = subprocess.check_output(
            ["java", "-version"], stderr=subprocess.STDOUT, text=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    match = re.search(r'version\s+"(?:1\.)?(\d+)', output)
    return int(match.group(1)) if match else None


def download_verified(url: str, destination: Path, expected_sha256: str) -> None:
    if destination.exists():
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        if digest.lower() == expected_sha256.lower():
            print(f"Already verified: {destination.name}")
            return
        raise RuntimeError(
            f"{destination} exists but SHA-256 does not match the pinned manifest. "
            "Move it aside before rerunning setup."
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    request = urllib.request.Request(
        url, headers={"User-Agent": "EaglercraftX-Server-26.2-setup"}
    )
    print(f"Downloading {destination.name} ...")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            with temporary.open("wb") as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    output.write(chunk)
        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
        if digest.lower() != expected_sha256.lower():
            raise RuntimeError(
                f"SHA-256 mismatch for {destination.name}: {digest}"
            )
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    detected_java = java_major()
    minimum = MANIFEST["minimumJavaMajor"]
    if detected_java is None:
        print("Java was not found. Install Java 25+ and add it to PATH.", file=sys.stderr)
        return 1
    if detected_java < minimum:
        print(
            f"Java {detected_java} detected; this Paper 26.2 build requires Java {minimum}+.",
            file=sys.stderr,
        )
        return 1

    SERVER.mkdir(parents=True, exist_ok=True)
    PLUGINS.mkdir(parents=True, exist_ok=True)

    paper_info = MANIFEST["paper"]
    paper = SERVER / paper_info["fileName"]
    download_verified(paper_info["url"], paper, paper_info["sha256"])

    plugin_info = MANIFEST["eaglerXPaper"]
    plugin = PLUGINS / plugin_info["fileName"]
    download_verified(plugin_info["url"], plugin, plugin_info["sha256"])

    stable = SERVER / "paper.jar"
    if not stable.exists():
        # A copy avoids symlink differences across Windows/Linux.
        stable.write_bytes(paper.read_bytes())

    properties = SERVER / "server.properties"
    if not properties.exists():
        properties.write_text(
            "# Local-first defaults. Review security and networking before exposing publicly.\n"
            "server-port=25565\n"
            "server-ip=127.0.0.1\n"
            "online-mode=false\n"
            "white-list=true\n"
            "enforce-whitelist=true\n"
            "motd=Eaglercraft 26.2 Server\n"
            "max-players=10\n"
            "spawn-protection=16\n",
            encoding="utf-8",
        )

    eula = SERVER / "eula.txt"
    if not eula.exists():
        eula.write_text(
            "# Read https://aka.ms/MinecraftEULA before accepting.\n"
            "eula=false\n",
            encoding="utf-8",
        )

    print("\nSetup files prepared in:", SERVER)
    print("Before starting, read the README and review the EULA.")
    print("The EULA remains false until you explicitly accept it.")
    print("Local-only networking and whitelist are enabled as safer defaults.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Setup failed: {error}", file=sys.stderr)
        raise SystemExit(1)
