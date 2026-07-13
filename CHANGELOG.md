# Changelog

## Show Operations Upgrade - 2026-07-13

- Removed `Stop NT Performance Hub.bat`; closing the visible server window is the clearer stop path, while Restart remains available for reloads.

- Added start, stop, restart, and status launchers backed by `tools/nt_server_control.ps1`.
- Improved `Update From GitHub.bat` so the performance PC refuses dirty local code, pulls with `--ff-only`, and offers to restart or start the server.
- Added `/api/preflight` and `/preflight` for show-readiness checks across server health, local config, media paths, Beat Link, OSC targets, Git state, LAN URLs, and uptime.
- Added `Push To GitHub.bat` for laptop-side commit-and-push updates with a prompted update note.

## Initial NT Performance Hub Source - 2026-06-29

Purpose: create a clean portable Codex-folder app of the browser app and reduce tablet/runtime load before packaging it for other computers.

Changes:

- Created this NT Performance Hub folder as a clean source snapshot without machine-local generated config, data, Python cache, virtualenvs, or runtime logs.
- Added lightweight `/api/status` mode so regular browser polling can skip the large settings payload.
- Added optional cached BeatLink status reads for light status requests, while full requests still poll BeatLink.
- Reduced BeatLink source and aggregate poll timeouts so unreachable network machines do not stall status responses as long.
- Made default artwork and branding paths project-relative for portability.
- Added short static-asset caching for browser files while keeping API responses uncached.
- Changed tablet breakpoints so landscape tablets around 1024px use the tablet layout instead of the cramped desktop sidebar layout.
- Hotfixed the live surface layout so Active Moment stays in normal document flow, section navigation no longer scrolls content underneath it, Live Deck cards use real grid rows instead of JS masonry rows, and dashboard control groups contain their own scrolling instead of spilling into neighboring boxes.
- Bumped browser asset query strings for the layout hotfix so tablets fetch the updated CSS and JS immediately.
- Tightened the Live Deck staged-preview strip so the Next state, GO, Clear, and Tap Route controls share space cleanly on tablet instead of leaving a large empty state panel and squeezed route controls.
- Added visibility-aware browser polling so hidden tablets pause live refreshes and resume with a full refresh.
- Added `Install NT Performance Hub.bat`, `PORTABLE_INSTALL.md`, `tools/diagnostic_check.py`, and `config/app_config.example.json`.

- Reworked Settings network routing around machines with multiple saved IP addresses, clearer tablet connector URLs, and automatic deduped OSC fan-out to every saved machine route.
- Simplified the Looks page and default look bank to open-ended Look 1 through Look 10 entries that only store Color 1, Color 2, and Color 3, while preserving route links for Lights, Visuals, Main Cam, PIP Cam, Background, and Scene triggers.
- Clarified Now Playing artwork modes: CDJ now re-sends current BeatLink text on Resume CDJ, Studio/Vinyl messages are editable from the Now Playing page, active manual-mode saves refresh artwork/text immediately, and a Rebuild Music Index command can create data/music_library_index.json from Music Root for album-art matching.

Verification target:

- `node --check web/app.js`
- `node --check web/generative.js`
- Python AST parse for `app.py`
- Local `/health`, light `/api/status`, and full `/api/status` timing checks
- Browser smoke check at tablet landscape and portrait sizes

## Previous Source Folder

Purpose: browser control app for live Lights, Visuals, Cameras, Looks, Sequencer, Now Playing, Settings, and Log sections.

Recent v4 direction:

- Simplified lighting live controls with Color 1, Color 2, and Color 3 banks.
- Kept percentage preset buttons for lighting sliders.
- Limited light OSC controls to three outputs per control.
- Removed camera opacity sliders from the camera performance section.
- Clarified main, PIP, background, and scene camera trigger grouping.
## 2026-06-29 - Live-first preview routing tune
- Made Live the default interaction model across Looks: look grid, look launcher, favorite look buttons, and the look builder apply immediately unless Preview route is explicitly enabled.
- Kept the global Preview route as an intentional staging mode, with Stage labels only while Preview is active and disabled GO/Clear controls in live mode.
- Tuned Live Deck tablet sizing so cards no longer stretch to the tallest neighbor, the staging lane is shorter, and look cards use compact Apply/Stage actions.
## 2026-06-29 - Default look label cleanup
- Stopped treating the app default state as active Look 1 in Live Deck and Current Selection status.
- The Active card now shows the live/manual color state unless the source is an actual `performance:Look Name` command.
## 2026-06-29 - Remove Look 1 quick recall buttons
- Removed the Reapply and Look 1 quick buttons from the Live Deck Looks card.
- Removed the matching Reapply Look and Look 1 buttons from the Lights Current Output header because they created confusing duplicate recall paths.
## 2026-06-29 - Now Playing videogame mode
- Added a Videogame manual mode button to Now Playing with editable default text set to Ravenswatch.
- Added Videogame Artwork and Videogame Text settings alongside the vinyl/studio image and text fields.
- Wired videogame mode through linked looks, saved look routing, config refresh, BLT text output, and artwork output.
## 2026-06-30 - Videogames mode label
- Renamed the Now Playing mode label to Videogames while leaving the editable default/current game text as Ravenswatch.

## 2026-06-30 - Videogames settings save
- Fixed core settings saves for Videogames artwork/text so typed paths persist and refresh the active manual mode.
- Updated the local Videogames artwork path to `C:\Users\ryant\Videos\Resolume Visuals\Album Artwork\Videogames.png`.

## 2026-07-01 - Live Deck Now Playing and BPM
- Added Now Playing mode triggers, editable manual text, and section access to the Live Deck.
- Added compact BPM color-rotation controls to the Live Deck Lights card.
- Made tablet setup and OSC panels consistently collapsed by default behind details controls.

## 2026-07-01 - Live Deck light colors and visual clip grid
- Made the Live Deck Color 1, Color 2, and Color 3 cards editable with direct color selectors.
- Expanded Visual triggers to three layers of ten clip slots while keeping existing `visual_#` IDs compatible with saved routes.
- Rendered both Live Deck Visuals and the Visuals page as a Resolume-style layer/clip grid.
## 2026-07-02 - Color 1/2/3 palette roles and BPM rotation
- Renamed live color roles to Color 1, Color 2, and Color 3 across looks, Live Deck controls, palette actions, and artwork fallback selectors.
- Kept album artwork matching mapped to three color slots, including neutral fallback roles for all three slots.
- Reworked BPM automation from a fixed Color 1/2 flip into a configurable color rotation with slot checkboxes.
## 2026-07-02 - BPM rotation promoted
- Moved BPM Color Rotation out of the Lights looks sidebar into the main Lights controls.
- Added Color 1/2/3 rotation slot checkboxes directly to the full BPM panel.
- Changed the old two-color action to rotate the currently selected color slots instead of only flipping Color 1 and Color 2.
- Renamed remaining visible OSC target wording from Primary to Main so color language stays Color 1/2/3.
- Updated default color-comment templates to use COLOR1/COLOR2/COLOR3 while keeping legacy parsing compatible.
## 2026-07-02 - Visual clip label syntax
- Standardized Visual clip buttons, defaults, and saved labels to the `L# C#` coordinate syntax across Live Deck, Visuals, and Visuals OSC settings.
- Expanded the saved visual controls block to all 30 Resolume-style slots while preserving existing clip addresses.
## 2026-07-02 - Live Deck Now Playing controls
- Reordered visual clip rows so Layer 3 is top, Layer 2 is middle, and Layer 1 is bottom.
- Added always-visible Album Colors controls and BPM Color Rotation controls to the Live Deck Now Playing card.

