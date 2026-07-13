# Portable Install

This NT Performance Hub folder is intended to be copied to another Windows machine and hosted locally from that machine.

## Fast Path

1. Copy the whole `NT Performance Hub` folder to the show computer.
2. Run `Install NT Performance Hub.bat` once.
3. Run `Start NT Performance Hub.bat`.
4. Open `http://127.0.0.1:8080/` on the show computer.
5. On a tablet, open one of the LAN URLs printed by the server, usually `http://<show-computer-ip>:8080/`.

## Configure The New Machine

Copy `config/app_config.example.json` to `config/app_config.json`, then edit these values for the room:

- `music_root`: local path like `D:\Music` or a network share like `\\SHOW-PC\Music`.
- `network_machines`: machine labels and IP addresses for the laptop, show PC, and stream PC.
- `network_routes`: which machine has Beat Link Trigger and which machine receives Resolume OSC.
- `osc_targets`: every Resolume or stream machine that should receive OSC commands.
- `vinyl_logo_path` and `studio_artwork_path`: put portable branding files in `assets/` or use absolute paths on the show machine.

## Network Notes

- Run the app with host `0.0.0.0` when a tablet or another computer needs access.
- Allow Python through Windows Firewall on the private network for port `8080`.
- Keep Beat Link Trigger reachable from the host machine on the configured `beatlink_port`.
- If the music collection lives on another computer, use a stable Windows share path and make sure the show computer can read it before starting the app.

## Generated Files

These stay local to each machine and should not be treated as source:

- `config/app_config.json`
- `data/music_library_index.json`
- `data/current_artwork.jpg`
- `logs/*.csv`
- `logs/*.log`
- `.venv/`

## Diagnostics

With the app running, use:

```powershell
.\.venv\Scripts\python.exe .\tools\diagnostic_check.py --url http://127.0.0.1:8080
```

Without the app running, use:

```powershell
.\.venv\Scripts\python.exe .\tools\diagnostic_check.py
```