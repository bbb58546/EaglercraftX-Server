# Eaglercraft 26.2 server (separate migration path)

This folder adds a **separate** Paper 26.2 + EaglerXPaper setup. The existing legacy BungeeCord/EaglercraftXBungee files are intentionally left untouched.

## Requirements

- Java 25 or newer
- Python 3
- Several GB of available RAM and disk space
- Read and comply with the Minecraft EULA

## Setup

From the repository root:

```bash
python3 modern-26.2/setup.py
```

On Windows, use `py -3 modern-26.2\setup.py`.

The script downloads pinned Paper 26.2 and EaglerXPaper files, verifies SHA-256 checksums, and prepares `server-26.2/`. It does not download or bundle the browser client.

## Accept the EULA and start

Read https://aka.ms/MinecraftEULA. If you agree, edit `server-26.2/eula.txt` and change `eula=false` to `eula=true`.

Then run:

- Linux/macOS: `sh modern-26.2/start-server.sh`
- Windows: `modern-26.2\start-server.bat`

## Automated checks

GitHub Actions validates the Python syntax, manifest structure and SHA-256 formatting, and shell launcher syntax on pushes to this migration branch. Passing these checks does **not** prove that the downloaded server boots or that a browser client can connect; those still require an end-to-end test.

## Important limitations

- This is an initial setup path, **not a claim that the server has been tested end-to-end**.
- Eaglercraft 26.2 is a newer client family; this path uses Paper 26.2 with the community EaglerXPaper bridge rather than the old EaglercraftXBungee plugin.
- The initial properties bind to `127.0.0.1` and enable the whitelist. That is intentionally local-only until you deliberately configure networking.
- `online-mode=false` is used for Eagler-compatible offline identities. Do not expose an offline-mode server publicly without first configuring and testing an appropriate authentication plugin and access controls.
- The whitelist starts enabled. Add allowed player names from the server console before joining.
- The browser game client is not included. Use a client build you are permitted to use, and configure a secure WebSocket (`wss://`) endpoint before public hosting.
- Existing 1.8.8 world data and plugins are not automatically compatible with 26.2. Back up any world before attempting conversion.
