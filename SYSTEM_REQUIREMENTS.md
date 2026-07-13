# System Requirements

This is the plain-English checklist for what NT Performance Hub needs around it.

`requirements.txt` is only for Python packages. This file is for the actual show setup: computers, software, network, Resolume, Beat Link Trigger, and music paths.

## The Simple Version

You need:

- One Windows computer to run NT Performance Hub.
- Python installed on that computer.
- A browser on any device you want to control from.
- All devices on the same network.
- [Beat Link Trigger](https://github.com/Deep-Symmetry/beat-link-trigger) if you want live CDJ track info.
- Resolume if you want visuals, cameras, scenes, text, or opacity controlled by OSC.
- A music folder the server computer can read if you want album-art matching.

## Recommended Show Layout

- Performance PC: runs NT Performance Hub, Resolume, and ideally connects by Ethernet.
- Laptop: used for editing the app and pushing updates to GitHub.
- Phone/tablet: opens the web app over Wi-Fi for live control.
- Beat Link Trigger machine: reads CDJ / Pro DJ Link data.
- Resolume machine: receives OSC commands from NT Performance Hub.

One computer can do more than one job. For example, the performance PC can run both NT Performance Hub and Resolume.

## Network Basics

Everything needs to be on the same local network.

Default NT Performance Hub address:

```text
http://127.0.0.1:8080/
```

Tablet or other PC address:

```text
http://<performance-pc-ip>:8080/
```

Example:

```text
http://192.168.1.50:8080/
```

Windows Firewall must allow Python on the private network so phones/tablets can connect.

## Beat Link Trigger

Use [Beat Link Trigger](https://github.com/Deep-Symmetry/beat-link-trigger) when you want NT Performance Hub to read live CDJ track information.

Default Beat Link Trigger address:

```text
http://<beatlink-machine-ip>:17081/params.json
```

Default port:

```text
17081
```

If Beat Link Trigger is not running, manual Now Playing modes still work. Preflight will show a warning.

## Resolume

Use Resolume when NT Performance Hub should trigger visuals, cameras, scenes, text, or opacity.

In Resolume:

- Enable OSC input.
- Use the same OSC port configured in NT Performance Hub.
- Keep the machine on the same network.

Default OSC port:

```text
7000
```

OSC uses UDP. That means NT Performance Hub can send commands, but it cannot fully prove Resolume received every message.

## Music And Artwork

For album-art matching, the performance PC must be able to read the music folder.

Examples:

```text
D:\Music
\\SHOW-PC\Music
```

Artwork and machine-specific settings live in:

```text
config/app_config.json
```

Start from:

```text
config/app_config.example.json
```

## Before A Show

1. Run `Start NT Performance Hub.bat`.
2. Open `http://127.0.0.1:8080/preflight`.
3. Confirm the app server is running.
4. Confirm the tablet URL works.
5. Confirm Beat Link Trigger if using CDJ data.
6. Confirm Resolume OSC targets if using Resolume.
7. Confirm music/artwork paths if using album art.
8. Confirm Git state is clean enough for the performance PC.

Warnings are normal if show hardware is disconnected. Errors are the things to fix before depending on the system live.

