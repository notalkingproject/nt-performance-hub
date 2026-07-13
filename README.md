# NT Performance Hub

This folder is the browser-control app for a DJ/VJ performance system built around Beat Link Trigger, album artwork, lighting color logic, camera cues, visual cues, and Resolume OSC.

The browser app is the main direction for live control from the show computer, another laptop, or an eventual tablet surface. The legacy Tkinter GUI is preserved in `archive/legacy_desktop_gui/` for reference and compatibility.

## Current Shape

The browser app is a performance hub with these major sections:

- **Lights** - modular live lighting workspace with looks and compact BPM in a sub-pane, and primary color/slider controls first in the main pane.
- **Visuals** - Resolume visual cue buttons, visual opacity, and browser-rendered generative visuals.
- **Cameras** - main, PIP, background, and scene trigger groups with visually separated trigger banks.
- **Looks** - combined performance presets and linked cues. A look can store lighting values, Now Playing mode, section preset, visual cue, generative visual settings, camera cues, background cue, and scene cue.
- **Sequencer** - saved Show sequences that arrange looks over bars, beats, seconds, or minutes.
- **Now Playing** - BeatLink / BLT metadata, album artwork monitoring, manual modes, and stream text OSC outputs.
- **Settings** - core config plus section-specific OSC settings.
- **Log** - recent OSC sends and app events.

The app uses a left rail so the current preview and section navigation stay available while the main right pane shows the selected work area.

## Folder Structure

- `app.py` - local HTTP server, status API, config API, OSC sender, preset engine, artwork palette logic, camera/visual/Now Playing commands.
- `web/index.html` - browser app structure.
- `web/app.js` - browser app state, UI rendering, command handlers, settings editors, look editor, OSC builder.
- `web/styles.css` - tablet-oriented dark UI styling.
- `web/generative.html`, `web/generative.js`, `web/generative.css` - fullscreen browser-rendered generative visual output.
- `Start NT Performance Hub.bat` - Windows launcher for the browser app server.
- `Install NT Performance Hub.bat` - one-time Windows setup for the local Python environment.
- `Update From GitHub.bat` - performance-PC updater after the GitHub remote is connected.
- `config/` - local app configuration and visual defaults.
- `data/` - generated music-library index data.
- `logs/` - generated performance and track-history logs.
- `archive/legacy_desktop_gui/` - preserved desktop GUI.
- `beatlink_watcher_resolume_osc.py` - Beat Link Trigger polling, MP3 matching, metadata, and OSC helpers.
- `extract_album_artwork.py` - embedded artwork extraction helper.
- `DESIGN_PRINCIPLES.md` - product and engineering guidance for future UI/code changes.

Project notes:

- `CHANGELOG.md` tracks the change history.
- `PORTABLE_INSTALL.md` is the install/run guide for another Windows machine or a local show computer.
- `config/app_config.example.json` is a portable starting point; copy it to `config/app_config.json` only on the machine you are setting up.

Generated local state is not intended as source code:

- `data/music_library_index.json`
- `config/app_config.json`
- `config/visual_defaults.json`
- `logs/performance_lighting_YYYY-MM-DD.csv`
- `logs/track_color_history_YYYY-MM-DD.csv`

## Launch

Run the app server:

```powershell
.\Start NT Performance Hub.bat
```

Then open this on the show computer:

```text
http://127.0.0.1:8080/
```

For another computer or tablet, open the LAN address shown by the server, for example:

```text
http://192.168.1.50:8080/
```

If another device cannot connect, check that it is on the same network and that Windows Firewall allows inbound access to port `8080` for Python.

## OSC Outputs

The app can send every OSC command to multiple Resolume receivers. Manage this in **Settings -> OSC Output Targets**.

Current configured targets:

- Laptop Resolume: `192.168.1.189:7000`
- Stream PC: `192.168.1.9:7000`

The legacy **Active Resolume IP** remains the primary target for compatibility, but live commands fan out to every enabled OSC target.

## Looks

Looks are now the center of the performance workflow.

A look can store:

- Primary, secondary, and accent colors.
- Motion, strobe, saturation, brightness, FX, and pulse percentages.
- Now Playing mode: CDJ metadata, Vinyl mode, or NO TALKING STUDIO.
- Section preset.
- Visual cue.
- Generative visual preset, intensity, complexity, motion, beat response, color source, phrase morph, seed behavior, quality, and output level.
- Main camera cue.
- PIP camera cue.
- Background camera cue.
- Scene cue.

On the Looks page, each card can be edited directly. The light controls on the card send live while you adjust them. **Save** stores the edited light values plus cue selections, and **Trigger** launches that saved look. Empty cue fields such as `None` or `No change` simply do nothing for that category.

The Lights page also exposes looks as a vertical sub-pane so performance presets stay available without forcing the main color and slider controls below the fold.

The Look Builder includes an editable **Look Name** field. Typing a new name and saving creates a new look from the current live light state plus the selected cue links. Editing an existing card name and saving renames that look.

## Generative Visuals

Open the fullscreen output at:

```text
http://127.0.0.1:8080/visuals/generative
```

