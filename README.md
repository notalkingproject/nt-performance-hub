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
- A starter Macros section for future OSC, hotkey, webhook, or script buttons.

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
- Spotify developer login setup later if you want Spotify Now Playing metadata/artwork.

Read `SYSTEM_REQUIREMENTS.md` for the plain-English show setup checklist.


## Optional Integrations

OBS control uses OBS WebSocket on the show PC. Enable OBS WebSocket in OBS, then set the host, port, and password in Settings. The password is saved only in your local ignored config file.

Spotify is scaffolded as a future Now Playing source. The plan is OAuth login, then use Spotify metadata/artwork for Now Playing and artwork-driven lights. Do not commit Spotify secrets or tokens to GitHub.
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

