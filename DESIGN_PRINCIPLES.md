# Design Principles

This document is the working product and engineering guide for NT Performance Hub. It should be updated when the app direction changes, and it should be read before major UI or control-flow changes.

## Product Goal

Build a fast, tablet-friendly performance hub for NO TALKING DJ/VJ sets, stream control, and show automation.

The app should let the performer move through a set without thinking about file paths, OSC syntax, or multiple disconnected tools. A song, look, artwork state, camera cue, visual cue, generator state, and stream display should feel like one connected performance decision.

## Core Workflow

The app is organized around a fast Live Deck plus detailed section pages:

- **Live Deck** is the primary performance surface. It exposes the most-used controls from each function in one place and supports Live / Preview cue routing with a global GO action.
- **Lights** controls immediate color and motion output.
- **Visuals** controls Resolume visual clips and visual opacity.
- **Generator** controls browser-rendered generative visual output, preview, presets, and capture routing.
- **Cameras** controls main, PIP, background, scenes, and camera opacity.
- **Looks** combines lighting presets with linked Now Playing, visual, generator, camera, and scene cues.
- **Sequencer** turns saved Looks into Show timelines using bars, beats, seconds, or minutes.
- **Now Playing** monitors metadata, album artwork, and stream text output.
- **Settings** configures the system without hiding important OSC mappings far away from the feature they affect.
- **Log** keeps recent OSC sends and app events visible for troubleshooting.

Looks are the main composition layer. If a performer wants "Vinyl Mode with these colors, this generator preset, and this camera angle," that should be a look.

Shows are the sequencing layer. If a performer wants an entire podcast episode, DJ set, or song arrangement to progress through looks automatically, that should be saved as a Show.

## UI Principles

1. Keep performance controls close to performance context.

   A user should not need to jump to a separate Settings page to change an OSC address for the thing they are actively configuring. Section-specific OSC sub-settings are preferred.

2. Prefer direct manipulation over abstract tables.

   Sliders, color swatches, dropdowns, and cue buttons are easier on a touchscreen than dense grids. Tables are acceptable for advanced bulk editing, but the main path should feel like a control surface.

3. Use the left rail for persistent awareness.

   The left rail should start with Now Playing summary, then section navigation and machine status. Do not duplicate the live light preview in the rail when the Active Moment strip already owns that output context.

4. Prioritize the active control surface.

   On performance pages, the most frequently touched controls should appear first in the main workspace. Supporting controls like preset selection, BPM automation, or setup helpers can live in sub-panes when that keeps live sliders and cue buttons immediately reachable.

5. Do not let fixed-width controls break the stage surface.

   UI must wrap within the right pane. Use `minmax(0, 1fr)`, `auto-fit`, and `min-width: 0` aggressively for grids. Avoid hard minimum widths that push content off-screen.

6. Save means persistence. Change means performance.

   Live controls should send when changed. Save buttons should store configuration, presets, looks, OSC maps, or defaults. Avoid Send buttons for ordinary live values, except the explicit Live / Preview workflow where Preview stages cues and GO launches the staged cue bundle.

7. Use clear performance language.

   Prefer "Stop" over harsher language for setting intensity to zero. Prefer simple look actions: "Save" stores the edited card, and "Trigger" launches it.

8. Make state visible.

   Each section should show what is currently selected: colors, look, visual, camera, scene, Now Playing mode, and key output status.

9. Tablet-first does not mean oversized.

   Controls should be large enough to tap, but dense enough for live performance scanning. Avoid decorative cards inside cards. Keep controls stable and predictable.

10. Navigation belongs in the left rail.

   The left rail owns movement between major functions. The Live Deck should show or hide function panels in place, while the left rail remains the primary way to open the full Lights, Visuals, Cameras, Looks, Sequencer, Generator, Settings, or Log pages. A compact Details link in a Live Deck card is allowed when it jumps directly to that card's matching full detail page.

11. The Performance deck mirrors the function list.

   Each live function should appear as its own optimized Live Deck panel: Looks, Lights, Visuals, Cameras, Sequencer, and Generator should not be merged just because they fit together visually. The top Live Deck controls show or hide these panels; the left rail opens the detailed page for each function.

