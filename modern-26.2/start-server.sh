#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SERVER="$ROOT/server-26.2"
if [ ! -f "$SERVER/paper.jar" ]; then
  echo "Run python3 modern-26.2/setup.py first."
  exit 1
fi
if ! grep -q '^eula=true$' "$SERVER/eula.txt"; then
  echo "Read https://aka.ms/MinecraftEULA and set eula=true in server-26.2/eula.txt only if you agree."
  exit 1
fi
cd "$SERVER"
exec java -Xms1G -Xmx3G -jar paper.jar --nogui
