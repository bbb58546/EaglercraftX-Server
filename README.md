# Eaglercraft Server

This fork keeps the original legacy server files while adding a separate **Eaglercraft 26.2** setup path.

## Eaglercraft 26.2 (new setup path)

The new setup lives in `modern-26.2/` and uses **Paper 26.2 + EaglerXPaper**. It is separate from the older BungeeCord + EaglercraftXBungee setup.

### Requirements

- Java 25+
- Python 3
- Enough free disk space and RAM for the server
- Read and comply with the Minecraft EULA

### Setup

From the repository root:

```bash
python3 modern-26.2/setup.py
```

On Windows:

```bat
py -3 modern-26.2\setup.py
```

The setup downloads pinned server files, verifies their SHA-256 checksums, and prepares `server-26.2/`. It does not download or bundle a browser client.

Read https://aka.ms/MinecraftEULA. If you agree, change `eula=false` to `eula=true` in `server-26.2/eula.txt`.

Start it with:

- Linux/macOS: `sh modern-26.2/start-server.sh`
- Windows: `modern-26.2\start-server.bat`

The initial configuration binds to localhost and enables the whitelist. This is intentional: do not expose an offline-mode server publicly until appropriate authentication and access controls have been configured and tested. Add permitted players to the whitelist from the server console.

See [modern-26.2/README.md](modern-26.2/README.md) for limitations and next steps.

## Legacy server

The existing `bungee/`, `server/`, and legacy scripts remain for the older EaglercraftX server setup. They have **not** been upgraded to 26.2 and should not be mixed with the new Paper 26.2 setup.

## Status

The 26.2 setup path is an initial migration scaffold. The downloaded files are checksum-pinned, but the server has not yet been launched or tested end-to-end in this repository. A compatible 26.2 browser client and a properly configured WebSocket endpoint are still needed for remote browser players.