12. Live Deck controls shape the surface, not the navigation.

   Use clearly labeled show/hide function chips to reshape the visible performance surface. Per-card controls may hide that card from the deck or link to that same function's detail page, but they should not become a second full navigation menu.

13. Keep the active moment visible across pages.

   The right workspace should begin with a persistent Active Moment strip on every major page, not only the Live Deck. Lights, Visuals, Cameras, Looks, Sequencer, Generator, Now Playing, Settings, and Log should all keep the active/preview context visible above their detail controls. The strip answers what is live right now: active look, preview look, visual, camera scene, generator, and sequence state. It must look visually different from the work panels below it, using a distinct band treatment, role accents, and stronger hierarchy instead of another row of gray cards. Keep it dense and scannable; it is a status surface, not another control panel.

14. The top chrome should not compete with the show.

   Avoid spending the top of the performance page on app branding or generic connection pills. Connection state can live in status/detail areas; the first visible row of the performance surface should be the Active Moment strip.

15. Looks use a Live / Preview flow on the Live Deck.

   The Live Deck should support A/B operation: the live state stays visible, Preview stages a look or cue bundle, and GO launches the staged preview. Active and Next/Preview should show parallel structure so the performer can compare them at a glance. The detailed Looks page can remain the place for editing and direct look management.

16. Look state includes light state.

   Do not split "Look" and "Light Output" into competing status cards when they describe the same current performance state. The top Active Moment strip should consolidate current light colors and look name into simple Active and Next/Preview look cards.

17. Hide no-change noise in the performance HUD.

   The Active Moment strip should not show repeated tiny "No change" cue cells or detailed route summaries. Active and Preview should stay simple: label, look name, color swatches, and a short state note. Detailed media, camera, scene, and Now Playing links belong in the Looks detail/editor surfaces.

18. Hold controls must always restore.

   Momentary buttons should capture the current value on press, send the held value while pressed, and restore the captured value on release, cancel, or lost pointer capture. Use this for burst-style controls such as pulse, strobe, camera punch-in, visual freeze, or generator accents.

## Button And Control Sizing

The app is a performance surface, so buttons need a consistent hierarchy. Use these defaults unless the surrounding component has a stronger local reason:

- **Section navigation**: 44-50px tall, left rail only, full-width, strong active state.
- **Live cue pads**: 38-42px tall for repeated cues such as visual slots, camera sets, scenes, and relationship shortcuts. Use compact text and fixed grid rows so pads do not stretch into oversized tiles.
- **Primary actions**: 42-48px tall for actions like Reapply, Play, Save, Trigger, or Apply Palette. These may be wider than cue pads but should not dominate a quadrant.
- **Stop / blackout / zero actions**: same size as nearby primary actions, but visually distinct with restrained red styling.
- **Visibility toggles**: 30-34px tall chips or checkbox-backed segmented controls. Use fixed chip widths on the Live Deck so the show/hide row stays predictable; use them to show/hide dashboard panels, not to navigate to another page.
- **Sequencer performance cues**: 34-42px tall compact cue buttons with a small index and truncated cue name. The Live Deck Sequencer should expose Play, Pause, Next, Stop, Loop, and immediate cue triggers without becoming the full editor.
- **Active moment strip**: 58-88px tall status cells inside a distinct top band. Active and Next/Preview look cells are the first wide cells and should share the same detail structure; the remaining status cells should use fixed, compact rhythm with short labels and single-line values.
- **A/B preview controls**: Live and Preview routing controls sit above cue buttons, with a clear GO action for staged cues.
- **Momentary buttons**: same height as nearby cue pads, amber active state, no sticky toggle behavior.
- **Sliders and selects**: keep labels above or beside controls with a stable row height. A compact slider card should be roughly 68-76px tall; avoid letting CSS grid stretch it taller just because the parent has extra space.

Spacing should be just as consistent as sizing:

- Use 6px gaps inside dense cue grids.
- Use 8px gaps between related controls in one card.
- Use 10-14px gaps between major panels or columns.
- Use 8px border radius for cards and controls unless the existing local component needs a smaller radius.

