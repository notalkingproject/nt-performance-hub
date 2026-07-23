const shell = document.querySelector(".display-shell");
const artworkPanel = document.querySelector(".artwork-panel");
const artwork = document.querySelector("#artwork");
const connection = document.querySelector("#connection");
const title = document.querySelector("#title");
const artist = document.querySelector("#artist");
const album = document.querySelector("#album");
const source = document.querySelector("#source");
const playback = document.querySelector("#playback");
const progressBar = document.querySelector("#progressBar");
const elapsed = document.querySelector("#elapsed");
const duration = document.querySelector("#duration");
let currentState = null;
let progressBase = null;
let progressTimer = 0;
let refreshTimer = 0;

function validHex(value) { return /^#[0-9a-f]{6}$/i.test(String(value || "")); }
function applyPalette(palette = {}) {
  if (validHex(palette.primary)) document.documentElement.style.setProperty("--accent", palette.primary);
  if (validHex(palette.accent)) document.documentElement.style.setProperty("--accent-2", palette.accent);
}
function formatTime(ms) {
  if (!Number.isFinite(ms) || ms < 0) return "--:--";
  const seconds = Math.floor(ms / 1000);
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
}
function updateProgress() {
  if (!currentState || !currentState.duration_ms || currentState.duration_ms <= 0 || progressBase === null) return;
  let value = progressBase;
  if (currentState.is_playing) value += Date.now() - (currentState.received_at || Date.now());
  value = Math.max(0, Math.min(value, currentState.duration_ms));
  progressBar.style.width = `${Math.min(100, (value / currentState.duration_ms) * 100)}%`;
  elapsed.textContent = formatTime(value);
  duration.textContent = formatTime(currentState.duration_ms);
}
function render(state) {
  currentState = { ...state, received_at: Date.now() };
  progressBase = Number.isFinite(Number(state.progress_ms)) ? Number(state.progress_ms) : null;
  const hasTitle = Boolean(state.title || state.artist || state.album);
  shell.classList.toggle("idle", !hasTitle);
  shell.classList.toggle("no-progress", !(state.duration_ms && progressBase !== null));
  title.textContent = hasTitle ? (state.title || "Untitled") : "Nothing playing";
  artist.textContent = state.artist || "";
  album.textContent = state.album || "";
  source.textContent = state.source_label || state.source || "Now Playing";
  playback.textContent = state.is_paused ? "Paused" : state.is_playing ? "Playing" : hasTitle ? "Ready" : "Idle";
  connection.textContent = "Connected";
  applyPalette(state.palette || {});
  if (state.has_artwork && state.artwork_url) {
    const next = `${state.artwork_url}${state.artwork_url.includes("?") ? "&" : "?"}display=${encodeURIComponent(state.state_version || Date.now())}`;
    if (artwork.getAttribute("src") !== next) artwork.src = next;
    artworkPanel.classList.add("has-artwork");
  } else {
    artwork.removeAttribute("src");
    artworkPanel.classList.remove("has-artwork");
  }
  updateProgress();
}
async function loadInitial() {
  try {
    const response = await fetch("/api/now-playing", { cache: "no-store" });
    const payload = await response.json();
    if (payload.ok && payload.now_playing) render(payload.now_playing);
  } catch (_error) {
    connection.textContent = "Connection error";
  }
}
function connectEvents() {
  const events = new EventSource("/api/now-playing/events");
  events.addEventListener("open", () => { connection.textContent = "Connected"; });
  events.addEventListener("now-playing", (event) => {
    try { render(JSON.parse(event.data)); } catch (_error) { connection.textContent = "Event parse error"; }
  });
  events.addEventListener("error", () => { connection.textContent = "Connection lost - reconnecting"; });
}
loadInitial();
connectEvents();
progressTimer = window.setInterval(updateProgress, 1000);
refreshTimer = window.setInterval(loadInitial, 5000);
window.addEventListener("beforeunload", () => {
  window.clearInterval(progressTimer);
  window.clearInterval(refreshTimer);
});
