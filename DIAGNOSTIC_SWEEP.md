# Diagnostic Sweep

Date: 2026-06-29
Folder: `NT Performance Hub`

## Findings

- The browser app was doing a full `/api/status` fetch every poll and then rebuilding expensive UI areas, including settings forms, local OSC forms, preset editor, sequencer, math scene gallery, artwork images, and live controls.
- `/api/status` also rebuilt the full settings payload server-side every time, even when the browser only needed live state.
- Status polling could wait on BeatLink network sources. Unreachable or sleeping machines can make the app feel slow even when the tablet itself is fine.
- Static browser files were sent with `Cache-Control: no-store`, so tablets had no chance to reuse `web/app.js` and `web/styles.css` between reloads.
- Landscape tablets around 1024px wide were missing the tablet layout breakpoint and could fall into the cramped desktop sidebar layout.
- Generated config/data/log files in the old folder were machine-local and should not be copied as source for portable installs.

## Changes Made

- Added a lightweight status mode: `/api/status?settings=0&blt=0`.
- Browser polling now requests the full settings payload only on initial load, periodic refresh, settings view, manual refresh, or detected config changes.
- Browser polling now asks for live BeatLink polling less often outside the Now Playing view.
- Hidden browser tabs stop scheduling live refreshes and perform a full refresh when visible again.
- Artwork image URLs now change only when the artwork timestamp changes, avoiding needless image reloads every poll.
- Project-relative default paths now point generated artwork to `data/current_artwork.jpg` and branding placeholders to `assets/`.
- Static assets now get short private caching while API responses remain uncached.
- Tablet CSS breakpoint increased to include 1024px landscape tablets, and camera/active-moment grids use auto-fit sizing to avoid overlapping bubbles.
- Added install, diagnostics, and config-example files for moving the app to another computer.

## Verification Notes

Measured against `http://127.0.0.1:8082` on this machine:

- `/health`: about 25 ms from the Python diagnostic script.
- `/api/status?settings=0&blt=0`: about 15 ms from the Python diagnostic script.
- `/api/status?settings=1&blt=0`: about 8 ms from the Python diagnostic script.

Avoid using `localhost` for timing on this Windows setup; it showed about two seconds of name-resolution delay even when the app endpoint was healthy. The launcher and docs now prefer `127.0.0.1` for the show computer and LAN IPs for tablets.
## Best Next Packaging Step

For a true one-click installer, package this folder with either:

- a prebuilt `.venv` created on the target Windows/Python release, or
- a small installer wrapper that runs `Install NT Performance Hub.bat`, opens Windows Firewall guidance, and then launches `Start NT Performance Hub.bat`.

The current NT Performance Hub folder is ready for manual portable installs and local hosting tests.