Repeated button grids must set stable rows:

```css
.cue-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(76px, 1fr));
  grid-auto-rows: minmax(40px, auto);
  align-content: start;
  gap: 6px;
}
```

Avoid `1fr` row sizing for button grids unless the intent is a deliberately large pad bank. A normal cue grid should not stretch buttons vertically to fill spare panel height.

Live Deck panels should auto-size to their actual content. Do not force every quadrant to match the tallest card in its row. If the dashboard needs a two-column packed layout, use measured row spans or content-driven rows so Looks, Lights, Visuals, Cameras, Sequencer, and Generator can each occupy the amount of space they need without large empty gray areas.

Use visual hierarchy before adding more text. Differentiate button types by role:

- Cue pads: neutral base, section-colored border, clear active state.
- Current/selected cue: section-colored active state and stronger border.
- Primary action: green or section-accent treatment.
- Utility/default action: amber or neutral treatment.
- Stop action: restrained red treatment.

## Look Design

A look should be editable in one place and should include:

- Light values: primary, secondary, accent, motion, strobe, saturation, brightness, FX, pulse.
- Now Playing mode: CDJ metadata, Vinyl mode, NO TALKING STUDIO, or no change.
- Section preset.
- Visual cue.
- Generator preset and generator state.
- Main camera cue.
- PIP camera cue.
- Background camera cue.
- Scene cue.

When editing a look, the user should be able to hear/see changes immediately, then save once.

Do not expose a separate "linked" toggle in the main look editor. A look stores all selected settings; empty values mean no change. Runtime controls may still let the performer trigger media cues while leaving the current light output held, such as when **Apply Lights with Looks** is off.

Look names must be editable wherever a look is being built. Typing a new name and saving should create a new look instead of forcing the user into a separate preset table.

## Show Sequencing

A Show is a named sequence of look triggers. The sequencer should make the link explicit: each row points to a saved look, and that look carries lights, Now Playing, visuals, cameras, and scene cues.

Sequencing should support two timing families:

- Musical timing: bars and beats for song sections.
- Wall-clock timing: seconds and minutes for podcasts, streams, and full-show automation.

The sequencer should feel like a live transport, not a spreadsheet. Keep the core actions visible: Play, Pause, Stop, Next Step, Save Show, and Loop Show.

Looping is a performance feature. It should be easy to turn on for repeating song sections, rehearsal, ambient streams, or holding patterns, and just as easy to stop.

The Live Deck Sequencer should expose sequence banks, a Now/Next cue stack, immediate jump-to-cue buttons, and cue type color hints. Cue type color should be subtle and role-based: look, visual, camera, or generic cue.

Manual override should be visible when the performer fires live controls outside the running sequence. It should reassure the user that direct intervention happened without blocking the sequence tools.

Rows should remain readable under pressure. Each row should show the look, timing, unit, and note/section label. Advanced timing can grow later, but the first read should answer: "what look fires, and when?"

Timing labels should behave like a cue list: "After previous" waits before firing that row, while "At show time" uses an absolute position from the beginning of playback.

Playback should be able to run the current unsaved rows for experimentation, while Save Show makes the sequence reusable.

## Generative Visual Design

Generative visuals are performance visuals, not disconnected experiments.

They should behave like Visual Cue types and belong to the same composition workflow as Resolume clips, cameras, Now Playing state, scenes, and lights. A performer should be able to save a Look that includes a generative visual preset and then trigger that Look manually or through a Show without visiting a separate toy surface.

The Python server remains authoritative for saved generative presets, current generative visual state, Look integration, Show integration, normalization, and snapshots. Browser output pages render the current normalized state; they do not own show state.

Generative visual controls should use performance language:

- Preset.
- Color source.
- Intensity.
- Complexity.
- Motion.
- Beat response.
- Scale.
- Zoom.
- Rotation.
- Symmetry.
- Warp.
- Line width.
- Trail.
- Phrase morph.
- Quality.
- Output level.
- Freeze.
- Stop.

The Generator section should show the output preview inside the app, while still allowing a dedicated fullscreen browser window for capture. The app should make the current color inputs visible so the performer can connect the light palette to the generated image at a glance.

