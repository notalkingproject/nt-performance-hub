# NT Performance Hub

NT Performance Hub is a local browser app for running live show controls from a PC, laptop, phone, or tablet. Its main purpose is to give you a phone/tablet control surface while DJing, so you can match lights, trigger visuals, recall looks, and adjust performance parameters on the fly.

The main use case is simple: NT Performance Hub sends OSC control values for performance parameters, preferably to Resolume. In our setup, Resolume is the visual and light-control hub.

It helps control:

- Lights, saved looks, and fast color matching from a phone or tablet.
- Resolume visuals, cameras, scenes, opacity, and performance parameters.
- Now Playing text from Beat Link Trigger or manual modes.
- Album artwork colors.
- Browser-based generative visuals.
- Show sequences.
- Optional OBS recording/streaming controls.
- Macros: configurable OSC Buttons and server-run OSC Clocks for Resolume text or cue automation.

## How The Show Setup Works

- CDJs are connected together on the same Ethernet / Pro DJ Link network.
- [Beat Link Trigger](https://github.com/Deep-Symmetry/beat-link-trigger) listens to the CDJs on that network.
- The master player drives Now Playing, so the app follows the track currently leading the DJ set.
- NT Performance Hub turns phone/tablet touches, looks, buttons, sliders, artwork colors, and Now Playing data into OSC values.
- Resolume receives those OSC values and uses them to control visuals, lights, text layers, camera scenes, and other performance parameters.

## Quick Start

Double-click:

```text
Start NT Performance Hub.bat
```

Then open:

```text
http://127.0.0.1:8080/
```

To use a phone, tablet, or another computer, open the LAN address printed by the Start or Status window. It will look like:

```text
http://192.168.1.50:8080/
```

Before a show, open:

```text
http://127.0.0.1:8080/preflight
```


## Macros

The Macros page provides reusable show actions that are saved in the app config and run through the Python server.

### OSC Button

An OSC Button is a tablet-friendly button with a saved name, enabled state, OSC address, OSC value type, value, and optional OSC destination selection. Press **Trigger** from the editor or press the macro on the Live Deck to send one OSC action. Destination selection uses the existing OSC Targets list; leaving all destination boxes unchecked sends to every enabled OSC target.

Supported value types are Trigger/impulse, Float, Integer, String, and Boolean. Configure the OSC address to match the Resolume parameter or action you want to control.

### OSC Clock

An OSC Clock sends the server computer's local time as an OSC string once per minute. The browser does not need to stay open: the clock scheduler runs in the Python server and resumes after NT Performance Hub restarts.

Clock settings include name, enabled state, OSC address, OSC destinations, 12-hour or 24-hour format, optional prefix, optional suffix, a live preview, and **Send Now** for testing. The 12-hour format sends values such as `9:42 PM`; the 24-hour format sends values such as `21:42`. Seconds are never included.

Additional macro types such as hotkeys, webhooks, scripts, scheduled cues, or compound actions can be added later on top of the same server-owned macro model.

## The Main Buttons

- `Start NT Performance Hub.bat` starts the app.
- `Restart NT Performance Hub.bat` restarts the app when you want a clean reload.
- `NT Performance Hub Status.bat` shows the local URL, tablet URL, health, and process ID.
- `Install NT Performance Hub.bat` sets up Python packages on a new machine.
- `Push To GitHub.bat` saves laptop edits to GitHub.
- `Update From GitHub.bat` pulls the latest version onto the performance PC.

## Stopping The App

If the server is running in a command window, close that window to stop the app.

Use `Restart NT Performance Hub.bat` when you want to reload the server without thinking through the stop/start steps.

## What You Need

Basic app requirements:

- A Windows PC to run the server.
- Python 3.11 or newer.
- A modern browser.
- Same network or Wi-Fi for phones, tablets, and other PCs.
- Windows Firewall allowing Python on private networks.

Show-system requirements:

- CDJs on the same Ethernet / Pro DJ Link network.
- [Beat Link Trigger](https://github.com/Deep-Symmetry/beat-link-trigger) if you want live CDJ / Pro DJ Link Now Playing data.
- Resolume if you want visuals, lights, cameras, scenes, or text layers controlled by OSC.
- Stable IP addresses or machine names for show devices.
- A readable music folder if using artwork matching.
- OBS with WebSocket enabled if you want recording/streaming controls.
- Spotify developer credentials are required for live Spotify Now Playing via the local OAuth PKCE connection.

Read `SYSTEM_REQUIREMENTS.md` for the plain-English show setup checklist.


## Optional Integrations

OBS control uses OBS WebSocket on the show PC. Enable OBS WebSocket in OBS, then set the host, port, and password in Settings. The password is saved only in your local ignored config file.

Spotify Now Playing uses Spotify OAuth PKCE, stores local tokens in ignored `data/spotify_tokens.json`, polls Spotify only while Spotify mode is active, sends the existing Now Playing OSC outputs, and updates `current_artwork.jpg`. Automatic artwork color matching remains controlled only by the Lights album-art matching setting.
## GitHub Workflow

On the laptop where you edit:

```text
Push To GitHub.bat
```

On the performance PC:

```text
Update From GitHub.bat
```

Machine-specific config, logs, generated data, and PID files stay local and are ignored by Git.

## Important Files

- `app.py` is the local web server and show-control engine.
- `web/` contains the browser interface.
- `config/app_config.example.json` is the starting config for a new machine.
- `SYSTEM_REQUIREMENTS.md` explains the needed show software and connections.
- `PORTABLE_INSTALL.md` explains setup on another Windows machine.
- `DESIGN_PRINCIPLES.md` explains design direction for future edits.
- `CHANGELOG.md` tracks notable changes.

## Python Packages

`requirements.txt` is only for Python packages installed by `pip`.

It does not list Beat Link Trigger, Resolume, CDJs, network gear, or firewall settings. Those are covered in `SYSTEM_REQUIREMENTS.md`.



## Unified Now Playing Display

NT Performance Hub now keeps one server-owned Now Playing read model for display clients. Spotify, BeatLink / CDJ, Vinyl, Studio, and Videogames publish normalized state into this service while the explicit source selector remains authoritative. Updating an inactive source does not take over the public display.

Display page:

```text
/display/now-playing
```

Read-only local API endpoints:

```text
GET /api/now-playing
GET /api/now-playing/status
GET /api/now-playing/artwork
GET /api/now-playing/events
```

Example response:

```json
{
  "ok": true,
  "now_playing": {
    "source": "spotify",
    "source_label": "Spotify",
    "title": "Track Name",
    "artist": "Artist Name",
    "album": "Album Name",
    "artwork_url": "/api/now-playing/artwork?v=12",
    "has_artwork": true,
    "is_playing": true,
    "is_paused": false,
    "progress_ms": 83000,
    "duration_ms": 248000,
    "state_version": 123
  }
}
```

`/api/now-playing/events` is a Server-Sent Events stream. Browsers reconnect automatically and receive the current state immediately after connecting. Artwork URLs use the artwork version query parameter for cache busting.

To open the display from another device, start NT Performance Hub, use the computer's private-network address, and open:

```text
http://YOUR_COMPUTER_IP:8080/display/now-playing
```

Use the configured app port if you changed it from `8080`. Windows Firewall may need to allow the NT Performance Hub port on private networks. Do not expose this server directly to the public internet.

The display API intentionally excludes Spotify tokens, OAuth state, local filesystem paths, OSC target addresses, SMB music-library paths, raw source payloads, and private app configuration. It is read-only and cannot switch sources or trigger outputs.
