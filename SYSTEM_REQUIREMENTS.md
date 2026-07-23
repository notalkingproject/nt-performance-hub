# System Requirements

This is the plain-English checklist for what NT Performance Hub needs around it.

`requirements.txt` is only for Python packages. This file is for the actual show setup: computers, software, network, Resolume, Beat Link Trigger, CDJs, and music paths.

## The Simple Version

You need:

- One Windows computer to run NT Performance Hub.
- Python installed on that computer.
- A browser on any device you want to control from.
- All control devices on the same network.
- CDJs connected on the same Ethernet / Pro DJ Link network.
- [Beat Link Trigger](https://github.com/Deep-Symmetry/beat-link-trigger) if you want live CDJ track info.
- Resolume if you want visuals, lights, cameras, scenes, text, or opacity controlled by OSC.
- A music folder the server computer can read if you want album-art matching.
- OBS with WebSocket enabled if you want the app to start/stop recording or streaming.
- Spotify account/API setup later if you want Spotify metadata to feed Now Playing and artwork colors.

## What The App Does

NT Performance Hub is a phone/tablet-friendly OSC control hub for live DJ performance.

In this setup, the app lets you use a phone, tablet, or browser to match lights, control visuals, recall looks, and adjust performance parameters while DJing. It sends OSC values that we control. Those values can come from buttons, sliders, looks, sequences, album artwork, manual Now Playing modes, or Beat Link Trigger data.

The preferred target is Resolume. Resolume then handles the visual and light-control side of the show.

## Recommended Show Layout

- Performance PC: runs NT Performance Hub and Resolume, ideally connected by Ethernet.
- Laptop: used for editing the app and pushing updates to GitHub.
- Phone/tablet: opens the web app over Wi-Fi for on-the-fly performance control while DJing.
- CDJs: connected together on the Ethernet / Pro DJ Link network.
- Beat Link Trigger machine: listens to the CDJs and exposes track/player data.
- Resolume machine: receives OSC commands from NT Performance Hub.

One computer can do more than one job. For example, the performance PC can run NT Performance Hub, Beat Link Trigger, and Resolume if the network is set up correctly.

## Network Basics

Everything that uses the web app needs to be on the same local network.

The CDJs and Beat Link Trigger need to be on the same Ethernet / Pro DJ Link network so Beat Link Trigger can see the players.

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

## Beat Link Trigger And Now Playing

Use [Beat Link Trigger](https://github.com/Deep-Symmetry/beat-link-trigger) when you want NT Performance Hub to read live CDJ track information.

The CDJs should be on the same Ethernet / Pro DJ Link network as Beat Link Trigger.

NT Performance Hub uses Beat Link Trigger data to follow the master player for Now Playing. In normal use, the master player is the deck currently driving the DJ set, and that deck drives the Now Playing title, artist, artwork lookup, and related OSC text output.

Default Beat Link Trigger address:

```text
http://<beatlink-machine-ip>:17081/params.json
```

Default port:

```text
17081
```

If Beat Link Trigger is not running, manual Now Playing modes still work. Preflight will show a warning.

## Resolume And OSC

Use Resolume when NT Performance Hub should control visuals, lights, cameras, scenes, text, or opacity.

In our use case, Resolume is the main target for performance-control OSC. NT Performance Hub sends controlled OSC values, and Resolume maps those values to clips, layers, parameters, text, effects, or lighting/video routes.

In Resolume:

- Enable OSC input.
- Use the same OSC port configured in NT Performance Hub.
- Map the OSC addresses you want to control.
- Keep the Resolume machine on the same network as NT Performance Hub.

Default OSC port:

```text
7000
```

OSC uses UDP. That means NT Performance Hub can send commands, but it cannot fully prove Resolume received every message.


## OBS And Spotify

OBS control is optional. If you use it, OBS should run on the same performance PC as NT Performance Hub. Enable OBS WebSocket in OBS, then save the host, port, and password in NT Performance Hub Settings.

Spotify is planned as its own Now Playing source. It should use a login flow so the app can read current track metadata and artwork without storing secrets in GitHub. Local tokens and secrets belong in ignored config files only.
## Music And Artwork

For album-art matching, the performance PC must be able to read the music folder.

Examples:

```text
D:\Music
\\MUSIC-SERVER\Music
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
5. Confirm the CDJs are on the Ethernet / Pro DJ Link network.
6. Confirm Beat Link Trigger sees the players if using CDJ data.
7. Confirm the master player drives Now Playing as expected.
8. Confirm Resolume OSC targets if using Resolume.
9. Confirm music/artwork paths if using album art.
10. Confirm Git state is clean enough for the performance PC.

Warnings are normal if show hardware is disconnected. Errors are the things to fix before depending on the system live.