Preset browsing should be visual. Cards should include a small generated thumbnail, mood, best-use context, renderer/quality metadata, and a short description so the operator can remember the look under pressure.

Generator motion should support automation. A performer should be able to pick a parameter, choose a BPM division or free seconds clock, set depth/center, and choose a simple modulation shape without leaving the Generator page.

Generator presets should apply complete recipes. Clicking a preset must update the visible generator controls, sync controls, live server state, and renderer behavior together. Avoid adding a slider unless the visual renderer has a clear mapping for that parameter.

The visual output should be sleek, dark, mathematical, hypnotic, projection-friendly, and useful as a Resolume layer. Avoid novelty rainbow equalizer aesthetics. Prefer looks that feel closer to ShaderToy, Hydra, p5.js generative art, scientific visualization, and Resolume VJ clips.

Visualizer pages should remain robust during performance. If live state disconnects, keep rendering with the last known state. Show connection and FPS in a debug overlay. If a preset fails, fall back to a stable preset. If performance drops, reduce quality before the operator has to intervene.

## OSC Design

OSC addresses should be treated as structured performance mappings, not raw strings only.

OSC output destinations are a separate layer from OSC addresses. A cue address such as `/composition/.../connect` should be authored once, then fanned out to every enabled OSC target such as Laptop Resolume, Stream PC, or a backup show machine. One failed destination should not prevent other enabled destinations from receiving the message.

For Resolume paths, provide an OSC builder with:

- Layer type: group or layer.
- Layer / group number.
- Column type: column or clip.
- Column / clip number.
- Action path.

Always preserve manual full-address entry. Some Resolume addresses will be unusual, and the user must be able to paste or type them directly.

Names and labels should be shared live across the app. If a scene, visual, or camera label changes in OSC settings, all dropdowns and look cards should use the updated label.

## Artwork + Metadata Design

Album artwork and Now Playing metadata are stream-display drivers, not only lighting helpers.

The Now Playing page should monitor metadata and stream text output separately. The Lights page can still include artwork color matching because it is useful during performance.

In the persistent left rail, keep album/current-display artwork with Now Playing metadata. The separate output preview should show the current lighting output as a stage/fixture-style preview, not album art. A light preview should communicate primary, secondary, accent, brightness, saturation, motion, FX, and pulse at a glance.

Artwork palette logic should:

- Prefer distinct saturated colors from album art.
- Avoid choosing near-duplicate colors for primary, secondary, and accent.
- Use neutral primary, neutral secondary, and neutral accent when the cover is black, white, gray, or low saturation.
- Fill missing roles from neutral colors if the artwork does not provide enough usable colors.

## Code Principles

1. Keep the server authoritative for show state.

   The browser renders and edits, but the Python server owns config, preset normalization, OSC sending, and snapshots.

2. Normalize at boundaries.

   Incoming config and preset payloads should be cleaned by backend helpers before being saved.

3. Keep automation server-owned.

   Macros and scheduled outputs should store normalized configuration on the Python server. Browsers may edit, preview, and trigger actions, but recurring automation such as clocks must continue without an open browser and must reuse the shared OSC destination layer.

4. Reuse local render helpers.

   Shared UI patterns like cue dropdowns, OSC builders, sliders, and look cards should be implemented once and reused.

5. Avoid unrelated refactors.

   Changes should stay close to the requested workflow unless a shared helper clearly reduces future friction.

6. Verify the cheap things every time.

   At minimum, run JavaScript syntax checks and Python compile checks after app changes. When the browser tool is available, visually check layout at desktop and tablet-like widths.

## Layout Guardrails

Use these patterns for responsive safety:

```css
.panel,
.section-view,
.grid-child {
  min-width: 0;
}

.responsive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
}
```

Avoid layouts that require all controls to fit in one row. If a row has more than three or four controls, it should usually wrap.

## Documentation Principle

When a feature changes the workflow, update `README.md`. When a feature changes the app philosophy or recurring implementation strategy, update this file.

- Source integrations publish normalized state into one server-owned Now Playing service. Display clients consume a read-only public representation and never depend directly on source-specific integrations.