This page renders mathematical visuals in the browser on a black projection-friendly canvas. Capture that browser window into Resolume, OBS, NDI, Spout, or a normal window/browser source. For Resolume, open the visualizer in a dedicated browser window, then use the browser/window capture route that fits your show computer setup.

The left rail includes a dedicated **Generator** section with an embedded live preview, selected color swatches, thumbnail preset cards, mood/use descriptions, BPM sync automation, and live controls for preset, color source, intensity, complexity, motion, beat response, scale, zoom, rotation, symmetry, warp, line width, trail, phrase morph, auto seed, quality, freeze, stop, and output level. Changes send immediately to the Python server. The server owns the current state and exposes it through `/api/generative/state`.

Starter presets:

- Lissajous Orbit.
- Moire Grid.
- Superformula Mandala.
- Particle Vortex.
- Shader Plasma.
- Harmonic Tunnel.
- Vector Field.
- Crystal Rings.
- Wave Ribbons.
- Starfield Gate.
- Kaleido Mesh.
- Liquid Topo.
- Pulse Bars.
- Constellation Web.
- Scanline Bloom.
- Orbital Dust.

Looks can store generative visual settings alongside light values, Now Playing mode, Resolume visual cue, cameras, and scene. When a Show triggers a Look, any stored generative visual settings apply naturally because Shows trigger Looks.

Visualizer keyboard controls:

- `1`-`5` select starter presets locally.
- `H` toggles the debug overlay.
- `F` requests fullscreen.
- `Q` cycles quality.
- `Space` freezes or unfreezes animation locally.
- `0` toggles blackout locally.

Performance troubleshooting:

- The visualizer continues rendering from the last known state if polling disconnects.
- The debug overlay shows connection and FPS.
- Quality automatically steps down if FPS stays below 25 for more than five seconds.
- If a preset throws, the renderer falls back to Lissajous Orbit.
- Use **Stop** in the Visuals panel for a server-owned blackout/disabled state.

## Sequencer

The Sequencer page is the automation layer: a saved **Show** is a named list of look triggers. A look already contains the light values, Now Playing mode, visual cue, camera cues, opacity choices, and scene cue, so sequencing a show means sequencing complete performance states.

Each sequence step stores:

- The look link to trigger.
- Trigger style: after the previous step or at show time.
- Amount.
- Unit: bars, beats, seconds, or minutes.
- A note or song-section label.

`After previous` waits that amount before firing the row. `At show time` treats the amount as an absolute position from the start of playback.

The show transport can **Play**, **Pause**, **Stop**, and **Next Step** directly from the browser. Enable **Loop Show** for repeating song-section cycles, ambient holding patterns, rehearsal passes, or podcast/live-stream beds that should keep rotating until stopped.

This is intended to support full-show automation, podcast/feed production, and song-section cueing where looks advance by musical section or by timed events. Bars and beats use the current app BPM, including Now Playing BPM when follow mode is active.

## OSC Mapping

OSC settings are section-local so you can edit addresses near the controls they affect:

- Lights OSC lives with Lights.
- Visual OSC lives with Visuals.
- Camera and scene OSC lives with Cameras.
- Now Playing text OSC lives with Now Playing.

Resolume-style OSC address fields include an OSC builder. You can edit:

- Layer type: group or layer.
- Layer / group number.
- Column type: column or clip.
- Column / clip number.
- Action path.

The full OSC address can still be typed manually. If it matches the Resolume path pattern, the builder reads it back into the smaller fields. This is meant for fast changes when Resolume layer or column numbers shift.

OSC builder controls wrap inside their section cards so long Lights OSC mappings stay editable without pushing the page sideways.

## Artwork + Now Playing

The app monitors album artwork and BeatLink / BLT metadata separately from the lighting surface, while still showing artwork controls near Lights for fast color matching.

The artwork color matcher can:

- Extract colors from the current artwork.
- Apply a detected palette to primary, secondary, and accent.
- Preserve current preset colors when desired.
- Use automatic artwork colors.
- Use fallback-only behavior.
- Pick neutral primary, neutral secondary, and neutral accent colors for black, white, gray, or low-saturation covers.

The palette algorithm prefers distinct saturated artwork colors first. If an album cover is dominated by whites, blacks, grays, or does not produce enough distinct colors, it fills the missing roles from the configured neutral colors.

## Live Controls

Most performance controls send immediately when changed. The old individual Send-button pattern is being phased out in favor of:

- Tap buttons for cue changes.
- Sliders for continuous values.
- Stop buttons for setting intensity-style values to zero.
- Save buttons only for configuration or preset persistence.

## Setup

Install Python dependencies:

```powershell
py -m pip install -r requirements.txt
```

If `py` is not available:

```powershell
python -m pip install -r requirements.txt
```

## Legacy Desktop GUI

Run:

```powershell
.\archive\legacy_desktop_gui\Start Legacy Desktop GUI.bat
```

Use the browser app for new live-control work. The archived desktop GUI stays available for compatibility checks and old workflows.

## Logs

The detailed daily OSC log is saved as:

```text
logs/performance_lighting_YYYY-MM-DD.csv
```

A setlist-friendly history is saved as:

```text
logs/track_color_history_YYYY-MM-DD.csv
```

The history includes track load/end rows, MP3 comments, suggested color comments, selected colors, source, and matched file.
