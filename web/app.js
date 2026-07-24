const statusEl = document.querySelector("#connectionStatus");
const previewArtworkImage = document.querySelector("#previewArtworkImage");
const previewArtworkEmpty = document.querySelector("#previewArtworkEmpty");
const artworkImage = document.querySelector("#artworkImage");
const artworkEmpty = document.querySelector("#artworkEmpty");
const artworkPath = document.querySelector("#artworkPath");
const serverAddress = document.querySelector("#serverAddress");
const connectionProfile = document.querySelector("#connectionProfile");
const resolumeAddress = document.querySelector("#resolumeAddress");
const bltAddress = document.querySelector("#bltAddress");
const configState = document.querySelector("#configState");
const remoteUrls = document.querySelector("#remoteUrls");
const selectedLook = document.querySelector("#selectedLook");
const selectedColors = document.querySelector("#selectedColors");
const selectedVisual = document.querySelector("#selectedVisual");
const selectedCameras = document.querySelector("#selectedCameras");
const selectedNowPlaying = document.querySelector("#selectedNowPlaying");
const refreshButton = document.querySelector("#refreshButton");
const presetButtons = document.querySelector("#presetButtons");
const outputGrid = document.querySelector("#outputGrid");
const lastEvent = document.querySelector("#lastEvent");
const bpmInput = document.querySelector("#bpmInput");
const bpmSlider = document.querySelector("#bpmSlider");
const bpmDown = document.querySelector("#bpmDown");
const bpmUp = document.querySelector("#bpmUp");
const bpmFollow = document.querySelector("#bpmFollow");
const bpmStart = document.querySelector("#bpmStart");
const bpmResync = document.querySelector("#bpmResync");
const bpmStop = document.querySelector("#bpmStop");
const bpmStatus = document.querySelector("#bpmStatus");
const bpmClockSummary = document.querySelector("#bpmClockSummary");
const bpmRotationControls = document.querySelector("#bpmRotationControls");
const divisionButtons = document.querySelector("#divisionButtons");
const linkControls = document.querySelector("#linkControls");
const settingsForm = document.querySelector("#settingsForm");
const settingsStatus = document.querySelector("#settingsStatus");
const exportOscSettings = document.querySelector("#exportOscSettings");
const downloadOscSettings = document.querySelector("#downloadOscSettings");
const importOscSettings = document.querySelector("#importOscSettings");
const importProjectOscSettings = document.querySelector("#importProjectOscSettings");
const oscBackupFileNameInput = document.querySelector("#oscBackupFileName");
const oscImportFileNameInput = document.querySelector("#oscImportFileName");
const oscBackupFileList = document.querySelector("#oscBackupFileList");
const oscBackupStatus = document.querySelector("#oscBackupStatus");
const saveSettings = document.querySelector("#saveSettings");
const saveSettingsSticky = document.querySelector("#saveSettingsSticky");
const obsSettingsForm = document.querySelector("#obsSettingsForm");
const obsSettingsStatus = document.querySelector("#obsSettingsStatus");
const saveObsSettings = document.querySelector("#saveObsSettings");
const colorComment = document.querySelector("#colorComment");
const copyColorComment = document.querySelector("#copyColorComment");
const extractPalette = document.querySelector("#extractPalette");
const applyPalette = document.querySelector("#applyPalette");
const useCurrentColors = document.querySelector("#useCurrentColors");
const palettePreview = document.querySelector("#palettePreview");
const paletteStatus = document.querySelector("#paletteStatus");
const neutralArtworkPrimary = document.querySelector("#neutralArtworkPrimary");
const neutralArtworkSecondary = document.querySelector("#neutralArtworkSecondary");
const neutralArtworkAccent = document.querySelector("#neutralArtworkAccent");
const keepPresetColorsToggle = document.querySelector("#keepPresetColorsToggle");
const autoArtworkToggle = document.querySelector("#autoArtworkToggle");
const lookLightsToggles = document.querySelectorAll("[data-look-lights-toggle]");
const presetGroupTabs = document.querySelector("#presetGroupTabs");
const presetEditor = document.querySelector("#presetEditor");
const presetStatus = document.querySelector("#presetStatus");
const savePresets = document.querySelector("#savePresets");
const saveCurrentLook = document.querySelector("#saveCurrentLook");
const saveCurrentLookSelect = document.querySelector("#saveCurrentLookSelect");
const lookBuilderName = document.querySelector("#lookBuilderName");
const saveLookStatus = document.querySelector("#saveLookStatus");
const launchSelectedLook = document.querySelector("#launchSelectedLook");
const saveLookRouting = document.querySelector("#saveLookRouting");
const lookBuilderSummary = document.querySelector("#lookBuilderSummary");
const lookBuilderForm = document.querySelector("#lookBuilderForm");
const showSequenceName = document.querySelector("#showSequenceName");
const showSequenceSelect = document.querySelector("#showSequenceSelect");
const showSequenceRows = document.querySelector("#showSequenceRows");
const showSequenceStatus = document.querySelector("#showSequenceStatus");
const showSequenceLoop = document.querySelector("#showSequenceLoop");
const showSequenceTransport = document.querySelector("#showSequenceTransport");
const playShowSequence = document.querySelector("#playShowSequence");
const pauseShowSequence = document.querySelector("#pauseShowSequence");
const nextShowSequenceStep = document.querySelector("#nextShowSequenceStep");
const stopShowSequence = document.querySelector("#stopShowSequence");
const saveShowSequence = document.querySelector("#saveShowSequence");
const addSequenceStep = document.querySelector("#addSequenceStep");
const sendAllLinks = document.querySelector("#sendAllLinks");
const reapplyCurrentLook = document.querySelector("#reapplyCurrentLook");
const applyDefaultLook = document.querySelector("#applyDefaultLook");
const commandLog = document.querySelector("#commandLog");
const clearLog = document.querySelector("#clearLog");
const colorPreviewWindow = document.querySelector("#colorPreviewWindow");
const quickSettingsForm = document.querySelector("#quickSettingsForm");
const quickSettingsStatus = document.querySelector("#quickSettingsStatus");
const saveQuickSettings = document.querySelector("#saveQuickSettings");
const lightsOscForm = document.querySelector("#lightsOscForm");
const lightsOscStatus = document.querySelector("#lightsOscStatus");
const saveLightsOsc = document.querySelector("#saveLightsOsc");
const visualsOscForm = document.querySelector("#visualsOscForm");
const visualsOscStatus = document.querySelector("#visualsOscStatus");
const saveVisualsOsc = document.querySelector("#saveVisualsOsc");
const camerasOscForm = document.querySelector("#camerasOscForm");
const camerasOscStatus = document.querySelector("#camerasOscStatus");
const saveCamerasOsc = document.querySelector("#saveCamerasOsc");
const nowPlayingOscForm = document.querySelector("#nowPlayingOscForm");
const nowPlayingOscStatus = document.querySelector("#nowPlayingOscStatus");
const nowPlayingSourceTabs = document.querySelector("#nowPlayingSourceTabs");
const nowPlayingSourceStatus = document.querySelector("#nowPlayingSourceStatus");
const nowPlayingSettingsLabel = document.querySelector("#nowPlayingSettingsLabel");
const beatlinkSourceForm = document.querySelector("#beatlinkSourceForm");
const beatlinkParamsUrl = document.querySelector("#beatlinkParamsUrl");
const musicRoot = document.querySelector("#musicRoot");
const artworkOutputPath = document.querySelector("#artworkOutputPath");
const fallbackArtworkPath = document.querySelector("#fallbackArtworkPath");
const defaultFallbackTemplate = document.querySelector("#defaultFallbackTemplate");
const cdjArtworkWidth = document.querySelector("#cdjArtworkWidth");
const cdjArtworkHeight = document.querySelector("#cdjArtworkHeight");
const fallbackArtworkWidth = document.querySelector("#fallbackArtworkWidth");
const fallbackArtworkHeight = document.querySelector("#fallbackArtworkHeight");
const beatlinkSourceStatus = document.querySelector("#beatlinkSourceStatus");
const spotifySourceForm = document.querySelector("#spotifySourceForm");
const spotifyEnabled = document.querySelector("#spotifyEnabled");
const spotifyTrackText = document.querySelector("#spotifyTrackText");
const spotifyArtworkPath = document.querySelector("#spotifyArtworkPath");
const spotifyArtworkWidth = document.querySelector("#spotifyArtworkWidth");
const spotifyArtworkHeight = document.querySelector("#spotifyArtworkHeight");
const spotifyClientId = document.querySelector("#spotifyClientId");
const spotifyRedirectUri = document.querySelector("#spotifyRedirectUri");
const spotifyMarket = document.querySelector("#spotifyMarket");
const spotifyTrackTemplate = document.querySelector("#spotifyTrackTemplate");
const spotifyStatusBadge = document.querySelector("#spotifyStatusBadge");
const spotifyRuntimeTitle = document.querySelector("#spotifyRuntimeTitle");
const spotifyRuntimeArtist = document.querySelector("#spotifyRuntimeArtist");
const spotifyRuntimeAlbum = document.querySelector("#spotifyRuntimeAlbum");
const spotifyRuntimePlayback = document.querySelector("#spotifyRuntimePlayback");
const spotifyRuntimeDevice = document.querySelector("#spotifyRuntimeDevice");
const spotifyRuntimeLastPoll = document.querySelector("#spotifyRuntimeLastPoll");
const spotifyRuntimeLastError = document.querySelector("#spotifyRuntimeLastError");
const spotifyConnect = document.querySelector("#spotifyConnect");
const spotifyDisconnect = document.querySelector("#spotifyDisconnect");
const spotifyUseNowPlaying = document.querySelector("#spotifyUseNowPlaying");
const saveNowPlayingOsc = document.querySelector("#saveNowPlayingOsc");
const manualModeForm = document.querySelector("#manualModeForm");
const vinylTrackText = document.querySelector("#vinylTrackText");
const vinylArtworkPath = document.querySelector("#vinylArtworkPath");
const vinylArtworkWidth = document.querySelector("#vinylArtworkWidth");
const vinylArtworkHeight = document.querySelector("#vinylArtworkHeight");
const studioTrackText = document.querySelector("#studioTrackText");
const studioArtworkPath = document.querySelector("#studioArtworkPath");
const studioArtworkWidth = document.querySelector("#studioArtworkWidth");
const studioArtworkHeight = document.querySelector("#studioArtworkHeight");
const videogameTrackText = document.querySelector("#videogameTrackText");
const videogameArtworkPath = document.querySelector("#videogameArtworkPath");
const videogameArtworkWidth = document.querySelector("#videogameArtworkWidth");
const videogameArtworkHeight = document.querySelector("#videogameArtworkHeight");
const vinylModeButtonText = document.querySelector("#vinylModeButtonText");
const studioModeButtonText = document.querySelector("#studioModeButtonText");
const videogameModeButtonText = document.querySelector("#videogameModeButtonText");
const saveManualModeText = document.querySelector("#saveManualModeText");
const rebuildMusicIndex = document.querySelector("#rebuildMusicIndex");
const manualModeStatus = document.querySelector("#manualModeStatus");
const nowPlayingOpacityControl = document.querySelector("#nowPlayingOpacityControl");
const visualNowPlayingOpacityControl = document.querySelector("#visualNowPlayingOpacityControl");
const visualOpacityControl = document.querySelector("#visualOpacityControl");
const generativeVisualControls = document.querySelector("#generativeVisualControls");
const generativeVisualStatus = document.querySelector("#generativeVisualStatus");
const generatorPreviewFrame = document.querySelector("#generatorPreviewFrame");
const generatorColorPreview = document.querySelector("#generatorColorPreview");
const generatorPresetGallery = document.querySelector("#generatorPresetGallery");
const generatorQuickPresetGrid = document.querySelector("#generatorQuickPresetGrid");
const generatorBpmSync = document.querySelector("#generatorBpmSync");
const generatorLayerStack = document.querySelector("#generatorLayerStack");
const mathSceneFilters = document.querySelector("#mathSceneFilters");
const mathSceneGallery = document.querySelector("#mathSceneGallery");
const mathSceneStatus = document.querySelector("#mathSceneStatus");
const openGenerativeVisualizer = document.querySelector("#openGenerativeVisualizer");
const freezeGenerativeVisual = document.querySelector("#freezeGenerativeVisual");
const stopGenerativeVisual = document.querySelector("#stopGenerativeVisual");

const trackNowPlaying = document.querySelector("#trackNowPlaying");
const liveTrackNowPlaying = document.querySelector("#liveTrackNowPlaying");
const liveTrackArtist = document.querySelector("#liveTrackArtist");
const liveTrackBpm = document.querySelector("#liveTrackBpm");
const liveTrackPlayer = document.querySelector("#liveTrackPlayer");
const liveTrackMode = document.querySelector("#liveTrackMode");
const perfTrackNowPlaying = document.querySelector("#perfTrackNowPlaying");
const perfTrackArtist = document.querySelector("#perfTrackArtist");
const perfTrackAlbum = document.querySelector("#perfTrackAlbum");
const perfTrackBpm = document.querySelector("#perfTrackBpm");
const perfTrackPlayer = document.querySelector("#perfTrackPlayer");
const perfTrackMode = document.querySelector("#perfTrackMode");
const perfTrackDisplay = document.querySelector("#perfTrackDisplay");
const trackArtworkImage = document.querySelector("#trackArtworkImage");
const trackArtworkEmpty = document.querySelector("#trackArtworkEmpty");
const trackArtworkPath = document.querySelector("#trackArtworkPath");
const trackTitle = document.querySelector("#trackTitle");
const trackArtist = document.querySelector("#trackArtist");
const trackAlbum = document.querySelector("#trackAlbum");
const trackBpm = document.querySelector("#trackBpm");
const trackPlayer = document.querySelector("#trackPlayer");
const trackDevice = document.querySelector("#trackDevice");
const trackMatchedFile = document.querySelector("#trackMatchedFile");
const trackCommentFound = document.querySelector("#trackCommentFound");
const trackParsedValues = document.querySelector("#trackParsedValues");
const trackMissingValues = document.querySelector("#trackMissingValues");
const trackAppliedFrom = document.querySelector("#trackAppliedFrom");
const trackAutoSend = document.querySelector("#trackAutoSend");
const sequenceTimingTools = document.querySelector("#sequenceTimingTools");
const sequenceBankFilters = document.querySelector("#sequenceBankFilters");
const sequenceBankHint = document.querySelector("#sequenceBankHint");
const sequenceLookBank = document.querySelector("#sequenceLookBank");
const trackDailyLog = document.querySelector("#trackDailyLog");
const trackColorComment = document.querySelector("#trackColorComment");
const trackUseCurrentColors = document.querySelector("#trackUseCurrentColors");
const trackCopyColorComment = document.querySelector("#trackCopyColorComment");
const manualModeButtons = document.querySelectorAll(".manual-buttons [data-command]");
const relationshipButtons = document.querySelectorAll("[data-command='rotate_colors'], [data-relationship]");
const cameraContainers = {
  main_box: document.querySelector("#mainBoxCams"),
  pip_box: document.querySelector("#pipBoxCams"),
  background: document.querySelector("#backgroundCams"),
  visuals_cams: document.querySelector("#visualsCams"),
};
const cameraOpacityControls = {
  main_box: document.querySelector("#mainBoxCamOpacityControl"),
  pip_box: document.querySelector("#pipBoxCamOpacityControl"),
  background: document.querySelector("#backgroundCamOpacityControl"),
  visuals_cams: document.querySelector("#visualsCamOpacityControl"),
};

const sceneControls = document.querySelector("#sceneControls");
const visualControls = document.querySelector("#visualControls");
const visualCueRoute = document.querySelector("#visualCueRoute");
const cameraCueRoute = document.querySelector("#cameraCueRoute");
const presetLinks = document.querySelector("#presetLinks");
const lookLauncherGrid = document.querySelector("#lookLauncherGrid");
const lookLinkForm = document.querySelector("#lookLinkForm");
const saveLookLinks = document.querySelector("#saveLookLinks");
const lookLinksStatus = document.querySelector("#lookLinksStatus");
const activeMomentStrip = document.querySelector("#activeMomentStrip");
const overviewLookPreview = document.querySelector("#overviewLookPreview");
const overviewLookGrid = document.querySelector("#overviewLookGrid");
const overviewLightState = document.querySelector("#overviewLightState");
const overviewLightControls = document.querySelector("#overviewLightControls");
const overviewBpmControls = document.querySelector("#overviewBpmControls");
const overviewNowPlaying = document.querySelector("#overviewNowPlaying");
const overviewVisualGrid = document.querySelector("#overviewVisualGrid");
const overviewGeneratorGrid = document.querySelector("#overviewGeneratorGrid");
const overviewCameraGrid = document.querySelector("#overviewCameraGrid");
const overviewSequenceTransport = document.querySelector("#overviewSequenceTransport");
const overviewObsControls = document.querySelector("#overviewObsControls");
const obsSectionControls = document.querySelector("#obsSectionControls");
const overviewMacroButtons = document.querySelector("#overviewMacroButtons");
const macrosList = document.querySelector("#macrosList");
const macrosPager = document.querySelector("#macrosPager");
const macrosStatus = document.querySelector("#macrosStatus");
const addOscButtonMacro = document.querySelector("#addOscButtonMacro");
const addOscClockMacro = document.querySelector("#addOscClockMacro");
const overviewReapplyLook = document.querySelector("#overviewReapplyLook");
const overviewDefaultLook = document.querySelector("#overviewDefaultLook");
const overviewPulseHold = document.querySelector("#overviewPulseHold");
const liveDeckViewSummary = document.querySelector("#liveDeckViewSummary");
const liveDeckGrid = document.querySelector(".live-deck-grid");
const liveDeckPanelToggles = document.querySelectorAll("[data-live-panel-toggle]");
const liveDeckPanelCards = document.querySelectorAll("[data-live-panel-card]");
const liveDeckHideButtons = document.querySelectorAll("[data-live-panel-hide]");
const systemConfidence = document.querySelector("#systemConfidence");
const panicSafeButton = document.querySelector("#panicSafeButton");
const stagedCueLane = document.querySelector("#stagedCueLane");
const stagedCueHint = document.querySelector("#stagedCueHint");
const liveDeckLookName = document.querySelector("#liveDeckLookName");
const saveLiveDeckLook = document.querySelector("#saveLiveDeckLook");
const liveDeckSaveStatus = document.querySelector("#liveDeckSaveStatus");
const songMomentMarkers = document.querySelector("#songMomentMarkers");
const favoriteBankSelect = document.querySelector("#favoriteBankSelect");
const favoriteCategoryTabs = document.querySelector("#favoriteCategoryTabs");
const favoriteBankGrid = document.querySelector("#favoriteBankGrid");
const favoriteBankEditor = document.querySelector("#favoriteBankEditor");
const panicSafeEditor = document.querySelector("#panicSafeEditor");

let selectedDivision = "1/4";
let selectedMathSceneCategory = "All";
let appSettings = null;
let presetData = null;
let latestShow = null;
let settingsDirty = false;
let obsSettingsDirty = false;
let quickSettingsDirty = false;
let lookLinksDirty = false;
let lookBuilderDirty = false;
let liveDeckLookNameDirty = false;
let lightsOscDirty = false;
let visualsOscDirty = false;
let camerasOscDirty = false;
let nowPlayingOscDirty = false;
let manualModeDirty = false;
let macroDrafts = [];
let macrosPage = 0;
const MACROS_PER_PAGE = 5;
let optimisticNowPlayingMode = "";
let optimisticPerformanceLookName = "";
let activeNowPlayingSource = "";
let activeCameraOscSection = "main_box";
let activeVisualOscSection = "off";
let activeLightOscSection = "color1";
let activePresetGroup = "performance";
let activeSettingsSection = "core";
let activeShowSequence = "Main Show";
let sequenceBankMode = "looks";
let activeSequenceCueIndex = 0;
let showSequenceDirty = false;
let showSequenceTimer = null;
let showSequenceRunning = false;

const NT_ADMIN_TOKEN_STORAGE_KEY = "ntPerformanceHubAdminToken";
const ntNativeFetch = window.fetch.bind(window);
let ntAdminToken = localStorage.getItem(NT_ADMIN_TOKEN_STORAGE_KEY) || "";

function isSameOriginRequest(input) {
  try {
    const url = new URL(typeof input === "string" ? input : input.url, window.location.href);
    return url.origin === window.location.origin;
  } catch (_error) {
    return false;
  }
}

function shouldAttachAdminToken(input) {
  if (!isSameOriginRequest(input)) return false;
  const url = new URL(typeof input === "string" ? input : input.url, window.location.href);
  if (url.pathname === "/api/admin/session") return false;
  return url.pathname.startsWith("/api/") || url.pathname === "/spotify/login";
}

function withAdminToken(input, init = {}) {
  const nextInit = { ...init };
  const headers = new Headers(nextInit.headers || (input instanceof Request ? input.headers : undefined));
  if (ntAdminToken) headers.set("X-NT-Admin-Token", ntAdminToken);
  nextInit.headers = headers;
  return nextInit;
}

window.fetch = async (input, init = {}) => {
  if (!shouldAttachAdminToken(input)) return ntNativeFetch(input, init);
  let response = await ntNativeFetch(input, withAdminToken(input, init));
  if (response.status !== 401) return response;
  const entered = window.prompt("NT Performance Hub admin token required for controls on this device.");
  if (!entered) return response;
  ntAdminToken = entered.trim();
  localStorage.setItem(NT_ADMIN_TOKEN_STORAGE_KEY, ntAdminToken);
  response = await ntNativeFetch(input, withAdminToken(input, init));
  if (response.status === 401) {
    localStorage.removeItem(NT_ADMIN_TOKEN_STORAGE_KEY);
    ntAdminToken = "";
  }
  return response;
};

async function bootstrapAdminSession() {
  if (ntAdminToken) return;
  try {
    const response = await ntNativeFetch("/api/admin/session", { cache: "no-store" });
    const result = await response.json();
    if (response.ok && result.ok && result.admin_token) {
      ntAdminToken = String(result.admin_token);
      localStorage.setItem(NT_ADMIN_TOKEN_STORAGE_KEY, ntAdminToken);
    }
  } catch (_error) {
    // Remote display/control clients do not receive the local admin bootstrap token.
  }
}
let showSequencePaused = false;
let showSequenceStepIndex = 0;
let showSequenceStartedAt = 0;
let presetDirty = false;
let statusTimer = null;
let statusRequestInFlight = false;
let statusPollCount = 0;
let latestConfigRevision = "";
let latestShowSignature = "";
let latestArtworkToken = "";
let activeSectionId = "liveDeckSection";
const FULL_STATUS_POLL_EVERY = 12;
const BLT_STATUS_POLL_EVERY = 3;
let bpmPreviewTimer = null;
let latestPaletteArtworkUpdated = "";
let paletteRefreshInFlight = false;
let stagedPerformanceCue = (() => {
  try {
    const saved = JSON.parse(localStorage.getItem("liveDeckStagedCue") || "{}");
    return saved && typeof saved === "object" ? saved : {};
  } catch (_error) {
    return {};
  }
})();
let stagedPerformanceLookName = stagedPerformanceCue.look || localStorage.getItem("liveDeckStagedLook") || "";
let stagedPerformanceLookSource = localStorage.getItem("liveDeckStagedLookSource") || "";
if (!stagedPerformanceCue.look && stagedPerformanceLookName) stagedPerformanceCue = { look: stagedPerformanceLookName };
let cueDispatchMode = "live";
let activeFavoriteCategory = localStorage.getItem("liveDeckFavoriteCategory") || "looks";
let panicHoldTimer = null;
let manualOverrideUntil = 0;
let manualOverrideTimer = null;
const LIVE_DECK_PANEL_KEYS = ["now-playing", "lights", "visuals", "cameras", "looks", "sequences", "obs", "macros", "generator"];
const LIVE_DECK_DEFAULT_PANELS = { "now-playing": true, lights: true, visuals: true, cameras: true, looks: true, sequences: true, obs: true, macros: true, generator: true };
const OSC_BACKUP_KEYS = [
  "resolume_host",
  "resolume_port",
  "beatlink_host",
  "beatlink_port",
  "beatlink_base_url",
  "blt_params_url",
  "network_routes",
  "osc_targets",
  "link_labels",
  "osc_addresses",
  "osc_extra_addresses",
  "osc_output_notes",
  "blt_osc_outputs",
  "now_playing_opacity_address",
  "visual_controls",
  "visual_slider_controls",
  "visual_opacity_address",
  "camera_controls",
  "camera_opacity_addresses",
  "camera_opacity_labels",
  "preset_links",
  "show_sequences",
  "look_apply_lights",
  "bpm_osc_bpm_address",
  "bpm_osc_start_address",
  "bpm_osc_resync_address",
  "bpm_osc_stop_address"
];

localStorage.setItem("liveDeckCueDispatchMode", cueDispatchMode);
if (Object.values(stagedPerformanceCue).some(Boolean)) {
  stagedPerformanceCue = {};
  stagedPerformanceLookName = "";
  stagedPerformanceLookSource = "";
  localStorage.removeItem("liveDeckStagedCue");
  localStorage.removeItem("liveDeckStagedLook");
  localStorage.removeItem("liveDeckStagedLookSource");
}
let liveDeckVisiblePanels = loadLiveDeckVisiblePanels();
let liveDeckResizeFrame = null;

const DEFAULT_BPM_DIVISIONS = ["1/64", "1/32", "1/16", "1/8", "1/4", "1/2 bar", "1 bar", "2 bars", "4 bars", "8 bars", "16 bars", "32 bars"];
const BPM_DIVISION_MULTIPLIERS = {
  "1/64": 4 / 64,
  "1/32": 4 / 32,
  "1/16": 4 / 16,
  "1/8": 4 / 8,
  "1/4": 4 / 4,
  "1/2 bar": 2,
  "1 bar": 4,
  "2 bars": 8,
  "4 bars": 16,
  "8 bars": 32,
  "16 bars": 64,
  "32 bars": 128,
};
const STEP_AMOUNT_LIMITS = {
  bars: { min: 0, max: 32, step: 1 },
  beats: { min: 0, max: 128, step: 1 },
  seconds: { min: 0, max: 300, step: 1 },
  minutes: { min: 0, max: 60, step: 1 },
};
const SEQUENCE_BANK_MODES = [
  ["looks", "Looks"],
  ["visuals", "Visuals"],
  ["main_box", "Main Cam"],
  ["pip_box", "PIP Cam"],
  ["background", "BG Cam"],
  ["visuals_cams", "Visuals Cam"],
  ["scene", "Scenes"],
];
const GENERATIVE_SLIDER_FIELDS = [
  ["intensity", "Intensity", 0.72],
  ["complexity", "Complexity", 0.48],
  ["motion", "Motion", 0.62],
  ["beat_response", "Beat Response", 0.52],
  ["scale", "Scale", 0.54],
  ["zoom", "Zoom", 0.5],
  ["rotation", "Rotation", 0.42],
  ["symmetry", "Symmetry", 0.5],
  ["warp", "Warp", 0.38],
  ["line_width", "Line Width", 0.42],
  ["trail", "Trail", 0.56],
  ["opacity", "Output Level", 1],
];
const GENERATIVE_AUTOMATION_TARGETS = [
  ["warp", "Warp"],
  ["scale", "Scale"],
  ["zoom", "Zoom"],
  ["rotation", "Rotation"],
  ["symmetry", "Symmetry"],
  ["line_width", "Line Width"],
  ["trail", "Trail"],
  ["intensity", "Intensity"],
  ["complexity", "Complexity"],
  ["motion", "Motion"],
  ["beat_response", "Beat Response"],
  ["opacity", "Output Level"],
];
const GENERATIVE_LAYER_STYLES = [
  ["glow_grid", "Glow Grid"],
  ["scanlines", "Scanlines"],
  ["vignette", "Vignette"],
  ["echo", "Echo"],
  ["sparkle", "Sparkle"],
  ["none", "None"],
];

const lookColorFields = [
  ["PRIMARY", "Color 1"],
  ["SECONDARY", "Color 2"],
  ["STROBE", "Color 3"],
];
const presetControlKeys = {
  PRIMARY: "color1",
  SECONDARY: "color2",
  STROBE: "strobe_color",
  MOTION: "motion",
  SATURATION: "saturation",
  BRIGHTNESS: "brightness",
  FX: "fx",
  PULSE: "pulse",
};
const LIVE_LIGHT_COLOR_KEYS = ["color1", "color2", "strobe_color"];
const LIVE_LIGHT_SLIDER_KEYS = ["motion", "saturation", "brightness"];
const LIVE_LIGHT_CONTROL_KEYS = [...LIVE_LIGHT_COLOR_KEYS, ...LIVE_LIGHT_SLIDER_KEYS];
const BPM_ROTATION_OPTIONS = [
  ["color1", "Color 1"],
  ["color2", "Color 2"],
  ["strobe_color", "Color 3"],
];
const BPM_TIMING_OSC_FIELDS = [
  ["bpm_osc_bpm_address", "BPM Value", "/composition/layers/1/video/opacity"],
  ["bpm_osc_start_address", "Tempo Start", "/composition/layers/1/clips/1/connect"],
  ["bpm_osc_resync_address", "Tempo Resync", "/composition/layers/1/clips/2/connect"],
  ["bpm_osc_stop_address", "Tempo Stop", "/composition/layers/1/clips/3/connect"],
];
const LIGHT_OSC_FILTERS = [
  ["color1", "Color 1"],
  ["color2", "Color 2"],
  ["strobe_color", "Color 3"],
  ["sliders", "Sliders"],
  ["timing", "BPM Timing"],
  ["all", "All"],
];
const VISUAL_LAYER_COUNT = 3;
const VISUAL_CLIPS_PER_LAYER = 10;
const LIGHT_SLIDER_STOPS = [0, 10, 25, 50, 75, 90, 100];
const DEFAULT_LIGHT_OSC_OUTPUT_SLOTS = 3;
const COLOR_LIGHT_OSC_OUTPUT_SLOTS = 10;
const LIGHT_OSC_NOTE_PLACEHOLDERS = [
  "Main mapped target",
  "Background hue - Main cam",
  "Background hue - PIP cam",
  "Background hue - BG cam",
  "Background hue - Now Playing",
  "Visual layer hue",
  "Clip accent hue",
  "Spare color target",
  "Spare color target",
  "Spare color target",
];
const lookControlTimers = {};

const quickSettingFields = [
  ["bpm_flip_bpm", "Default BPM", "text"],
  ["bpm_flip_division", "Default Division", "select:bpm"],
  ["bpm_rotation_slots", "Rotate Colors", "checks:bpm-rotation"],
  ["bpm_follow_now_playing", "Follow Now Playing BPM", "checkbox"],
  ["look_apply_lights", "Apply Lights with Looks", "checkbox"],
];

const settingGroups = [
  {
    title: "Current Active Routing",
    fields: [
      ["show_machine_name", "This Machine Name", "text"],
      ["app_bind_host", "Web App Bind Host", "text"],
      ["app_port", "Web App Port", "number"],
      ["public_control_url", "Control URL Override", "text"],
      ["blt_params_url", "Active BeatLink Trigger URL", "text"],
      ["resolume_host", "Active Resolume IP", "text"],
      ["resolume_port", "Active Resolume OSC Port", "number"],
    ],
  },
];

const obsSettingFields = [
  ["obs_enabled", "Enable OBS Control", "checkbox"],
  ["obs_host", "OBS WebSocket Host", "text"],
  ["obs_port", "OBS WebSocket Port", "number"],
  ["obs_password", "OBS WebSocket Password", "password"],
];

function setConnection(state, text) {
  if (!statusEl) return;
  statusEl.className = `status-pill ${state}`;
  statusEl.textContent = text;
}

function colorHex(name) {
  return appSettings?.colors?.hex?.[name] || presetData?.colors?.hex?.[name] || "#333842";
}

function colorHueDegree(name) {
  const degree = appSettings?.colors?.hue_degrees?.[name] ?? presetData?.colors?.hue_degrees?.[name];
  return Number.isFinite(Number(degree)) ? Number(degree) : null;
}

function colorHueLabel(name) {
  const degree = colorHueDegree(name);
  return degree === null ? displayColorName(name) : `${displayColorName(name)} - ${degree} deg`;
}
function displayColorName(name) {
  return String(name || "")
    .replace(/[_-]+/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function lightColorControlLabel(control) {
  if (control.key === "color1") return "Color 1";
  if (control.key === "color2") return "Color 2";
  if (control.key === "strobe_color") return "Color 3";
  return control.label || control.default_label || "Color";
}

function normalizeBpmRotationSlots(value, fallback = BPM_ROTATION_OPTIONS.map(([key]) => key)) {
  const aliases = {
    1: "color1",
    color1: "color1",
    color_1: "color1",
    primary: "color1",
    2: "color2",
    color2: "color2",
    color_2: "color2",
    secondary: "color2",
    3: "strobe_color",
    color3: "strobe_color",
    color_3: "strobe_color",
    tertiary: "strobe_color",
    accent: "strobe_color",
    strobe: "strobe_color",
    strobe_color: "strobe_color",
  };
  const rawItems = Array.isArray(value)
    ? value
    : typeof value === "string"
      ? value.split(/[,;\s]+/)
      : [];
  const selected = [];
  for (const item of rawItems) {
    const token = String(item || "").trim().toLowerCase().replace(/[\s-]+/g, "_");
    const key = aliases[token];
    if (key && !selected.includes(key)) selected.push(key);
  }
  const ordered = BPM_ROTATION_OPTIONS.map(([key]) => key).filter((key) => selected.includes(key));
  return ordered.length ? ordered : [...fallback];
}

function currentBpmRotationSlots() {
  return normalizeBpmRotationSlots(latestShow?.bpm_rotation_slots || appSettings?.bpm_rotation_slots);
}

function colorSlotLabel(key) {
  return BPM_ROTATION_OPTIONS.find(([slot]) => slot === key)?.[1] || key;
}

function bpmRotationLabel(slots = currentBpmRotationSlots()) {
  return slots.map(colorSlotLabel).join(" + ") || "No colors";
}

function colorSlotValue(colors, key) {
  if (!colors) return "";
  if (key === "color1") return colors.color1 || colors.primary || "";
  if (key === "color2") return colors.color2 || colors.secondary || "";
  if (key === "strobe_color") return colors.color3 || colors.tertiary || colors.accent || "";
  return "";
}

function showToast(text, error = false) {
  if (!lastEvent) return;
  lastEvent.textContent = text;
  lastEvent.className = error ? "muted toast error" : "muted toast";
}

function loadLiveDeckVisiblePanels() {
  const defaults = { ...LIVE_DECK_DEFAULT_PANELS };
  try {
    const saved = JSON.parse(localStorage.getItem("liveDeckVisiblePanels") || "null");
    if (saved && typeof saved === "object") {
      const merged = { ...defaults, ...saved };
      if (Object.prototype.hasOwnProperty.call(saved, "cues")) {
        if (!Object.prototype.hasOwnProperty.call(saved, "cameras")) merged.cameras = saved.cues !== false;
        if (!Object.prototype.hasOwnProperty.call(saved, "sequences")) merged.sequences = saved.cues !== false;
      }
      delete merged.cues;
      return merged;
    }
  } catch (_error) {
    // Ignore malformed local preferences and restore the default deck.
  }
  return defaults;
}

function saveLiveDeckVisiblePanels() {
  localStorage.setItem("liveDeckVisiblePanels", JSON.stringify(liveDeckVisiblePanels));
}

function setLiveDeckVisibility(nextVisiblePanels) {
  liveDeckVisiblePanels = { ...LIVE_DECK_DEFAULT_PANELS, ...nextVisiblePanels };
  saveLiveDeckVisiblePanels();
  applyLiveDeckVisibility();
}

function applyLiveDeckVisibility() {
  liveDeckPanelCards.forEach((card) => {
    const key = card.dataset.livePanelCard;
    card.hidden = liveDeckVisiblePanels[key] === false;
  });
  liveDeckPanelToggles.forEach((input) => {
    input.checked = liveDeckVisiblePanels[input.dataset.livePanelToggle] !== false;
  });
  if (liveDeckViewSummary) {
    const visibleCount = LIVE_DECK_PANEL_KEYS.filter((key) => liveDeckVisiblePanels[key] !== false).length;
    liveDeckViewSummary.textContent = visibleCount === 1 ? "1 panel visible" : `${visibleCount} panels visible`;
  }
  scheduleLiveDeckResize();
}

function renderRemoteUrls(urls) {
  remoteUrls.replaceChildren();
  const items = [];
  const seen = new Set();
  const pushUrl = (label, url, kind = "") => {
    const cleanUrl = String(url || "").trim();
    if (!cleanUrl || seen.has(cleanUrl)) return;
    seen.add(cleanUrl);
    items.push({ label, url: cleanUrl, kind });
  };

  pushUrl("This Computer / Local", appSettings?.local_control_url, "local");
  const lanUrls = appSettings?.lan_control_urls || urls || [];
  lanUrls.forEach((url, index) => pushUrl(index === 0 ? "Tablet Connector" : `Tablet Connector ${index + 1}`, url, "tablet"));
  pushUrl("Saved Tablet Override", appSettings?.public_control_url, "override");

  if (!items.length) {
    const item = document.createElement("div");
    item.className = "remote-url";
    item.textContent = "No LAN IP detected yet";
    remoteUrls.append(item);
    return;
  }
  for (const itemData of items) {
    const item = document.createElement("div");
    item.className = `remote-url ${itemData.kind}`.trim();
    const strong = document.createElement("strong");
    strong.textContent = itemData.label;
    const span = document.createElement("span");
    span.textContent = itemData.url;
    item.append(strong, span);
    remoteUrls.append(item);
  }
}
function renderPresetButtons(names) {
  presetButtons.replaceChildren();
  const performancePresets = presetData?.groups?.performance || {};
  const links = appSettings?.preset_links || {};
  const cameraConfig = appSettings?.camera_controls || {};
  const activePreset = activePerformanceName();
  for (const name of names) {
    const values = performancePresets[name] || {};
    const link = links[name] || {};
    const button = document.createElement("button");
    button.type = "button";
    button.className = "preset-button preset-look-button";
    button.classList.toggle("active", activePreset === name);
    button.classList.toggle("preview", isPreviewCueDispatch() && stagedPerformanceCue.look === name);

    const top = document.createElement("span");
    top.className = "preset-look-top";
    const label = document.createElement("span");
    label.textContent = name;
    top.append(label, makeLookSwatches(values));
    button.append(top, makeLookCueStrip(name, link, cameraConfig, { compact: true }));
    button.addEventListener("click", (event) => handleQuickEditTriggerClick(event, button, () => openLookQuickEditor(name), () => dispatchPerformanceLook(name, "look")));
    attachQuickEditShortcut(button, () => openLookQuickEditor(name));
    presetButtons.append(button);
  }
}

function isPreviewCueDispatch() {
  return cueDispatchMode === "preview";
}

function cueButtonTitle(kind, staged = false) {
  if (isPreviewCueDispatch()) return staged ? `${kind} is staged for GO. Tap to keep it in Preview.` : `Stage this ${kind} for Preview. GO sends all staged cues live.`;
  return staged ? `${kind} is staged for GO. Tap to send it live now.` : `Send this ${kind} live now. Switch to Preview to stage it instead.`;
}

function setCueDispatchMode(mode) {
  const nextMode = mode === "preview" ? "preview" : "live";
  if (cueDispatchMode === nextMode) return;
  cueDispatchMode = nextMode;
  localStorage.setItem("liveDeckCueDispatchMode", cueDispatchMode);
  if (!isPreviewCueDispatch() && stagedCueHasActions()) {
    stagedPerformanceCue = {};
    stagedPerformanceLookName = "";
    stagedPerformanceLookSource = "";
    saveStagedPerformanceCue();
  }
  renderCueRouteControls();
  renderStagedCueLane();
  renderOverviewVisuals();
  renderOverviewCameras();
  renderOverviewGenerator();
  refreshLookDispatchSurfaces();
  renderVisualControls();
  renderCameraControls();
  scheduleLiveDeckResize();
  showToast(isPreviewCueDispatch() ? "Preview route on: taps stage for GO" : "Live route on: taps apply immediately");
}

function makeCueRouteToggle(label = "Cue destination") {
  const route = document.createElement("div");
  route.className = "cue-route-control";
  const title = document.createElement("span");
  title.textContent = label;
  const choices = document.createElement("div");
  choices.className = "cue-route-choices";
  const live = document.createElement("button");
  live.type = "button";
  live.className = "cue-route-button live";
  live.textContent = "Live";
  live.ariaPressed = String(!isPreviewCueDispatch());
  live.classList.toggle("active", !isPreviewCueDispatch());
  live.title = "Taps apply live immediately";
  live.addEventListener("click", () => setCueDispatchMode("live"));
  const preview = document.createElement("button");
  preview.type = "button";
  preview.className = "cue-route-button preview";
  preview.textContent = "Preview";
  preview.ariaPressed = String(isPreviewCueDispatch());
  preview.classList.toggle("active", isPreviewCueDispatch());
  preview.title = "Taps stage for the global GO button";
  preview.addEventListener("click", () => setCueDispatchMode("preview"));
  choices.append(live, preview);
  route.append(title, choices);
  return route;
}

function renderCueRouteControls() {
  for (const container of [visualCueRoute, cameraCueRoute]) {
    if (!container) continue;
    container.replaceChildren(makeCueRouteToggle("Tap destination"));
  }
}

function lookApplyLights() {
  return appSettings?.look_apply_lights !== false;
}

function linkedLookPayload(name) {
  return { command: "linked_look", name, apply_lights: lookApplyLights() };
}

function lookDispatchTitle(name) {
  const cueText = lookApplyLights()
    ? "linked lights, visuals, cameras, and generator cues"
    : "linked visuals, cameras, and generator cues while lights stay held";
  return isPreviewCueDispatch()
    ? `Stage ${name} with its ${cueText}`
    : `Apply ${name} live now with its ${cueText}`;
}

function refreshLookDispatchSurfaces() {
  renderOverviewLooks(Object.keys(presetData?.groups?.performance || {}));
  renderPresetButtons(Object.keys(presetData?.groups?.performance || {}));
  renderLookLauncher();
  renderActiveMomentStrip(latestShow);
}

function dispatchPerformanceLook(name, source = "") {
  if (!name) return stagePerformanceLook("");
  if (isPreviewCueDispatch()) {
    stagePerformanceLook(name, source);
    showToast(`${name} staged for GO`);
    return;
  }
  optimisticPerformanceLookName = name;
  if (latestShow) {
    latestShow = {
      ...latestShow,
      active_look_name: name,
      source: lookApplyLights() ? `performance:${name}` : latestShow.source,
    };
  }
  refreshLookDispatchSurfaces();
  renderSelectedButtons(latestShow);
  markManualOverride();
  sendCommand(linkedLookPayload(name)).then((result) => {
    if (!result && optimisticPerformanceLookName === name) {
      optimisticPerformanceLookName = "";
      refreshLookDispatchSurfaces();
      renderSelectedButtons(latestShow);
    }
  });
  showToast(`${name} applied live`);
}
function dispatchVisualCue(id) {
  if (isPreviewCueDispatch()) {
    stageVisualCue(id);
    showToast("Visual staged for GO");
    return;
  }
  rememberVisualSelection(id);
  sendCommand({ command: "visual_trigger", id });
}

function dispatchCameraCue(group, id) {
  if (isPreviewCueDispatch()) {
    stageCameraCue(group, id);
    showToast(`${group === "scene" ? "Scene" : "Camera"} staged for GO`);
    return;
  }
  if (group === "scene") sendCommand({ command: "camera_trigger", kind: "scene", id });
  else sendCommand({ command: "camera_trigger", kind: "camera", group, id });
}

function dispatchGeneratorCue(presetId) {
  if (isPreviewCueDispatch()) {
    stageGeneratorCue(presetId);
    showToast("Generator staged for GO");
    return;
  }
  const values = valuesWithPresetDefaults(presetId);
  setLocalGenerativeVisual(values);
  sendCommand({ command: "generative_visual", values });
}

function saveStagedPerformanceCue() {
  if (Object.keys(stagedPerformanceCue).length) localStorage.setItem("liveDeckStagedCue", JSON.stringify(stagedPerformanceCue));
  else localStorage.removeItem("liveDeckStagedCue");
  if (stagedPerformanceLookName) localStorage.setItem("liveDeckStagedLook", stagedPerformanceLookName);
  else localStorage.removeItem("liveDeckStagedLook");
  if (stagedPerformanceLookSource) localStorage.setItem("liveDeckStagedLookSource", stagedPerformanceLookSource);
  else localStorage.removeItem("liveDeckStagedLookSource");
}

function stagedCueHasActions() {
  return Object.values(stagedPerformanceCue).some(Boolean);
}

function stageCuePatch(patch, source = "") {
  stagedPerformanceCue = { ...stagedPerformanceCue, ...patch };
  Object.keys(stagedPerformanceCue).forEach((key) => {
    if (!stagedPerformanceCue[key]) delete stagedPerformanceCue[key];
  });
  stagedPerformanceLookName = stagedPerformanceCue.look || "";
  if (source) stagedPerformanceLookSource = source;
  saveStagedPerformanceCue();
  renderOverviewLooks(Object.keys(presetData?.groups?.performance || {}));
  renderPresetButtons(Object.keys(presetData?.groups?.performance || {}));
  renderLookLauncher();
  renderOverviewVisuals();
  renderOverviewCameras();
  renderOverviewGenerator();
  renderGeneratorQuickPresets();
  renderGeneratorPresetGallery();
  renderVisualControls();
  renderCameraControls();
  renderCueRouteControls();
  renderStagedCueLane();
  renderActiveMomentStrip(latestShow);
  scheduleLiveDeckResize();
}

function stagePerformanceLook(name, source = "") {
  if (!name) {
    stagedPerformanceCue = {};
    stagedPerformanceLookName = "";
    stagedPerformanceLookSource = "";
    saveStagedPerformanceCue();
    renderOverviewLooks(Object.keys(presetData?.groups?.performance || {}));
    renderPresetButtons(Object.keys(presetData?.groups?.performance || {}));
    renderLookLauncher();
    renderOverviewVisuals();
    renderOverviewCameras();
    renderOverviewGenerator();
    renderGeneratorQuickPresets();
    renderGeneratorPresetGallery();
    renderVisualControls();
    renderCameraControls();
    renderCueRouteControls();
    renderStagedCueLane();
    renderActiveMomentStrip(latestShow);
    scheduleLiveDeckResize();
    return;
  }
  const link = appSettings?.preset_links?.[name] || {};
  stagedPerformanceCue = {
    look: name,
    visual_id: link.visual_id || "",
    main_box_id: link.main_box_id || "",
    pip_box_id: link.pip_box_id || "",
    background_id: link.background_id || "",
    visuals_cams_id: link.visuals_cams_id || "",
    scene_id: link.scene_id || "",
  };
  stagedPerformanceLookName = name;
  stagedPerformanceLookSource = source;
  saveStagedPerformanceCue();
  stageCuePatch({}, source);
}

function stageVisualCue(id) {
  stageCuePatch({ visual_id: id }, "visual");
}

function stageCameraCue(group, id) {
  stageCuePatch({ [group === "scene" ? "scene_id" : `${group}_id`]: id }, group === "scene" ? "scene" : "camera");
}

function stageGeneratorCue(presetId) {
  stageCuePatch({ generator_preset: presetId }, "generator");
}

function stagedCueSummary() {
  const cue = stagedPerformanceCue;
  const camera = appSettings?.camera_controls || {};
  const parts = [];
  if (cue.look) parts.push(`Look: ${cue.look}`);
  if (cue.visual_id) parts.push(`Visual: ${optionLabel(appSettings?.visual_controls, cue.visual_id, cue.visual_id)}`);
  if (cue.main_box_id) parts.push(`Main: ${optionLabel(camera.groups?.main_box, cue.main_box_id, cue.main_box_id)}`);
  if (cue.pip_box_id) parts.push(`PIP: ${optionLabel(camera.groups?.pip_box, cue.pip_box_id, cue.pip_box_id)}`);
  if (cue.background_id) parts.push(`BG: ${optionLabel(camera.groups?.background, cue.background_id, cue.background_id)}`);
  if (cue.visuals_cams_id) parts.push(`Visuals Cam: ${optionLabel(camera.groups?.visuals_cams, cue.visuals_cams_id, cue.visuals_cams_id)}`);
  if (cue.scene_id) parts.push(`Scene: ${optionLabel(camera.scenes, cue.scene_id, cue.scene_id)}`);
  if (cue.generator_preset) parts.push(`Generator: ${generativePresetOptions()[cue.generator_preset]?.name || cue.generator_preset}`);
  return parts;
}

async function launchStagedPerformanceLook() {
  if (!stagedCueHasActions()) {
    showToast("Stage a look, visual, camera, scene, or generator first.", true);
    return;
  }
  const cue = { ...stagedPerformanceCue };
  try {
    markManualOverride();
    const linked = cue.look ? appSettings?.preset_links?.[cue.look] || {} : {};
    if (cue.look) await sendCommandForResult(linkedLookPayload(cue.look));
    if (cue.visual_id && cue.visual_id !== linked.visual_id) await sendCommandForResult({ command: "visual_trigger", id: cue.visual_id });
    for (const group of ["main_box", "pip_box", "background", "visuals_cams"]) {
      if (cue[`${group}_id`] && cue[`${group}_id`] !== linked[`${group}_id`]) await sendCommandForResult({ command: "camera_trigger", kind: "camera", group, id: cue[`${group}_id`] });
    }
    if (cue.scene_id && cue.scene_id !== linked.scene_id) await sendCommandForResult({ command: "camera_trigger", kind: "scene", id: cue.scene_id });
    if (cue.generator_preset) {
      const values = valuesWithPresetDefaults(cue.generator_preset);
      setLocalGenerativeVisual(values);
      await sendCommandForResult({ command: "generative_visual", values });
    }
    stagePerformanceLook("");
    showToast("Staged cue sent live");
    await loadStatus();
  } catch (error) {
    showToast(String(error.message || error), true);
  }
}

const FAVORITE_CATEGORIES = [
  ["looks", "Looks"],
  ["visuals", "Visuals"],
  ["main_box", "Main Cams"],
  ["pip_box", "PIP Cams"],
  ["background", "BG Cams"],
  ["visuals_cams", "Visuals Cams"],
  ["scenes", "Scenes"],
  ["generator", "Generator"],
];

function performanceBanks() {
  return Array.isArray(appSettings?.performance_banks) ? appSettings.performance_banks : [];
}

function activePerformanceBank() {
  const banks = performanceBanks();
  return banks.find((bank) => bank.id === appSettings?.active_performance_bank) || banks[0] || null;
}

function favoriteChoices(category) {
  const camera = appSettings?.camera_controls || {};
  if (category === "looks") return Object.keys(presetData?.groups?.performance || {}).map((id) => ({ id, label: id }));
  if (category === "visuals") return (appSettings?.visual_controls || []).map((item) => ({ id: item.id, label: item.label || item.name || item.id }));
  if (["main_box", "pip_box", "background", "visuals_cams"].includes(category)) return (camera.groups?.[category] || []).map((item) => ({ id: item.id, label: item.label || item.name || item.id }));
  if (category === "scenes") return (camera.scenes || []).map((item) => ({ id: item.id, label: item.label || item.name || item.id }));
  if (category === "generator") return Object.entries(generativePresetOptions()).map(([id, item]) => ({ id, label: item.name || id }));
  return [];
}

function favoriteChoiceLabel(category, id) {
  return favoriteChoices(category).find((item) => item.id === id)?.label || id;
}

function favoriteQuickEditTarget(category, id) {
  const cameraConfig = appSettings?.camera_controls || {};
  if (category === "looks") return () => openLookQuickEditor(id);
  if (category === "visuals") {
    const item = (appSettings?.visual_controls || []).find((candidate) => candidate.id === id);
    return item ? () => openVisualClipOscEditor(item, visualLayerNumber(item), visualClipNumber(item)) : null;
  }
  if (["main_box", "pip_box", "background", "visuals_cams"].includes(category)) {
    const item = (cameraConfig.groups?.[category] || []).find((candidate) => candidate.id === id);
    return item ? () => openCameraOscEditor(category, item) : null;
  }
  if (category === "scenes") {
    const item = (cameraConfig.scenes || []).find((candidate) => candidate.id === id);
    return item ? () => openCameraOscEditor("scene", item) : null;
  }
  return null;
}

function stagedCueCompactText(summary) {
  if (!summary.length) return isPreviewCueDispatch() ? "Preview mode: choose cues, then GO" : "Live mode: taps send now";
  if (summary.length === 1) return "1 action ready";
  return `${summary.length} actions ready`;
}

function setLiveDeckSaveStatus(text, transient = false) {
  if (!liveDeckSaveStatus) return;
  liveDeckSaveStatus.textContent = text;
  if (!transient) return;
  const token = String(Date.now());
  liveDeckSaveStatus.dataset.messageToken = token;
  window.setTimeout(() => {
    if (liveDeckSaveStatus?.dataset.messageToken === token) {
      delete liveDeckSaveStatus.dataset.messageToken;
      renderLiveDeckLookCapture(latestShow);
    }
  }, 5000);
}

function renderLiveDeckLookCapture(show = latestShow) {
  if (!liveDeckLookName) return;
  const activeName = activePerformanceName();
  liveDeckLookName.placeholder = activeName ? `${activeName} or new label` : "Type a look label";
  if (!liveDeckLookNameDirty && document.activeElement !== liveDeckLookName && !liveDeckLookName.value.trim()) {
    liveDeckLookName.value = activeName || "";
  }
  if (liveDeckSaveStatus && !liveDeckSaveStatus.dataset.messageToken) {
    const mode = nowPlayingModeLabel(show?.manual_mode || "cdj");
    liveDeckSaveStatus.textContent = `Captures lights, ${mode}, BPM, visuals, cams, generator.`;
  }
}

function applySavedLookResult(result, name) {
  if (result.config) {
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    settingsDirty = false;
    lookLinksDirty = false;
    lookBuilderDirty = false;
  }
  if (result.presets) presetData = result.presets;
  if (result.state) renderShowState(result.state);
  renderSaveLookPicker();
  if (saveCurrentLookSelect) saveCurrentLookSelect.value = name;
  if (lookBuilderName && !lookBuilderDirty) lookBuilderName.value = name;
  renderOverviewLooks(Object.keys(presetData?.groups?.performance || {}));
  renderPresetButtons(Object.keys(presetData?.groups?.performance || {}));
  renderLookLauncher();
  renderLookBuilder();
  renderPresetEditor();
  renderPresetLinks();
  renderLookLinkForm();
  renderSequencer();
}

async function saveCurrentShowStateFromLiveDeck() {
  const name = (liveDeckLookName?.value || "").trim();
  if (!name) {
    setLiveDeckSaveStatus("Name the look first.", true);
    liveDeckLookName?.focus();
    return;
  }
  try {
    setLiveDeckSaveStatus(`Saving ${name}...`);
    const result = await sendCommandForResult({ command: "save_current_look", name }, { quiet: true });
    applySavedLookResult(result, name);
    liveDeckLookNameDirty = false;
    setLiveDeckSaveStatus(result.message || `Saved current show state as ${name}.`, true);
    if (saveLookStatus) saveLookStatus.textContent = result.message || `Saved current show state as ${name}.`;
    showToast(result.message || `Saved ${name}`);
    await loadStatus({ full: true, force: true });
  } catch (error) {
    const message = String(error.message || error);
    setLiveDeckSaveStatus(message, true);
    showToast(message, true);
  }
}

function renderStagedCueLane() {
  if (!stagedCueLane) return;
  stagedCueLane.replaceChildren();
  const summary = stagedCueSummary();
  const state = document.createElement("div");
  state.className = "staged-cue-state";
  const label = document.createElement("span");
  label.textContent = "NEXT";
  const look = document.createElement("strong");
  look.textContent = summary[0] || "No cue staged";
  const source = document.createElement("small");
  source.textContent = stagedCueCompactText(summary);
  if (summary.length > 1) source.title = summary.join(" / ");
  else if (stagedPerformanceLookSource) source.title = `Suggested by ${stagedPerformanceLookSource}`;
  state.append(label, look, source);
  const actions = document.createElement("div");
  actions.className = "staged-cue-actions";
  const go = document.createElement("button");
  go.type = "button";
  go.className = "staged-go-button";
  go.textContent = "GO";
  go.disabled = !stagedCueHasActions() || !isPreviewCueDispatch();
  go.addEventListener("click", launchStagedPerformanceLook);
  const clear = document.createElement("button");
  clear.type = "button";
  clear.textContent = "Clear";
  clear.disabled = !stagedCueHasActions();
  clear.addEventListener("click", () => stagePerformanceLook(""));
  const route = makeCueRouteToggle("Tap route");
  route.classList.add("staged-cue-route");
  actions.append(go, clear, route);
  stagedCueLane.append(state, actions);
  if (stagedCueHint) stagedCueHint.textContent = summary.length ? `${stagedCueCompactText(summary)}. Open Details for routing.` : isPreviewCueDispatch() ? "Preview route is on: choose cues, then hit GO." : "Live route is on: switch to Preview only when you want to stage cues.";
}

function renderSongMomentMarkers() {
  if (!songMomentMarkers) return;
  songMomentMarkers.replaceChildren();
  const moments = activePerformanceBank()?.song_moments || {};
  const assigned = ["intro", "build", "drop", "outro"].filter((moment) => moments[moment]);
  songMomentMarkers.closest(".performance-command-panel")?.classList.toggle("has-song-moments", assigned.length > 0);
  assigned.forEach((moment) => {
    const look = moments[moment];
    const button = document.createElement("button");
    button.type = "button";
    button.className = "song-moment-button";
    button.ariaLabel = `${moment} stages ${look}`;
    const title = document.createElement("strong");
    title.textContent = moment;
    const detail = document.createElement("span");
    detail.textContent = look;
    button.append(title, detail);
    button.addEventListener("click", () => stagePerformanceLook(look, moment));
    songMomentMarkers.append(button);
  });
}

function renderFavoriteBankSurface() {
  const bank = activePerformanceBank();
  if (favoriteBankSelect) {
    favoriteBankSelect.replaceChildren();
    performanceBanks().forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = item.name;
      favoriteBankSelect.append(option);
    });
    favoriteBankSelect.value = bank?.id || "";
  }
  if (favoriteCategoryTabs) {
    favoriteCategoryTabs.replaceChildren();
    if (!FAVORITE_CATEGORIES.some(([id]) => id === activeFavoriteCategory)) activeFavoriteCategory = "looks";
    FAVORITE_CATEGORIES.forEach(([category, label]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = label;
      button.classList.toggle("active", category === activeFavoriteCategory);
      button.ariaPressed = String(category === activeFavoriteCategory);
      button.setAttribute("role", "tab");
      button.addEventListener("click", () => {
        activeFavoriteCategory = category;
        localStorage.setItem("liveDeckFavoriteCategory", category);
        renderFavoriteBankSurface();
      });
      favoriteCategoryTabs.append(button);
    });
  }
  if (!favoriteBankGrid) return;
  favoriteBankGrid.replaceChildren();
  const ids = bank?.favorites?.[activeFavoriteCategory] || [];
  if (!ids.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = `No ${FAVORITE_CATEGORIES.find(([id]) => id === activeFavoriteCategory)?.[1].toLowerCase() || "favorites"} in this bank yet. Add them in Looks.`;
    favoriteBankGrid.append(empty);
    return;
  }
  ids.forEach((id) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "favorite-cue-button";
    const label = favoriteChoiceLabel(activeFavoriteCategory, id);
    button.textContent = label;
    const openEditor = favoriteQuickEditTarget(activeFavoriteCategory, id);
    const editHint = openEditor ? " - Right-click, long-press, or Shift-click to edit OSC" : "";
    button.title = activeFavoriteCategory === "looks" ? `${lookDispatchTitle(label)}${editHint}` : `Send ${label}${editHint}`;
    if (openEditor) {
      button.addEventListener("click", (event) => handleQuickEditTriggerClick(event, button, openEditor, () => triggerFavorite(activeFavoriteCategory, id)));
      attachQuickEditShortcut(button, openEditor);
    } else {
      button.addEventListener("click", () => triggerFavorite(activeFavoriteCategory, id));
    }
    favoriteBankGrid.append(button);
  });
}

function triggerFavorite(category, id) {
  if (category === "looks") return dispatchPerformanceLook(id, "favorite bank");
  if (category === "visuals") return dispatchVisualCue(id);
  if (["main_box", "pip_box", "background", "visuals_cams"].includes(category)) return dispatchCameraCue(category, id);
  if (category === "scenes") return dispatchCameraCue("scene", id);
  if (category === "generator") return applyGenerativePreset(id);
}

async function persistPerformanceBanks(banks, activeId, successMessage = "Favorite bank saved") {
  if (favoriteBankEditor?.contains(document.activeElement)) document.activeElement.blur();
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ performance_banks: banks, active_performance_bank: activeId }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config?.preset_groups || presetData;
    renderPerformanceSurfaces();
    showToast(successMessage);
  } catch (error) {
    showToast(String(error.message || error), true);
  }
}

function clonePerformanceBanks() {
  return JSON.parse(JSON.stringify(performanceBanks()));
}

function renderFavoriteBankEditor() {
  if (!favoriteBankEditor || !appSettings) return;
  if (favoriteBankEditor.contains(document.activeElement)) return;
  favoriteBankEditor.replaceChildren();
  const bank = activePerformanceBank();
  if (!bank) return;
  const controls = document.createElement("div");
  controls.className = "favorite-bank-editor-controls";
  const bankLabel = document.createElement("span");
  bankLabel.className = "song-moment-set-label";
  bankLabel.textContent = "Set / venue";
  const bankSelect = document.createElement("select");
  performanceBanks().forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.name;
    bankSelect.append(option);
  });
  bankSelect.value = bank.id;
  bankSelect.addEventListener("change", () => persistPerformanceBanks(clonePerformanceBanks(), bankSelect.value, "Song moment set changed"));
  const nameInput = document.createElement("input");
  nameInput.value = bank.name;
  nameInput.maxLength = 48;
  nameInput.setAttribute("aria-label", "Set or venue name");
  const saveName = document.createElement("button");
  saveName.type = "button";
  saveName.textContent = "Save name";
  saveName.addEventListener("click", () => {
    const banks = clonePerformanceBanks();
    const target = banks.find((item) => item.id === bank.id);
    if (target) target.name = nameInput.value.trim() || target.name;
    persistPerformanceBanks(banks, bank.id, "Song moment set named");
  });
  const addBank = document.createElement("button");
  addBank.type = "button";
  addBank.textContent = "New set";
  addBank.addEventListener("click", () => {
    const banks = clonePerformanceBanks();
    const name = `Set ${banks.length + 1}`;
    const id = `set-${Date.now()}`;
    banks.push({ id, name, favorites: {}, song_moments: {} });
    persistPerformanceBanks(banks, id, "New song moment set created");
  });
  controls.append(bankLabel, bankSelect, nameInput, saveName, addBank);
  favoriteBankEditor.append(controls);

  const momentPanel = document.createElement("section");
  momentPanel.className = "favorite-moment-editor";
  const momentHeading = document.createElement("h3");
  momentHeading.textContent = "What should each song moment stage?";
  const momentHelp = document.createElement("p");
  momentHelp.className = "muted";
  momentHelp.textContent = "Each assignment stages the full linked look. Nothing is sent until you press the global GO button.";
  momentPanel.append(momentHeading, momentHelp);
  const momentGrid = document.createElement("div");
  momentGrid.className = "favorite-moment-grid";
  ["intro", "build", "drop", "outro"].forEach((moment) => {
    const field = document.createElement("label");
    const title = document.createElement("span");
    title.textContent = `${moment} stages`;
    const select = document.createElement("select");
    const empty = document.createElement("option");
    empty.value = "";
    empty.textContent = "No look assigned";
    select.append(empty);
    favoriteChoices("looks").forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = item.label;
      select.append(option);
    });
    select.value = bank.song_moments?.[moment] || "";
    select.addEventListener("change", () => {
      const banks = clonePerformanceBanks();
      const target = banks.find((item) => item.id === bank.id);
      target.song_moments = { ...(target.song_moments || {}), [moment]: select.value };
      persistPerformanceBanks(banks, bank.id, `${moment} staging assignment saved`);
    });
    field.append(title, select);
    momentGrid.append(field);
  });
  momentPanel.append(momentGrid);
  favoriteBankEditor.append(momentPanel);
}

async function persistPanicSafe(safety) {
  if (panicSafeEditor?.contains(document.activeElement)) document.activeElement.blur();
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ panic_safe: safety }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config?.preset_groups || presetData;
    renderPerformanceSurfaces();
    showToast("Panic safe state saved");
  } catch (error) {
    showToast(String(error.message || error), true);
  }
}

function renderPanicSafeEditor() {
  if (!panicSafeEditor || !appSettings) return;
  if (panicSafeEditor.contains(document.activeElement)) return;
  panicSafeEditor.replaceChildren();
  const safety = appSettings.panic_safe || {};
  const form = document.createElement("div");
  form.className = "panic-safe-form";
  const fields = [
    ["look", "Safe look", favoriteChoices("looks")],
    ["visual_id", "Safe visual", favoriteChoices("visuals")],
    ["main_box_id", "Safe main cam", favoriteChoices("main_box")],
    ["pip_box_id", "Safe PIP cam", favoriteChoices("pip_box")],
    ["background_id", "Safe background cam", favoriteChoices("background")],
    ["visuals_cams_id", "Safe visuals cam", favoriteChoices("visuals_cams")],
    ["scene_id", "Safe scene", favoriteChoices("scenes")],
  ];
  fields.forEach(([key, label, options]) => {
    const field = document.createElement("label");
    const title = document.createElement("span");
    title.textContent = label;
    const select = document.createElement("select");
    if (key !== "look") {
      const empty = document.createElement("option");
      empty.value = "";
      empty.textContent = "No override";
      select.append(empty);
    }
    options.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = item.label;
      select.append(option);
    });
    select.value = safety[key] || "";
    select.dataset.panicKey = key;
    field.append(title, select);
    form.append(field);
  });
  const generator = document.createElement("label");
  generator.className = "panic-safe-check";
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = safety.stop_generator !== false;
  checkbox.dataset.panicKey = "stop_generator";
  const label = document.createElement("span");
  label.textContent = "Stop generator output";
  generator.append(checkbox, label);
  form.append(generator);
  const save = document.createElement("button");
  save.type = "button";
  save.textContent = "Save panic safe state";
  save.addEventListener("click", () => {
    const next = {};
    form.querySelectorAll("[data-panic-key]").forEach((input) => {
      next[input.dataset.panicKey] = input.type === "checkbox" ? input.checked : input.value;
    });
    persistPanicSafe(next);
  });
  panicSafeEditor.append(form, save);
}

function renderPerformanceSurfaces() {
  renderStagedCueLane();
  renderSongMomentMarkers();
  renderFavoriteBankSurface();
  renderFavoriteBankEditor();
  renderPanicSafeEditor();
  renderActiveMomentStrip(latestShow);
}

function renderSystemConfidence(items = []) {
  if (!systemConfidence) return;
  systemConfidence.replaceChildren();
  items.forEach((item) => {
    const card = document.createElement("div");
    card.className = `system-confidence-item ${item.state || "unknown"}`;
    card.title = item.detail || "";
    const name = document.createElement("span");
    name.textContent = item.label;
    const value = document.createElement("strong");
    value.textContent = item.summary;
    card.append(name, value);
    systemConfidence.append(card);
  });
}


function startPanicHold() {
  if (!panicSafeButton || panicHoldTimer) return;
  panicSafeButton.classList.add("holding");
  panicSafeButton.textContent = "Keep holding...";
  panicHoldTimer = setTimeout(() => {
    panicHoldTimer = null;
    panicSafeButton.classList.remove("holding");
    panicSafeButton.textContent = "SAFE sent";
    stopShowSequencePlayback("Panic safe stopped the sequence.");
    stagePerformanceLook("");
    sendCommand({ command: "panic_safe" });
    setTimeout(() => { if (panicSafeButton) panicSafeButton.textContent = "Hold SAFE"; }, 1400);
  }, 1000);
}

function cancelPanicHold() {
  if (panicHoldTimer) clearTimeout(panicHoldTimer);
  panicHoldTimer = null;
  if (panicSafeButton?.textContent === "Keep holding...") {
    panicSafeButton.classList.remove("holding");
    panicSafeButton.textContent = "Hold SAFE";
  }
}

function lookStateDetails(name, show = latestShow) {
  const performancePresets = presetData?.groups?.performance || {};
  const links = appSettings?.preset_links || {};
  const cameraConfig = appSettings?.camera_controls || {};
  const presetValues = name ? performancePresets[name] : null;
  const values = presetValues || {
    PRIMARY: colorSlotValue(show?.colors, "color1"),
    SECONDARY: colorSlotValue(show?.colors, "color2"),
    STROBE: colorSlotValue(show?.colors, "strobe_color"),
  };
  return {
    name: name || "Manual",
    values,
    link: name ? links[name] || {} : {},
    cameraConfig,
  };
}

function generativeVisualLinkLabel(link = {}) {
  const values = link.generative_visual || {};
  if (!Object.keys(values).length) return "No change";
  if (values.blackout || values.enabled === false) return "Stopped";
  return generativePresetOptions()[values.preset]?.name || values.preset || "Generator";
}

function bpmLinkLabel(link = {}) {
  if (!link.bpm_enabled) return "No change";
  const mode = link.bpm_flip_mode === "seconds" ? `${link.bpm_seconds || 8}s` : `${link.bpm || 125} BPM ${link.bpm_division || "1/4"}`;
  const running = link.bpm_running ? "Run" : "Stop";
  return `${running} - ${mode} - ${bpmRotationLabel(normalizeBpmRotationSlots(link.bpm_rotation_slots))}`;
}

function lookCueItems(link = {}, cameraConfig = {}) {
  return [
    ["Now Playing", link.now_playing_mode ? link.now_playing_mode.toUpperCase() : "No change"],
    ["Section", link.section_preset || "No change"],
    ["Visual", optionLabel(appSettings?.visual_controls, link.visual_id)],
    ["Generator", generativeVisualLinkLabel(link)],
    ["BPM", bpmLinkLabel(link)],
    ["Main Cam", optionLabel(cameraConfig.groups?.main_box, link.main_box_id)],
    ["PIP Cam", optionLabel(cameraConfig.groups?.pip_box, link.pip_box_id)],
    ["BG Cam", optionLabel(cameraConfig.groups?.background, link.background_id)],
    ["Visuals Cam", optionLabel(cameraConfig.groups?.visuals_cams, link.visuals_cams_id)],
    ["Scene", optionLabel(cameraConfig.scenes, link.scene_id)],
  ];
}

function isNoCueChange(value) {
  return value === "None" || value === "No change" || value === "-" || value === "";
}

function makeLookStatePanel(label, name, options = {}) {
  const detail = lookStateDetails(name, options.show);
  const panel = document.createElement("div");
  panel.className = `look-state-panel ${options.mode || ""}`.trim();
  const heading = document.createElement("div");
  heading.className = "look-state-heading";
  const labelEl = document.createElement("span");
  labelEl.textContent = label;
  const nameEl = document.createElement("strong");
  nameEl.textContent = options.placeholder || detail.name;
  heading.append(labelEl, nameEl);
  const note = document.createElement("em");
  note.className = "look-state-note";
  if (options.placeholder && !name) note.textContent = "Nothing staged";
  else if (!name) note.textContent = "Live controls";
  else note.textContent = options.mode === "preview" ? "Staged for GO" : "Live now";
  panel.append(heading, makeLookSwatches(detail.values), note);
  return panel;
}

function renderOverviewLookPreview() {
  if (!overviewLookPreview) return;
  overviewLookPreview.replaceChildren();
  const currentName = activePerformanceName() || "";
  const previewEnabled = isPreviewCueDispatch();
  overviewLookPreview.classList.toggle("live-route", !previewEnabled);
  overviewLookPreview.append(makeLookStatePanel("Active", currentName, { mode: "active", show: latestShow }));
  if (!previewEnabled) return;
  overviewLookPreview.append(makeLookStatePanel("Next", stagedPerformanceLookName, { mode: "preview", placeholder: stagedPerformanceLookName || "Pick a look" }));
  const launch = document.createElement("button");
  launch.type = "button";
  launch.textContent = "GO";
  launch.disabled = !stagedPerformanceLookName;
  launch.addEventListener("click", launchStagedPerformanceLook);
  const clear = document.createElement("button");
  clear.type = "button";
  clear.textContent = "Clear Preview";
  clear.disabled = !stagedPerformanceLookName;
  clear.addEventListener("click", () => stagePerformanceLook(""));
  overviewLookPreview.append(launch, clear);
}

function renderOverviewLooks(names) {
  if (!overviewLookGrid || !presetData || !appSettings) return;
  overviewLookGrid.replaceChildren();
  if (stagedPerformanceLookName && !names.includes(stagedPerformanceLookName)) stagePerformanceLook("");
  renderOverviewLookPreview();
  const performancePresets = presetData.groups?.performance || {};
  const links = appSettings.preset_links || {};
  const cameraConfig = appSettings.camera_controls || {};
  const activePreset = activePerformanceName();
  for (const name of names) {
    const values = performancePresets[name] || {};
    const link = links[name] || {};
    const card = document.createElement("article");
    card.className = "overview-look-card";

    const preview = document.createElement("button");
    preview.type = "button";
    preview.className = "overview-look-button";
    preview.ariaLabel = `${isPreviewCueDispatch() ? "Stage" : "Apply"} ${name} look`;
    preview.title = lookDispatchTitle(name);
    preview.classList.toggle("active", activePreset === name);
    preview.classList.toggle("preview", isPreviewCueDispatch() && stagedPerformanceLookName === name);
    const label = document.createElement("strong");
    label.textContent = name;
    preview.append(label, makeLookSwatches(values), makeLookCueStrip(name, link, cameraConfig, { compact: true }));
    preview.addEventListener("click", (event) => handleQuickEditTriggerClick(event, preview, () => openLookQuickEditor(name), () => dispatchPerformanceLook(name, "look")));
    attachQuickEditShortcut(preview, () => openLookQuickEditor(name));

    const goLive = document.createElement("button");
    goLive.type = "button";
    goLive.className = "overview-look-go-live";
    goLive.textContent = isPreviewCueDispatch() ? "Stage" : "Apply";
    goLive.ariaLabel = `${isPreviewCueDispatch() ? "Stage" : "Apply"} ${name} look`;
    goLive.title = lookDispatchTitle(name);
    goLive.addEventListener("click", (event) => handleQuickEditTriggerClick(event, goLive, () => openLookQuickEditor(name), () => dispatchPerformanceLook(name, "look")));
    attachQuickEditShortcut(goLive, () => openLookQuickEditor(name));

    card.append(preview, goLive);
    overviewLookGrid.append(card);
  }
}

function renderLookLauncher() {
  if (!lookLauncherGrid || !appSettings || !presetData) return;
  lookLauncherGrid.replaceChildren();
  const looks = presetData.groups?.performance || {};
  const links = appSettings.preset_links || {};
  const cameraConfig = appSettings.camera_controls || {};
  const activeName = activePerformanceName();
  for (const [name, values] of Object.entries(looks)) {
    const link = links[name] || {};
    const button = document.createElement("button");
    button.type = "button";
    button.className = "look-launch-button";
    button.classList.toggle("active", activeName === name);
    button.classList.toggle("preview", isPreviewCueDispatch() && stagedPerformanceCue.look === name);
    button.ariaPressed = String(activeName === name);
    button.ariaLabel = `Launch ${name} look`;
    button.title = lookDispatchTitle(name);

    const title = document.createElement("strong");
    title.textContent = name;
    const meta = document.createElement("small");
    const linkedVisual = optionLabel(appSettings.visual_controls, link.visual_id, "");
    const linkedScene = optionLabel(cameraConfig.scenes, link.scene_id, "");
    meta.textContent = [linkedVisual, linkedScene].filter(Boolean).join(" / ") || "Linked live cues";
    button.append(title, makeLookSwatches(values), meta);
    button.addEventListener("click", (event) => handleQuickEditTriggerClick(event, button, () => openLookQuickEditor(name), () => dispatchPerformanceLook(name, "look")));
    attachQuickEditShortcut(button, () => openLookQuickEditor(name));
    lookLauncherGrid.append(button);
  }
}
function renderOverviewLightState(show) {
  if (!overviewLightState || !show) return;
  if (overviewLightState.contains(document.activeElement)) return;
  const colors = show.colors || {};
  const colorNames = appSettings?.colors?.names || [];
  overviewLightState.replaceChildren();
  [
    ["Color 1", "color1", colorSlotValue(colors, "color1")],
    ["Color 2", "color2", colorSlotValue(colors, "color2")],
    ["Color 3", "strobe_color", colorSlotValue(colors, "strobe_color")],
  ].forEach(([label, key, fallback]) => {
    const output = outputByKey(key) || {};
    const selected = output.color || fallback || "";
    const card = document.createElement("label");
    card.className = "overview-color-card overview-color-control";
    card.style.setProperty("--overview-color", colorHex(selected));
    const chip = document.createElement("i");
    const text = document.createElement("span");
    text.textContent = label;
    const select = document.createElement("select");
    const names = selected && !colorNames.includes(selected) ? [selected, ...colorNames] : colorNames;
    for (const colorName of names) {
      const option = document.createElement("option");
      option.value = colorName;
      option.textContent = colorName;
      select.append(option);
    }
    select.value = selected || select.value;
    select.disabled = !names.length;
    select.addEventListener("change", () => sendCommand({ command: "set_control", key, value: select.value }));
    card.append(chip, text, select);
    overviewLightState.append(card);
  });
}

function renderOverviewLightControls() {
  if (!overviewLightControls || !appSettings || !latestShow) return;
  if (overviewLightControls.contains(document.activeElement)) return;
  overviewLightControls.replaceChildren();
  for (const control of liveLightSliderControls()) {
    const output = outputByKey(control.key) || {};
    const field = document.createElement("label");
    field.className = "overview-control";
    const text = document.createElement("span");
    text.textContent = control.label;
    field.append(text);

    if (control.kind === "color") {
      const select = document.createElement("select");
      select.value = output.color || "";
      for (const colorName of appSettings.colors.names || []) {
        const option = document.createElement("option");
        option.value = colorName;
        option.textContent = colorName;
        select.append(option);
      }
      select.value = output.color || select.value;
      select.addEventListener("change", () => sendCommand({ command: "set_control", key: control.key, value: select.value }));
      field.append(select);
    } else {
      const row = document.createElement("div");
      row.className = "overview-range-row";
      const readout = document.createElement("strong");
      const range = document.createElement("input");
      const selected = Math.round(Number(output.value || 0) * 100);
      range.type = "range";
      range.min = "0";
      range.max = "100";
      range.step = "1";
      range.value = String(selected);
      readout.textContent = `${selected}%`;
      let lastSent = selected;
      const sendValue = () => {
        const next = Math.max(0, Math.min(100, Math.round(Number(range.value || 0))));
        readout.textContent = `${next}%`;
        if (next !== lastSent) {
          lastSent = next;
          sendCommand({ command: "set_control", key: control.key, value: next });
        }
      };
      range.addEventListener("input", sendValue);
      range.addEventListener("change", sendValue);
      row.append(range, readout);
      field.append(row);
    }
    overviewLightControls.append(field);
  }
}

function overviewBpmDivisions() {
  const available = appSettings?.bpm_divisions || DEFAULT_BPM_DIVISIONS;
  const preferred = ["1/8", "1/4", "1/2 bar", "1 bar", "2 bars", "4 bars"];
  const divisions = preferred.filter((division) => available.includes(division));
  if (selectedDivision && available.includes(selectedDivision) && !divisions.includes(selectedDivision)) divisions.push(selectedDivision);
  return divisions.length ? divisions : available.slice(0, 6);
}

function renderOverviewBpmControls(show = latestShow) {
  if (!overviewBpmControls || !show || !appSettings) return;
  overviewBpmControls.replaceChildren();
  overviewBpmControls.append(makeOverviewBpmSurface(show));
}

function makeOverviewBpmSurface(show = latestShow, options = {}) {
  const surface = document.createElement("div");
  surface.className = options.className || "overview-bpm-surface";
  const summary = makeBpmClockSummary("BPM Color Rotation", formatBpmStatus(show));
  summary.classList.add("overview-bpm-summary");

  const editor = document.createElement("div");
  editor.className = "overview-bpm-editor";
  const label = document.createElement("label");
  label.className = "overview-bpm-input-field";
  const labelText = document.createElement("span");
  labelText.textContent = "BPM";
  const input = document.createElement("input");
  input.type = "number";
  input.inputMode = "decimal";
  input.min = "40";
  input.max = "240";
  input.step = "0.1";
  input.value = String(show?.bpm || bpmInput?.value || 125);
  label.append(labelText, input);
  const slider = document.createElement("input");
  slider.className = "overview-bpm-slider";
  slider.type = "range";
  slider.min = "40";
  slider.max = "240";
  slider.step = "0.1";
  slider.value = input.value;
  const syncOverviewBpm = (value, send = false) => {
    const bpm = Math.max(40, Math.min(240, Number(value) || 125));
    const display = Number.isInteger(bpm) ? String(bpm) : bpm.toFixed(1).replace(/\.0$/, "");
    input.value = display;
    slider.value = String(bpm);
    setBpmUiValue(display);
    if (send) sendCommand({ command: "bpm_update", bpm: display, division: selectedDivision });
  };
  input.addEventListener("input", () => syncOverviewBpm(input.value, false));
  input.addEventListener("change", () => syncOverviewBpm(input.value, true));
  slider.addEventListener("input", () => syncOverviewBpm(slider.value, false));
  slider.addEventListener("change", () => syncOverviewBpm(slider.value, true));
  editor.append(label, slider);

  const actions = document.createElement("div");
  actions.className = "overview-bpm-actions";
  [
    ["-1", () => nudgeBpm(-1), "down"],
    ["+1", () => nudgeBpm(1), "up"],
    [show.bpm_follow_now_playing ? "Follow On" : "Follow", () => sendCommand({ command: "bpm_follow", enabled: !Boolean(latestShow?.bpm_follow_now_playing) }), "follow"],
    ["Start", () => sendCommand({ command: "bpm_start", bpm: bpmInput.value, division: selectedDivision }), "start"],
    ["Resync", () => sendCommand({ command: "bpm_resync", bpm: bpmInput.value, division: selectedDivision }), "resync"],
    ["Stop", () => sendCommand({ command: "bpm_stop" }), "stop"],
  ].forEach(([label, handler, key]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.classList.toggle("active", key === "follow" && Boolean(show.bpm_follow_now_playing));
    button.classList.toggle("active", key === "start" && Boolean(show.bpm_running));
    button.classList.toggle("danger", key === "stop");
    button.addEventListener("click", handler);
    actions.append(button);
  });

  const divisions = makeBpmDivisionGrid({
    className: "overview-bpm-division-grid",
    buttonClass: "overview-bpm-division-button",
    divisions: overviewBpmDivisions(),
    onPick: updateAppBpmDivision,
  });
  surface.append(summary, editor, makeBpmRotationChecks({ className: "overview-bpm-rotation", autoSave: true }), actions, divisions);
  return surface;
}

function nowPlayingModeLabel(mode) {
  if (mode === "cdj" || !mode) return "CDJ Beatlink";
  if (mode === "vinyl") return "Vinyl";
  if (mode === "studio") return "Studio";
  if (mode === "videogame") return "Videogames";
  if (mode === "spotify") return "Spotify";
  return `${mode} mode`;
}

function createOverviewNowPlayingInput(name, label, value) {
  const field = document.createElement("label");
  field.className = "overview-now-playing-field";
  const span = document.createElement("span");
  span.textContent = label;
  const input = document.createElement("input");
  input.name = name;
  input.type = "text";
  input.autocomplete = "off";
  input.value = value || "";
  field.append(span, input);
  return field;
}

async function saveOverviewManualModeText(form, statusEl) {
  const data = new FormData(form);
  const payload = {
    vinyl_track_text: data.get("vinyl_track_text") || "Record Playing",
    studio_track_text: data.get("studio_track_text") || "NO TALKING STUDIO",
    videogame_track_text: data.get("videogame_track_text") || "Ravenswatch",
  };
  try {
    statusEl.textContent = "Saving text...";
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    manualModeDirty = false;
    statusEl.textContent = result.message || "Now Playing text saved.";
    renderManualModeForm();
    renderSettingsForm();
      renderObsSettingsForm();
    if (result.state) renderShowState(result.state);
    await loadStatus({ full: true, force: true });
  } catch (error) {
    statusEl.textContent = String(error.message || error);
  }
}

async function saveOverviewArtworkOptionPayload(payload, statusEl) {
  if (statusEl) statusEl.textContent = "Saving album colors...";
  await saveArtworkOptionPayload(payload, { statusEl });
}

function makeOverviewAlbumColorControls(status) {
  const panel = document.createElement("div");
  panel.className = "overview-album-colors";
  const header = document.createElement("div");
  header.className = "overview-album-colors-header";
  const title = document.createElement("strong");
  title.textContent = "Album Colors";
  const state = document.createElement("span");
  state.textContent = appSettings?.use_artwork_palette ? "Auto ON" : "Auto OFF";
  state.classList.toggle("active", Boolean(appSettings?.use_artwork_palette));
  header.append(title, state);

  const meta = document.createElement("small");
  meta.className = "overview-album-colors-status";
  meta.textContent = status?.artwork?.status || "Palette waits for current artwork.";

  const actions = document.createElement("div");
  actions.className = "overview-album-colors-actions";
  [
    [
      appSettings?.use_artwork_palette ? "Auto On" : "Auto Off",
      () => saveOverviewArtworkOptionPayload({ use_artwork_palette: !Boolean(appSettings?.use_artwork_palette) }, meta),
      Boolean(appSettings?.use_artwork_palette),
    ],
    ["Apply", () => refreshPalette(true, { statusEl: meta, previewEl: null }), false],
    ["Refresh", () => refreshPalette(false, { statusEl: meta, previewEl: null }), false],
  ].forEach(([label, handler, active]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.className = "overview-album-color-button";
    button.classList.toggle("active", Boolean(active));
    button.addEventListener("click", handler);
    actions.append(button);
  });

  panel.append(header, actions, meta);
  return panel;
}

function renderOverviewNowPlaying(status) {
  if (!overviewNowPlaying) return;
  const active = document.activeElement;
  if (active && overviewNowPlaying.contains(active) && ["INPUT", "TEXTAREA", "SELECT"].includes(active.tagName)) return;
  const show = status?.show || latestShow || {};
  const blt = status?.blt || {};
  const track = blt.context || {};
  const mode = show.manual_mode || "cdj";
  const isCdjMode = mode === "cdj";
  const hasTrack = Boolean(isCdjMode && blt.ok && (track.title || track.artist || track.full_track));
  const currentText = hasTrack
    ? track.full_track || track.title || "BeatLink track loaded"
    : isCdjMode
      ? blt.status || "Waiting for BeatLink"
      : manualModeText(mode) || nowPlayingModeLabel(mode);
  const metaText = hasTrack
    ? [track.artist, track.bpm ? `${track.bpm} BPM` : "", track.player || track.player_number].filter(Boolean).join(" / ")
    : isCdjMode
      ? "CDJ Beatlink"
      : "Manual mode";

  overviewNowPlaying.replaceChildren();
  const summary = document.createElement("div");
  summary.className = "overview-now-playing-summary";
  const modeCard = document.createElement("div");
  const modeLabel = document.createElement("span");
  modeLabel.textContent = "Mode";
  const modeValue = document.createElement("strong");
  modeValue.textContent = nowPlayingModeLabel(mode);
  modeCard.append(modeLabel, modeValue);
  const displayCard = document.createElement("div");
  const displayLabel = document.createElement("span");
  displayLabel.textContent = "Display";
  const displayValue = document.createElement("strong");
  displayValue.textContent = currentText;
  const displayMeta = document.createElement("small");
  displayMeta.textContent = metaText || "-";
  displayCard.append(displayLabel, displayValue, displayMeta);
  summary.append(modeCard, displayCard);

  const actions = document.createElement("div");
  actions.className = "overview-now-playing-buttons";
  [
    ["CDJ Beatlink", "resume", isCdjMode],
    ["Vinyl", "vinyl", mode === "vinyl"],
    ["Studio", "studio", mode === "studio"],
    ["Videogames", "videogame", mode === "videogame"],
    ["Safe Reset", "safe_reset", false, true],
  ].forEach(([label, command, activeMode, danger]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.className = "overview-now-playing-button";
    button.classList.toggle("active", Boolean(activeMode));
    button.classList.toggle("danger", Boolean(danger));
    button.addEventListener("click", () => sendCommand({ command }));
    actions.append(button);
  });
  const pageButton = document.createElement("button");
  pageButton.type = "button";
  pageButton.textContent = "Open Page";
  pageButton.className = "overview-now-playing-button page";
  pageButton.addEventListener("click", () => activateSection("nowPlayingSection"));
  actions.append(pageButton);

  const settings = document.createElement("details");
  settings.className = "overview-card-settings";
  const settingsSummary = document.createElement("summary");
  settingsSummary.textContent = "Text";
  const form = document.createElement("form");
  form.className = "overview-now-playing-form";
  form.append(
    createOverviewNowPlayingInput("vinyl_track_text", "Vinyl", appSettings?.vinyl_track_text || "Record Playing"),
    createOverviewNowPlayingInput("studio_track_text", "Studio", appSettings?.studio_track_text || "NO TALKING STUDIO"),
    createOverviewNowPlayingInput("videogame_track_text", "Videogames", appSettings?.videogame_track_text || "Ravenswatch"),
  );
  const save = document.createElement("button");
  save.type = "button";
  save.textContent = "Save Text";
  const link = document.createElement("a");
  link.className = "overview-settings-link";
  link.href = "#nowPlayingSection";
  link.dataset.sectionLink = "nowPlayingSection";
  link.textContent = "Open Page";
  link.addEventListener("click", (event) => {
    event.preventDefault();
    activateSection("nowPlayingSection");
  });
  const statusLine = document.createElement("small");
  statusLine.className = "overview-now-playing-status";
  statusLine.textContent = "Text saves into Settings.";
  save.addEventListener("click", () => saveOverviewManualModeText(form, statusLine));
  form.append(save, link, statusLine);
  settings.append(settingsSummary, form);
  const opacity = document.createElement("div");
  renderNowPlayingOpacityControl(opacity, true);
  overviewNowPlaying.append(summary, actions, opacity, makeOverviewAlbumColorControls(status), makeOverviewBpmSurface(show, { className: "overview-now-playing-bpm" }), settings);
}

function visualLayerNumber(item) {
  const index = Math.max(1, Number(item?.index || 1));
  const explicit = Number(item?.layer);
  return Number.isFinite(explicit) && explicit > 0
    ? explicit
    : Math.floor((index - 1) / VISUAL_CLIPS_PER_LAYER) + 1;
}

function visualClipNumber(item) {
  const index = Math.max(1, Number(item?.index || 1));
  const explicit = Number(item?.clip);
  return Number.isFinite(explicit) && explicit >= 0
    ? explicit
    : ((index - 1) % VISUAL_CLIPS_PER_LAYER) + 1;
}

function isVisualOffItem(item, clip = visualClipNumber(item)) {
  return clip === 0 || String(item?.kind || "").toLowerCase() === "off";
}

function visualClipCoordinateLabel(layer, clip) {
  return clip === 0 ? `L${layer} X` : `L${layer} C${clip}`;
}

function visualClipButtonLabel(item, layer, clip) {
  return isVisualOffItem(item, clip) ? "X" : visualClipCoordinateLabel(layer, clip);
}


function defaultVisualOffControl(layer) {
  return {
    id: `visual_l${layer}_off`,
    index: 0,
    layer,
    clip: 0,
    kind: "off",
    name: `Layer ${layer} Clips Off`,
    label: `L${layer} X`,
    address: "",
  };
}

function visualControlsWithLayerOff(items = appSettings?.visual_controls || []) {
  const controls = [...(items || [])];
  const ids = new Set(controls.map((item) => String(item?.id || "")));
  for (let layer = 1; layer <= VISUAL_LAYER_COUNT; layer += 1) {
    const offId = `visual_l${layer}_off`;
    const hasOff = ids.has(offId) || controls.some((item) => visualLayerNumber(item) === layer && isVisualOffItem(item));
    if (!hasOff) controls.unshift(defaultVisualOffControl(layer));
  }
  return controls;
}

function visualClipTitle(item, layer, clip, isPreview) {
  const cueTitle = cueButtonTitle("visual", isPreview);
  const isOff = isVisualOffItem(item, clip);
  const defaultName = isOff ? `Layer ${layer} Clips Off` : `Layer ${layer} Clip ${clip}`;
  const name = String(item?.name || item?.label || "").trim();
  const editHint = item ? "Right-click, long-press, or Shift-click to edit OSC" : "";
  return [defaultName, name && name !== defaultName ? name : "", cueTitle, editHint]
    .filter(Boolean)
    .join(" - ");
}

function visualItemsByLayer(items) {
  const byLayer = new Map();
  for (const item of items || []) {
    byLayer.set(`${visualLayerNumber(item)}:${visualClipNumber(item)}`, item);
  }
  return byLayer;
}

function selectedVisualByLayer(show = latestShow) {
  const selected = {};
  const source = show?.last_visual_by_layer || {};
  for (let layer = 1; layer <= VISUAL_LAYER_COUNT; layer += 1) {
    selected[String(layer)] = source[String(layer)] || "";
  }
  const fallback = show?.last_visual_button || "";
  const fallbackItem = visualItemById(fallback);
  if (fallbackItem) {
    const layer = visualLayerNumber(fallbackItem);
    if (layer) selected[String(layer)] = selected[String(layer)] || fallback;
  }
  return selected;
}

function visualItemById(id) {
  const itemId = String(id || "");
  if (!itemId) return null;
  return visualControlsWithLayerOff().find((item) => item.id === itemId) || null;
}

function rememberVisualSelection(id) {
  const item = visualItemById(id);
  if (!item) return;
  const layer = visualLayerNumber(item);
  if (!layer) return;
  const current = latestShow || {};
  const byLayer = { ...(current.last_visual_by_layer || {}) };
  byLayer[String(layer)] = item.id;
  latestShow = {
    ...current,
    last_visual_button: item.id,
    last_visual_by_layer: byLayer,
  };
  renderOverviewVisuals();
  renderVisualControls();
}
function getVisualOscAddressInput(id) {
  if (!visualsOscForm) return null;
  const control = visualsOscForm.elements.namedItem(`visual_address_${id}`);
  return control && typeof control.focus === "function" ? control : null;
}

function highlightQuickEditTarget(row) {
  if (!row) return;
  row.classList.remove("quick-osc-target");
  void row.offsetWidth;
  row.classList.add("quick-osc-target");
  window.setTimeout(() => row.classList.remove("quick-osc-target"), 2600);
}

function quickEditClickMode(event, button) {
  if (button.dataset.quickOscEditHandled === "true") {
    delete button.dataset.quickOscEditHandled;
    event.preventDefault();
    event.stopPropagation();
    return "handled";
  }
  if (event.shiftKey || event.altKey) {
    event.preventDefault();
    event.stopPropagation();
    return "open";
  }
  return "";
}

function attachQuickEditShortcut(button, openEditor) {
  let longPressTimer = 0;
  let pressStart = null;

  const clearLongPress = () => {
    if (longPressTimer) window.clearTimeout(longPressTimer);
    longPressTimer = 0;
    pressStart = null;
  };

  const openFromGesture = (event, consumeNextClick = false) => {
    event.preventDefault();
    event.stopPropagation();
    if (consumeNextClick) {
      button.dataset.quickOscEditHandled = "true";
      window.setTimeout(() => {
        if (button.dataset.quickOscEditHandled === "true") delete button.dataset.quickOscEditHandled;
      }, 1600);
    }
    openEditor();
  };

  button.addEventListener("contextmenu", (event) => {
    const consumeNextClick = button.dataset.quickOscEditHandled === "true" || (event.pointerType && event.pointerType !== "mouse");
    openFromGesture(event, Boolean(consumeNextClick));
    if (!consumeNextClick) delete button.dataset.quickOscEditHandled;
  });
  button.addEventListener("pointerdown", (event) => {
    if (event.pointerType === "mouse" || event.button !== 0) return;
    pressStart = { x: event.clientX, y: event.clientY };
    longPressTimer = window.setTimeout(() => openFromGesture(event, true), 650);
  });
  button.addEventListener("pointermove", (event) => {
    if (!longPressTimer || !pressStart) return;
    if (Math.hypot(event.clientX - pressStart.x, event.clientY - pressStart.y) > 12) clearLongPress();
  });
  ["pointerup", "pointercancel", "pointerleave"].forEach((type) => {
    button.addEventListener(type, clearLongPress);
  });
}

function openVisualClipOscEditor(item, layer, clip) {
  if (!item || !visualsOscForm) return false;
  activateSection("visualsSection", { scroll: false });
  const panel = visualsOscForm.closest("details");
  if (panel) panel.open = true;
  if (!visualsOscForm.children.length && appSettings) renderVisualsOscForm();
  setActiveVisualOscSection(isVisualOffItem(item, clip) ? "off" : "buttons");

  const address = getVisualOscAddressInput(item.id);
  if (!address) {
    if (visualsOscStatus) visualsOscStatus.textContent = `Could not find ${visualClipCoordinateLabel(layer, clip)} in Visuals OSC.`;
    return false;
  }

  const row = address.closest(".visual-setting-row") || address.closest(".osc-address-cell") || address;
  const label = visualClipCoordinateLabel(layer, clip);
  if (visualsOscStatus) visualsOscStatus.textContent = `Editing ${label} OSC address. Save Visuals OSC when finished.`;

  window.requestAnimationFrame(() => {
    row.scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
    window.setTimeout(() => {
      try {
        address.focus({ preventScroll: true });
      } catch (_error) {
        address.focus();
      }
      if (typeof address.select === "function") address.select();
      highlightQuickEditTarget(row);
    }, 160);
  });
  return true;
}

function visualClipClickQuickEditMode(event, button) {
  return quickEditClickMode(event, button);
}

function attachVisualClipOscShortcuts(button, item, layer, clip) {
  attachQuickEditShortcut(button, () => openVisualClipOscEditor(item, layer, clip));
}

function handleQuickEditTriggerClick(event, button, openEditor, normalAction) {
  const quickEditMode = quickEditClickMode(event, button);
  if (quickEditMode === "handled") return;
  if (quickEditMode === "open") {
    openEditor();
    return;
  }
  normalAction();
}

function lookEditCard(name) {
  if (!presetLinks) return null;
  return Array.from(presetLinks.querySelectorAll(".preset-link-card")).find((card) => {
    const input = card.querySelector(".look-card-name");
    return input?.dataset.originalName === name || input?.value === name;
  }) || null;
}

function openLookQuickEditor(name) {
  if (!name || !presetLinks) return false;
  activateSection("looksSection", { scroll: false });
  const panel = presetLinks.closest("details");
  if (panel) panel.open = true;
  if (!presetLinks.children.length && appSettings && presetData) renderPresetLinks();

  const card = lookEditCard(name);
  if (!card) {
    if (saveLookStatus) saveLookStatus.textContent = `Could not find ${name} in look settings.`;
    return false;
  }

  if (saveLookStatus) saveLookStatus.textContent = `Editing ${name}. Save when finished.`;
  window.requestAnimationFrame(() => {
    card.scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
    window.setTimeout(() => {
      const input = card.querySelector(".look-card-name");
      try {
        input?.focus({ preventScroll: true });
      } catch (_error) {
        input?.focus();
      }
      if (typeof input?.select === "function") input.select();
      highlightQuickEditTarget(card);
    }, 160);
  });
  return true;
}

function cameraOscSectionKey(groupKey) {
  return groupKey === "scene" ? "scenes" : groupKey;
}

function cameraQuickEditLabel(groupKey, item) {
  const groupLabel = groupKey === "main_box" ? "Main Cam" : groupKey === "pip_box" ? "PIP Cam" : groupKey === "background" ? "BG Cam" : groupKey === "visuals_cams" ? "Visuals Cam" : "Scene";
  return `${groupLabel}: ${item?.label || item?.name || item?.id || "Camera"}`;
}

function getCameraOscAddressInput(id) {
  if (!camerasOscForm) return null;
  const control = camerasOscForm.elements.namedItem(`camera_address_${id}`);
  return control && typeof control.focus === "function" ? control : null;
}

function openCameraOscEditor(groupKey, item) {
  if (!item || !camerasOscForm) return false;
  activateSection("camerasSection", { scroll: false });
  const panel = camerasOscForm.closest("details");
  if (panel) panel.open = true;
  if (!camerasOscForm.children.length && appSettings) renderCamerasOscForm();
  setActiveCameraOscSection(cameraOscSectionKey(groupKey));

  const address = getCameraOscAddressInput(item.id);
  if (!address) {
    if (camerasOscStatus) camerasOscStatus.textContent = `Could not find ${cameraQuickEditLabel(groupKey, item)} in Camera OSC.`;
    return false;
  }

  const row = address.closest(".camera-setting-row") || address.closest(".osc-address-cell") || address;
  const label = cameraQuickEditLabel(groupKey, item);
  if (camerasOscStatus) camerasOscStatus.textContent = `Editing ${label} OSC address. Save Camera OSC when finished.`;

  window.requestAnimationFrame(() => {
    row.scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
    window.setTimeout(() => {
      try {
        address.focus({ preventScroll: true });
      } catch (_error) {
        address.focus();
      }
      if (typeof address.select === "function") address.select();
      highlightQuickEditTarget(row);
    }, 160);
  });
  return true;
}

function createVisualClipButton(item, layer, clip, options = {}) {
  const isOverview = options.variant === "overview";
  const staged = options.staged || "";
  const selected = options.selected || "";
  const selectedByLayer = options.selectedByLayer || {};
  const isOff = isVisualOffItem(item, clip);
  const selectedForLayer = selectedByLayer[String(layer)] || "";
  const isActive = Boolean(item && (selectedForLayer ? selectedForLayer === item.id : selected === item.id));
  const isPreview = Boolean(item && staged === item.id);
  const button = document.createElement("button");
  button.type = "button";
  button.className = isOverview
    ? "overview-cue-button visual-cue visual-clip-button"
    : "visual-button visual-clip-button";
  button.classList.toggle("visual-off-button", isOff);
  button.classList.toggle("active", isActive);
  button.classList.toggle("preview", isPreview);
  button.disabled = !item;
  button.ariaPressed = String(isPreview || isActive);
  button.ariaLabel = item
    ? `${isOff ? "Turn off" : "Trigger"} Layer ${layer}${isOff ? " clips" : ` Clip ${clip}`}; edit OSC address from context menu or long press`
    : `Layer ${layer} ${isOff ? "off" : `Clip ${clip}`} unavailable`;
  button.title = item ? visualClipTitle(item, layer, clip, isPreview) : `Layer ${layer} ${isOff ? "Off" : `Clip ${clip}`}`;
  button.textContent = visualClipButtonLabel(item, layer, clip);
  if (item) {
    button.dataset.visualId = item.id;
    button.addEventListener("click", (event) => {
      const quickEditMode = visualClipClickQuickEditMode(event, button);
      if (quickEditMode === "handled") return;
      if (quickEditMode === "open") {
        openVisualClipOscEditor(item, layer, clip);
        return;
      }
      dispatchVisualCue(item.id);
    });
    attachVisualClipOscShortcuts(button, item, layer, clip);
  }
  return button;
}

function renderVisualLayerGrid(container, items, options = {}) {
  const isOverview = options.variant === "overview";
  container.classList.toggle("overview-visual-layers", isOverview);
  container.classList.toggle("visual-layer-stack", !isOverview);
  container.replaceChildren();
  const byLayer = visualItemsByLayer(items);

  const ruler = document.createElement("div");
  ruler.className = "visual-column-ruler";
  const corner = document.createElement("span");
  corner.textContent = "Clip";
  ruler.append(corner);
  const offColumn = document.createElement("span");
  offColumn.textContent = "X";
  ruler.append(offColumn);
  for (let clip = 1; clip <= VISUAL_CLIPS_PER_LAYER; clip += 1) {
    const column = document.createElement("span");
    column.textContent = String(clip);
    ruler.append(column);
  }
  container.append(ruler);

  for (let layer = VISUAL_LAYER_COUNT; layer >= 1; layer -= 1) {
    const row = document.createElement("div");
    row.className = "visual-layer-row";
    const label = document.createElement("strong");
    label.className = "visual-layer-label";
    label.textContent = `Layer ${layer}`;
    row.append(label);
    row.append(createVisualClipButton(byLayer.get(`${layer}:0`), layer, 0, options));
    for (let clip = 1; clip <= VISUAL_CLIPS_PER_LAYER; clip += 1) {
      row.append(createVisualClipButton(byLayer.get(`${layer}:${clip}`), layer, clip, options));
    }
    container.append(row);
  }
}

function renderOverviewVisuals() {
  if (!overviewVisualGrid || !appSettings) return;
  renderVisualLayerGrid(overviewVisualGrid, visualControlsWithLayerOff(), {
    variant: "overview",
    selected: latestShow?.last_visual_button || "",
    selectedByLayer: selectedVisualByLayer(latestShow),
    staged: stagedPerformanceCue.visual_id || "",
  });
}
function renderOverviewGenerator() {
  if (!overviewGeneratorGrid || !appSettings) return;
  overviewGeneratorGrid.replaceChildren();
  const current = currentGenerativeVisual();
  const presetIds = Object.keys(generativePresetOptions()).slice(0, 4);
  const summary = document.createElement("div");
  summary.className = "overview-generator-summary";
  summary.textContent = `Generator: ${generativePresetOptions()[current.preset]?.name || current.preset || "Ready"}`;
  overviewGeneratorGrid.append(summary);
  for (const presetId of presetIds) {
    const preset = generativePresetOptions()[presetId];
    const button = document.createElement("button");
    button.type = "button";
    button.className = "overview-cue-button generator-cue";
    const staged = stagedPerformanceCue.generator_preset === presetId;
    button.classList.toggle("active", current.preset === presetId && current.enabled !== false && !current.blackout);
    button.classList.toggle("preview", staged);
    button.textContent = preset?.name || presetId;
    button.title = cueButtonTitle("generator", staged);
    button.addEventListener("click", () => dispatchGeneratorCue(presetId));
    overviewGeneratorGrid.append(button);
  }
  const stop = document.createElement("button");
  stop.type = "button";
  stop.textContent = "Stop Generator";
  stop.className = "overview-cue-button generator-cue danger";
  stop.addEventListener("click", () => sendCommand({ command: "generative_visual_stop" }));
  overviewGeneratorGrid.append(stop);
}

function renderOverviewCameras() {
  if (!overviewCameraGrid || !appSettings) return;
  overviewCameraGrid.replaceChildren();
  const cameraConfig = appSettings.camera_controls || {};
  const selected = latestShow?.last_camera_buttons || {};
  const groups = [
    ["Main", "main_box", cameraConfig.groups?.main_box || []],
    ["PIP", "pip_box", cameraConfig.groups?.pip_box || []],
    ["BG", "background", cameraConfig.groups?.background || []],
    ["Visuals", "visuals_cams", cameraConfig.groups?.visuals_cams || []],
    ["Scenes", "scene", cameraConfig.scenes || []],
  ];
  for (const [label, groupKey, items] of groups) {
    const group = document.createElement("div");
    group.className = "overview-camera-group";
    const title = document.createElement("strong");
    title.textContent = label;
    const grid = document.createElement("div");
    grid.className = "overview-button-grid compact";
    for (const item of items) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = item.label || item.name || item.id;
      button.className = groupKey === "scene" ? "overview-cue-button scene-cue" : "overview-cue-button camera-cue";
      const active = groupKey === "scene" ? selected.scene === item.id : selected[groupKey] === item.id;
      const staged = groupKey === "scene" ? stagedPerformanceCue.scene_id === item.id : stagedPerformanceCue[`${groupKey}_id`] === item.id;
      button.classList.toggle("active", active);
      button.classList.toggle("preview", staged);
      button.title = `${cueButtonTitle(groupKey === "scene" ? "scene" : "camera", staged)} - Right-click, long-press, or Shift-click to edit OSC`;
      button.addEventListener("click", (event) => handleQuickEditTriggerClick(event, button, () => openCameraOscEditor(groupKey, item), () => dispatchCameraCue(groupKey, item.id)));
      attachQuickEditShortcut(button, () => openCameraOscEditor(groupKey, item));
      grid.append(button);
    }
    group.append(title, grid);
    overviewCameraGrid.append(group);
  }
  for (const groupKey of ["main_box", "pip_box", "background", "visuals_cams"]) {
    const mixGroup = document.createElement("div");
    mixGroup.className = "overview-camera-group overview-camera-opacity-group";
    const mixTitle = document.createElement("strong");
    mixTitle.textContent = cameraOpacityShortLabel(groupKey);
    const mixControl = document.createElement("div");
    renderCameraOpacityControl(groupKey, mixControl, true);
    mixGroup.append(mixTitle, mixControl);
    overviewCameraGrid.append(mixGroup);
  }
}

function selectedCameraLabel(groupKey) {
  const selected = latestShow?.last_camera_buttons || {};
  const cameraConfig = appSettings?.camera_controls || {};
  if (groupKey === "scene") return optionLabel(cameraConfig.scenes, selected.scene, "-");
  return optionLabel(cameraConfig.groups?.[groupKey], selected[groupKey], "-");
}

function sequenceStatusLabel() {
  if (showSequenceRunning) return showSequencePaused ? "Paused" : "Playing";
  return manualOverrideUntil > Date.now() ? "Manual override" : "Ready";
}

function lightPreviewParts(show, compact = false) {
  const outputs = show?.outputs || [];
  const byKey = (key) => outputs.find((output) => output.key === key) || {};
  const primary = byKey("color1");
  const secondary = byKey("color2");
  const accent = byKey("strobe_color");
  const motion = Math.round(Number(byKey("motion").value || 0) * 100);
  const saturation = Math.round(Number(byKey("saturation").value ?? 1) * 100);
  const brightness = Math.round(Number(byKey("brightness").value ?? 1) * 100);
  const fx = Math.round(Number(byKey("fx").value || 0) * 100);
  const pulse = Math.round(Number(byKey("pulse").value || 0) * 100);
  const primaryHex = primary.hex || "#4b3dff";
  const secondaryHex = secondary.hex || "#ff2bd6";
  const accentHex = accent.hex || "#7b2cff";

  const stage = document.createElement("div");
  stage.className = compact ? "rail-light-preview compact-light-preview" : "rail-light-preview";
  stage.style.setProperty("--primary", primaryHex);
  stage.style.setProperty("--secondary", secondaryHex);
  stage.style.setProperty("--accent-color", accentHex);
  stage.style.setProperty("--brightness-level", String(Math.max(0.15, brightness / 100)));
  stage.style.setProperty("--saturation-level", String(Math.max(35, saturation) / 100));
  stage.style.setProperty("--motion-level", `${Math.max(8, motion)}%`);
  stage.style.setProperty("--pulse-level", `${Math.max(8, pulse)}%`);
  stage.style.setProperty("--fx-level", `${Math.max(8, fx)}%`);

  const beams = document.createElement("div");
  beams.className = "rail-light-beams";
  const fixtures = document.createElement("div");
  fixtures.className = "rail-fixture-row";
  [primaryHex, secondaryHex, accentHex, primaryHex, secondaryHex].forEach((hex, index) => {
    const fixture = document.createElement("i");
    fixture.style.setProperty("--fixture-color", hex);
    fixture.style.setProperty("--fixture-delay", `${index * 12}%`);
    fixtures.append(fixture);
  });
  const title = document.createElement("strong");
  title.textContent = `${primary.color || "color 1"} / ${secondary.color || "color 2"} / ${accent.color || "color 3"}`;
  const wash = document.createElement("div");
  wash.className = "rail-light-wash";
  stage.append(beams, fixtures, title, wash);

  const metrics = document.createElement("div");
  metrics.className = compact ? "rail-light-metrics compact-light-metrics" : "rail-light-metrics";
  [
    ["Bright", brightness],
    ["Sat", saturation],
    ["Motion", motion],
    ["FX", fx],
    ["Pulse", pulse],
  ].forEach(([label, value]) => {
    const item = document.createElement("span");
    item.innerHTML = `<small>${label}</small><b>${value}%</b>`;
    metrics.append(item);
  });

  return { stage, metrics };
}

function lightOutputSummary(show) {
  const outputs = show?.outputs || [];
  const byKey = (key) => outputs.find((output) => output.key === key) || {};
  const primary = byKey("color1");
  const secondary = byKey("color2");
  const accent = byKey("strobe_color");
  const motion = Math.round(Number(byKey("motion").value || 0) * 100);
  const saturation = Math.round(Number(byKey("saturation").value ?? 1) * 100);
  const brightness = Math.round(Number(byKey("brightness").value ?? 1) * 100);
  const fx = Math.round(Number(byKey("fx").value || 0) * 100);
  const pulse = Math.round(Number(byKey("pulse").value || 0) * 100);
  return {
    colors: [
      { role: "Color 1", name: primary.color || "color 1", hex: primary.hex || "#4b3dff" },
      { role: "Color 2", name: secondary.color || "color 2", hex: secondary.hex || "#ff2bd6" },
      { role: "Color 3", name: accent.color || "color 3", hex: accent.hex || "#7b2cff" },
    ],
    levels: [
      ["Bright", brightness],
      ["Sat", saturation],
      ["Motion", motion],
      ["FX", fx],
      ["Pulse", pulse],
    ],
  };
}

function createActiveLightOutput(show) {
  const summary = lightOutputSummary(show);
  const root = document.createElement("div");
  root.className = "active-light-output";
  root.style.setProperty("--primary", summary.colors[0].hex);
  root.style.setProperty("--secondary", summary.colors[1].hex);
  root.style.setProperty("--accent-color", summary.colors[2].hex);

  const swatches = document.createElement("div");
  swatches.className = "active-light-swatches";
  summary.colors.forEach((color) => {
    const swatch = document.createElement("div");
    swatch.className = "active-light-swatch";
    swatch.style.setProperty("--swatch-color", color.hex);
    const chip = document.createElement("i");
    const copy = document.createElement("span");
    copy.innerHTML = `<small>${color.role}</small><b>${color.name}</b>`;
    swatch.append(chip, copy);
    swatches.append(swatch);
  });

  const meter = document.createElement("div");
  meter.className = "active-light-meter";
  meter.setAttribute("aria-hidden", "true");
  summary.colors.forEach((color) => {
    const segment = document.createElement("i");
    segment.style.setProperty("--segment-color", color.hex);
    meter.append(segment);
  });

  const levels = document.createElement("div");
  levels.className = "active-light-levels";
  summary.levels.forEach(([label, value]) => {
    const item = document.createElement("span");
    item.innerHTML = `<small>${label}</small><b>${value}%</b>`;
    levels.append(item);
  });

  root.append(swatches, meter, levels);
  return root;
}

function renderActiveMomentStrip(show) {
  if (!activeMomentStrip || !appSettings) return;
  const generator = show?.generative_visual || currentGenerativeVisual();
  const generatorName = generativePresetOptions()[generator?.preset]?.name || generator?.preset || "Ready";
  const staged = stagedPerformanceCue;
  const visualLabel = staged.visual_id
    ? `Next: ${optionLabel(appSettings.visual_controls, staged.visual_id, staged.visual_id)}`
    : optionLabel(appSettings.visual_controls, show?.last_visual_button, "-");
  const stagedCamId = staged.scene_id || staged.main_box_id || staged.pip_box_id || staged.background_id || staged.visuals_cams_id || "";
  const stagedCamLabel = staged.scene_id
    ? optionLabel(appSettings.camera_controls?.scenes, staged.scene_id, staged.scene_id)
    : staged.main_box_id
      ? optionLabel(appSettings.camera_controls?.groups?.main_box, staged.main_box_id, staged.main_box_id)
      : staged.pip_box_id
        ? optionLabel(appSettings.camera_controls?.groups?.pip_box, staged.pip_box_id, staged.pip_box_id)
        : staged.background_id
          ? optionLabel(appSettings.camera_controls?.groups?.background, staged.background_id, staged.background_id)
          : optionLabel(appSettings.camera_controls?.groups?.visuals_cams, staged.visuals_cams_id, staged.visuals_cams_id);
  const cameraScene = stagedCamId ? `Next: ${stagedCamLabel}` : selectedCameraLabel("scene");
  const stagedGenerator = staged.generator_preset ? generativePresetOptions()[staged.generator_preset]?.name || staged.generator_preset : "";
  const items = [
    ["Visual", visualLabel, "visual"],
    ["Cam", cameraScene, "cam"],
    ["Generator", stagedGenerator ? `Next: ${stagedGenerator}` : generator?.blackout || generator?.enabled === false ? "Stopped" : generatorName, "generator"],
    ["Sequence", `${activeShowSequence} - ${sequenceStatusLabel()}`, "sequence"],
  ];
  activeMomentStrip.replaceChildren();
  const activeItem = document.createElement("div");
  activeItem.className = "active-moment-item active-moment-look-state active-moment-active-look";
  activeItem.append(makeLookStatePanel("Active", activePerformanceName() || "", { mode: "active", show }));
  const previewItem = document.createElement("div");
  previewItem.className = "active-moment-item active-moment-look-state active-moment-preview-look";
  previewItem.append(makeLookStatePanel("Next", stagedPerformanceLookName, { mode: "preview", placeholder: stagedPerformanceLookName || "Pick a look" }));
  activeMomentStrip.append(activeItem, previewItem);
  items.forEach(([label, value, type]) => {
    const item = document.createElement("div");
    item.className = `active-moment-item active-moment-status active-moment-${type}`;
    const small = document.createElement("span");
    small.textContent = label;
    const strong = document.createElement("strong");
    strong.textContent = value;
    item.append(small, strong);
    activeMomentStrip.append(item);
  });
}

function activeShowSequenceConfig() {
  const sequences = appSettings?.show_sequences || {};
  return sequences[activeShowSequence] || sequences["Main Show"] || { name: activeShowSequence || "Main Show", loop: false, steps: [] };
}

function overviewSequenceSteps() {
  const sequence = activeShowSequenceConfig();
  return Array.isArray(sequence.steps) ? sequence.steps.filter(sequenceStepHasAction) : [];
}

async function toggleOverviewSequenceLoop() {
  if (!appSettings) return;
  const sequence = activeShowSequenceConfig();
  const sequenceName = sequence.name || activeShowSequence || "Main Show";
  const sequences = { ...(appSettings.show_sequences || {}) };
  sequences[sequenceName] = {
    ...sequence,
    name: sequenceName,
    loop: !Boolean(sequence.loop),
    steps: Array.isArray(sequence.steps) ? sequence.steps : [],
  };
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ show_sequences: sequences }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    if (showSequenceLoop) showSequenceLoop.checked = Boolean(sequences[sequenceName].loop);
    showToast(`${sequenceName} loop ${sequences[sequenceName].loop ? "on" : "off"}`);
    renderOverviewSequence();
    await loadStatus();
  } catch (error) {
    showToast(String(error.message || error), true);
  }
}

async function triggerOverviewSequenceCue(index) {
  const steps = overviewSequenceSteps();
  if (!steps.length) {
    setSequenceTransport("Stopped", "No saved sequence cues are ready to trigger.");
    renderOverviewSequence();
    return;
  }
  clearSequenceTimer();
  showSequenceRunning = true;
  showSequencePaused = true;
  showSequenceStartedAt = 0;
  await triggerSequenceStep(index, steps, "Cue");
}

function sequenceStepType(step) {
  if (step?.look) return "look";
  if (step?.visual_id) return "visual";
  if (step?.scene_id || step?.main_box_id || step?.pip_box_id || step?.background_id || step?.visuals_cams_id) return "camera";
  return "cue";
}

function renderOverviewSequenceBanks() {
  const banks = document.createElement("div");
  banks.className = "overview-sequence-banks";
  Object.keys(appSettings?.show_sequences || {}).forEach((name) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = name;
    button.classList.toggle("active", name === activeShowSequence);
    button.addEventListener("click", () => {
      stopShowSequencePlayback(`Loaded ${name}.`);
      activeShowSequence = name;
      if (showSequenceSelect) showSequenceSelect.value = name;
      renderSequencer();
      renderOverviewSequence();
    });
    banks.append(button);
  });
  return banks;
}

function renderOverviewCueStack(steps) {
  const stack = document.createElement("div");
  stack.className = "overview-cue-stack";
  const currentIndex = showSequenceRunning || showSequencePaused ? showSequenceStepIndex : -1;
  const start = currentIndex >= 0 ? currentIndex : 0;
  steps.slice(start, start + 4).forEach((step, offset) => {
    const index = start + offset;
    const item = document.createElement("button");
    item.type = "button";
    item.className = `overview-cue-stack-item cue-type-${sequenceStepType(step)}`;
    item.classList.toggle("current", index === currentIndex);
    const tag = document.createElement("span");
    tag.textContent = index === currentIndex ? "Now" : offset === 0 && currentIndex < 0 ? "Ready" : "Next";
    const strong = document.createElement("strong");
    strong.textContent = sequenceStepLabel(step);
    const meta = document.createElement("small");
    meta.textContent = step.note || sequenceStepType(step);
    item.append(tag, strong, meta);
    item.addEventListener("click", () => triggerOverviewSequenceCue(index));
    stack.append(item);
  });
  if (!steps.length) {
    const empty = document.createElement("div");
    empty.className = "overview-sequence-empty";
    empty.textContent = "No saved cues yet.";
    stack.append(empty);
  }
  return stack;
}

function renderOverviewSequence() {
  if (!overviewSequenceTransport) return;
  overviewSequenceTransport.replaceChildren();
  const sequence = activeShowSequenceConfig();
  const steps = overviewSequenceSteps();
  const status = sequenceStatusLabel();
  const banks = renderOverviewSequenceBanks();
  const summary = document.createElement("div");
  summary.className = "overview-sequence-summary";
  summary.innerHTML = `<strong>${activeShowSequence}</strong><span>${status} - ${steps.length} cues${sequence.loop ? " - loop on" : ""}</span>`;
  const controls = document.createElement("div");
  controls.className = "overview-sequence-buttons";
  [
    ["Play", startShowSequencePlayback, "play"],
    ["Pause", pauseShowSequencePlayback, "pause"],
    ["Next", triggerNextShowSequenceStep, "next"],
    ["Stop", () => stopShowSequencePlayback(), "stop"],
    [sequence.loop ? "Loop On" : "Loop Off", toggleOverviewSequenceLoop, "loop"],
  ].forEach(([label, handler, kind]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.classList.toggle("active", kind === "play" && showSequenceRunning && !showSequencePaused);
    button.classList.toggle("active", kind === "pause" && showSequenceRunning && showSequencePaused);
    button.classList.toggle("active", kind === "loop" && Boolean(sequence.loop));
    button.classList.toggle("danger", kind === "stop");
    button.addEventListener("click", handler);
    controls.append(button);
  });
  const cueGrid = document.createElement("div");
  cueGrid.className = "overview-sequence-cues";
  steps.slice(0, 10).forEach((step, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `overview-cue-button sequence-cue cue-type-${sequenceStepType(step)}`;
    button.classList.toggle("active", index === showSequenceStepIndex && (showSequenceRunning || showSequencePaused));
    const number = document.createElement("span");
    number.textContent = String(index + 1);
    const label = document.createElement("strong");
    label.textContent = sequenceStepLabel(step);
    button.append(number, label);
    button.addEventListener("click", () => triggerOverviewSequenceCue(index));
    cueGrid.append(button);
  });
  if (steps.length > 10) {
    const more = document.createElement("a");
    more.className = "overview-sequence-more";
    more.href = "#sequencerSection";
    more.dataset.sectionLink = "sequencerSection";
    more.textContent = `+${steps.length - 10} more`;
    more.addEventListener("click", (event) => {
      event.preventDefault();
      activateSection("sequencerSection");
      history.pushState(null, "", "#sequencerSection");
    });
    cueGrid.append(more);
  }
  if (!steps.length) {
    const empty = document.createElement("div");
    empty.className = "overview-sequence-empty";
    empty.textContent = "No saved cues yet.";
    cueGrid.append(empty);
  }
  overviewSequenceTransport.append(banks, summary, controls, renderOverviewCueStack(steps), cueGrid);
}

function boolStatus(value, onLabel, offLabel, unknownLabel = "Unknown") {
  if (value === true) return onLabel;
  if (value === false) return offLabel;
  return unknownLabel;
}

function obsStatusText(obs = {}) {
  const recording = obs.recording === true
    ? obs.record_paused === true ? "Recording paused" : "Recording"
    : obs.recording === false ? "Record idle" : "Record unknown";
  const streaming = boolStatus(obs.streaming, "Streaming", "Stream idle", "Stream unknown");
  const replay = boolStatus(obs.replay_buffer, "Replay on", "Replay off", "Replay unknown");
  const virtualCam = boolStatus(obs.virtual_cam, "Virtual cam on", "Virtual cam off", "VCam unknown");
  const studio = boolStatus(obs.studio_mode, "Studio on", "Studio off", "Studio unknown");
  return `${recording} / ${streaming} / ${replay} / ${virtualCam} / ${studio}`;
}

function makeObsButton(text, command, tone, enabled) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = text;
  button.className = `overview-obs-button ${tone || "status"}`;
  button.disabled = !enabled;
  button.addEventListener("click", () => sendCommand({ command }));
  return button;
}

function makeObsGroup(title, items, enabled) {
  const group = document.createElement("div");
  group.className = "obs-control-group";
  const heading = document.createElement("div");
  heading.className = "obs-control-group-title";
  heading.textContent = title;
  const grid = document.createElement("div");
  grid.className = "overview-obs-button-grid";
  items.forEach(([text, command, tone]) => grid.append(makeObsButton(text, command, tone, enabled)));
  group.append(heading, grid);
  return group;
}

function renderObsControlsInto(container, show = latestShow) {
  if (!container) return;
  container.replaceChildren();
  const enabled = Boolean(appSettings?.obs_enabled);
  const fullPage = container === obsSectionControls;
  const obs = show?.obs || appSettings?.obs_status || {};
  const status = document.createElement("div");
  status.className = enabled ? "overview-obs-status enabled" : "overview-obs-status";
  const label = document.createElement("span");
  label.textContent = enabled ? "OBS WebSocket" : "OBS disabled";
  const message = document.createElement("strong");
  message.textContent = enabled ? obsStatusText(obs) : "Enable in Settings";
  status.append(label, message);

  const groups = document.createElement("div");
  groups.className = fullPage ? "obs-control-groups full" : "obs-control-groups compact";
  if (fullPage) {
    groups.append(
      makeObsGroup("Recording", [
        ["Start", "obs_record_start", "record"],
        ["Stop", "obs_record_stop", "danger"],
      ], enabled),
      makeObsGroup("Streaming", [
        ["Start", "obs_stream_start", "stream"],
        ["Stop", "obs_stream_stop", "danger"],
      ], enabled),
      makeObsGroup("Utilities", [
        ["Refresh", "obs_refresh_status", "status"],
        ["Version", "obs_version", "utility"],
        ["Stats", "obs_stats", "utility"],
        ["Studio Mode", "obs_studio_toggle", "utility"],
        ["Studio Cut", "obs_studio_transition", "utility"],
      ], enabled)
    );
  } else {
    groups.append(makeObsGroup("OBS", [
      ["Refresh", "obs_refresh_status", "status"],
      ["Start Rec", "obs_record_start", "record"],
      ["Stop Rec", "obs_record_stop", "danger"],
      ["Rec Status", "obs_record_status", "status"],
      ["Start Stream", "obs_stream_start", "stream"],
      ["Stop Stream", "obs_stream_stop", "danger"],
    ], enabled));
  }

  const hint = document.createElement("p");
  hint.className = "muted overview-obs-hint";
  const errors = obs.errors && Object.keys(obs.errors).length ? ` Status notes: ${Object.keys(obs.errors).join(", ")}.` : "";
  hint.textContent = enabled
    ? `${obs.message || `Target ${appSettings?.obs_host || "127.0.0.1"}:${appSettings?.obs_port || 4455}`}${errors}`
    : "OBS control will use OBS WebSocket on the show PC.";
  container.append(status, groups, hint);
}
function renderOverviewObsControls(show = latestShow) {
  renderObsControlsInto(overviewObsControls, show);
  renderObsControlsInto(obsSectionControls, show);
}

function macroTypeLabel(type) {
  return type === "osc_clock" ? "OSC Clock" : "OSC Button";
}

function macroStatusFor(id) {
  return latestShow?.macro_status?.[id] || appSettings?.macro_status?.[id] || {};
}

function macroClockPreview(macro) {
  const now = new Date();
  let text = "";
  if ((macro.time_format || "12h") === "24h") {
    text = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;
  } else {
    const hour = now.getHours() % 12 || 12;
    text = `${hour}:${String(now.getMinutes()).padStart(2, "0")} ${now.getHours() < 12 ? "AM" : "PM"}`;
  }
  return `${macro.prefix || ""}${text}${macro.suffix || ""}`;
}

function enabledOscTargets() {
  return (appSettings?.osc_targets || []).filter((target) => target.enabled !== false && target.host);
}

function macroTargetPicker(macro) {
  const wrap = document.createElement("div");
  wrap.className = "macro-target-picker";
  const selected = new Set(macro.target_ids || []);
  const targets = enabledOscTargets();
  if (!targets.length) {
    const empty = document.createElement("small");
    empty.textContent = "No enabled OSC targets configured.";
    wrap.append(empty);
    return wrap;
  }
  const hint = document.createElement("small");
  hint.textContent = selected.size ? "Selected destinations" : "All enabled destinations";
  wrap.append(hint);
  for (const target of targets) {
    const label = document.createElement("label");
    const input = document.createElement("input");
    input.type = "checkbox";
    input.name = `macro_target_${macro.id || "new"}`;
    input.value = target.id;
    input.checked = selected.has(target.id);
    const span = document.createElement("span");
    span.textContent = target.label || target.id;
    label.append(input, span);
    wrap.append(label);
  }
  return wrap;
}

function macroValueTypeSelect(value = "trigger") {
  const select = document.createElement("select");
  select.name = "value_type";
  [["trigger", "Trigger / impulse"], ["float", "Float"], ["int", "Integer"], ["string", "String"], ["bool", "Boolean"]].forEach(([key, label]) => {
    const option = document.createElement("option");
    option.value = key;
    option.textContent = label;
    select.append(option);
  });
  select.value = value || "trigger";
  return select;
}

function macroClockFormatSelect(value = "12h") {
  const select = document.createElement("select");
  select.name = "time_format";
  [["12h", "12-hour"], ["24h", "24-hour"]].forEach(([key, label]) => {
    const option = document.createElement("option");
    option.value = key;
    option.textContent = label;
    select.append(option);
  });
  select.value = value || "12h";
  return select;
}

function macroField(labelText, input) {
  const label = document.createElement("label");
  label.className = "macro-field";
  const span = document.createElement("span");
  span.textContent = labelText;
  label.append(span, input);
  return label;
}

function macroAddressField(macro) {
  const address = document.createElement("input");
  address.name = "address";
  address.value = macro.address || "";
  address.placeholder = "/composition/.../text";
  const cell = document.createElement("div");
  cell.className = "osc-address-cell";
  cell.append(address, makeOscAddressBuilder(address));
  return macroField("OSC Address", cell);
}

function collectMacroCardPayload(card) {
  const type = card.dataset.macroType || "osc_button";
  const payload = {
    id: card.dataset.macroId || "",
    type,
    name: card.querySelector('[name="name"]')?.value || "",
    enabled: Boolean(card.querySelector('[name="enabled"]')?.checked),
    address: card.querySelector('[name="address"]')?.value || "",
    target_ids: Array.from(card.querySelectorAll('.macro-target-picker input[type="checkbox"]:checked')).map((input) => input.value),
  };
  if (type === "osc_clock") {
    payload.time_format = card.querySelector('[name="time_format"]')?.value || "12h";
    payload.prefix = card.querySelector('[name="prefix"]')?.value || "";
    payload.suffix = card.querySelector('[name="suffix"]')?.value || "";
  } else {
    payload.value_type = card.querySelector('[name="value_type"]')?.value || "trigger";
    payload.value = card.querySelector('[name="value"]')?.value || "";
  }
  return payload;
}

function nextMacroDraftId() {
  return `draft_${Date.now()}_${Math.random().toString(16).slice(2)}`;
}

function syncMacroDraftsFromDom() {
  if (!macrosList) return;
  const drafts = [];
  macrosList.querySelectorAll(".macro-card[data-macro-draft-id]").forEach((card) => {
    const draft = collectMacroCardPayload(card);
    draft.draft_id = card.dataset.macroDraftId;
    draft.id = "";
    drafts.push(draft);
  });
  macroDrafts = drafts;
}

function removeMacroDraft(draftId) {
  macrosList?.querySelector(`[data-macro-draft-id="${draftId}"]`)?.remove();
  macroDrafts = macroDrafts.filter((draft) => draft.draft_id !== draftId);
  renderMacrosSection();
  if (macrosStatus) macrosStatus.textContent = "Draft macro discarded.";
}

function applyMacroResult(result, fallbackStatus = "Macros updated.") {
  if (result.config) {
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
  } else if (result.macros && appSettings) {
    appSettings.macros = result.macros;
    appSettings.macro_status = result.macro_status || appSettings.macro_status || {};
  }
  if (result.state) renderShowState(result.state, { full: true });
  renderOverviewMacros();
  renderMacrosSection();
  if (macrosStatus) macrosStatus.textContent = result.message || fallbackStatus;
}

async function saveMacroCard(card) {
  try {
    if (macrosStatus) macrosStatus.textContent = "Saving macro...";
    const response = await fetch("/api/macros", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ macro: collectMacroCardPayload(card) }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    if (card.dataset.macroDraftId) removeMacroDraft(card.dataset.macroDraftId);
    applyMacroResult(result, "Macro saved.");
    await loadStatus({ full: true, force: true });
  } catch (error) {
    if (macrosStatus) macrosStatus.textContent = String(error.message || error);
  }
}

async function triggerMacro(id) {
  try {
    if (macrosStatus) macrosStatus.textContent = "Sending macro...";
    const response = await fetch("/api/macros/trigger", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    applyMacroResult(result, "Macro sent.");
  } catch (error) {
    if (macrosStatus) macrosStatus.textContent = String(error.message || error);
    showToast(String(error.message || error), true);
  }
}

async function deleteMacro(id, name) {
  if (!window.confirm(`Delete ${name || "this macro"}?`)) return;
  try {
    const response = await fetch("/api/macros/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    applyMacroResult(result, "Macro deleted.");
    await loadStatus({ full: true, force: true });
  } catch (error) {
    if (macrosStatus) macrosStatus.textContent = String(error.message || error);
  }
}

function makeMacroCard(macro) {
  const card = document.createElement("article");
  card.className = "macro-card";
  card.dataset.macroId = macro.id || "";
  if (macro.draft_id) card.dataset.macroDraftId = macro.draft_id;
  card.dataset.macroType = macro.type || "osc_button";
  const header = document.createElement("div");
  header.className = "macro-card-header";
  const title = document.createElement("div");
  const type = document.createElement("span");
  type.className = "macro-type-pill";
  type.textContent = macroTypeLabel(macro.type);
  const name = document.createElement("input");
  name.name = "name";
  name.value = macro.name || macroTypeLabel(macro.type);
  title.append(type, name);
  const enabled = document.createElement("label");
  enabled.className = "macro-enabled-toggle";
  const enabledInput = document.createElement("input");
  enabledInput.type = "checkbox";
  enabledInput.name = "enabled";
  enabledInput.checked = macro.enabled !== false;
  const enabledText = document.createElement("span");
  enabledText.textContent = "Enabled";
  enabled.append(enabledInput, enabledText);
  header.append(title, enabled);
  const fields = document.createElement("div");
  fields.className = "macro-fields";
  fields.append(macroAddressField(macro), macroField("Destinations", macroTargetPicker(macro)));
  if (macro.type === "osc_clock") {
    const format = macroClockFormatSelect(macro.time_format || "12h");
    const prefix = document.createElement("input");
    prefix.name = "prefix";
    prefix.value = macro.prefix || "";
    const suffix = document.createElement("input");
    suffix.name = "suffix";
    suffix.value = macro.suffix || "";
    const preview = document.createElement("output");
    preview.className = "macro-clock-preview";
    const updatePreview = () => {
      preview.value = macroClockPreview({ time_format: format.value, prefix: prefix.value, suffix: suffix.value });
      preview.textContent = preview.value;
    };
    [format, prefix, suffix].forEach((input) => input.addEventListener("input", updatePreview));
    updatePreview();
    fields.append(macroField("Time Format", format), macroField("Prefix", prefix), macroField("Suffix", suffix), macroField("Preview", preview));
  } else {
    const valueType = macroValueTypeSelect(macro.value_type || "trigger");
    const value = document.createElement("input");
    value.name = "value";
    value.value = macro.value ?? "";
    value.placeholder = "1";
    const syncValueState = () => {
      value.disabled = valueType.value === "trigger";
      if (valueType.value === "trigger") value.value = "1";
      if (valueType.value === "bool") value.placeholder = "true";
    };
    valueType.addEventListener("input", syncValueState);
    syncValueState();
    fields.append(macroField("Value Type", valueType), macroField("Value", value));
  }
  const status = document.createElement("div");
  status.className = "macro-runtime-status";
  const runtime = macroStatusFor(macro.id);
  if (macro.type === "osc_clock") {
    status.textContent = runtime.error ? `Error: ${runtime.error}` : runtime.last_sent_value ? `Last sent ${runtime.last_sent_value} at ${runtime.last_sent_time || "-"}` : macro.enabled === false ? "Clock stopped." : "Clock waiting to send.";
    status.classList.toggle("error", Boolean(runtime.error));
  } else {
    status.textContent = macro.enabled === false ? "Button disabled." : "Ready to trigger.";
  }
  const actions = document.createElement("div");
  actions.className = "macro-actions";
  const save = document.createElement("button");
  save.type = "button";
  save.textContent = "Save";
  save.addEventListener("click", () => saveMacroCard(card));
  const test = document.createElement("button");
  test.type = "button";
  test.textContent = macro.type === "osc_clock" ? "Send Now" : "Trigger";
  test.disabled = !macro.id;
  test.addEventListener("click", () => triggerMacro(macro.id));
  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "danger";
  remove.textContent = "Delete";
  remove.disabled = !macro.id && !macro.draft_id;
  remove.addEventListener("click", () => {
    if (macro.draft_id) removeMacroDraft(macro.draft_id);
    else deleteMacro(macro.id, macro.name);
  });
  actions.append(save, test, remove);
  card.append(header, fields, status, actions);
  return card;
}

function macrosForDisplay() {
  return [...macroDrafts, ...(appSettings?.macros || [])];
}

function clampMacrosPage(total) {
  const pageCount = Math.max(1, Math.ceil(total / MACROS_PER_PAGE));
  macrosPage = Math.max(0, Math.min(macrosPage, pageCount - 1));
  return pageCount;
}

function renderMacrosPager(total) {
  if (!macrosPager) return;
  macrosPager.replaceChildren();
  const pageCount = clampMacrosPage(total);
  const summary = document.createElement("span");
  summary.className = "macros-page-summary";
  const start = total ? macrosPage * MACROS_PER_PAGE + 1 : 0;
  const end = Math.min(total, start + MACROS_PER_PAGE - 1);
  summary.textContent = total ? `Macros ${start}-${end} of ${total}` : "No macros";
  const previous = document.createElement("button");
  previous.type = "button";
  previous.textContent = "Previous";
  previous.disabled = macrosPage <= 0;
  previous.addEventListener("click", () => {
    syncMacroDraftsFromDom();
    macrosPage = Math.max(0, macrosPage - 1);
    renderMacrosSection({ skipSync: true });
  });
  const next = document.createElement("button");
  next.type = "button";
  next.textContent = "Next";
  next.disabled = macrosPage >= pageCount - 1;
  next.addEventListener("click", () => {
    syncMacroDraftsFromDom();
    macrosPage = Math.min(pageCount - 1, macrosPage + 1);
    renderMacrosSection({ skipSync: true });
  });
  macrosPager.append(summary, previous, next);
}

function renderMacrosSection(options = {}) {
  if (!macrosList || !appSettings) return;
  if (!options.skipSync && macrosList.querySelector(".macro-card[data-macro-draft-id]")) syncMacroDraftsFromDom();
  if (!options.force && macrosList.contains(document.activeElement)) return;
  const macros = macrosForDisplay();
  const pageCount = clampMacrosPage(macros.length);
  const pageItems = macros.slice(macrosPage * MACROS_PER_PAGE, macrosPage * MACROS_PER_PAGE + MACROS_PER_PAGE);
  macrosList.replaceChildren();
  renderMacrosPager(macros.length);
  if (!macros.length) {
    const empty = document.createElement("p");
    empty.className = "muted macro-empty-state";
    empty.textContent = "No macros yet. Add an OSC Button or OSC Clock to begin.";
    macrosList.append(empty);
    return;
  }
  pageItems.forEach((macro) => macrosList.append(makeMacroCard(macro)));
  if (macrosStatus && !options.keepStatus) {
    const start = macrosPage * MACROS_PER_PAGE + 1;
    const end = Math.min(macros.length, start + MACROS_PER_PAGE - 1);
    macrosStatus.textContent = `Showing ${start}-${end} of ${macros.length} macros. Page ${macrosPage + 1} of ${pageCount}.`;
  }
}

function addDraftMacro(type) {
  syncMacroDraftsFromDom();
  const draft = type === "osc_clock"
    ? { draft_id: nextMacroDraftId(), id: "", type, name: "OSC Clock", enabled: true, address: "", target_ids: [], time_format: "12h", prefix: "", suffix: "" }
    : { draft_id: nextMacroDraftId(), id: "", type, name: "OSC Button", enabled: true, address: "", target_ids: [], value_type: "trigger", value: "1" };
  macroDrafts.unshift(draft);
  macrosPage = 0;
  renderMacrosSection({ skipSync: true, force: true, keepStatus: true });
  const firstDraftInput = macrosList?.querySelector(`[data-macro-draft-id="${draft.draft_id}"] input[name="name"]`);
  firstDraftInput?.focus();
  firstDraftInput?.select();
  if (macrosStatus) macrosStatus.textContent = "New macro added. Configure it, then Save.";
}
function renderOverviewMacros() {
  if (!overviewMacroButtons) return;
  overviewMacroButtons.replaceChildren();
  const macros = appSettings?.macros || [];
  const buttons = macros.filter((macro) => macro.type === "osc_button" && macro.enabled !== false);
  const clocks = macros.filter((macro) => macro.type === "osc_clock");
  if (!buttons.length && !clocks.length) {
    const empty = document.createElement("span");
    empty.className = "muted overview-macro-empty";
    empty.textContent = "No macros configured.";
    overviewMacroButtons.append(empty);
    return;
  }
  buttons.forEach((macro) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "overview-macro-button";
    button.textContent = macro.name || "OSC Button";
    button.addEventListener("click", () => triggerMacro(macro.id));
    overviewMacroButtons.append(button);
  });
  clocks.forEach((macro) => {
    const status = macroStatusFor(macro.id);
    const clock = document.createElement("div");
    clock.className = "overview-macro-clock";
    clock.classList.toggle("error", Boolean(status.error));
    const name = document.createElement("strong");
    name.textContent = macro.name || "OSC Clock";
    const detail = document.createElement("span");
    detail.textContent = status.error || status.last_sent_value || (macro.enabled === false ? "Stopped" : "Running");
    clock.append(name, detail);
    overviewMacroButtons.append(clock);
  });
}
function currentSpotifyStatus(status = null) {
  return status?.spotify || status?.config?.spotify_status || status?.settings?.spotify_status || appSettings?.spotify_status || latestShow?.spotify || null;
}

function spotifyNeedsConnection(status = null) {
  const spotify = currentSpotifyStatus(status) || {};
  return Boolean(appSettings?.spotify_enabled || spotify.enabled) && !Boolean(spotify.connected);
}
function spotifyCurrentDisplay(current = null) {
  if (!current || current.item_type === "none") return { title: "No active Spotify playback", artist: "-", album: "-" };
  const title = current.title || current.track_id || "Spotify track";
  const artist = current.artist || "-";
  return {
    title: artist && artist !== "-" ? `${artist} - ${title}` : title,
    artist,
    album: current.album || "-",
  };
}

function formatSpotifyDuration(ms) {
  const value = Number(ms || 0);
  if (!Number.isFinite(value) || value <= 0) return "0:00";
  const totalSeconds = Math.floor(value / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
}

function renderSpotifyStatus(status = null) {
  const spotify = currentSpotifyStatus(status) || {};
  const current = spotify.current || null;
  const display = spotifyCurrentDisplay(current);
  const enabled = Boolean(appSettings?.spotify_enabled || spotify.enabled);  const connected = Boolean(spotify.connected);
  const active = Boolean(spotify.active_source);
  if (spotifyAuthStatus) {
    if (active) spotifyAuthStatus.textContent = "Spotify source active";    else if (connected) spotifyAuthStatus.textContent = "Connected; select Spotify as the Now Playing source.";
    else if (enabled) spotifyAuthStatus.textContent = "Connect Spotify to use live Now Playing.";
    else spotifyAuthStatus.textContent = "Disabled";
  }
  if (spotifyStatusBadge) {
    spotifyStatusBadge.textContent = active ? "Active" : connected ? "Connected" : "Disconnected";
    spotifyStatusBadge.classList.toggle("enabled", active || connected);
  }
  if (spotifyRuntimeTitle) spotifyRuntimeTitle.textContent = display.title;
  if (spotifyRuntimeArtist) spotifyRuntimeArtist.textContent = display.artist;
  if (spotifyRuntimeAlbum) spotifyRuntimeAlbum.textContent = display.album;
  if (spotifyRuntimePlayback) {
    const playbackState = current?.is_playing ? "Playing" : current ? "Paused" : "Idle";
    const progress = `${formatSpotifyDuration(current?.progress_ms)} / ${formatSpotifyDuration(current?.duration_ms)}`;
    spotifyRuntimePlayback.textContent = current && current.item_type !== "none" ? `${playbackState} (${progress})` : playbackState;
  }
  if (spotifyRuntimeDevice) spotifyRuntimeDevice.textContent = current?.device_name || "-";
  if (spotifyRuntimeLastPoll) spotifyRuntimeLastPoll.textContent = spotify.last_poll || spotify.last_success || "-";
  if (spotifyRuntimeLastError) spotifyRuntimeLastError.textContent = spotify.last_error || "-";
}
function resizeLiveDeckCards() {
  if (!liveDeckGrid) return;
  liveDeckPanelCards.forEach((card) => {
    card.style.gridRowEnd = "";
  });
}

function scheduleLiveDeckResize() {
  if (liveDeckResizeFrame) cancelAnimationFrame(liveDeckResizeFrame);
  liveDeckResizeFrame = requestAnimationFrame(() => {
    liveDeckResizeFrame = null;
    resizeLiveDeckCards();
  });
}

function renderLiveDeck(show) {
  const names = Object.keys(presetData?.groups?.performance || {});
  renderActiveMomentStrip(show);
  renderLiveDeckLookCapture(show);
  renderOverviewNowPlaying({ show, blt: {}, artwork: {} });
  renderOverviewLooks(names);
  renderOverviewLightState(show);
  renderOverviewLightControls();
  renderOverviewBpmControls(show);
  renderOverviewVisuals();
  renderOverviewCameras();
  renderCueRouteControls();
  renderOverviewSequence();
  renderOverviewObsControls(show);
  renderOverviewMacros();
  renderOverviewGenerator();
  scheduleLiveDeckResize();
}

function confirmedPerformanceName(show = latestShow) {
  if (show?.source?.startsWith("performance:")) return show.source.slice("performance:".length).split("+")[0];
  if (!lookApplyLights() && show?.active_look_name) return show.active_look_name;
  return "";
}

function activePerformanceName() {
  return optimisticPerformanceLookName || confirmedPerformanceName(latestShow);
}
function reapplyActivePerformanceLook() {
  const name = activePerformanceName() || saveCurrentLookSelect?.value || "Look 1";
  sendCommand(linkedLookPayload(name));
}

function applyDefaultPerformanceLook() {
  sendCommand(linkedLookPayload("Look 1"));
}

function markManualOverride() {
  manualOverrideUntil = Date.now() + 12000;
  if (manualOverrideTimer) clearTimeout(manualOverrideTimer);
  manualOverrideTimer = setTimeout(() => {
    manualOverrideTimer = null;
    if (manualOverrideUntil <= Date.now()) {
      renderActiveMomentStrip(latestShow);
      renderOverviewSequence();
    }
  }, 12100);
}

function setupMomentaryControl(button, controlKey, holdValue = 100) {
  if (!button) return;
  let restoreValue = 0;
  let activePointerId = null;
  const press = (event) => {
    if (activePointerId !== null) return;
    activePointerId = event.pointerId ?? "mouse";
    const output = outputByKey(controlKey) || {};
    restoreValue = Math.round(Number(output.value || 0) * 100);
    button.classList.add("active");
    markManualOverride();
    sendCommand({ command: "set_control", key: controlKey, value: holdValue }, { quiet: true, manualOverride: false });
    if (event.pointerId !== undefined) button.setPointerCapture?.(event.pointerId);
  };
  const release = (event) => {
    if (activePointerId === null) return;
    if (event?.pointerId !== undefined && activePointerId !== event.pointerId) return;
    activePointerId = null;
    button.classList.remove("active");
    sendCommand({ command: "set_control", key: controlKey, value: restoreValue }, { quiet: true, manualOverride: false });
  };
  button.addEventListener("pointerdown", press);
  button.addEventListener("pointerup", release);
  button.addEventListener("pointercancel", release);
  button.addEventListener("lostpointercapture", release);
  button.addEventListener("keydown", (event) => {
    if (event.key !== " " && event.key !== "Enter") return;
    event.preventDefault();
    press(event);
  });
  button.addEventListener("keyup", (event) => {
    if (event.key !== " " && event.key !== "Enter") return;
    event.preventDefault();
    release(event);
  });
}

function makeLookSwatches(values) {
  const swatches = document.createElement("span");
  swatches.className = "preset-preview-swatches";
  for (const key of ["PRIMARY", "SECONDARY", "STROBE"]) {
    const swatch = document.createElement("i");
    swatch.title = `${key}: ${values?.[key] || "-"}`;
    swatch.style.background = colorHex(values?.[key]);
    swatches.append(swatch);
  }
  return swatches;
}

function makeLookCueStrip(name, link, cameraConfig, options = {}) {
  const strip = document.createElement("span");
  strip.className = options.compact ? "look-cue-strip compact" : "look-cue-strip";
  for (const [label, value] of lookCueItems(link, cameraConfig)) {
    const item = document.createElement("span");
    item.className = isNoCueChange(value) ? "look-cue muted-cue" : "look-cue";
    const small = document.createElement("small");
    small.textContent = label;
    const strong = document.createElement("strong");
    strong.textContent = value;
    item.append(small, strong);
    strip.append(item);
  }
  return strip;
}

function lookValuesForName(name) {
  return presetData?.groups?.performance?.[name] || {};
}

function cuePaletteForLook(name) {
  const values = lookValuesForName(name);
  return {
    primaryName: values.PRIMARY || "",
    secondaryName: values.SECONDARY || "",
    accentName: values.STROBE || "",
    primary: colorHex(values.PRIMARY),
    secondary: colorHex(values.SECONDARY),
    accent: colorHex(values.STROBE),
  };
}

function applyCuePaletteVars(element, lookName) {
  const palette = cuePaletteForLook(lookName);
  element.style.setProperty("--cue-primary", palette.primary);
  element.style.setProperty("--cue-secondary", palette.secondary);
  element.style.setProperty("--cue-accent", palette.accent);
}

function makeSequenceLookPreview(step) {
  const lookName = step.look || "";
  const link = appSettings?.preset_links?.[lookName] || {};
  const cameraConfig = appSettings?.camera_controls || {};
  const palette = cuePaletteForLook(lookName);
  const preview = document.createElement("div");
  preview.className = "sequence-look-preview";
  preview.style.setProperty("--cue-primary", palette.primary);
  preview.style.setProperty("--cue-secondary", palette.secondary);
  preview.style.setProperty("--cue-accent", palette.accent);

  const colorBar = document.createElement("div");
  colorBar.className = "sequence-look-color-bar";
  const colorItems = [
    ["Color 1", palette.primaryName, palette.primary],
    ["Color 2", palette.secondaryName, palette.secondary],
    ["Color 3", palette.accentName, palette.accent],
  ];
  for (const [label, name, hex] of colorItems) {
    const item = document.createElement("span");
    item.style.setProperty("--swatch", hex);
    item.innerHTML = `<i></i><small>${label}</small><strong>${name || "-"}</strong>`;
    colorBar.append(item);
  }

  const cueStrip = document.createElement("div");
  cueStrip.className = "sequence-look-output-strip";
  const outputItems = [
    ["Visual", optionLabel(appSettings?.visual_controls, step.visual_id || link.visual_id)],
    ["Main", optionLabel(cameraConfig.groups?.main_box, step.main_box_id || link.main_box_id)],
    ["PIP", optionLabel(cameraConfig.groups?.pip_box, step.pip_box_id || link.pip_box_id)],
    ["BG", optionLabel(cameraConfig.groups?.background, step.background_id || link.background_id)],
    ["Visuals", optionLabel(cameraConfig.groups?.visuals_cams, step.visuals_cams_id || link.visuals_cams_id)],
    ["Scene", optionLabel(cameraConfig.scenes, step.scene_id || link.scene_id)],
  ];
  for (const [label, value] of outputItems) {
    const item = document.createElement("span");
    item.className = value === "None" || value === "No change" ? "muted-output" : "";
    item.innerHTML = `<small>${label}</small><strong>${value}</strong>`;
    cueStrip.append(item);
  }

  preview.append(colorBar, cueStrip);
  return preview;
}

function makeLookLightSummary(values) {
  const summary = document.createElement("div");
  summary.className = "look-light-summary";
  const colorBlock = document.createElement("div");
  colorBlock.className = "look-light-colors";
  const colors = [
    ["Color 1", values.PRIMARY],
    ["Color 2", values.SECONDARY],
    ["Color 3", values.STROBE],
  ];
  for (const [label, value] of colors) {
    const item = document.createElement("div");
    const swatch = document.createElement("span");
    swatch.style.background = colorHex(value);
    const small = document.createElement("small");
    small.textContent = label;
    const strong = document.createElement("strong");
    strong.textContent = value || "-";
    item.append(swatch, small, strong);
    colorBlock.append(item);
  }

  summary.append(colorBlock);
  return summary;
}
function makeLookLightEditor(name, values, onDirty) {
  const editor = document.createElement("div");
  editor.className = "look-light-editor";
  editor.dataset.look = name;
  const colorRow = document.createElement("div");
  colorRow.className = "look-color-editor";
  for (const [key, labelText] of lookColorFields) {
    colorRow.append(makeLookColorControl(key, labelText, values[key], onDirty));
  }

  editor.append(colorRow);
  return editor;
}
function makeLookColorControl(key, labelText, value, onDirty) {
  const label = document.createElement("label");
  label.className = "look-color-field";
  const swatch = document.createElement("span");
  swatch.className = "look-color-swatch";
  swatch.style.background = colorHex(value);
  const name = document.createElement("small");
  name.textContent = labelText;
  const select = document.createElement("select");
  select.dataset.presetKey = key;
  for (const colorName of presetData?.colors?.names || appSettings?.colors?.names || []) {
    const option = document.createElement("option");
    option.value = colorName;
    option.textContent = colorName;
    select.append(option);
  }
  select.value = value || select.options[0]?.value || "";
  select.addEventListener("change", () => {
    swatch.style.background = colorHex(select.value);
    onDirty();
    scheduleLookControlSend(key, select.value, 0);
  });
  label.append(swatch, name, select);
  return label;
}

function scheduleLookControlSend(presetKey, value, delay = 120) {
  const controlKey = presetControlKeys[presetKey];
  if (!controlKey) return;
  if (lookControlTimers[presetKey]) clearTimeout(lookControlTimers[presetKey]);
  lookControlTimers[presetKey] = setTimeout(() => {
    sendCommand({ command: "set_control", key: controlKey, value }, { quiet: true });
  }, delay);
}

function collectLookLightValues(editor) {
  const values = {};
  editor.querySelectorAll("[data-preset-key]").forEach((input) => {
    const key = input.dataset.presetKey;
    if (!key) return;
    values[key] = input.value;
  });
  return values;
}
function renderDivisionButtons() {
  divisionButtons.replaceChildren();
  divisionButtons.append(makeBpmDivisionGrid({
    className: "division-grid-inner",
    onPick: updateAppBpmDivision,
  }));
}

function renderBpmClockSummary() {
  if (!bpmClockSummary) return;
  bpmClockSummary.replaceChildren();
  const summary = makeBpmClockSummary(
    "Color Rotation",
    `${bpmClockSummaryText("Global timing")}${latestShow?.bpm_follow_now_playing ? " - following Now Playing BPM" : ""}`,
  );
  bpmClockSummary.append(...summary.childNodes);
}

function renderBpmRotationControls() {
  if (!bpmRotationControls) return;
  bpmRotationControls.replaceChildren();
  bpmRotationControls.append(makeBpmRotationChecks({ className: "bpm-rotation-checks full-bpm-rotation", autoSave: true }));
}

function currentBpmMode() {
  return latestShow?.bpm_flip_mode === "seconds" ? "seconds" : "bars";
}

function currentBpmSecondsValue() {
  return Math.max(0.1, Number(latestShow?.bpm_seconds || appSettings?.bpm_flip_seconds || 8) || 8);
}

function currentBpmIntervalMs(division = selectedDivision) {
  if (currentBpmMode() === "seconds") return currentBpmSecondsValue() * 1000;
  return intervalMsForDivision(currentSequenceBpm(), division);
}

function bpmClockSummaryText(label = "App Clock") {
  const bpm = currentSequenceBpm();
  const bpmLabel = Number.isInteger(bpm) ? String(bpm) : bpm.toFixed(1).replace(/\.0$/, "");
  const rotation = `rotating ${bpmRotationLabel()}`;
  if (currentBpmMode() === "seconds") return `${label} - seconds - every ${formatDuration(currentBpmIntervalMs())} - ${rotation}`;
  return `${label} - ${bpmLabel} BPM - ${selectedDivision} - ${formatDuration(currentBpmIntervalMs())} - ${rotation}`;
}

function makeBpmClockSummary(label, detail = "") {
  const summary = document.createElement("div");
  summary.className = "bpm-clock-summary";
  const title = document.createElement("span");
  title.textContent = label;
  const strong = document.createElement("strong");
  strong.textContent = currentBpmMode() === "seconds" ? "Seconds" : `${Math.round(currentSequenceBpm() * 10) / 10} BPM`;
  const small = document.createElement("small");
  small.textContent = detail || bpmClockSummaryText("Clock");
  summary.append(title, strong, small);
  return summary;
}

function makeBpmRotationChecks(options = {}) {
  const group = document.createElement("div");
  group.className = options.className || "bpm-rotation-checks";
  if (options.name) group.dataset.fieldName = options.name;
  const selected = new Set(normalizeBpmRotationSlots(options.value || currentBpmRotationSlots()));
  const title = document.createElement("span");
  title.textContent = options.title || "Rotate";
  group.append(title);
  for (const [key, labelText] of BPM_ROTATION_OPTIONS) {
    const label = document.createElement("label");
    const input = document.createElement("input");
    input.type = "checkbox";
    input.name = options.name || "bpm_rotation_slots";
    input.value = key;
    input.checked = selected.has(key);
    const text = document.createElement("span");
    text.textContent = labelText;
    input.addEventListener("change", async () => {
      if (options.onChange) options.onChange(group);
      if (options.autoSave) {
        const slots = collectBpmRotationSlots(group);
        if (slots.length < 2) {
          showToast("Choose at least two colors to rotate.", true);
          renderOverviewBpmControls(latestShow);
          return;
        }
        await saveBpmRotationSlots(slots);
      }
    });
    label.append(input, text);
    group.append(label);
  }
  return group;
}

function collectBpmRotationSlots(container = document) {
  return BPM_ROTATION_OPTIONS
    .map(([key]) => key)
    .filter((key) => Boolean(container.querySelector(`input[name="bpm_rotation_slots"][value="${key}"]`)?.checked));
}

async function saveBpmRotationSlots(slots) {
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ bpm_rotation_slots: slots }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    if (result.state) renderShowState(result.state);
    renderQuickSettingsForm();
    renderOverviewBpmControls(result.state || latestShow);
    showToast(`Rotating ${bpmRotationLabel(slots)}`);
  } catch (error) {
    showToast(String(error.message || error), true);
    renderOverviewBpmControls(latestShow);
  }
}
function makeBpmDivisionGrid(options = {}) {
  const grid = document.createElement("div");
  grid.className = options.className || "bpm-clock-division-grid";
  const divisions = options.divisions || appSettings?.bpm_divisions || DEFAULT_BPM_DIVISIONS;
  const selected = options.selected || selectedDivision;
  for (const division of divisions) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = options.buttonClass || "bpm-clock-division-button";
    button.classList.toggle("active", currentBpmMode() !== "seconds" && division === selected);
    button.innerHTML = `<strong>${division}</strong><span>${formatDuration(intervalMsForDivision(currentSequenceBpm(), division))}</span>`;
    button.addEventListener("click", () => (options.onPick || updateAppBpmDivision)(division));
    grid.append(button);
  }
  return grid;
}

function refreshBpmSurfaces() {
  renderBpmClockSummary();
  renderBpmRotationControls();
  renderDivisionButtons();
  renderOverviewBpmControls(latestShow);
  renderSequenceTimingTools();
  renderGeneratorBpmSync();
  renderSequenceRowsFromSteps(collectShowSequenceSteps());
}

function updateAppBpmDivision(division) {
  selectedDivision = division;
  refreshBpmSurfaces();
  const payload = { command: "bpm_update", division };
  if (!latestShow?.bpm_follow_now_playing) payload.bpm = bpmInput.value;
  sendCommand(payload);
}

function durationMsForAmount(amount, unit, bpm = currentSequenceBpm()) {
  const safeAmount = Math.max(0, Number(amount || 0));
  if (unit === "minutes") return safeAmount * 60000;
  if (unit === "seconds") return safeAmount * 1000;
  const beatMs = 60000 / Math.max(1, Number(bpm) || 120);
  if (unit === "bars") return safeAmount * 4 * beatMs;
  return safeAmount * beatMs;
}

function intervalMsForDivision(bpm, division) {
  return (60000 / Math.max(1, Number(bpm) || 120)) * (BPM_DIVISION_MULTIPLIERS[division] || BPM_DIVISION_MULTIPLIERS["1/4"]);
}

function formatDuration(ms) {
  const safeMs = Math.max(0, Number(ms) || 0);
  if (safeMs < 1000) return `${Math.round(safeMs)} ms`;
  const totalSeconds = safeMs / 1000;
  if (totalSeconds < 60) {
    const display = totalSeconds >= 10 ? totalSeconds.toFixed(1) : totalSeconds.toFixed(2);
    return `${display.replace(/\.0+$/, "")} sec`;
  }
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = Math.round(totalSeconds % 60);
  if (minutes < 60) return seconds ? `${minutes} min ${seconds} sec` : `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return remainingMinutes ? `${hours} hr ${remainingMinutes} min` : `${hours} hr`;
}

function renderOutputs(outputs) {
  if (!outputGrid) return;
  outputGrid.replaceChildren();
  for (const output of outputs || []) {
    const card = document.createElement("div");
    card.className = "output-card";
    card.dataset.key = output.key || "";
    const label = document.createElement("div");
    label.className = "label";
    label.textContent = `Link ${output.link} - ${output.label}`;
    const value = document.createElement("div");
    value.className = "value";
    if (output.hex) {
      const swatch = document.createElement("span");
      swatch.className = "swatch";
      swatch.style.background = output.hex;
      value.append(swatch);
    }
    value.append(output.display || Number(output.value || 0).toFixed(3));
    card.append(label, value);
    outputGrid.append(card);
  }
}

function formatBpmStatus(show) {
  if (!show) return "Idle - rotating " + bpmRotationLabel();
  const mode = show.bpm_running ? "Running" : "Idle";
  const follow = show.bpm_follow_now_playing ? " - following now playing" : "";
  const rotation = ` - rotating ${bpmRotationLabel(normalizeBpmRotationSlots(show.bpm_rotation_slots))}`;
  if (show.bpm_flip_mode === "seconds") {
    return `${mode} - every ${formatDuration(show.bpm_interval_ms)}${rotation}`;
  }
  return `${mode} - ${show.bpm} BPM - ${show.bpm_division} - every ${formatDuration(show.bpm_interval_ms)}${rotation}${follow}`;
}

function setBpmUiValue(value) {
  const bpm = Number(value);
  if (!Number.isFinite(bpm)) return;
  const clamped = Math.max(40, Math.min(240, bpm));
  const display = Number.isInteger(clamped) ? String(clamped) : clamped.toFixed(1).replace(/\.0$/, "");
  bpmInput.value = display;
  if (bpmSlider) bpmSlider.value = String(clamped);
}

function sendBpmUpdate() {
  refreshBpmSurfaces();
  sendCommand({ command: "bpm_update", bpm: bpmInput.value, division: selectedDivision });
}

function nudgeBpm(amount) {
  const current = Number.parseFloat(bpmInput.value || "125");
  const next = (Number.isFinite(current) ? current : 125) + amount;
  setBpmUiValue(Math.round(next * 10) / 10);
  refreshBpmSurfaces();
  sendBpmUpdate();
}

function previewTypedBpm(value) {
  const bpm = Number(value);
  if (!Number.isFinite(bpm)) return;
  if (bpmSlider) bpmSlider.value = String(Math.max(40, Math.min(240, bpm)));
  refreshBpmSurfaces();
}

function rotatePreviewState() {
  if (!latestShow?.bpm_running) return;
  const outputs = latestShow.outputs || [];
  const slots = currentBpmRotationSlots();
  if (slots.length < 2) return;
  const selectedOutputs = slots.map((key) => outputs.find((output) => output.key === key));
  if (selectedOutputs.some((output) => !output)) return;
  const snapshots = selectedOutputs.map((output) => ({
    color: output.color,
    display: output.display,
    value: output.value,
    hex: output.hex,
  }));
  selectedOutputs.forEach((output, index) => {
    const source = snapshots[(index + 1) % snapshots.length];
    const oldColor = output.color || "";
    output.color = source.color;
    output.value = source.value;
    output.hex = source.hex;
    output.display = oldColor && output.display
      ? output.display.replace(oldColor, source.color || "")
      : source.display;
    updateLinkControlPreview(output.key, output);
  });
  const byKey = (key) => outputs.find((output) => output.key === key) || {};
  latestShow.colors = {
    ...(latestShow.colors || {}),
    color1: byKey("color1").color,
    color2: byKey("color2").color,
    color3: byKey("strobe_color").color,
    primary: byKey("color1").color,
    secondary: byKey("color2").color,
    tertiary: byKey("strobe_color").color,
    accent: byKey("strobe_color").color,
  };
  latestShow.color_comment = `COLOR1=${latestShow.colors.color1};COLOR2=${latestShow.colors.color2};COLOR3=${latestShow.colors.color3}`;

  if (colorComment) colorComment.textContent = latestShow.color_comment || "-";
  renderColorPreview(latestShow);
  renderOutputs(latestShow.outputs);
}

function updateLinkControlPreview(key, output) {
  const row = linkControls.querySelector(`.link-row[data-key="${key}"]`);
  if (!row) return;
  const readout = row.querySelector(".readout");
  if (readout) readout.textContent = output.display || "";
  row.querySelectorAll(".color-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.value === output.color);
  });
}

function syncBpmPreviewTimer(show) {
  if (bpmPreviewTimer) {
    clearInterval(bpmPreviewTimer);
    bpmPreviewTimer = null;
  }
  if (!show?.bpm_running) return;
  const interval = Number(show.bpm_interval_ms || 500);
  const visualInterval = Math.max(45, interval);
  bpmPreviewTimer = setInterval(rotatePreviewState, visualInterval);
}

function renderColorPreview(show) {
  if (!colorPreviewWindow || !show) return;
  colorPreviewWindow.replaceChildren();
  const { stage, metrics } = lightPreviewParts(show);
  colorPreviewWindow.append(stage, metrics);
}

function renderCommandLog(show) {
  const lines = show?.command_log || [];
  commandLog.textContent = lines.length ? lines.join("\n") : "Waiting for commands.";
}

function renderShowState(show, options = {}) {
  if (!show) return;
  const full = options.full !== false;
  const active = options.activeSectionId || activeSectionId;
  const signature = JSON.stringify(show);
  const changed = signature !== latestShowSignature;
  latestShow = show;
  if (optimisticPerformanceLookName && confirmedPerformanceName(show) === optimisticPerformanceLookName) optimisticPerformanceLookName = "";
  if (optimisticNowPlayingMode && show.manual_mode) optimisticNowPlayingMode = "";
  selectedDivision = show.bpm_division || selectedDivision;
  setBpmUiValue(show.bpm || bpmInput.value);
  bpmStatus.textContent = formatBpmStatus(show);
  if (lastEvent) {
    lastEvent.textContent = show.last_event || "Ready";
    lastEvent.className = "muted";
  }
  if (colorComment) colorComment.textContent = show.color_comment || "-";
  renderBpmClockSummary();
  renderBpmRotationControls();
  if (!full && !changed) {
    syncBpmPreviewTimer(show);
    return;
  }
  latestShowSignature = signature;

  renderColorPreview(show);
  renderOutputs(show.outputs);
  renderSelectionSummary(show);
  renderCommandLog(show);
  renderSelectedButtons(show);

  if (full || active === "lightsSection" || active === "liveDeckSection") {
    renderDivisionButtons();
    renderLinkControls();
  }
  if (full || active === "visualsSection") renderVisualControls();
  if (full || active === "camerasSection") renderCameraControls();
  if (full || active === "looksSection") {
    renderPresetLinks();
    renderLookLauncher();
    renderLookLinkForm();
  }
  if (full || active === "generatorSection" || active === "visualsSection") {
    renderGeneratorBpmSync();
    renderGeneratorQuickPresets();
  }
  if (full || active === "sequencerSection") renderSequenceTimingTools();
  if (full || active === "macrosSection") renderMacrosSection();
  if (full || active === "liveDeckSection") {
    renderLiveDeck(show);
    renderPerformanceSurfaces();
  } else if (active === "looksSection") {
    renderPerformanceSurfaces();
  }
  syncBpmPreviewTimer(show);
}

function manualModeText(mode) {
  if (mode === "vinyl") return appSettings?.vinyl_track_text || "Record Playing";
  if (mode === "studio") return appSettings?.studio_track_text || "NO TALKING STUDIO";
  if (mode === "videogame") return appSettings?.videogame_track_text || "Ravenswatch";
  if (mode === "spotify") return appSettings?.spotify_track_text || "Spotify Now Playing";
  return "";
}

function renderManualModeForm() {
  if (!appSettings) return;
  if (vinylModeButtonText) vinylModeButtonText.textContent = manualModeText("vinyl");
  if (studioModeButtonText) studioModeButtonText.textContent = manualModeText("studio");
  if (videogameModeButtonText) videogameModeButtonText.textContent = "Videogames";
  if (manualModeDirty) return;
  if (manualModeForm && !manualModeForm.contains(document.activeElement)) {
    if (vinylTrackText) vinylTrackText.value = appSettings.vinyl_track_text || "Record Playing";
    if (vinylArtworkPath) vinylArtworkPath.value = appSettings.vinyl_logo_path || "";
    if (vinylArtworkWidth) vinylArtworkWidth.value = appSettings.vinyl_artwork_width || "";
    if (vinylArtworkHeight) vinylArtworkHeight.value = appSettings.vinyl_artwork_height || "";
    if (studioTrackText) studioTrackText.value = appSettings.studio_track_text || "NO TALKING STUDIO";
    if (studioArtworkPath) studioArtworkPath.value = appSettings.studio_artwork_path || "";
    if (studioArtworkWidth) studioArtworkWidth.value = appSettings.studio_artwork_width || "";
    if (studioArtworkHeight) studioArtworkHeight.value = appSettings.studio_artwork_height || "";
    if (videogameTrackText) videogameTrackText.value = appSettings.videogame_track_text || "Ravenswatch";
    if (videogameArtworkPath) videogameArtworkPath.value = appSettings.videogame_artwork_path || "";
    if (videogameArtworkWidth) videogameArtworkWidth.value = appSettings.videogame_artwork_width || "";
    if (videogameArtworkHeight) videogameArtworkHeight.value = appSettings.videogame_artwork_height || "";
  }
  if (beatlinkSourceForm && !beatlinkSourceForm.contains(document.activeElement)) {
    if (beatlinkParamsUrl) beatlinkParamsUrl.value = appSettings.blt_params_url || "";
    if (musicRoot) musicRoot.value = appSettings.music_root || "";
    if (artworkOutputPath) artworkOutputPath.value = appSettings.artwork_output || "";
    if (fallbackArtworkPath) fallbackArtworkPath.value = appSettings.fallback_artwork_path || "";
    if (defaultFallbackTemplate) defaultFallbackTemplate.value = appSettings.default_fallback_template || "";
    if (cdjArtworkWidth) cdjArtworkWidth.value = appSettings.cdj_artwork_width || "";
    if (cdjArtworkHeight) cdjArtworkHeight.value = appSettings.cdj_artwork_height || "";
    if (fallbackArtworkWidth) fallbackArtworkWidth.value = appSettings.fallback_artwork_width || "";
    if (fallbackArtworkHeight) fallbackArtworkHeight.value = appSettings.fallback_artwork_height || "";
  }
  if (spotifySourceForm && !spotifySourceForm.contains(document.activeElement)) {
    if (spotifyEnabled) spotifyEnabled.checked = Boolean(appSettings.spotify_enabled);
    if (spotifyTrackText) spotifyTrackText.value = appSettings.spotify_track_text || "Spotify Now Playing";
    if (spotifyArtworkPath) spotifyArtworkPath.value = appSettings.spotify_artwork_path || "";
    if (spotifyArtworkWidth) spotifyArtworkWidth.value = appSettings.spotify_artwork_width || "";
    if (spotifyArtworkHeight) spotifyArtworkHeight.value = appSettings.spotify_artwork_height || "";
    if (spotifyClientId) spotifyClientId.value = appSettings.spotify_client_id || "";
    if (spotifyRedirectUri) spotifyRedirectUri.value = appSettings.spotify_redirect_uri || "http://127.0.0.1:8080/spotify/callback";
    if (spotifyMarket) spotifyMarket.value = appSettings.spotify_market || "US";
    if (spotifyTrackTemplate) spotifyTrackTemplate.value = appSettings.spotify_track_template || "{artist} - {title}";
    renderSpotifyStatus({ spotify: appSettings.spotify_status });
  }
}

function nowPlayingModeForCommand(command) {
  if (command === "resume" || command === "safe_reset") return "cdj";
  if (["spotify", "vinyl", "studio", "videogame"].includes(command)) return command;
  return "cdj";
}

function nowPlayingSourceForMode(mode) {
  if (mode === "spotify") return "spotify";
  if (mode === "vinyl" || mode === "studio" || mode === "videogame") return "manual";
  return "beatlink";
}

function renderNowPlayingSourceTabs(show = latestShow) {
  const mode = optimisticNowPlayingMode || show?.manual_mode || "cdj";
  const source = activeNowPlayingSource || nowPlayingSourceForMode(mode);
  const labels = { beatlink: "CDJ Beatlink Settings", spotify: "Spotify Settings", manual: "Manual Settings" };
  if (nowPlayingSourceStatus) nowPlayingSourceStatus.textContent = `Live: ${nowPlayingModeLabel(mode)}`;
  if (nowPlayingSettingsLabel) nowPlayingSettingsLabel.textContent = labels[source] || "Now Playing Settings";
  document.querySelectorAll("[data-now-playing-source]").forEach((button) => {
    button.classList.toggle("active", button.dataset.nowPlayingSource === source);
  });
  document.querySelectorAll("[data-now-playing-panel]").forEach((panel) => {
    panel.classList.toggle("active", panel.dataset.nowPlayingPanel === source);
  });
}

function renderSelectedButtons(show) {
  renderManualModeForm();
  renderNowPlayingSourceTabs(show);
  const mode = optimisticNowPlayingMode || show?.manual_mode || "cdj";
  renderNowPlayingOpacityControl(nowPlayingOpacityControl);
  manualModeButtons.forEach((button) => {
    const command = button.dataset.command;
    const active =
      (mode === "vinyl" && command === "vinyl") ||
      (mode === "studio" && command === "studio") ||
      (mode === "videogame" && command === "videogame") ||
      (mode === "spotify" && command === "spotify") ||
      (mode === "cdj" && command === "resume");
    button.classList.toggle("active", active);
  });
  bpmStart.classList.toggle("active", Boolean(show?.bpm_running));
  bpmStop.classList.toggle("active", !show?.bpm_running);
  bpmFollow.classList.toggle("active", Boolean(show?.bpm_follow_now_playing));
  relationshipButtons.forEach((button) => button.classList.remove("active"));
}

function currentLookName(show) {
  if (!show?.source) return "-";
  if (show.source.startsWith("performance:")) return show.source.slice("performance:".length);
  if (!lookApplyLights() && show?.active_look_name) return show.active_look_name;
  if (show.source === "default") return "Manual";
  return show.source;
}

function renderSelectionSummary(show) {
  if (!show) return;
  const colors = show.colors || {};
  if (selectedLook) selectedLook.textContent = currentLookName(show);
  if (selectedColors) {
    selectedColors.textContent = [colorSlotValue(colors, "color1"), colorSlotValue(colors, "color2"), colorSlotValue(colors, "strobe_color")].filter(Boolean).join(" / ") || "-";
  }
  if (selectedVisual) {
    selectedVisual.textContent = optionLabel(appSettings?.visual_controls, show.last_visual_button, "-");
  }
  if (selectedCameras) {
    const cameraConfig = appSettings?.camera_controls || {};
    const selected = show.last_camera_buttons || {};
    const labels = [
      optionLabel(cameraConfig.groups?.main_box, selected.main_box, ""),
      optionLabel(cameraConfig.groups?.pip_box, selected.pip_box, ""),
      optionLabel(cameraConfig.groups?.background, selected.background, ""),
      optionLabel(cameraConfig.groups?.visuals_cams, selected.visuals_cams, ""),
      optionLabel(cameraConfig.scenes, selected.scene, ""),
    ].filter(Boolean);
    selectedCameras.textContent = labels.length ? labels.join(" / ") : "-";
  }
  if (selectedNowPlaying) {
    selectedNowPlaying.textContent = nowPlayingModeLabel(show.manual_mode || "cdj");
  }
}

function renderTrackMetadata(status) {
  const show = status.show || {};
  const blt = status.blt || {};
  const track = blt.context || {};
  const modeValue = show.manual_mode || "cdj";
  const isCdjMode = modeValue === "cdj";
  const isSpotifyMode = modeValue === "spotify";
  const spotifyStatus = currentSpotifyStatus(status) || {};
  const spotifyCurrent = spotifyStatus.current || null;
  const hasSpotifyTrack = Boolean(isSpotifyMode && spotifyCurrent && spotifyCurrent.item_type !== "none" && (spotifyCurrent.title || spotifyCurrent.track_id || spotifyCurrent.track_uri));
  const hasTrack = Boolean(isCdjMode && blt.ok && (track.title || track.artist || track.full_track));
  const manualText = manualModeText(modeValue) || `${modeValue || "manual"} mode`;
  const spotifyDisplay = spotifyCurrentDisplay(spotifyCurrent);
  const blankSpotify = isSpotifyMode && !hasSpotifyTrack;
  trackNowPlaying.textContent = hasTrack
    ? track.full_track || track.title || "BeatLink track loaded"
    : hasSpotifyTrack
      ? spotifyDisplay.title
      : isCdjMode
        ? blt.status || "Waiting for BeatLink watcher data"
        : blankSpotify
          ? ""
          : manualText;
  const nowPlaying = trackNowPlaying.textContent;
  const artist = hasTrack ? track.artist || "-" : hasSpotifyTrack ? spotifyDisplay.artist : blankSpotify ? "" : isCdjMode ? "-" : "manual mode";
  const album = hasTrack ? track.album || "-" : hasSpotifyTrack ? spotifyDisplay.album : blankSpotify ? "" : isCdjMode ? "-" : modeValue || "-";
  const bpm = hasTrack ? track.bpm || "-" : blankSpotify ? "" : isCdjMode ? "-" : show.bpm ? `${show.bpm}` : "-";
  const player = hasTrack ? track.player || track.player_number || "-" : hasSpotifyTrack ? spotifyCurrent.device_name || "Spotify" : blankSpotify ? "" : isCdjMode ? "-" : modeValue || "-";
  const displayMode = isCdjMode ? "CDJ Beatlink" : isSpotifyMode ? "Spotify" : `${modeValue || "manual"} mode`;
  if (liveTrackNowPlaying) liveTrackNowPlaying.textContent = nowPlaying;
  if (liveTrackArtist) liveTrackArtist.textContent = artist;
  if (liveTrackBpm) liveTrackBpm.textContent = bpm;
  if (liveTrackPlayer) liveTrackPlayer.textContent = player;
  if (liveTrackMode) liveTrackMode.textContent = displayMode;
  perfTrackNowPlaying.textContent = nowPlaying;
  perfTrackArtist.textContent = artist;
  perfTrackAlbum.textContent = album;
  perfTrackBpm.textContent = bpm;
  perfTrackPlayer.textContent = player;
  perfTrackMode.textContent = displayMode;
  trackTitle.textContent = hasTrack ? track.title || "-" : hasSpotifyTrack ? spotifyCurrent.title || "-" : blankSpotify ? "" : isCdjMode ? "-" : manualText;
  trackArtist.textContent = artist;
  trackAlbum.textContent = album;
  trackBpm.textContent = bpm;
  trackPlayer.textContent = player;
  trackDevice.textContent = hasTrack ? track.device_name || "-" : hasSpotifyTrack ? spotifyCurrent.device_name || "Spotify" : blankSpotify ? "" : isCdjMode ? "-" : "remote";
  trackMatchedFile.textContent = hasTrack ? track.matched_file || status.artwork?.matched_file || status.artwork?.status || "-" : hasSpotifyTrack ? spotifyCurrent.artwork_url || "Spotify artwork" : blankSpotify ? "" : status.artwork?.status || "-";
  trackCommentFound.textContent = hasTrack ? track.comment || "No rekordbox comment found" : hasSpotifyTrack ? "Spotify metadata" : blankSpotify ? "" : show.color_comment ? "Current generated color comment" : "-";
  trackParsedValues.textContent = hasTrack ? track.track_info || "-" : hasSpotifyTrack ? spotifyCurrent.track_uri || spotifyCurrent.track_id || "-" : blankSpotify ? "" : show.color_comment || "-";
  trackMissingValues.textContent = hasSpotifyTrack ? "Spotify sends enabled Now Playing OSC outputs when activated." : blankSpotify ? "" : status.artwork?.status || (blt.ok ? "BeatLink data connected" : blt.error || "Resolved by current output state");
  trackAppliedFrom.textContent = hasSpotifyTrack ? "Spotify" : hasTrack ? "BeatLink params" : blankSpotify ? "Spotify" : show.source || "-";
  trackAutoSend.textContent = isCdjMode ? "CDJ Beatlink mode" : isSpotifyMode ? "Spotify mode" : "Manual artwork mode";
  trackDailyLog.textContent = hasTrack ? "Polling BeatLink params.json for live metadata." : hasSpotifyTrack ? "Using live Spotify playback from the local API." : blankSpotify ? "" : isCdjMode ? "Waiting for live BeatLink metadata." : "Manual mode sends the configured text and artwork.";
  trackColorComment.textContent = show.color_comment || "-";
  renderOverviewNowPlaying(status);
  renderSpotifyStatus(status);
}

function outputByKey(key) {
  return (latestShow?.outputs || []).find((output) => output.key === key);
}

function lightControlsByKeys(keys) {
  const byKey = new Map((appSettings?.controls || []).map((control) => [control.key, control]));
  return keys.map((key) => byKey.get(key)).filter(Boolean);
}

function liveLightControls() {
  return lightControlsByKeys(LIVE_LIGHT_CONTROL_KEYS);
}

function liveLightColorControls() {
  return lightControlsByKeys(LIVE_LIGHT_COLOR_KEYS);
}

function liveLightSliderControls() {
  return lightControlsByKeys(LIVE_LIGHT_SLIDER_KEYS);
}

function nearestPercent(value) {
  const choices = (appSettings?.percent_choices || [0, 10, 25, 50, 75, 90, 95, 100]).map(Number);
  const numeric = Number(value);
  return choices.reduce((nearest, choice) => {
    return Math.abs(choice - numeric) < Math.abs(nearest - numeric) ? choice : nearest;
  }, choices[0] ?? 0);
}

function createPercentSlider(control, selected, readout) {
  const choices = (appSettings.percent_choices || []).map(Number);
  const wrapper = document.createElement("div");
  wrapper.className = "percent-slider-control";

  const top = document.createElement("div");
  top.className = "percent-slider-top";
  const value = document.createElement("strong");
  value.textContent = `${selected}%`;
  const slider = document.createElement("input");
  slider.type = "range";
  slider.min = "0";
  slider.max = "100";
  slider.step = "1";
  slider.value = String(selected);
  slider.setAttribute("aria-label", control.label);
  top.append(value, slider);

  const stops = document.createElement("div");
  stops.className = "percent-stops";
  let lastSent = selected;
  const setLocalValue = (percent) => {
    const next = nearestPercent(percent);
    slider.value = String(next);
    value.textContent = `${next}%`;
    readout.textContent = `${control.label} ${next}%`;
    stops.querySelectorAll("button").forEach((button) => {
      button.classList.toggle("active", Number(button.dataset.value) === next);
    });
    return next;
  };
  const sendIfChanged = (percent) => {
    const next = setLocalValue(percent);
    if (next !== lastSent) {
      lastSent = next;
      sendCommand({ command: "set_control", key: control.key, value: next });
    }
  };

  for (const percent of choices) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "percent-stop";
    button.dataset.value = String(percent);
    button.classList.toggle("active", selected === percent);
    button.textContent = `${percent}%`;
    button.addEventListener("click", () => {
      sendIfChanged(percent);
    });
    stops.append(button);
  }

  slider.addEventListener("input", () => sendIfChanged(slider.value));
  slider.addEventListener("change", () => sendIfChanged(slider.value));

  wrapper.append(top, stops);
  return wrapper;
}

function renderLinkControls() {
  if (!appSettings || !latestShow || !linkControls) return;
  if (linkControls.contains(document.activeElement) && document.activeElement?.type === "range") return;
  const colorControls = liveLightColorControls();
  const sliderControls = liveLightSliderControls();
  linkControls.replaceChildren();
  if (!colorControls.length && !sliderControls.length) return;

  const surface = document.createElement("div");
  surface.className = "light-control-surface";

  const colorList = document.createElement("div");
  colorList.className = "light-color-selection-list";
  for (const control of colorControls) {
    const output = outputByKey(control.key) || {};
    const colorName = output.color || "";
    const picker = document.createElement("section");
    picker.className = "light-color-picker";
    picker.dataset.key = control.key;

    const head = document.createElement("div");
    head.className = "light-color-picker-head";
    const title = document.createElement("strong");
    title.textContent = lightColorControlLabel(control);
    const current = document.createElement("span");
    current.textContent = displayColorName(colorName || "-");
    current.style.setProperty("--current-color", output.hex || colorHex(colorName));
    head.append(title, current);

    const options = document.createElement("div");
    options.className = "light-color-options";
    options.setAttribute("aria-label", `${lightColorControlLabel(control)} color choices`);
    for (const optionName of appSettings.colors.names || []) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "light-color-option";
      button.classList.toggle("active", colorName === optionName);
      button.style.setProperty("--option-color", colorHex(optionName));
      button.title = `${lightColorControlLabel(control)} ${colorHueLabel(optionName)}`;
      button.setAttribute("aria-label", `Set ${lightColorControlLabel(control)} to ${colorHueLabel(optionName)}`);
      const hueDegree = colorHueDegree(optionName);
      if (hueDegree !== null) button.dataset.hueDegree = String(hueDegree);
      const swatch = document.createElement("i");
      const label = document.createElement("span");
      label.textContent = displayColorName(optionName);
      button.append(swatch, label);
      button.addEventListener("click", () => sendCommand({ command: "set_control", key: control.key, value: optionName }));
      options.append(button);
    }

    picker.append(head, options);
    colorList.append(picker);
  }
  surface.append(colorList);

  const sliders = document.createElement("div");
  sliders.className = "light-slider-bank";
  for (const control of sliderControls) {
    const output = outputByKey(control.key) || {};
    const row = document.createElement("div");
    row.className = "light-slider-row";
    row.title = control.label;

    const hidden = document.createElement("span");
    hidden.className = "sr-only";
    hidden.textContent = control.label;

    const slider = document.createElement("input");
    slider.type = "range";
    slider.min = "0";
    slider.max = "100";
    slider.step = "1";
    slider.setAttribute("aria-label", control.label);

    const value = document.createElement("output");
    value.className = "light-slider-value";

    const stops = document.createElement("div");
    stops.className = "light-slider-stops";
    const stopButtons = [];

    let lastSent = Math.round(Number(output.value || 0) * 100);
    const setLocalValue = (rawValue) => {
      const next = Math.max(0, Math.min(100, Math.round(Number(rawValue || 0))));
      slider.value = String(next);
      value.value = String(next);
      value.textContent = `${next}%`;
      row.style.setProperty("--slider-level", `${next}%`);
      stopButtons.forEach((button) => button.classList.toggle("active", Number(button.dataset.value) === next));
      return next;
    };
    const sendIfChanged = (rawValue) => {
      const next = setLocalValue(rawValue);
      if (next !== lastSent) {
        lastSent = next;
        sendCommand({ command: "set_control", key: control.key, value: next });
      }
    };

    for (const stop of LIGHT_SLIDER_STOPS) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "light-slider-stop";
      button.dataset.value = String(stop);
      button.textContent = String(stop);
      button.title = `Set ${control.label} to ${stop}%`;
      button.addEventListener("click", () => sendIfChanged(stop));
      stopButtons.push(button);
      stops.append(button);
    }

    setLocalValue(lastSent);
    slider.addEventListener("input", () => sendIfChanged(slider.value));
    slider.addEventListener("change", () => sendIfChanged(slider.value));
    row.append(hidden, slider, value, stops);
    sliders.append(row);
  }
  surface.append(sliders);
  linkControls.append(surface);
}
function renderOpacityControl(container, label, value, hasAddress, commandPayload, options = {}) {
  if (!container || container.contains(document.activeElement)) return;
  const selected = Math.max(0, Math.min(100, Math.round(Number(value ?? 100))));
  const switchOnly = Boolean(options.switchOnly);
  container.replaceChildren();

  const title = document.createElement("div");
  title.className = "opacity-title";
  const name = document.createElement("span");
  name.textContent = label;
  const readout = document.createElement("strong");
  readout.textContent = `${selected}%`;
  title.append(name, readout);

  const body = document.createElement("div");
  body.className = "opacity-body";
  let slider = null;
  if (!switchOnly) {
    slider = document.createElement("input");
    slider.type = "range";
    slider.min = "0";
    slider.max = "100";
    slider.step = "1";
    slider.value = String(selected);
    slider.setAttribute("aria-label", label);
    body.append(slider);
  }

  const quick = document.createElement("div");
  quick.className = "opacity-presets";
  const presets = options.presets || [[0, "Off"], [50, "Half"], [100, "Full"]];
  const presetButtons = presets.map(([amount, text]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "opacity-preset";
    button.textContent = text;
    button.title = `Set ${label} to ${amount}%`;
    button.dataset.amount = String(amount);
    quick.append(button);
    return button;
  });

  let lastSent = selected;
  const sendOpacity = (rawValue) => {
    const next = Math.max(0, Math.min(100, Math.round(Number(rawValue || 0))));
    if (slider) slider.value = String(next);
    readout.textContent = `${next}%`;
    presetButtons.forEach((button) => button.classList.toggle("active", Number(button.dataset.amount) === next));
    if (next !== lastSent) {
      lastSent = next;
      sendCommand(commandPayload(next));
    }
  };

  if (slider) {
    slider.addEventListener("input", () => sendOpacity(slider.value));
    slider.addEventListener("change", () => sendOpacity(slider.value));
  }
  presetButtons.forEach((button) => button.addEventListener("click", () => sendOpacity(button.dataset.amount)));
  sendOpacity(selected);

  container.classList.toggle("needs-address", !hasAddress);
  container.append(title);
  if (!switchOnly) container.append(body);
  container.append(quick);
}

function renderVisualOpacityControl() {
  if (!visualOpacityControl || visualOpacityControl.contains(document.activeElement)) return;
  visualOpacityControl.replaceChildren();
  const sliders = appSettings?.visual_slider_controls || [];
  const values = latestShow?.visual_sliders || {};
  for (const slider of sliders) {
    const slot = document.createElement("div");
    slot.className = "opacity-control visual-slider-control";
    renderOpacityControl(
      slot,
      slider.label || slider.name || "Visual Slider",
      values[slider.id] ?? (slider.id === "visual_slider_1" ? latestShow?.visual_opacity : 100),
      Boolean(slider.address),
      (next) => ({ command: "visual_slider", id: slider.id, value: next }),
    );
    visualOpacityControl.append(slot);
  }
}

function nowPlayingOpacityValue() {
  return latestShow?.now_playing_opacity ?? 100;
}

function nowPlayingOpacityAddress() {
  return appSettings?.now_playing_opacity_address || "";
}

function renderNowPlayingOpacityControl(container, compact = false) {
  if (!container) return;
  container.classList.add("opacity-control", "now-playing-opacity-control");
  container.classList.toggle("compact-opacity-control", Boolean(compact));
  renderOpacityControl(
    container,
    "Now Playing Opacity",
    nowPlayingOpacityValue(),
    Boolean(nowPlayingOpacityAddress()),
    (next) => ({ command: "now_playing_opacity", value: next }),
    { presets: [[0, "Off"], [50, "Blend"], [100, "On"]] },
  );
}

const cameraOpacityLabels = {
  main_box: "Main Box Mix",
  pip_box: "PIP Box Mix",
  background: "BG Cam Mix",
  visuals_cams: "Visuals Cam Mix",
};

const cameraOpacityShortLabels = {
  main_box: "Main Mix",
  pip_box: "PIP Mix",
  background: "BG Mix",
  visuals_cams: "Visuals Mix",
};

const cameraOpacityClassNames = {
  main_box: "main-box-camera-opacity-control",
  pip_box: "pip-box-camera-opacity-control",
  background: "background-camera-opacity-control",
  visuals_cams: "visuals-camera-opacity-control",
};

function cameraOpacityLabel(groupKey) {
  return appSettings?.camera_opacity_labels?.[groupKey] || cameraOpacityLabels[groupKey] || "Cam Mix";
}

function cameraOpacityShortLabel(groupKey) {
  return cameraOpacityShortLabels[groupKey] || cameraOpacityLabel(groupKey);
}

function cameraOpacityValue(groupKey) {
  return latestShow?.camera_opacity?.[groupKey] ?? 100;
}

function cameraOpacityAddress(groupKey) {
  return appSettings?.camera_opacity_addresses?.[groupKey] || "";
}

function renderCameraOpacityControl(groupKey, container, compact = false) {
  if (!container) return;
  container.classList.add("opacity-control", "camera-opacity-control", cameraOpacityClassNames[groupKey] || "camera-mix-opacity-control");
  container.classList.toggle("compact-opacity-control", Boolean(compact));
  renderOpacityControl(
    container,
    cameraOpacityLabel(groupKey),
    cameraOpacityValue(groupKey),
    Boolean(cameraOpacityAddress(groupKey)),
    (next) => ({ command: "camera_opacity", group: groupKey, value: next }),
    { presets: [[0, "Off"], [100, "On"]], switchOnly: true },
  );
}

function renderCameraControls() {
  if (!appSettings) return;
  const cameraConfig = appSettings.camera_controls || {};
  const groups = cameraConfig.groups || {};
  const selected = latestShow?.last_camera_buttons || {};
  for (const [groupKey, container] of Object.entries(cameraContainers)) {
    if (!container) continue;
    container.replaceChildren();
    for (const item of groups[groupKey] || []) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = item.label || `Set ${item.column}`;
      button.className = "camera-button";
      button.classList.toggle("active", selected[groupKey] === item.id);
      button.classList.toggle("preview", isPreviewCueDispatch() && stagedPerformanceCue[`${groupKey}_id`] === item.id);
      button.ariaPressed = String(stagedPerformanceCue[`${groupKey}_id`] === item.id);
      button.title = `${cueButtonTitle("camera", stagedPerformanceCue[`${groupKey}_id`] === item.id)} - Right-click, long-press, or Shift-click to edit OSC`;
      button.addEventListener("click", (event) => handleQuickEditTriggerClick(event, button, () => openCameraOscEditor(groupKey, item), () => dispatchCameraCue(groupKey, item.id)));
      attachQuickEditShortcut(button, () => openCameraOscEditor(groupKey, item));
      container.append(button);
    }
  }
  if (sceneControls) {
    sceneControls.replaceChildren();
    for (const item of cameraConfig.scenes || []) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = item.label || `Scene ${item.index}`;
      button.className = "camera-button scene-button";
      button.classList.toggle("active", selected.scene === item.id);
      button.classList.toggle("preview", isPreviewCueDispatch() && stagedPerformanceCue.scene_id === item.id);
      button.ariaPressed = String(stagedPerformanceCue.scene_id === item.id);
      button.title = `${cueButtonTitle("scene", stagedPerformanceCue.scene_id === item.id)} - Right-click, long-press, or Shift-click to edit OSC`;
      button.addEventListener("click", (event) => handleQuickEditTriggerClick(event, button, () => openCameraOscEditor("scene", item), () => dispatchCameraCue("scene", item.id)));
      attachQuickEditShortcut(button, () => openCameraOscEditor("scene", item));
      sceneControls.append(button);
    }
  }
  for (const [groupKey, control] of Object.entries(cameraOpacityControls)) {
    renderCameraOpacityControl(groupKey, control);
  }
}

function renderVisualControls() {
  if (!appSettings || !visualControls) return;
  renderVisualOpacityControl();
  renderNowPlayingOpacityControl(visualNowPlayingOpacityControl);
  renderGenerativeVisualControls();
  renderVisualLayerGrid(visualControls, visualControlsWithLayerOff(), {
    variant: "full",
    selected: latestShow?.last_visual_button || "",
    selectedByLayer: selectedVisualByLayer(latestShow),
    staged: isPreviewCueDispatch() ? stagedPerformanceCue.visual_id : "",
  });
}

function generativePresetOptions() {
  return appSettings?.generative_visual_presets || {};
}

function currentGenerativeVisual() {
  return latestShow?.generative_visual || appSettings?.current_generative_visual || {};
}

function valuesWithPresetDefaults(presetId) {
  const preset = generativePresetOptions()[presetId] || {};
  const base = collectGenerativeValues();
  const values = {
    ...base,
    preset: presetId,
    enabled: true,
    blackout: false,
    color_source: preset.default_color_source || base.color_source || "look",
    quality: preset.default_quality || base.quality || "medium",
    automation_enabled: Boolean(preset.default_automation_enabled ?? base.automation_enabled ?? false),
    automation_target: preset.default_automation_target || base.automation_target || "warp",
    automation_mode: preset.default_automation_mode || base.automation_mode || "bpm",
    automation_division: preset.default_automation_division || base.automation_division || "1 bar",
    automation_shape: preset.default_automation_shape || base.automation_shape || "sine",
    automation_depth: Number(preset.default_automation_depth ?? base.automation_depth ?? 0.35),
    automation_offset: Number(preset.default_automation_offset ?? base.automation_offset ?? 0.5),
  };
  for (const [key, _label, defaultValue] of GENERATIVE_SLIDER_FIELDS) {
    values[key] = Number(preset[`default_${key}`] ?? base[key] ?? defaultValue);
  }
  return values;
}

function setLocalGenerativeVisual(values) {
  if (latestShow) latestShow.generative_visual = { ...(latestShow.generative_visual || {}), ...values };
  if (appSettings) appSettings.current_generative_visual = { ...(appSettings.current_generative_visual || {}), ...values };
}

function applyGenerativePreset(presetId) {
  dispatchGeneratorCue(presetId);
}

function makeGenSelect(name, labelText, value, options, onChange) {
  const label = document.createElement("label");
  label.className = "quick-field";
  const span = document.createElement("span");
  span.textContent = labelText;
  const select = document.createElement("select");
  select.name = name;
  for (const [optionValue, optionLabelText] of options) {
    const option = document.createElement("option");
    option.value = optionValue;
    option.textContent = optionLabelText;
    select.append(option);
  }
  select.value = value;
  select.addEventListener("change", onChange);
  label.append(span, select);
  return label;
}

function makeGenSlider(name, labelText, value, onInput) {
  const label = document.createElement("label");
  label.className = "generative-slider quick-field";
  const top = document.createElement("div");
  top.className = "generative-slider-top";
  const span = document.createElement("span");
  span.textContent = labelText;
  const readout = document.createElement("strong");
  readout.textContent = `${Math.round(Number(value || 0) * 100)}%`;
  top.append(span, readout);
  const input = document.createElement("input");
  input.name = name;
  input.type = "range";
  input.min = "0";
  input.max = "1";
  input.step = "0.01";
  input.value = String(value ?? 0);
  input.addEventListener("input", () => {
    readout.textContent = `${Math.round(Number(input.value) * 100)}%`;
    onInput();
  });
  label.append(top, input);
  return label;
}

function makeGenToggle(name, labelText, checked, onChange) {
  const label = document.createElement("label");
  label.className = "quick-field quick-toggle";
  const span = document.createElement("span");
  span.textContent = labelText;
  const input = document.createElement("input");
  input.name = name;
  input.type = "checkbox";
  input.checked = Boolean(checked);
  input.addEventListener("change", onChange);
  label.append(span, input);
  return label;
}

function collectGenerativeValues(container = generativeVisualControls) {
  const current = currentGenerativeVisual();
  const get = (name) => container?.querySelector(`[name="${name}"]`);
  const syncGet = (name) => generatorBpmSync?.querySelector(`[name="${name}"]`);
  const layerGet = (name) => generatorLayerStack?.querySelector(`[name="${name}"]`);
  const values = {
    enabled: true,
    preset: get("gen_preset")?.value || current.preset || "lissajous_orbit",
    color_source: get("gen_color_source")?.value || current.color_source || "look",
    phrase_morph: Boolean(get("gen_phrase_morph")?.checked ?? current.phrase_morph ?? true),
    auto_seed: Boolean(get("gen_auto_seed")?.checked ?? current.auto_seed ?? true),
    quality: get("gen_quality")?.value || current.quality || "medium",
    automation_enabled: Boolean(syncGet("gen_automation_enabled")?.checked ?? current.automation_enabled ?? false),
    automation_target: syncGet("gen_automation_target")?.value || current.automation_target || "warp",
    automation_mode: syncGet("gen_automation_mode")?.value || current.automation_mode || "bpm",
    automation_division: generatorBpmSync?.querySelector(`[name="gen_automation_division"].active`)?.value || current.automation_division || "1 bar",
    automation_shape: syncGet("gen_automation_shape")?.value || current.automation_shape || "sine",
    automation_depth: Number(syncGet("gen_automation_depth")?.value ?? current.automation_depth ?? 0.35),
    automation_offset: Number(syncGet("gen_automation_offset")?.value ?? current.automation_offset ?? 0.5),
    layer_enabled: Boolean(layerGet("gen_layer_enabled")?.checked ?? current.layer_enabled ?? true),
    layer_style: layerGet("gen_layer_style")?.value || current.layer_style || "glow_grid",
    layer_mix: Number(layerGet("gen_layer_mix")?.value ?? current.layer_mix ?? 0.32),
    layer_speed: Number(layerGet("gen_layer_speed")?.value ?? current.layer_speed ?? 0.4),
    freeze: Boolean(get("gen_freeze")?.checked ?? current.freeze ?? false),
    blackout: false,
  };
  for (const [key, _label, defaultValue] of GENERATIVE_SLIDER_FIELDS) {
    values[key] = Number(get(`gen_${key}`)?.value ?? current[key] ?? defaultValue);
  }
  return values;
}

let generativeSendTimer = null;
function sendGenerativeVisualUpdate(delay = 120) {
  if (generativeSendTimer) clearTimeout(generativeSendTimer);
  generativeSendTimer = setTimeout(() => {
    sendCommand({ command: "generative_visual", values: collectGenerativeValues() }, { quiet: true });
    if (generativeVisualStatus) generativeVisualStatus.textContent = "Generative visual output updated.";
  }, delay);
}

function renderGenerativeVisualControls(options = {}) {
  const force = Boolean(options.force);
  if (!appSettings || !generativeVisualControls || (!force && generativeVisualControls.contains(document.activeElement))) return;
  const current = currentGenerativeVisual();
  const presets = generativePresetOptions();
  const presetOptions = Object.values(presets).map((preset) => [preset.id, preset.name]);
  generativeVisualControls.replaceChildren();
  const sliders = GENERATIVE_SLIDER_FIELDS.map(([key, label, defaultValue]) => (
    makeGenSlider(`gen_${key}`, label, current[key] ?? defaultValue, () => sendGenerativeVisualUpdate())
  ));
  generativeVisualControls.append(
    makeGenSelect("gen_preset", "Active Preset", current.preset || "lissajous_orbit", presetOptions, (event) => {
      applyGenerativePreset(event.target.value);
    }),
    makeGenSelect("gen_color_source", "Color Source", current.color_source || "look", [["look", "Look Colors"], ["album", "Album Art"], ["track", "Track Tags"], ["manual", "Manual"]], () => sendGenerativeVisualUpdate(0)),
    ...sliders,
    makeGenToggle("gen_phrase_morph", "Phrase Morph", current.phrase_morph ?? true, () => sendGenerativeVisualUpdate(0)),
    makeGenToggle("gen_auto_seed", "Auto Seed on Track", current.auto_seed ?? true, () => sendGenerativeVisualUpdate(0)),
    makeGenSelect("gen_quality", "Quality", current.quality || "medium", [["low", "Low"], ["medium", "Medium"], ["high", "High"]], () => sendGenerativeVisualUpdate(0)),
  );
  if (generativeVisualStatus) {
    const preset = presets[current.preset] || {};
    const stateText = current.blackout ? "Stopped" : current.freeze ? "Frozen" : current.enabled === false ? "Disabled" : "Live";
    generativeVisualStatus.textContent = `${stateText}: ${preset.name || current.preset || "Generative visual"} - ${current.quality || "medium"} quality.`;
  }
  if (freezeGenerativeVisual) freezeGenerativeVisual.classList.toggle("active", Boolean(current.freeze));
  if (stopGenerativeVisual) stopGenerativeVisual.classList.toggle("active", Boolean(current.blackout || current.enabled === false));
  renderGeneratorColorPreview();
  renderGeneratorLayerStack({ force });
  renderGeneratorBpmSync({ force });
  renderGeneratorPresetGallery();
  renderMathSceneGallery();
}

function renderGeneratorLayerStack(options = {}) {
  if (!generatorLayerStack || !appSettings) return;
  if (!options.force && generatorLayerStack.contains(document.activeElement) && ["INPUT", "SELECT"].includes(document.activeElement?.tagName)) return;
  const current = currentGenerativeVisual();
  const styleLabel = GENERATIVE_LAYER_STYLES.find(([key]) => key === (current.layer_style || "glow_grid"))?.[1] || "Glow Grid";
  const summary = document.createElement("div");
  summary.className = "generator-layer-summary";
  summary.innerHTML = `<strong>${current.layer_enabled === false ? "Layer Off" : styleLabel}</strong><span>${Math.round(Number(current.layer_mix ?? 0.32) * 100)}% mix over ${current.preset ? (generativePresetOptions()[current.preset]?.name || current.preset) : "generator"}</span>`;
  const controls = document.createElement("div");
  controls.className = "generator-layer-controls";
  controls.append(
    makeGenToggle("gen_layer_enabled", "Overlay Layer", current.layer_enabled ?? true, () => sendGenerativeVisualUpdate(0)),
    makeGenSelect("gen_layer_style", "Style", current.layer_style || "glow_grid", GENERATIVE_LAYER_STYLES, () => sendGenerativeVisualUpdate(0)),
    makeGenSlider("gen_layer_mix", "Mix", current.layer_mix ?? 0.32, () => sendGenerativeVisualUpdate()),
    makeGenSlider("gen_layer_speed", "Motion", current.layer_speed ?? 0.4, () => sendGenerativeVisualUpdate()),
  );
  generatorLayerStack.replaceChildren(summary, controls);
}

function generatorAutomationLabel(value) {
  return GENERATIVE_AUTOMATION_TARGETS.find(([key]) => key === value)?.[1] || value;
}

function generatorSyncDurationMs(division, mode, bpm) {
  if (mode === "seconds") return (BPM_DIVISION_MULTIPLIERS[division] || BPM_DIVISION_MULTIPLIERS["1 bar"]) * 1000;
  return intervalMsForDivision(bpm, division);
}

function renderGeneratorBpmSync(options = {}) {
  if (!generatorBpmSync || !appSettings) return;
  if (!options.force && generatorBpmSync.contains(document.activeElement) && ["INPUT", "SELECT"].includes(document.activeElement?.tagName)) return;
  const current = currentGenerativeVisual();
  const bpm = currentSequenceBpm();
  const selected = selectedDivision || current.automation_division || "1 bar";
  const mode = current.automation_mode || "bpm";
  const controls = document.createElement("div");
  controls.className = "generator-sync-controls";
  controls.append(
    makeGenToggle("gen_automation_enabled", "Animate Parameter", current.automation_enabled ?? false, () => sendGenerativeVisualUpdate(0)),
    makeGenSelect("gen_automation_target", "Parameter", current.automation_target || "warp", GENERATIVE_AUTOMATION_TARGETS, () => sendGenerativeVisualUpdate(0)),
    makeGenSelect("gen_automation_mode", "Clock", current.automation_mode || "bpm", [["bpm", "BPM Bars"], ["seconds", "Seconds"]], () => sendGenerativeVisualUpdate(0)),
    makeGenSelect("gen_automation_shape", "Shape", current.automation_shape || "sine", [["sine", "Sine"], ["triangle", "Triangle"], ["saw", "Saw"], ["pulse", "Pulse"]], () => sendGenerativeVisualUpdate(0)),
    makeGenSlider("gen_automation_depth", "Depth", current.automation_depth ?? 0.35, () => sendGenerativeVisualUpdate()),
    makeGenSlider("gen_automation_offset", "Center", current.automation_offset ?? 0.5, () => sendGenerativeVisualUpdate()),
  );
  const summary = document.createElement("div");
  summary.className = "generator-sync-summary bpm-clock-summary";
  const target = generatorAutomationLabel(current.automation_target || "warp");
  const clockLabel = mode === "seconds" ? "Seconds" : `${Math.round(bpm * 10) / 10} BPM`;
  summary.innerHTML = `<span>App Clock</span><strong>${clockLabel}</strong><small>${target} moves every ${formatDuration(generatorSyncDurationMs(selected, mode, bpm))}</small>`;

  const divisionGrid = makeBpmDivisionGrid({
    className: "bpm-clock-division-grid generator-sync-division-grid",
    selected,
    onPick: (division) => {
      selectedDivision = division;
      const next = { ...collectGenerativeValues(), automation_division: division, automation_enabled: true, automation_mode: "bpm" };
      refreshBpmSurfaces();
      sendCommand({ command: "bpm_update", bpm: bpmInput.value, division }, { quiet: true });
      sendCommand({ command: "generative_visual", values: next });
    },
  });
  generatorBpmSync.replaceChildren(summary, controls, divisionGrid);
}

function renderGeneratorColorPreview() {
  if (!generatorColorPreview) return;
  const colors = latestShow?.colors || latestShow?.outputs || {};
  const items = [
    ["Color 1", colorSlotValue(colors, "color1") || "-"],
    ["Color 2", colorSlotValue(colors, "color2") || "-"],
    ["Color 3", colorSlotValue(colors, "strobe_color") || "-"],
  ];
  generatorColorPreview.replaceChildren();
  for (const [label, name] of items) {
    const card = document.createElement("div");
    card.className = "generator-color-card";
    card.style.setProperty("--swatch", colorHex(name));
    const swatch = document.createElement("i");
    const small = document.createElement("small");
    small.textContent = label;
    const strong = document.createElement("strong");
    strong.textContent = name;
    card.append(swatch, small, strong);
    generatorColorPreview.append(card);
  }
}

function paintGeneratorThumb(canvas, presetId) {
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;
  const colors = latestShow?.outputs || {};
  const primary = colorHex(colorSlotValue(colors, "color1") || "cyan");
  const secondary = colorHex(colorSlotValue(colors, "color2") || "blue");
  const accent = colorHex(colorSlotValue(colors, "strobe_color") || "magenta");
  ctx.clearRect(0, 0, width, height);
  const bg = ctx.createLinearGradient(0, 0, width, height);
  bg.addColorStop(0, "#05070a");
  bg.addColorStop(1, "#11141b");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, width, height);
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  const cx = width / 2;
  const cy = height / 2;
  const stroke = (color, alpha = 0.75, line = 2) => {
    ctx.strokeStyle = hexToRgba(color, alpha);
    ctx.lineWidth = line;
    ctx.shadowColor = hexToRgba(color, 0.55);
    ctx.shadowBlur = 10;
  };
  const dot = (x, y, color, size = 2.2, alpha = 0.8) => {
    ctx.fillStyle = hexToRgba(color, alpha);
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.fill();
  };
  if (presetId === "moire_grid") {
    for (let layer = 0; layer < 3; layer += 1) {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(-0.45 + layer * 0.34);
      stroke(layer % 2 ? secondary : primary, 0.42, 1.2);
      for (let x = -width; x < width; x += 13) {
        ctx.beginPath();
        ctx.moveTo(x, -height);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      ctx.restore();
    }
  } else if (presetId === "superformula_mandala" || presetId === "crystal_rings") {
    const points = presetId === "crystal_rings" ? 10 : 320;
    for (let ring = 1; ring <= 3; ring += 1) {
      stroke(ring % 2 ? primary : accent, 0.68, 1.4 + ring * 0.3);
      ctx.beginPath();
      for (let i = 0; i <= points; i += 1) {
        const t = (i / points) * Math.PI * 2;
        const r = (18 + ring * 13) * (1 + Math.sin(t * (presetId === "crystal_rings" ? 10 : 8)) * 0.12);
        const x = cx + Math.cos(t) * r;
        const y = cy + Math.sin(t) * r;
        if (!i) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
  } else if (presetId === "particle_vortex" || presetId === "orbital_dust") {
    for (let i = 0; i < 145; i += 1) {
      const t = i * 0.31;
      const r = 3 + i * 0.33;
      const x = cx + Math.cos(t) * r * 1.35;
      const y = cy + Math.sin(t) * r * 0.72;
      dot(x, y, i % 3 ? primary : accent, i % 5 === 0 ? 2.4 : 1.3, 0.62);
    }
  } else if (presetId === "shader_plasma" || presetId === "scanline_bloom") {
    const grad = ctx.createRadialGradient(cx, cy, 6, cx, cy, 72);
    grad.addColorStop(0, hexToRgba(accent, 0.8));
    grad.addColorStop(0.45, hexToRgba(primary, 0.38));
    grad.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, width, height);
    stroke(secondary, 0.42, 1);
    for (let y = 12; y < height; y += presetId === "scanline_bloom" ? 8 : 16) {
      ctx.beginPath();
      ctx.moveTo(8, y + Math.sin(y * 0.1) * 3);
      ctx.lineTo(width - 8, y + Math.cos(y * 0.08) * 3);
      ctx.stroke();
    }
  } else if (presetId === "harmonic_tunnel" || presetId === "starfield_gate") {
    for (let r = 5; r >= 1; r -= 1) {
      stroke(r % 2 ? primary : accent, 0.28 + r * 0.08, 1.2);
      ctx.beginPath();
      const sides = presetId === "starfield_gate" ? 4 : 7;
      for (let i = 0; i <= sides; i += 1) {
        const t = (i / sides) * Math.PI * 2 + r * 0.1;
        const radius = r * 10;
        const x = cx + Math.cos(t) * radius * 1.35;
        const y = cy + Math.sin(t) * radius * 0.8;
        if (!i) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
    if (presetId === "starfield_gate") {
      for (let i = 0; i < 40; i += 1) dot((i * 47) % width, (i * 31) % height, secondary, 1.1, 0.62);
    }
  } else if (presetId === "vector_field" || presetId === "constellation_web") {
    const pts = [];
    for (let y = 14; y < height; y += 15) {
      for (let x = 15; x < width; x += 20) {
        const angle = Math.sin(x * 0.05) + Math.cos(y * 0.08);
        if (presetId === "constellation_web") pts.push([x + Math.sin(y) * 4, y + Math.cos(x) * 4]);
        stroke((x + y) % 3 ? primary : accent, 0.42, 1.1);
        ctx.beginPath();
        ctx.moveTo(x - Math.cos(angle) * 5, y - Math.sin(angle) * 5);
        ctx.lineTo(x + Math.cos(angle) * 8, y + Math.sin(angle) * 8);
        ctx.stroke();
      }
    }
    if (presetId === "constellation_web") {
      stroke(secondary, 0.28, 0.8);
      for (let i = 0; i < pts.length - 1; i += 3) {
        ctx.beginPath();
        ctx.moveTo(pts[i][0], pts[i][1]);
        ctx.lineTo(pts[i + 1][0], pts[i + 1][1]);
        ctx.stroke();
      }
    }
  } else if (presetId === "wave_ribbons" || presetId === "liquid_topo") {
    for (let row = 0; row < 6; row += 1) {
      stroke(row % 2 ? secondary : primary, 0.34 + row * 0.04, 1.3);
      ctx.beginPath();
      for (let x = 0; x <= width; x += 4) {
        const y = 20 + row * 14 + Math.sin(x * 0.045 + row) * (presetId === "liquid_topo" ? 5 + row : 10);
        if (!x) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
  } else if (presetId === "pulse_bars") {
    for (let i = 0; i < 12; i += 1) {
      const h = 18 + Math.sin(i * 0.9) * 12 + (i % 3) * 7;
      ctx.fillStyle = hexToRgba(i % 2 ? primary : accent, 0.48);
      ctx.fillRect(12 + i * 16, cy - h / 2, 9, h);
    }
  } else if (presetId === "kaleido_mesh") {
    for (let i = 0; i < 14; i += 1) {
      stroke(i % 2 ? primary : accent, 0.46, 1);
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + Math.cos(i * Math.PI / 7) * 80, cy + Math.sin(i * Math.PI / 7) * 50);
      ctx.stroke();
    }
  } else {
    stroke(primary, 0.72, 1.8);
    ctx.beginPath();
    for (let i = 0; i <= 240; i += 1) {
      const t = (i / 240) * Math.PI * 2;
      const x = cx + Math.sin(3 * t) * 58;
      const y = cy + Math.cos(4 * t) * 36;
      if (!i) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }
  ctx.restore();
}

function hexToRgba(hex, alpha = 1) {
  const value = String(hex || "#ffffff").replace("#", "");
  const full = value.length === 3 ? value.split("").map((char) => char + char).join("") : value.padEnd(6, "f").slice(0, 6);
  const red = parseInt(full.slice(0, 2), 16);
  const green = parseInt(full.slice(2, 4), 16);
  const blue = parseInt(full.slice(4, 6), 16);
  return `rgba(${red}, ${green}, ${blue}, ${alpha})`;
}

function renderGeneratorQuickPresets() {
  if (!generatorQuickPresetGrid || !appSettings) return;
  const current = currentGenerativeVisual();
  const allIds = Object.keys(generativePresetOptions());
  const presetIds = [...allIds.slice(0, 7)];
  if (current.preset && !presetIds.includes(current.preset)) presetIds.push(current.preset);
  generatorQuickPresetGrid.replaceChildren();
  for (const presetId of presetIds) {
    const preset = generativePresetOptions()[presetId] || {};
    const button = document.createElement("button");
    button.type = "button";
    button.className = "generator-quick-preset";
    button.classList.toggle("active", current.preset === presetId && current.enabled !== false && !current.blackout);
    button.classList.toggle("preview", isPreviewCueDispatch() && stagedPerformanceCue.generator_preset === presetId);
    button.ariaPressed = String(stagedPerformanceCue.generator_preset === presetId);
    button.title = cueButtonTitle("generator", stagedPerformanceCue.generator_preset === presetId);
    button.textContent = preset.name || presetId;
    button.addEventListener("click", () => applyGenerativePreset(presetId));
    generatorQuickPresetGrid.append(button);
  }
}
function renderGeneratorPresetGallery() {
  if (!generatorPresetGallery || !appSettings) return;
  const current = currentGenerativeVisual();
  const presets = Object.values(generativePresetOptions());
  generatorPresetGallery.replaceChildren();
  for (const preset of presets) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "generator-preset-card";
    card.classList.toggle("active", current.preset === preset.id);
    card.classList.toggle("preview", stagedPerformanceCue.generator_preset === preset.id);
    card.title = cueButtonTitle("generator", stagedPerformanceCue.generator_preset === preset.id);
    const thumb = document.createElement("canvas");
    thumb.className = "generator-preset-thumb";
    thumb.width = 220;
    thumb.height = 118;
    const small = document.createElement("small");
    small.textContent = preset.category || "Generator";
    const strong = document.createElement("strong");
    strong.textContent = preset.name || preset.id;
    const meta = document.createElement("div");
    meta.className = "generator-preset-meta";
    for (const tag of [preset.renderer, preset.default_quality]) {
      if (!tag) continue;
      const pill = document.createElement("em");
      pill.textContent = tag;
      meta.append(pill);
    }
    const notes = document.createElement("span");
    notes.textContent = preset.notes || "";
    const mood = document.createElement("span");
    mood.className = "generator-preset-mood";
    mood.textContent = preset.mood ? `Mood: ${preset.mood}` : "";
    const bestFor = document.createElement("span");
    bestFor.className = "generator-preset-best";
    bestFor.textContent = preset.best_for ? `Best for: ${preset.best_for}` : "";
    card.append(thumb, small, strong, meta, mood, bestFor, notes);
    paintGeneratorThumb(thumb, preset.id);
    card.addEventListener("click", () => {
      applyGenerativePreset(preset.id);
    });
    generatorPresetGallery.append(card);
  }
}

function mathSceneTemplates() {
  return appSettings?.math_scene_templates || [];
}

function renderMathSceneFilters() {
  if (!mathSceneFilters) return;
  const categories = ["All", ...new Set(mathSceneTemplates().map((scene) => scene.category || "Math").filter(Boolean))];
  if (!categories.includes(selectedMathSceneCategory)) selectedMathSceneCategory = "All";
  mathSceneFilters.replaceChildren();
  for (const category of categories) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "math-scene-filter";
    button.classList.toggle("active", selectedMathSceneCategory === category);
    button.textContent = category;
    button.addEventListener("click", () => {
      selectedMathSceneCategory = category;
      renderMathSceneGallery();
    });
    mathSceneFilters.append(button);
  }
}

async function triggerMathScene(sceneId, mode = "trigger") {
  try {
    const result = await sendCommandForResult({ command: "math_scene_trigger", id: sceneId, mode });
    if (result.config) {
      appSettings = result.config;
      presetData = result.config.preset_groups || presetData;
      renderGenerativeVisualControls({ force: true });
      renderMathSceneGallery();
      renderLookLinkForm();
      renderLocalOscForms();
      renderSettingsForm();
      renderObsSettingsForm();
    }
    if (result.state) renderShowState(result.state);
    const message = result.message || "Math scene updated";
    if (mathSceneStatus) mathSceneStatus.textContent = message;
    showToast(message);
    await loadStatus();
    return true;
  } catch (error) {
    const message = String(error.message || error);
    if (mathSceneStatus) mathSceneStatus.textContent = message;
    showToast(message, true);
    return false;
  }
}

function renderMathSceneGallery() {
  if (!mathSceneGallery || !appSettings) return;
  renderMathSceneFilters();
  const current = currentGenerativeVisual();
  const scenes = mathSceneTemplates().filter((scene) => (
    selectedMathSceneCategory === "All" || scene.category === selectedMathSceneCategory
  ));
  mathSceneGallery.replaceChildren();
  for (const scene of scenes) {
    const card = document.createElement("article");
    card.className = "math-scene-card";
    card.classList.toggle("active", current.preset === scene.preset);

    const thumb = document.createElement("canvas");
    thumb.className = "generator-preset-thumb";
    thumb.width = 220;
    thumb.height = 118;
    paintGeneratorThumb(thumb, scene.preset);

    const eyebrow = document.createElement("small");
    eyebrow.textContent = `${scene.category || "Math"} - ${scene.math_family || "Formula"}`;
    const title = document.createElement("strong");
    title.textContent = scene.name || scene.id;
    const description = document.createElement("span");
    description.textContent = scene.description || "";
    const mood = document.createElement("span");
    mood.className = "math-scene-mood";
    mood.textContent = scene.mood ? `Mood: ${scene.mood}` : "";
    const best = document.createElement("span");
    best.textContent = scene.best_for ? `Best for: ${scene.best_for}` : "";

    const meta = document.createElement("div");
    meta.className = "generator-preset-meta";
    for (const tag of [scene.renderer, scene.performance_cost, ...(scene.style_tags || []).slice(0, 2)]) {
      if (!tag) continue;
      const pill = document.createElement("em");
      pill.textContent = tag;
      meta.append(pill);
    }

    const controls = document.createElement("div");
    controls.className = "math-scene-controls";
    for (const control of scene.recommended_controls || []) {
      const pill = document.createElement("em");
      pill.textContent = control.replaceAll("_", " ");
      controls.append(pill);
    }

    const actions = document.createElement("div");
    actions.className = "math-scene-actions";
    const preview = document.createElement("button");
    preview.type = "button";
    preview.textContent = "Preview";
    preview.addEventListener("click", () => triggerMathScene(scene.id, "preview"));
    const trigger = document.createElement("button");
    trigger.type = "button";
    trigger.textContent = "Trigger";
    trigger.addEventListener("click", () => triggerMathScene(scene.id, "trigger"));
    actions.append(preview, trigger);

    card.append(thumb, eyebrow, title, meta, mood, best, description, controls, actions);
    mathSceneGallery.append(card);
  }
}

function optionLabel(items, id, emptyText = "None") {
  if (!id) return emptyText;
  const item = (items || []).find((candidate) => candidate.id === id);
  return item ? item.label || item.name || id : id;
}

function renderPresetLinks() {
  if (!appSettings || !presetData || !presetLinks) return;
  if (presetLinks.contains(document.activeElement) && ["INPUT", "SELECT"].includes(document.activeElement?.tagName)) return;
  renderSaveLookPicker();
  presetLinks.replaceChildren();
  const performancePresets = presetData.groups?.performance || {};
  const links = appSettings.preset_links || {};
  const cameraConfig = appSettings.camera_controls || {};
  for (const name of Object.keys(performancePresets)) {
    const values = performancePresets[name] || {};
    const link = links[name] || {};
    const card = document.createElement("article");
    card.className = "preset-link-card";
    const title = document.createElement("div");
    title.className = "preset-link-title";
    const nameInput = document.createElement("input");
    nameInput.className = "look-card-name";
    nameInput.value = name;
    nameInput.dataset.originalName = name;
    title.append(nameInput);

    const overview = document.createElement("div");
    overview.className = "preset-link-overview";
    const markCardDirty = () => {
      card.classList.add("dirty");
      saveLookStatus.textContent = `Unsaved look changes for ${name}.`;
    };
    nameInput.addEventListener("input", markCardDirty);
    const lightEditor = makeLookLightEditor(name, values, markCardDirty);
    overview.append(lightEditor, makeLookCueStrip(name, link, cameraConfig));

    const routingForm = document.createElement("form");
    routingForm.className = "preset-link-routing";
    routingForm.dataset.look = name;
    const markDirty = () => {
      routingForm.classList.add("dirty");
      card.classList.add("dirty");
      saveLookStatus.textContent = `Unsaved look changes for ${name}.`;
    };
    routingForm.append(
      makePresetLinkField("Now Playing", selectForNowPlayingMode("now_playing_mode", link.now_playing_mode, markDirty)),
      makePresetLinkField("Now Level", selectForNowPlayingOpacity("now_playing_opacity", link.now_playing_opacity, markDirty)),
      makePresetLinkField("Section Preset", selectForPresetNames("section_preset", presetData.groups?.section || {}, link.section_preset, "No change", markDirty)),
      makePresetLinkField("Visual", selectForItems("visual_id", appSettings.visual_controls || [], link.visual_id, "None", markDirty)),
      makePresetLinkField("Main Cam", selectForItems("main_box_id", cameraConfig.groups?.main_box || [], link.main_box_id, "None", markDirty)),
      makePresetLinkField("PIP Cam", selectForItems("pip_box_id", cameraConfig.groups?.pip_box || [], link.pip_box_id, "None", markDirty)),
      makePresetLinkField("Background", selectForItems("background_id", cameraConfig.groups?.background || [], link.background_id, "None", markDirty)),
      makePresetLinkField("Visuals Cam", selectForItems("visuals_cams_id", cameraConfig.groups?.visuals_cams || [], link.visuals_cams_id, "None", markDirty)),
      makePresetLinkField("Scene", selectForItems("scene_id", cameraConfig.scenes || [], link.scene_id, "None", markDirty)),
    );

    const trigger = document.createElement("button");
    trigger.type = "button";
    trigger.textContent = "Trigger";
    trigger.addEventListener("click", async () => {
      if (card.classList.contains("dirty")) {
        const saved = await savePresetCard(nameInput.dataset.originalName, nameInput.value, lightEditor, routingForm);
        if (!saved) return;
      }
      sendCommand(linkedLookPayload(nameInput.value.trim() || nameInput.dataset.originalName));
    });
    const actions = document.createElement("div");
    actions.className = "preset-link-actions";
    const saveLook = document.createElement("button");
    saveLook.type = "button";
    saveLook.textContent = "Save";
    saveLook.title = `Save the edited light values and routing into ${name}`;
    saveLook.addEventListener("click", () => savePresetCard(nameInput.dataset.originalName, nameInput.value, lightEditor, routingForm));
    actions.append(saveLook, trigger);
    card.append(title, overview, routingForm, actions);
    presetLinks.append(card);
  }
}

function makePresetLinkField(labelText, select) {
  const label = document.createElement("label");
  label.className = "preset-link-field";
  const span = document.createElement("span");
  span.textContent = labelText;
  label.append(span, select);
  return label;
}

function renderSaveLookPicker() {
  if (!saveCurrentLookSelect || !presetData) return;
  const currentValue = saveCurrentLookSelect.value;
  saveCurrentLookSelect.replaceChildren();
  for (const name of Object.keys(presetData.groups?.performance || {})) {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = name;
    saveCurrentLookSelect.append(option);
  }
  const active = currentLookName(latestShow);
  saveCurrentLookSelect.value = currentValue || (active && active !== "-" ? active : saveCurrentLookSelect.options[0]?.value || "");
  if (lookBuilderName && !lookBuilderDirty) lookBuilderName.value = saveCurrentLookSelect.value || "";
  renderLookBuilder();
}

function selectLookForBuilder(name) {
  if (!saveCurrentLookSelect) return;
  saveCurrentLookSelect.value = name;
  if (lookBuilderName) lookBuilderName.value = name;
  lookBuilderDirty = false;
  renderLookBuilder();
  saveLookStatus.textContent = `Editing ${name}.`;
}

function currentLookBuilderName() {
  return (lookBuilderName?.value || saveCurrentLookSelect?.value || "").trim();
}

function presetValuesForLook(name) {
  return presetData?.groups?.performance?.[name] || {};
}

function renderLookBuilder() {
  if (!appSettings || !presetData || !lookBuilderForm || !saveCurrentLookSelect) return;
  if (lookBuilderDirty) return;
  const name = saveCurrentLookSelect.value || Object.keys(presetData.groups?.performance || {})[0] || "";
  if (!name) return;
  const link = appSettings.preset_links?.[name] || {};
  const values = presetValuesForLook(name);
  const cameraConfig = appSettings.camera_controls || {};

  lookBuilderSummary.replaceChildren();
  const colorRow = document.createElement("div");
  colorRow.className = "look-builder-colors";
  const colorLabels = { PRIMARY: "Color 1", SECONDARY: "Color 2", STROBE: "Color 3" };
  for (const key of ["PRIMARY", "SECONDARY", "STROBE"]) {
    const color = values[key] || "-";
    const item = document.createElement("div");
    const chip = document.createElement("span");
    chip.style.background = colorHex(color);
    const label = document.createElement("strong");
    label.textContent = color;
    const small = document.createElement("small");
    small.textContent = colorLabels[key] || key;
    item.append(chip, label, small);
    colorRow.append(item);
  }
  lookBuilderSummary.append(colorRow);

  const markDirty = () => {
    lookBuilderDirty = true;
    saveLookStatus.textContent = `Unsaved routing changes for ${name}.`;
  };
  lookBuilderForm.replaceChildren();

  lookBuilderForm.append(
    makeBuilderSelect("builder_now_playing", "Now Playing", selectForNowPlayingMode("builder_now_playing", link.now_playing_mode, markDirty)),
    makeBuilderSelect("builder_now_playing_opacity", "Now Level", selectForNowPlayingOpacity("builder_now_playing_opacity", link.now_playing_opacity, markDirty)),
    makeBuilderSelect("builder_section", "Section Preset", selectForPresetNames("builder_section", presetData.groups?.section || {}, link.section_preset, "No change", markDirty)),
    makeBuilderSelect("builder_visual", "Visual", selectForItems("builder_visual", appSettings.visual_controls || [], link.visual_id, "None", markDirty)),
    makeBuilderSelect("builder_main", "Main Cam", selectForItems("builder_main", cameraConfig.groups?.main_box || [], link.main_box_id, "None", markDirty)),
    makeBuilderSelect("builder_pip", "PIP Cam", selectForItems("builder_pip", cameraConfig.groups?.pip_box || [], link.pip_box_id, "None", markDirty)),
    makeBuilderSelect("builder_background", "Background", selectForItems("builder_background", cameraConfig.groups?.background || [], link.background_id, "None", markDirty)),
    makeBuilderSelect("builder_visuals_cams", "Visuals Cam", selectForItems("builder_visuals_cams", cameraConfig.groups?.visuals_cams || [], link.visuals_cams_id, "None", markDirty)),
    makeBuilderSelect("builder_scene", "Scene", selectForItems("builder_scene", cameraConfig.scenes || [], link.scene_id, "None", markDirty)),
  );
}
function makeBuilderSelect(_name, labelText, select) {
  const label = document.createElement("label");
  label.className = "quick-field";
  const span = document.createElement("span");
  span.textContent = labelText;
  label.append(span, select);
  return label;
}

function makeField(key, labelText, kind, onDirty = markSettingsDirty) {
  const label = document.createElement("label");
  label.className = "field";
  const span = document.createElement("span");
  span.textContent = labelText;
  label.append(span);

  let input;
  if (kind === "textarea") {
    input = document.createElement("textarea");
    input.rows = 3;
  } else if (kind === "select:color") {
    input = document.createElement("select");
    for (const name of appSettings.colors.names || []) {
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      input.append(option);
    }
  } else if (kind === "select:bpm") {
    input = document.createElement("select");
    for (const division of appSettings.bpm_divisions || []) {
      const option = document.createElement("option");
      option.value = division;
      option.textContent = division;
      input.append(option);
    }
  } else if (kind === "select:connection_profile") {
    input = document.createElement("select");
    for (const profile of appSettings.connection_profiles || []) {
      const option = document.createElement("option");
      option.value = profile.id;
      option.textContent = profile.name || profile.id;
      input.append(option);
    }
  } else if (kind === "checkbox") {
    input = document.createElement("input");
    input.type = "checkbox";
  } else {
    input = document.createElement("input");
    input.type = kind === "number" ? "number" : kind === "password" ? "password" : "text";
  }

  input.name = key;
  if (kind === "number" && (key === "output_pixels" || key.endsWith("_artwork_width") || key.endsWith("_artwork_height"))) {
    input.min = "64";
    input.max = "4096";
    input.step = "1";
    input.inputMode = "numeric";
  }
  if (kind === "checkbox") {
    input.checked = Boolean(appSettings[key]);
  } else {
    input.value = appSettings[key] ?? "";
  }
  input.addEventListener("input", onDirty);
  input.addEventListener("change", () => {
    onDirty();
    if (key === "active_connection_profile") applyConnectionProfileToSettings(input.value);
  });
  label.append(input);
  return label;
}

function applyConnectionProfileToSettings(profileId) {
  const profile = (appSettings?.connection_profiles || []).find((item) => item.id === profileId);
  if (!profile || !settingsForm) return;
  const fieldMap = {
    app_bind_host: profile.app_bind_host,
    app_port: profile.app_port,
    public_control_url: profile.public_control_url,
    beatlink_host: profile.beatlink_host,
    beatlink_port: profile.beatlink_port,
    beatlink_base_url: profile.beatlink_base_url,
    blt_params_url: profile.blt_params_url,
    resolume_host: profile.resolume_host,
    resolume_port: profile.resolume_port,
    visualizer_url: profile.visualizer_url,
  };
  for (const [key, value] of Object.entries(fieldMap)) {
    const field = settingsForm.elements[key];
    if (field) field.value = value ?? "";
  }
}

function settingsField(key) {
  return settingsForm?.elements?.[key] || null;
}

const networkMachineSlots = [
  { id: "laptop", label: "Laptop", host: "127.0.0.1", placeholders: ["127.0.0.1", "192.168.1.50", "Laptop Ethernet IP"] },
  { id: "pc", label: "PC", host: "", placeholders: ["192.168.1.60", "PC WiFi IP", "PC Ethernet IP"] },
  { id: "third", label: "Third Machine", host: "", placeholders: ["192.168.1.x", "Backup WiFi IP", "Backup Ethernet IP"] },
];

const networkAddressSlots = ["Main", "WiFi", "Ethernet"];

function setSettingsFieldValue(key, value) {
  const field = settingsField(key);
  if (field) field.value = value ?? "";
}

function normalizeNetworkPort(value, fallback) {
  const port = Number.parseInt(value, 10);
  if (Number.isFinite(port) && port >= 1 && port <= 65535) return String(port);
  return String(fallback);
}

function cleanNetworkAddress(value) {
  let text = String(value || "").trim();
  if (!text) return "";
  try {
    if (text.includes("://")) {
      const url = new URL(text);
      return url.hostname || "";
    }
  } catch (_error) {
    // Fall through and clean the raw text below.
  }
  text = text.replace(/^\/+|\/+$/g, "");
  if (text.includes("/")) text = text.split("/", 1)[0];
  const colonCount = (text.match(/:/g) || []).length;
  if (colonCount === 1) {
    const [host, port] = text.split(":");
    if (/^\d+$/.test(port)) text = host;
  }
  return text.trim();
}

function uniqueNetworkAddresses(values) {
  const addresses = [];
  const seen = new Set();
  for (const value of values) {
    const address = cleanNetworkAddress(value);
    if (!address) continue;
    const key = address.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    addresses.push(address);
  }
  return addresses;
}

function machineAddressSlots(machine) {
  const rawSlots = machine?.address_slots || {};
  const hasNamedSlots = rawSlots && ["main", "host", "wifi", "wifi_host", "ethernet", "ethernet_host"].some((key) => Object.prototype.hasOwnProperty.call(rawSlots, key));
  if (hasNamedSlots) {
    return {
      main: cleanNetworkAddress(rawSlots.main || rawSlots.host || ""),
      wifi: cleanNetworkAddress(rawSlots.wifi || rawSlots.wifi_host || ""),
      ethernet: cleanNetworkAddress(rawSlots.ethernet || rawSlots.ethernet_host || ""),
    };
  }
  const rawAddresses = Array.isArray(machine?.addresses) ? machine.addresses : [];
  return {
    main: cleanNetworkAddress(machine?.host || rawAddresses[0] || ""),
    wifi: cleanNetworkAddress(machine?.wifi_host || machine?.wifi || rawAddresses[1] || ""),
    ethernet: cleanNetworkAddress(machine?.ethernet_host || machine?.ethernet || rawAddresses[2] || ""),
  };
}

function machineAddresses(machine) {
  const slots = machineAddressSlots(machine);
  return uniqueNetworkAddresses([slots.main, slots.wifi, slots.ethernet]);
}
function machinePrimaryHost(machine) {
  return machineAddresses(machine)[0] || cleanNetworkAddress(machine?.host) || "";
}

function bltUrlForHost(host, port = 17081) {
  const cleanHost = cleanNetworkAddress(host) || "127.0.0.1";
  return `http://${cleanHost}:${normalizeNetworkPort(port, 17081)}/params.json`;
}

function hostFromBltUrl(rawUrl) {
  try {
    const url = new URL(String(rawUrl || "").trim());
    return url.hostname || "";
  } catch (_error) {
    return "";
  }
}

function portFromBltUrl(rawUrl) {
  try {
    const url = new URL(String(rawUrl || "").trim());
    return normalizeNetworkPort(url.port || "17081", 17081);
  } catch (_error) {
    return "17081";
  }
}

function currentNetworkHostGuess() {
  const resolumeHost = String(settingsField("resolume_host")?.value || appSettings?.resolume_host || "").trim();
  if (resolumeHost && !["127.0.0.1", "localhost"].includes(resolumeHost.toLowerCase())) return resolumeHost;
  const host = hostFromBltUrl(settingsField("blt_params_url")?.value || appSettings?.blt_params_url);
  if (host && !["127.0.0.1", "localhost"].includes(host.toLowerCase())) return host;
  return "";
}

function networkMachinesForSettings() {
  const configured = Array.isArray(appSettings?.network_machines) ? appSettings.network_machines : [];
  const configuredById = new Map(configured.map((machine) => [machine.id, machine]));
  const remoteGuess = currentNetworkHostGuess();
  return networkMachineSlots.map((slot) => {
    const configuredMachine = configuredById.get(slot.id) || {};
    const fallbackHost = slot.id === "pc" ? remoteGuess : slot.host;
    const slots = machineAddressSlots(configuredMachine);
    if (!slots.main && !slots.wifi && !slots.ethernet && fallbackHost) slots.main = cleanNetworkAddress(fallbackHost);
    const addresses = uniqueNetworkAddresses([slots.main, slots.wifi, slots.ethernet]);
    return {
      id: slot.id,
      label: configuredMachine.label || slot.label,
      host: slots.main || addresses[0] || "",
      wifi_host: slots.wifi,
      ethernet_host: slots.ethernet,
      address_slots: slots,
      addresses,
      addressValues: [slots.main, slots.wifi, slots.ethernet],
      placeholders: slot.placeholders,
    };
  });
}
function networkMachineRows() {
  return [...settingsForm.querySelectorAll(".network-machine-row")].map((row) => {
    const fields = [...row.querySelectorAll("[data-network-address]")]
      .sort((a, b) => Number(a.dataset.networkAddress || 0) - Number(b.dataset.networkAddress || 0));
    const addressValues = fields.map((input) => cleanNetworkAddress(input.value));
    const addressSlots = {
      main: addressValues[0] || "",
      wifi: addressValues[1] || "",
      ethernet: addressValues[2] || "",
    };
    const addresses = uniqueNetworkAddresses([addressSlots.main, addressSlots.wifi, addressSlots.ethernet]);
    return {
      id: row.dataset.machineId,
      label: row.querySelector("[data-network-field='label']")?.value || row.dataset.machineId,
      host: addressSlots.main || addresses[0] || "",
      wifi_host: addressSlots.wifi,
      ethernet_host: addressSlots.ethernet,
      address_slots: addressSlots,
      addresses,
    };
  });
}
function machineById(machines, id) {
  return machines.find((machine) => machine.id === id) || machines[0] || { id: "laptop", label: "Laptop", host: "127.0.0.1", addresses: ["127.0.0.1"] };
}

function machineIdForHost(machines, host, fallback = "laptop") {
  const cleanHost = cleanNetworkAddress(host).toLowerCase();
  if (!cleanHost) return fallback;
  const match = machines.find((machine) => machineAddresses(machine).some((address) => address.toLowerCase() === cleanHost));
  return match?.id || fallback;
}

function routeConfigForSettings(machines) {
  const routes = appSettings?.network_routes || {};
  const bltHost = hostFromBltUrl(appSettings?.blt_params_url);
  const resolumeHost = appSettings?.resolume_host || "";
  return {
    beatlink_machine: routes.beatlink_machine || machineIdForHost(machines, bltHost, "laptop"),
    beatlink_port: normalizeNetworkPort(routes.beatlink_port || portFromBltUrl(appSettings?.blt_params_url), 17081),
    resolume_machine: routes.resolume_machine || machineIdForHost(machines, resolumeHost, "laptop"),
    resolume_port: normalizeNetworkPort(routes.resolume_port || appSettings?.resolume_port, 7000),
  };
}

function collectNetworkRoutingPayload() {
  const machines = networkMachineRows();
  if (!machines.length) return {};
  const beatlinkMachineId = settingsForm.querySelector("[data-network-route='beatlink_machine']")?.value || "laptop";
  const resolumeMachineId = settingsForm.querySelector("[data-network-route='resolume_machine']")?.value || "laptop";
  const beatlinkPort = normalizeNetworkPort(settingsForm.querySelector("[data-network-route='beatlink_port']")?.value, 17081);
  const resolumePort = normalizeNetworkPort(settingsForm.querySelector("[data-network-route='resolume_port']")?.value, 7000);
  const beatlinkMachine = machineById(machines, beatlinkMachineId);
  const resolumeMachine = machineById(machines, resolumeMachineId);
  const beatlinkHost = machinePrimaryHost(beatlinkMachine) || "127.0.0.1";
  const resolumeHost = machinePrimaryHost(resolumeMachine) || "127.0.0.1";
  return {
    network_machines: machines,
    network_routes: {
      beatlink_machine: beatlinkMachine.id,
      beatlink_port: beatlinkPort,
      resolume_machine: resolumeMachine.id,
      resolume_port: resolumePort,
    },
    blt_params_url: bltUrlForHost(beatlinkHost, beatlinkPort),
    resolume_host: resolumeHost,
    resolume_port: resolumePort,
  };
}

function applyNetworkRoutingPayload(payload = collectNetworkRoutingPayload()) {
  if (!payload.blt_params_url) return;
  setSettingsFieldValue("app_bind_host", "0.0.0.0");
  if (!String(settingsField("app_port")?.value || "").trim()) setSettingsFieldValue("app_port", "8080");
  setSettingsFieldValue("public_control_url", "");
  setSettingsFieldValue("blt_params_url", payload.blt_params_url);
  setSettingsFieldValue("resolume_host", payload.resolume_host);
  setSettingsFieldValue("resolume_port", payload.resolume_port);
  markSettingsDirty();
}

function setNetworkRouteMachines(beatlinkMachine, resolumeMachine) {
  const beatlinkSelect = settingsForm.querySelector("[data-network-route='beatlink_machine']");
  const resolumeSelect = settingsForm.querySelector("[data-network-route='resolume_machine']");
  if (beatlinkSelect) beatlinkSelect.value = beatlinkMachine;
  if (resolumeSelect) resolumeSelect.value = resolumeMachine;
  applyNetworkRoutingPayload();
}

function makeRouteSelect(name, machines, selectedId) {
  const label = document.createElement("label");
  label.className = "field";
  const span = document.createElement("span");
  span.textContent = name;
  const select = document.createElement("select");
  select.dataset.networkRoute = name.toLowerCase().includes("beatlink") ? "beatlink_machine" : "resolume_machine";
  for (const machine of machines) {
    const addresses = machineAddresses(machine);
    const option = document.createElement("option");
    option.value = machine.id;
    option.textContent = addresses.length ? `${machine.label} (${addresses.length} IP${addresses.length === 1 ? "" : "s"})` : `${machine.label} (set IP)`;
    option.title = addresses.join(", ");
    select.append(option);
  }
  select.value = selectedId;
  select.addEventListener("change", markSettingsDirty);
  label.append(span, select);
  return label;
}

function makeNetworkPortField(labelText, routeKey, value) {
  const label = document.createElement("label");
  label.className = "field";
  const span = document.createElement("span");
  span.textContent = labelText;
  const input = document.createElement("input");
  input.type = "number";
  input.dataset.networkRoute = routeKey;
  input.value = value;
  input.addEventListener("input", markSettingsDirty);
  label.append(span, input);
  return label;
}

function makeSimpleNetworkPanel() {
  const panel = document.createElement("section");
  panel.className = "simple-network-panel";

  const title = document.createElement("h3");
  title.textContent = "Network Machines + Routes";

  const machines = networkMachinesForSettings();
  const routes = routeConfigForSettings(machines);

  const machineGrid = document.createElement("div");
  machineGrid.className = "network-machine-grid";
  for (const machine of machines) {
    const row = document.createElement("div");
    row.className = "network-machine-row";
    row.dataset.machineId = machine.id;

    const nameRow = document.createElement("div");
    nameRow.className = "network-machine-name-row";
    const nameLabel = document.createElement("span");
    nameLabel.textContent = "Machine";
    const label = document.createElement("input");
    label.type = "text";
    label.value = machine.label;
    label.dataset.networkField = "label";
    nameRow.append(nameLabel, label);

    const addressGrid = document.createElement("div");
    addressGrid.className = "network-address-grid";
    networkAddressSlots.forEach((slotLabel, addressIndex) => {
      const field = document.createElement("label");
      field.className = "network-address-field";
      const slot = document.createElement("span");
      slot.textContent = slotLabel;
      const input = document.createElement("input");
      input.type = "text";
      input.value = machine.addressValues?.[addressIndex] || machine.addresses[addressIndex] || "";
      input.placeholder = machine.placeholders?.[addressIndex] || "192.168.1.x";
      input.dataset.networkAddress = String(addressIndex);
      input.addEventListener("input", markSettingsDirty);
      field.append(slot, input);
      addressGrid.append(field);
    });

    label.addEventListener("input", markSettingsDirty);
    row.append(nameRow, addressGrid);
    machineGrid.append(row);
  }

  const routeGrid = document.createElement("div");
  routeGrid.className = "network-route-grid";
  routeGrid.append(
    makeRouteSelect("Preferred BeatLink Source", machines, routes.beatlink_machine),
    makeNetworkPortField("BeatLink Trigger Port", "beatlink_port", routes.beatlink_port),
    makeRouteSelect("Resolume OSC Receives On", machines, routes.resolume_machine),
    makeNetworkPortField("Resolume OSC Port", "resolume_port", routes.resolume_port),
  );

  const actions = document.createElement("div");
  actions.className = "simple-network-actions";
  const local = document.createElement("button");
  local.type = "button";
  local.textContent = "Prefer Laptop";
  local.addEventListener("click", () => setNetworkRouteMachines("laptop", "laptop"));

  const pc = document.createElement("button");
  pc.type = "button";
  pc.textContent = "Prefer PC";
  pc.addEventListener("click", () => setNetworkRouteMachines("pc", "pc"));

  const third = document.createElement("button");
  third.type = "button";
  third.textContent = "Prefer Third";
  third.addEventListener("click", () => setNetworkRouteMachines("third", "third"));

  const apply = document.createElement("button");
  apply.type = "button";
  apply.textContent = "Apply Preferred Route";
  apply.addEventListener("click", () => applyNetworkRoutingPayload());

  actions.append(local, pc, third, apply);

  const hint = document.createElement("p");
  hint.className = "muted simple-network-hint";
  hint.textContent = "Add WiFi and Ethernet addresses for each show machine. BeatLink checks every saved address; OSC sends to every saved machine IP on the Resolume OSC port. Leave unknown addresses blank.";

  panel.append(title, machineGrid, routeGrid, actions, hint);
  return panel;
}
function oscTargetsForSettings() {
  const configured = Array.isArray(appSettings?.osc_targets) ? appSettings.osc_targets : [];
  const fallback = {
    id: "active_resolume",
    label: "Active Resolume",
    host: appSettings?.resolume_host || "",
    port: appSettings?.resolume_port || 7000,
    enabled: true,
    primary: true,
  };
  const targets = configured.length ? configured : [fallback];
  return [
    ...targets,
    { id: "", label: "", host: "", port: appSettings?.resolume_port || 7000, enabled: false, primary: false },
    { id: "", label: "", host: "", port: appSettings?.resolume_port || 7000, enabled: false, primary: false },
  ];
}
function makeOscTargetsPanel() {
  const panel = document.createElement("section");
  panel.className = "osc-targets-panel";

  const title = document.createElement("h3");
  title.textContent = "OSC Output Fan-Out Targets";

  const grid = document.createElement("div");
  grid.className = "osc-target-grid";
  const header = document.createElement("div");
  header.className = "osc-target-row osc-target-header";
  header.innerHTML = "<span>On</span><span>Name</span><span>IP Address</span><span>Port</span><span>Main</span>";
  grid.append(header);

  oscTargetsForSettings().forEach((target, index) => {
    const row = document.createElement("div");
    row.className = "osc-target-row";
    row.dataset.targetIndex = String(index);
    row.dataset.oscTargetSource = target.source || "";
    row.dataset.originalLabel = target.label || "";
    row.dataset.originalHost = target.host || "";
    row.dataset.originalPort = String(target.port || 7000);
    row.dataset.originalEnabled = String(Boolean(target.enabled));
    row.dataset.originalPrimary = String(Boolean(target.primary));

    const enabled = document.createElement("input");
    enabled.type = "checkbox";
    enabled.dataset.oscTargetField = "enabled";
    enabled.checked = Boolean(target.enabled);

    const label = document.createElement("input");
    label.type = "text";
    label.dataset.oscTargetField = "label";
    label.value = target.label || "";
    label.placeholder = index === 0 ? "Laptop Resolume" : "Stream PC";

    const host = document.createElement("input");
    host.type = "text";
    host.dataset.oscTargetField = "host";
    host.value = target.host || "";
    host.placeholder = index === 0 ? "192.168.1.189" : "192.168.1.9";

    const port = document.createElement("input");
    port.type = "number";
    port.dataset.oscTargetField = "port";
    port.value = target.port || 7000;

    const primary = document.createElement("input");
    primary.type = "radio";
    primary.name = "osc_target_primary";
    primary.dataset.oscTargetField = "primary";
    primary.checked = Boolean(target.primary);

    for (const input of [enabled, label, host, port, primary]) {
      input.addEventListener("input", markSettingsDirty);
      input.addEventListener("change", markSettingsDirty);
    }

    row.append(enabled, label, host, port, primary);
    grid.append(row);
  });

  const hint = document.createElement("p");
  hint.className = "muted simple-network-hint";
  hint.textContent = "Automatic targets come from the machine IP list above. Add manual rows only for extra OSC receivers; uncheck a target when you need to pause one route.";

  panel.append(title, grid, hint);
  return panel;
}

function collectOscTargetsPayload() {
  const targets = [];
  settingsForm.querySelectorAll(".osc-target-row:not(.osc-target-header)").forEach((row, index) => {
    const host = row.querySelector("[data-osc-target-field='host']")?.value?.trim() || "";
    if (!host) return;
    const label = row.querySelector("[data-osc-target-field='label']")?.value?.trim() || `OSC Target ${index + 1}`;
    const port = normalizeNetworkPort(row.querySelector("[data-osc-target-field='port']")?.value, 7000);
    const enabled = Boolean(row.querySelector("[data-osc-target-field='enabled']")?.checked);
    const primary = Boolean(row.querySelector("[data-osc-target-field='primary']")?.checked);
    const unchangedAuto = row.dataset.oscTargetSource === "auto"
      && label === row.dataset.originalLabel
      && host === row.dataset.originalHost
      && port === row.dataset.originalPort
      && String(enabled) === row.dataset.originalEnabled
      && String(primary) === row.dataset.originalPrimary;
    if (unchangedAuto) return;
    targets.push({
      id: `${host}_${port}`.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, ""),
      label,
      host,
      port,
      enabled,
      primary,
    });
  });
  return { osc_targets: targets };
}
function renderSettingsForm() {
  if (!appSettings || !settingsForm || settingsDirty || settingsForm.contains(document.activeElement)) return;
  settingsForm.replaceChildren();
  for (const group of settingGroups) {
    const fieldset = document.createElement("fieldset");
    const legend = document.createElement("legend");
    legend.textContent = group.title;
    fieldset.append(legend);
    for (const [key, label, kind] of group.fields) {
      fieldset.append(makeField(key, label, kind));
    }
    if (group.title === "Current Active Routing") {
      settingsForm.append(makeSimpleNetworkPanel());
      settingsForm.append(makeOscTargetsPanel());
    }
    settingsForm.append(fieldset);
  }
}

function markObsSettingsDirty() {
  obsSettingsDirty = true;
  if (obsSettingsStatus) obsSettingsStatus.textContent = "Unsaved OBS settings.";
}

function renderObsSettingsForm() {
  if (!appSettings || !obsSettingsForm || obsSettingsDirty || obsSettingsForm.contains(document.activeElement)) return;
  obsSettingsForm.replaceChildren();
  const fieldset = document.createElement("fieldset");
  const legend = document.createElement("legend");
  legend.textContent = "OBS WebSocket";
  fieldset.append(legend);
  for (const [key, label, kind] of obsSettingFields) {
    fieldset.append(makeField(key, label, kind, markObsSettingsDirty));
  }
  obsSettingsForm.append(fieldset);
}

function makeLocalTextField(name, labelText, value, onDirty, placeholder = "") {
  const label = document.createElement("label");
  label.className = "field";
  const span = document.createElement("span");
  span.textContent = labelText;
  const input = document.createElement("input");
  input.name = name;
  input.type = "text";
  input.value = value || "";
  input.placeholder = placeholder;
  input.addEventListener("input", onDirty);
  label.append(span, input);
  if (placeholder.startsWith("/composition/")) {
    label.classList.add("osc-address-field");
    label.append(makeOscAddressBuilder(input, onDirty));
  }
  return label;
}

function lightOscOutputSlots(control) {
  return LIVE_LIGHT_COLOR_KEYS.includes(control?.key) ? COLOR_LIGHT_OSC_OUTPUT_SLOTS : DEFAULT_LIGHT_OSC_OUTPUT_SLOTS;
}

function makeLightOscOutputRow(control, outputIndex, addressValue, noteValue, onDirty) {
  const row = document.createElement("div");
  row.className = "light-osc-output-row";
  const link = control.link;
  const outputNumber = outputIndex + 1;
  const title = document.createElement("strong");
  title.textContent = `OSC Output ${outputNumber}`;
  const addressName = outputIndex === 0 ? `address_${link}` : `extra_address_${link}_${outputIndex - 1}`;
  const address = makeLocalTextField(addressName, "Address", addressValue, onDirty, "/composition/layers/.../params/...");
  const note = makeLocalTextField(
    `output_note_${link}_${outputIndex}`,
    "Note",
    noteValue,
    onDirty,
    LIGHT_OSC_NOTE_PLACEHOLDERS[outputIndex] || "Mapped target note",
  );
  row.append(title, address, note);
  return row;
}

function parseResolumeAddress(address) {
  const text = String(address || "").trim();
  const direct = text.match(/^\/composition\/(layers|groups)\/(\d+)(\/(?!columns\/|clips\/).*)$/i);
  if (direct) {
    return {
      scope: direct[1].toLowerCase(),
      scopeNumber: direct[2],
      target: "direct",
      targetNumber: "1",
      action: direct[3] || "/video/opacity",
    };
  }
  const match = text.match(/^\/composition\/(layers|groups)\/(\d+)\/(columns|clips)\/(\d+)(\/.*)?$/i);
  if (!match) return null;
  return {
    scope: match[1].toLowerCase(),
    scopeNumber: match[2],
    target: match[3].toLowerCase(),
    targetNumber: match[4],
    action: match[5] || "/connect",
  };
}

function buildResolumeAddress(parts) {
  const scope = parts.scope || "groups";
  const scopeNumber = Math.max(1, Number.parseInt(parts.scopeNumber || "1", 10) || 1);
  const target = parts.target || "columns";
  const targetNumber = Math.max(1, Number.parseInt(parts.targetNumber || "1", 10) || 1);
  let action = String(parts.action || "/connect").trim();
  if (!action.startsWith("/")) action = `/${action}`;
  if (target === "direct") return `/composition/${scope}/${scopeNumber}${action}`;
  return `/composition/${scope}/${scopeNumber}/${target}/${targetNumber}${action}`;
}

function makeOscAddressBuilder(addressInput, onDirty, onAddressChange = null) {
  const directDefault = addressInput.placeholder?.includes("/video/opacity") && !addressInput.placeholder?.includes("/clips/") && !addressInput.placeholder?.includes("/columns/");
  const parsed = parseResolumeAddress(addressInput.value) || {
    scope: addressInput.placeholder?.includes("/layers/") ? "layers" : "groups",
    scopeNumber: "1",
    target: directDefault ? "direct" : addressInput.placeholder?.includes("/clips/") ? "clips" : "columns",
    targetNumber: "1",
    action: addressInput.placeholder?.includes("opacity") ? "/video/opacity" : "/connect",
  };
  const builder = document.createElement("div");
  builder.className = "osc-builder";

  const scope = makeBuilderSelectControl("Layer Type", [["groups", "Group"], ["layers", "Layer"]], parsed.scope);
  const scopeNumber = makeBuilderNumberControl("Layer / Group #", parsed.scopeNumber);
  const target = makeBuilderSelectControl("Target Type", [["direct", "Direct Param"], ["columns", "Column"], ["clips", "Clip"]], parsed.target);
  const targetNumber = makeBuilderNumberControl("Column / Clip #", parsed.targetNumber);
  const action = makeBuilderTextControl("Action Path", parsed.action);
  const controls = [scope, scopeNumber, target, targetNumber, action];
  const updateTargetNumberState = () => {
    targetNumber.input.disabled = target.input.value === "direct";
    targetNumber.label.classList.toggle("disabled", target.input.value === "direct");
  };

  const syncAddress = () => {
    addressInput.value = buildResolumeAddress({
      scope: scope.input.value,
      scopeNumber: scopeNumber.input.value,
      target: target.input.value,
      targetNumber: targetNumber.input.value,
      action: action.input.value,
    });
    onAddressChange?.(addressInput.value);
    onDirty();
    updateTargetNumberState();
  };

  const syncBuilder = () => {
    const next = parseResolumeAddress(addressInput.value);
    if (!next) return;
    scope.input.value = next.scope;
    scopeNumber.input.value = next.scopeNumber;
    target.input.value = next.target;
    targetNumber.input.value = next.targetNumber;
    action.input.value = next.action;
    updateTargetNumberState();
  };

  for (const control of controls) {
    control.input.addEventListener("input", syncAddress);
    control.input.addEventListener("change", syncAddress);
    builder.append(control.label);
  }
  addressInput.addEventListener("input", () => {
    syncBuilder();
    onAddressChange?.(addressInput.value);
  });
  updateTargetNumberState();
  return builder;
}

function makeBuilderSelectControl(text, options, selected) {
  const label = document.createElement("label");
  label.className = "osc-builder-field";
  const span = document.createElement("span");
  span.textContent = text;
  const input = document.createElement("select");
  for (const [value, labelText] of options) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = labelText;
    input.append(option);
  }
  input.value = selected || options[0][0];
  label.append(span, input);
  return { label, input };
}

function makeBuilderNumberControl(text, selected) {
  const label = document.createElement("label");
  label.className = "osc-builder-field compact";
  const span = document.createElement("span");
  span.textContent = text;
  const input = document.createElement("input");
  input.type = "number";
  input.min = "1";
  input.step = "1";
  input.value = selected || "1";
  label.append(span, input);
  return { label, input };
}

function makeBuilderTextControl(text, selected) {
  const label = document.createElement("label");
  label.className = "osc-builder-field action";
  const span = document.createElement("span");
  span.textContent = text;
  const input = document.createElement("input");
  input.type = "text";
  input.value = selected || "/connect";
  label.append(span, input);
  return { label, input };
}

function lightOscSectionForControl(control) {
  if (LIVE_LIGHT_COLOR_KEYS.includes(control?.key)) return control.key;
  return "sliders";
}

function makeLightOscFilters() {
  const filters = document.createElement("div");
  filters.className = "osc-filter-tabs light-osc-filter-tabs";
  for (const [key, label] of LIGHT_OSC_FILTERS) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "osc-filter-button";
    button.dataset.lightOscSection = key;
    button.textContent = label;
    button.addEventListener("click", () => setActiveLightOscSection(key));
    filters.append(button);
  }
  return filters;
}

function setActiveLightOscSection(key) {
  activeLightOscSection = key;
  document.querySelectorAll("[data-light-osc-section].osc-filter-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.lightOscSection === key);
  });
  document.querySelectorAll(".light-osc-section").forEach((section) => {
    const show = key === "all" || section.dataset.lightOscSection === key;
    section.classList.toggle("active", show);
  });
}

function makeBpmTimingOscSection(onDirty) {
  const fieldset = document.createElement("fieldset");
  fieldset.className = "wide-fieldset light-osc-section bpm-timing-osc-section";
  fieldset.dataset.lightOscSection = "timing";
  const legend = document.createElement("legend");
  legend.textContent = "BPM Timing OSC Outputs";
  fieldset.append(legend);

  const grid = document.createElement("div");
  grid.className = "bpm-timing-osc-grid";
  for (const [key, label, placeholder] of BPM_TIMING_OSC_FIELDS) {
    grid.append(makeLocalTextField(key, label, appSettings[key] || "", onDirty, placeholder));
  }
  fieldset.append(grid);
  return fieldset;
}
function renderLightsOscForm() {
  if (!appSettings || !lightsOscForm || lightsOscDirty || lightsOscForm.contains(document.activeElement)) return;
  lightsOscForm.replaceChildren();
  const markDirty = () => {
    lightsOscDirty = true;
    lightsOscStatus.textContent = "Unsaved Lights OSC changes.";
  };
  lightsOscForm.append(makeLightOscFilters());
  const fieldset = document.createElement("fieldset");
  fieldset.className = "wide-fieldset light-osc-control-fieldset";
  const legend = document.createElement("legend");
  legend.textContent = "Light Control OSC Outputs";
  fieldset.append(legend);
  for (const control of liveLightControls()) {
    const group = document.createElement("div");
    group.className = "light-osc-control-group light-osc-section";
    group.dataset.lightOscSection = lightOscSectionForControl(control);

    const heading = document.createElement("div");
    heading.className = "light-osc-control-heading";
    const title = document.createElement("strong");
    title.textContent = control.label || control.default_label || `Control ${control.link}`;
    const meta = document.createElement("span");
    meta.textContent = `Control ${control.link}`;
    heading.append(title, meta);

    const labelRow = document.createElement("div");
    labelRow.className = "light-osc-label-row";
    labelRow.append(makeLocalTextField(`label_${control.link}`, "Display name", appSettings.link_labels[String(control.link)] || control.label, markDirty));

    const outputs = document.createElement("div");
    outputs.className = "light-osc-output-grid";
    const extras = appSettings.osc_extra_addresses?.[String(control.link)] || [];
    const notes = appSettings.osc_output_notes?.[String(control.link)] || [];
    const outputSlots = lightOscOutputSlots(control);
    for (let index = 0; index < outputSlots; index += 1) {
      const addressValue = index === 0
        ? appSettings.osc_addresses[String(control.link)] || control.address
        : extras[index - 1] || "";
      outputs.append(makeLightOscOutputRow(control, index, addressValue, notes[index] || "", markDirty));
    }

    group.append(heading, labelRow, outputs);
    fieldset.append(group);
  }
  lightsOscForm.append(fieldset);
  lightsOscForm.append(makeBpmTimingOscSection(markDirty));
  setActiveLightOscSection(activeLightOscSection);
}
function renderNowPlayingOscForm() {
  if (!appSettings || !nowPlayingOscForm || nowPlayingOscDirty || nowPlayingOscForm.contains(document.activeElement)) return;
  nowPlayingOscForm.replaceChildren();
  const markDirty = () => {
    nowPlayingOscDirty = true;
    nowPlayingOscStatus.textContent = "Unsaved Now Playing OSC changes.";
  };
  const fieldset = document.createElement("fieldset");
  fieldset.className = "wide-fieldset";
  const legend = document.createElement("legend");
  legend.textContent = "BLT / Stream Text OSC Outputs";
  fieldset.append(legend);
  const header = document.createElement("div");
  header.className = "blt-output-row blt-output-header";
  header.innerHTML = "<span>On</span><span>Label</span><span>Field</span><span>OSC Address</span>";
  fieldset.append(header);
  for (const output of appSettings.blt_osc_outputs || []) {
    fieldset.append(makeBltOutputRow(output, markDirty));
  }
  const actions = document.createElement("div");
  actions.className = "settings-actions";
  const testBlt = document.createElement("button");
  testBlt.type = "button";
  testBlt.textContent = "Test Enabled Now Playing Outputs";
  testBlt.addEventListener("click", () => sendCommand({ command: "test_blt_outputs" }));
  actions.append(testBlt);
  fieldset.append(actions);
  nowPlayingOscForm.append(fieldset);

  const opacityFieldset = document.createElement("fieldset");
  opacityFieldset.className = "wide-fieldset";
  const opacityLegend = document.createElement("legend");
  opacityLegend.textContent = "Now Playing Opacity";
  opacityFieldset.append(opacityLegend);
  const opacityHeader = document.createElement("div");
  opacityHeader.className = "visual-slider-setting-row visual-slider-setting-header";
  opacityHeader.innerHTML = "<span>Slider</span><span>OSC Address</span>";
  opacityFieldset.append(opacityHeader);
  const opacityRow = document.createElement("div");
  opacityRow.className = "visual-slider-setting-row now-playing-opacity-setting-row";
  const opacityLabel = document.createElement("span");
  opacityLabel.textContent = "Now Playing Opacity";
  const opacityAddress = document.createElement("input");
  opacityAddress.name = "now_playing_opacity_address";
  opacityAddress.value = appSettings?.now_playing_opacity_address || "";
  opacityAddress.placeholder = "/composition/layers/.../video/opacity";
  opacityAddress.addEventListener("input", markDirty);
  const opacityAddressCell = document.createElement("div");
  opacityAddressCell.className = "osc-address-cell";
  opacityAddressCell.append(opacityAddress, makeOscAddressBuilder(opacityAddress, markDirty));
  opacityRow.append(opacityLabel, opacityAddressCell);
  opacityFieldset.append(opacityRow);
  nowPlayingOscForm.append(opacityFieldset);
}

function renderVisualsOscForm() {
  if (!appSettings || !visualsOscForm || visualsOscDirty || visualsOscForm.contains(document.activeElement)) return;
  visualsOscForm.replaceChildren();
  const markDirty = () => {
    visualsOscDirty = true;
    visualsOscStatus.textContent = "Unsaved Visuals OSC changes.";
  };

  const filters = document.createElement("div");
  filters.className = "osc-filter-tabs";
  [
    ["off", "Layer X / Off"],
    ["buttons", "Clip Buttons"],
    ["sliders", "Visual Sliders"],
    ["all", "All"],
  ].forEach(([key, label]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "osc-filter-button";
    button.dataset.visualOscSection = key;
    button.textContent = label;
    button.addEventListener("click", () => setActiveVisualOscSection(key));
    filters.append(button);
  });
  visualsOscForm.append(filters);

  const controls = visualControlsWithLayerOff();
  const offControls = controls.filter((item) => isVisualOffItem(item));
  const clipControls = controls.filter((item) => !isVisualOffItem(item));

  const makeButtonFieldset = (sectionKey, legendText, items, headerLabel) => {
    const fieldset = document.createElement("fieldset");
    fieldset.className = "wide-fieldset visual-osc-section";
    fieldset.dataset.visualOscSection = sectionKey;
    const legend = document.createElement("legend");
    legend.textContent = legendText;
    fieldset.append(legend);
    const header = document.createElement("div");
    header.className = "visual-setting-row visual-setting-header";
    header.innerHTML = `<span>${headerLabel}</span><span>OSC Address</span>`;
    fieldset.append(header);
    for (const item of items) {
      fieldset.append(makeVisualSettingRow(item, markDirty));
    }
    return fieldset;
  };

  visualsOscForm.append(makeButtonFieldset("off", "Layer Off / X Button OSC Addresses", offControls, "X Button Label"));
  visualsOscForm.append(makeButtonFieldset("buttons", "Visual Clip OSC Addresses", clipControls, "Clip Button Label"));

  const sliderFieldset = document.createElement("fieldset");
  sliderFieldset.className = "wide-fieldset visual-osc-section";
  sliderFieldset.dataset.visualOscSection = "sliders";
  const sliderLegend = document.createElement("legend");
  sliderLegend.textContent = "Visual Slider OSC Addresses";
  sliderFieldset.append(sliderLegend);
  const sliderHeader = document.createElement("div");
  sliderHeader.className = "visual-slider-setting-row visual-slider-setting-header";
  sliderHeader.innerHTML = "<span>Slider Label</span><span>OSC Address</span>";
  sliderFieldset.append(sliderHeader);
  for (const item of appSettings.visual_slider_controls || []) {
    sliderFieldset.append(makeVisualSliderSettingRow(item, markDirty));
  }
  visualsOscForm.append(sliderFieldset);
  setActiveVisualOscSection(activeVisualOscSection);
}
function setActiveVisualOscSection(key) {
  const validKeys = new Set(["off", "buttons", "sliders", "all"]);
  activeVisualOscSection = validKeys.has(key) ? key : "off";
  document.querySelectorAll("[data-visual-osc-section].osc-filter-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.visualOscSection === activeVisualOscSection);
  });
  document.querySelectorAll(".visual-osc-section").forEach((section) => {
    const show = activeVisualOscSection === "all" || section.dataset.visualOscSection === activeVisualOscSection;
    section.classList.toggle("active", show);
  });
}

function renderCamerasOscForm() {
  if (!appSettings || !camerasOscForm || camerasOscDirty || camerasOscForm.contains(document.activeElement)) return;
  camerasOscForm.replaceChildren();
  const markDirty = () => {
    camerasOscDirty = true;
    camerasOscStatus.textContent = "Unsaved Camera OSC changes.";
  };

  const filters = document.createElement("div");
  filters.className = "osc-filter-tabs";
  [
    ["main_box", "Main Box"],
    ["pip_box", "PIP Box"],
    ["background", "Background"],
    ["visuals_cams", "Visuals Cams"],
    ["scenes", "Scenes"],

    ["all", "All"],
  ].forEach(([key, label]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "osc-filter-button";
    button.dataset.cameraOscSection = key;
    button.textContent = label;
    button.addEventListener("click", () => setActiveCameraOscSection(key));
    filters.append(button);
  });
  camerasOscForm.append(filters);

  const cameraConfig = appSettings.camera_controls || {};
  const groupLabels = {
    main_box: "Main Box Cam OSC Addresses",
    pip_box: "PIP Box Cam OSC Addresses",
    background: "Background Cam OSC Addresses",
    visuals_cams: "Visuals Cam OSC Addresses",
  };
  for (const [groupKey, group] of Object.entries(cameraConfig.groups || {})) {
    const fieldset = makeCameraOscFieldset(groupKey, groupLabels[groupKey] || groupKey, "Button Label");
    for (const item of group) fieldset.append(makeCameraSettingRow("camera", item, markDirty));
    fieldset.append(makeCameraOpacitySettingRow(groupKey, cameraOpacityLabel(groupKey), markDirty));
    camerasOscForm.append(fieldset);
  }

  const sceneFieldset = makeCameraOscFieldset("scenes", "Scene OSC Addresses", "Scene Label");
  for (const item of cameraConfig.scenes || []) {
    sceneFieldset.append(makeCameraSettingRow("scene", item, markDirty));
  }
  camerasOscForm.append(sceneFieldset);

  setActiveCameraOscSection(activeCameraOscSection);
}

function makeCameraOscFieldset(sectionKey, legendText, firstHeader) {
  const fieldset = document.createElement("fieldset");
  fieldset.className = "wide-fieldset camera-osc-section";
  fieldset.dataset.cameraOscSection = sectionKey;
  const legend = document.createElement("legend");
  legend.textContent = legendText;
  fieldset.append(legend);
  const header = document.createElement("div");
  header.className = "camera-setting-row camera-setting-header";
  header.innerHTML = `<span>${firstHeader}</span><span>OSC Address</span>`;
  fieldset.append(header);
  return fieldset;
}

function setActiveCameraOscSection(key) {
  activeCameraOscSection = key;
  document.querySelectorAll("[data-camera-osc-section].osc-filter-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.cameraOscSection === key);
  });
  document.querySelectorAll(".camera-osc-section").forEach((section) => {
    const show = key === "all" || section.dataset.cameraOscSection === key;
    section.classList.toggle("active", show);
  });
}

function renderLocalOscForms() {
  renderLightsOscForm();
  renderVisualsOscForm();
  renderCamerasOscForm();
  renderNowPlayingOscForm();
}

function refreshCueLabelSurfaces() {
  renderVisualControls();
  renderCameraControls();
  renderPresetButtons(Object.keys(presetData?.groups?.performance || {}));
  renderLookBuilder();
  renderPresetLinks();
  renderLookLauncher();
  renderLookLinkForm();
  renderSequencer();
}

function setActiveSettingsSection(key) {
  activeSettingsSection = key;
  document.querySelectorAll(".settings-section-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.settingsSection === key);
  });
  document.querySelectorAll(".settings-section").forEach((section) => {
    section.classList.toggle("active", section.dataset.settingsSection === key);
  });
}

function renderLookLinkForm() {
  if (!appSettings || !presetData || !lookLinkForm || lookLinksDirty || lookLinkForm.contains(document.activeElement)) return;
  lookLinkForm.replaceChildren();
  const header = document.createElement("div");
  header.className = "preset-link-setting-row preset-link-setting-header";
  header.innerHTML = "<span>Look</span><span>Now Playing</span><span>Now Level</span><span>Section</span><span>Visual</span><span>Main Cam</span><span>PIP Cam</span><span>Background</span><span>Scene</span>";
  lookLinkForm.append(header);
  const performancePresets = presetData?.groups?.performance || appSettings.preset_groups?.groups?.performance || {};
  let presetIndex = 0;
  for (const name of Object.keys(performancePresets)) {
    lookLinkForm.append(makePresetLinkSettingRow(name, presetIndex));
    presetIndex += 1;
  }
}

function renderSequencer() {
  renderSequenceTimingTools();
  renderSequenceLookBank();
  if (!appSettings || !presetData || !showSequenceRows || showSequenceDirty || showSequenceRows.contains(document.activeElement)) return;
  const sequences = appSettings.show_sequences || {};
  const names = Object.keys(sequences);
  if (!names.includes(activeShowSequence)) activeShowSequence = names[0] || "Main Show";
  if (showSequenceSelect) {
    const current = showSequenceSelect.value || activeShowSequence;
    showSequenceSelect.replaceChildren();
    for (const name of names.length ? names : ["Main Show"]) {
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      showSequenceSelect.append(option);
    }
    showSequenceSelect.value = current && (names.includes(current) || !names.length) ? current : activeShowSequence;
    activeShowSequence = showSequenceSelect.value || activeShowSequence;
  }
  const sequence = sequences[activeShowSequence] || { name: activeShowSequence, steps: [] };
  if (showSequenceName) showSequenceName.value = sequence.name || activeShowSequence;
  if (showSequenceLoop) showSequenceLoop.checked = Boolean(sequence.loop);
  const steps = sequence.steps?.length ? sequence.steps : [{ look: Object.keys(presetData.groups?.performance || {})[0] || "", trigger_type: "after", amount: 0, unit: "bars", note: "Opening look" }];
  renderSequenceRowsFromSteps(steps);
}

function renderSequenceRowsFromSteps(steps) {
  if (!showSequenceRows) return;
  if (activeSequenceCueIndex >= steps.length) activeSequenceCueIndex = Math.max(0, steps.length - 1);
  showSequenceRows.replaceChildren();
  steps.forEach((step, index) => {
    showSequenceRows.append(makeSequenceStepRow(step, index, steps.length));
    showSequenceRows.append(makeSequenceInsertRow(index + 1));
  });
  if (!steps.length) showSequenceRows.append(makeSequenceInsertRow(0));
  updateActiveSequenceCueClass();
}

function renderSequenceTimingTools() {
  if (!sequenceTimingTools) return;
  if (sequenceTimingTools.contains(document.activeElement)) return;
  sequenceTimingTools.replaceChildren();

  const summary = document.createElement("section");
  summary.className = "sequence-timing-strip sequence-clock-compact";
  const modeBlock = makeBpmClockSummary("Timing", `Sequencer follows ${bpmClockSummaryText("app clock")}`);

  const divisionControl = document.createElement("label");
  divisionControl.className = "sequence-clock-select";
  const divisionLabel = document.createElement("span");
  divisionLabel.textContent = "Division";
  const divisionSelect = document.createElement("select");
  for (const division of appSettings?.bpm_divisions || DEFAULT_BPM_DIVISIONS) {
    const option = document.createElement("option");
    option.value = division;
    option.textContent = `${division} - ${formatDuration(intervalMsForDivision(currentSequenceBpm(), division))}`;
    divisionSelect.append(option);
  }
  divisionSelect.value = selectedDivision;
  divisionSelect.addEventListener("change", () => updateAppBpmDivision(divisionSelect.value));
  divisionControl.append(divisionLabel, divisionSelect);

  const secondsControls = document.createElement("div");
  secondsControls.className = "sequence-seconds-compact";
  const secondsValue = currentBpmSecondsValue();
  const secondsInput = document.createElement("input");
  secondsInput.type = "number";
  secondsInput.min = "0.1";
  secondsInput.max = "3600";
  secondsInput.step = "0.1";
  secondsInput.value = String(secondsValue);
  secondsInput.ariaLabel = "Seconds between color rotations";
  const secondsReadout = document.createElement("strong");
  secondsReadout.textContent = `Every ${formatDuration(secondsValue * 1000)}`;
  const syncSeconds = () => {
    const next = Math.max(0.1, Number(secondsInput.value) || secondsValue);
    secondsInput.value = String(next);
    secondsReadout.textContent = `Every ${formatDuration(next * 1000)}`;
  };
  secondsInput.addEventListener("input", syncSeconds);
  const useSeconds = document.createElement("button");
  useSeconds.type = "button";
  useSeconds.textContent = "Use Seconds";
  useSeconds.addEventListener("click", () => sendCommand({ command: "bpm_update", seconds: secondsInput.value }));
  secondsControls.append(secondsInput, secondsReadout, useSeconds);

  summary.append(modeBlock, divisionControl, secondsControls);
  sequenceTimingTools.append(summary);
}

function renderSequenceLookBank() {
  if (!sequenceLookBank || !appSettings || !presetData) return;
  if (sequenceLookBank.contains(document.activeElement)) return;
  renderSequenceBankFilters();
  sequenceLookBank.replaceChildren();
  if (sequenceBankHint) sequenceBankHint.textContent = sequenceBankMode === "looks" ? "Looks append" : "Applies to cue";
  if (sequenceBankMode !== "looks") {
    const activeHint = document.createElement("div");
    activeHint.className = "sequence-bank-active-cue";
    activeHint.textContent = `Active cue ${activeSequenceCueIndex + 1}`;
    sequenceLookBank.append(activeHint);
  }

  if (sequenceBankMode === "visuals") {
    renderSequenceItemBank(appSettings.visual_controls || [], (item) => applySequenceCuePatch({ visual_id: item.id }), "No visual buttons configured.");
    return;
  }

  if (["main_box", "pip_box", "background", "visuals_cams"].includes(sequenceBankMode)) {
    const cameraConfig = appSettings?.camera_controls || {};
    renderSequenceItemBank(cameraConfig.groups?.[sequenceBankMode] || [], (item) => applySequenceCuePatch({ [`${sequenceBankMode}_id`]: item.id }), "No camera buttons configured.");
    return;
  }

  if (sequenceBankMode === "scene") {
    const cameraConfig = appSettings?.camera_controls || {};
    renderSequenceItemBank(cameraConfig.scenes || [], (item) => applySequenceCuePatch({ scene_id: item.id }), "No scene buttons configured.");
    return;
  }

  const performancePresets = presetData?.groups?.performance || {};
  const names = Object.keys(performancePresets);
  if (!names.length) {
    const empty = document.createElement("div");
    empty.className = "sequence-empty-bank";
    empty.textContent = "Save a look first.";
    sequenceLookBank.append(empty);
    return;
  }
  for (const name of names) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "sequence-look-bank-button";
    const label = document.createElement("span");
    label.className = "sequence-look-bank-label";
    label.textContent = name;
    button.append(label, makeLookSwatches(performancePresets[name]));
    button.addEventListener("click", () => appendLookToSequence(name));
    sequenceLookBank.append(button);
  }
}

function renderSequenceBankFilters() {
  if (!sequenceBankFilters) return;
  sequenceBankFilters.replaceChildren();
  for (const [mode, label] of SEQUENCE_BANK_MODES) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.className = "sequence-bank-filter";
    button.classList.toggle("active", sequenceBankMode === mode);
    button.addEventListener("click", () => {
      sequenceBankMode = mode;
      renderSequenceLookBank();
    });
    sequenceBankFilters.append(button);
  }
}

function renderSequenceItemBank(items, onPick, emptyText) {
  if (!items?.length) {
    const empty = document.createElement("div");
    empty.className = "sequence-empty-bank";
    empty.textContent = emptyText;
    sequenceLookBank.append(empty);
    return;
  }
  for (const item of items) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "sequence-look-bank-button sequence-cue-palette-button";
    const label = document.createElement("span");
    label.className = "sequence-look-bank-label";
    label.textContent = item.label || item.name || item.id;
    const meta = document.createElement("small");
    meta.textContent = item.id;
    button.append(label, meta);
    button.addEventListener("click", () => onPick(item));
    sequenceLookBank.append(button);
  }
}

function makeSequenceStepRow(step, index, totalSteps) {
  const row = document.createElement("div");
  row.className = "show-sequence-row sequence-cue-card";
  row.dataset.index = String(index);
  row.addEventListener("click", () => setActiveSequenceCueIndex(index));
  applyCuePaletteVars(row, step.look);

  const durationMs = sequenceStepDurationMs(step);
  const durationLabel = formatDuration(durationMs);
  const span = Math.max(8, Math.min(100, Math.round(durationMs / Math.max(1, intervalMsForDivision(currentSequenceBpm(), "1 bar")) * 18)));
  row.style.setProperty("--cue-span", `${span}%`);

  const header = document.createElement("div");
  header.className = "sequence-step-header";
  const number = document.createElement("div");
  number.className = "sequence-cue-heading";
  number.innerHTML = `<span>Cue ${index + 1}</span><strong>${step.look || "Choose a look"}</strong><small>${step.trigger_type === "at" ? "At show time" : "After previous"} - ${durationLabel}</small>`;
  const moveControls = document.createElement("div");
  moveControls.className = "sequence-step-tools";
  const moveUp = document.createElement("button");
  moveUp.type = "button";
  moveUp.textContent = "Earlier";
  moveUp.disabled = index === 0;
  moveUp.addEventListener("click", () => moveSequenceStep(index, -1));
  const moveDown = document.createElement("button");
  moveDown.type = "button";
  moveDown.textContent = "Later";
  moveDown.disabled = index >= totalSteps - 1;
  moveDown.addEventListener("click", () => moveSequenceStep(index, 1));
  const remove = document.createElement("button");
  remove.type = "button";
  remove.textContent = "Remove";
  remove.addEventListener("click", () => removeSequenceStep(index));
  moveControls.append(moveUp, moveDown, remove);
  header.append(number, moveControls);

  const look = selectForPresetNames(`sequence_look_${index}`, presetData.groups?.performance || {}, step.look, "Select look", markSequenceDirty);
  look.classList.add("sequence-look-select");
  let lookPreview = makeSequenceLookPreview(step);
  look.addEventListener("input", () => {
    const nextStep = { ...step, look: look.value };
    applyCuePaletteVars(row, look.value);
    number.querySelector("strong").textContent = look.value || "Choose a look";
    const nextPreview = makeSequenceLookPreview(nextStep);
    lookPreview.replaceWith(nextPreview);
    lookPreview = nextPreview;
  });
  const trigger = document.createElement("select");
  trigger.name = `sequence_trigger_${index}`;
  [["after", "After previous"], ["at", "At show time"]].forEach(([value, label]) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    trigger.append(option);
  });
  trigger.value = step.trigger_type || "after";
  trigger.addEventListener("input", markSequenceDirty);

  const details = document.createElement("div");
  details.className = "sequence-step-details";
  const lookField = wrapSequenceField("Look", look);
  const triggerField = wrapSequenceField("Cue Type", trigger);

  const amount = document.createElement("input");
  amount.name = `sequence_amount_${index}`;
  amount.type = "number";
  amount.min = "0";
  amount.step = "1";
  amount.value = step.amount ?? 1;

  const unit = document.createElement("select");
  unit.name = `sequence_unit_${index}`;
  [["bars", "Bars"], ["beats", "Beats"], ["seconds", "Seconds"], ["minutes", "Minutes"]].forEach(([value, label]) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    unit.append(option);
  });
  unit.value = step.unit || "bars";

  const range = document.createElement("input");
  range.type = "range";
  range.className = "sequence-amount-slider";
  const preview = document.createElement("div");
  preview.className = "sequence-duration-preview";

  const configureAmountControls = () => {
    const limits = STEP_AMOUNT_LIMITS[unit.value] || STEP_AMOUNT_LIMITS.bars;
    amount.min = String(limits.min);
    amount.max = String(limits.max);
    amount.step = String(limits.step);
    range.min = String(limits.min);
    range.max = String(limits.max);
    range.step = String(limits.step);
    const clamped = Math.max(limits.min, Math.min(limits.max, Number(amount.value || 0)));
    range.value = String(clamped);
    const nextDuration = formatDuration(durationMsForAmount(amount.value, unit.value));
    preview.textContent = `${trigger.value === "at" ? "At" : "Wait"} ${nextDuration}`;
  };
  amount.addEventListener("input", () => {
    range.value = String(amount.value || 0);
    configureAmountControls();
    markSequenceDirty();
  });
  range.addEventListener("input", () => {
    amount.value = range.value;
    configureAmountControls();
    markSequenceDirty();
  });
  unit.addEventListener("input", () => {
    configureAmountControls();
    markSequenceDirty();
  });
  trigger.addEventListener("input", configureAmountControls);
  configureAmountControls();

  const quickDurations = document.createElement("div");
  quickDurations.className = "sequence-duration-chips";
  const durationChoices = [
    ["1b", 1, "bars"],
    ["2b", 2, "bars"],
    ["4b", 4, "bars"],
    ["8b", 8, "bars"],
    ["30s", 30, "seconds"],
  ];
  for (const [label, value, unitName] of durationChoices) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.classList.toggle("active", Number(amount.value || 0) === value && unit.value === unitName);
    button.addEventListener("click", () => {
      amount.value = String(value);
      unit.value = unitName;
      configureAmountControls();
      markSequenceDirty();
      renderSequenceRowsFromSteps(collectShowSequenceSteps());
    });
    quickDurations.append(button);
  }

  const timing = document.createElement("div");
  timing.className = "sequence-step-timing";
  timing.append(wrapSequenceField("Wait", amount), wrapSequenceField("Unit", unit), range, quickDurations, preview);

  const note = document.createElement("input");
  note.name = `sequence_note_${index}`;
  note.value = step.note || "";
  note.placeholder = "Intro, drop, guest cam...";
  note.addEventListener("input", markSequenceDirty);
  const noteField = wrapSequenceField("Label", note);

  const durationBar = document.createElement("div");
  durationBar.className = "sequence-cue-bar";
  durationBar.innerHTML = `<span></span><strong>${durationLabel}</strong>`;

  const cameraConfig = appSettings?.camera_controls || {};
  const overrides = document.createElement("div");
  overrides.className = "sequence-cue-overrides";
  overrides.append(
    wrapSequenceField("Visual", selectForItems(`sequence_visual_${index}`, appSettings.visual_controls || [], step.visual_id, "Use look", markSequenceDirty)),
    wrapSequenceField("Main Cam", selectForItems(`sequence_main_${index}`, cameraConfig.groups?.main_box || [], step.main_box_id, "Use look", markSequenceDirty)),
    wrapSequenceField("PIP Cam", selectForItems(`sequence_pip_${index}`, cameraConfig.groups?.pip_box || [], step.pip_box_id, "Use look", markSequenceDirty)),
    wrapSequenceField("BG Cam", selectForItems(`sequence_background_${index}`, cameraConfig.groups?.background || [], step.background_id, "Use look", markSequenceDirty)),
    wrapSequenceField("Visuals Cam", selectForItems(`sequence_visuals_cams_${index}`, cameraConfig.groups?.visuals_cams || [], step.visuals_cams_id, "Use look", markSequenceDirty)),
    wrapSequenceField("Scene", selectForItems(`sequence_scene_${index}`, cameraConfig.scenes || [], step.scene_id, "Use look", markSequenceDirty)),
  );

  row.append(header, durationBar);
  row.append(lookPreview);
  details.append(lookField, triggerField, timing, noteField);
  row.append(details, overrides);
  return row;
}

function wrapSequenceField(labelText, control) {
  const label = document.createElement("label");
  label.className = "sequence-field";
  const span = document.createElement("span");
  span.textContent = labelText;
  label.append(span, control);
  return label;
}

function setActiveSequenceCueIndex(index) {
  activeSequenceCueIndex = Math.max(0, Number(index) || 0);
  updateActiveSequenceCueClass();
  renderSequenceLookBank();
}

function updateActiveSequenceCueClass() {
  showSequenceRows?.querySelectorAll(".sequence-cue-card").forEach((row) => {
    row.classList.toggle("active", Number(row.dataset.index) === activeSequenceCueIndex);
  });
}

function applySequenceCuePatch(patch) {
  const steps = collectShowSequenceSteps();
  if (!steps.length) {
    steps.push({ look: "", trigger_type: "after", amount: 0, unit: "bars", note: "", ...patch });
    activeSequenceCueIndex = 0;
  } else {
    const index = Math.max(0, Math.min(activeSequenceCueIndex, steps.length - 1));
    steps[index] = { ...steps[index], ...patch };
    activeSequenceCueIndex = index;
  }
  renderSequenceRowsFromSteps(steps);
  markSequenceDirty();
}

function activeSequenceWait() {
  if (latestShow?.bpm_flip_mode === "seconds") {
    return { amount: Math.max(1, Math.round(Number(latestShow?.bpm_seconds || appSettings?.bpm_flip_seconds || 8) || 8)), unit: "seconds" };
  }
  const division = latestShow?.bpm_division || selectedDivision || "1 bar";
  const barsMatch = String(division).match(/^(\d+)\s+bars?$/i);
  if (barsMatch) return { amount: Number(barsMatch[1]), unit: "bars" };
  if (division === "1/2 bar") return { amount: 2, unit: "beats" };
  const multiplier = BPM_DIVISION_MULTIPLIERS[division] || BPM_DIVISION_MULTIPLIERS["1 bar"];
  return { amount: Math.max(1, Math.round(multiplier)), unit: "beats" };
}

function makeSequenceInsertRow(afterIndex) {
  const wrap = document.createElement("div");
  wrap.className = "sequence-insert-row";
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = afterIndex ? `Insert cue after ${afterIndex}` : "Add first cue";
  button.addEventListener("click", () => addShowSequenceStep(afterIndex));
  wrap.append(button);
  return wrap;
}

function markSequenceDirty() {
  showSequenceDirty = true;
  if (showSequenceStatus) showSequenceStatus.textContent = "Unsaved show sequence changes.";
}

function collectShowSequencePayload() {
  const sequenceName = (showSequenceName?.value || activeShowSequence || "Main Show").trim();
  const sequences = { ...(appSettings.show_sequences || {}) };
  if (activeShowSequence && activeShowSequence !== sequenceName) delete sequences[activeShowSequence];
  const steps = collectShowSequenceSteps();
  sequences[sequenceName] = { name: sequenceName, loop: Boolean(showSequenceLoop?.checked), steps };
  return { show_sequences: sequences };
}

function collectShowSequenceSteps() {
  const steps = [];
  showSequenceRows?.querySelectorAll(".show-sequence-row:not(.show-sequence-header)").forEach((row, index) => {
    steps.push({
      look: row.querySelector(`[name^="sequence_look_"]`)?.value || "",
      trigger_type: row.querySelector(`[name^="sequence_trigger_"]`)?.value || "after",
      amount: Number(row.querySelector(`[name^="sequence_amount_"]`)?.value || 0),
      unit: row.querySelector(`[name^="sequence_unit_"]`)?.value || "bars",
      note: row.querySelector(`[name^="sequence_note_"]`)?.value || "",
      visual_id: row.querySelector(`[name^="sequence_visual_"]`)?.value || "",
      main_box_id: row.querySelector(`[name^="sequence_main_"]`)?.value || "",
      pip_box_id: row.querySelector(`[name^="sequence_pip_"]`)?.value || "",
      background_id: row.querySelector(`[name^="sequence_background_"]`)?.value || "",
      visuals_cams_id: row.querySelector(`[name^="sequence_visuals_cams_"]`)?.value || "",
      scene_id: row.querySelector(`[name^="sequence_scene_"]`)?.value || "",
    });
    row.dataset.index = String(index);
  });
  return steps;
}

async function saveShowSequencePayload() {
  if (!showSequenceName?.value.trim()) {
    showSequenceStatus.textContent = "Name the show first.";
    return;
  }
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectShowSequencePayload()),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    activeShowSequence = showSequenceName.value.trim();
    showSequenceDirty = false;
    showSequenceStatus.textContent = `Saved show ${activeShowSequence}.`;
    showToast(`Saved show ${activeShowSequence}`);
    renderSequencer();
    await loadStatus();
  } catch (error) {
    const message = String(error.message || error);
    showSequenceStatus.textContent = message;
    showToast(message, true);
  }
}

function addShowSequenceStep(afterIndex = null) {
  if (!showSequenceRows) return;
  const steps = collectShowSequenceSteps();
  const insertAt = Number.isInteger(afterIndex) ? Math.max(0, Math.min(steps.length, afterIndex)) : steps.length;
  const wait = steps.length ? activeSequenceWait() : { amount: 0, unit: "bars" };
  steps.splice(insertAt, 0, { look: "", trigger_type: "after", amount: wait.amount, unit: wait.unit, note: "" });
  activeSequenceCueIndex = insertAt;
  renderSequenceRowsFromSteps(steps);
  markSequenceDirty();
}

function appendLookToSequence(name) {
  if (!showSequenceRows || !name) return;
  const steps = collectShowSequenceSteps();
  const isFirstEmpty = steps.length === 1 && !steps[0].look;
  const wait = isFirstEmpty ? { amount: 0, unit: "bars" } : activeSequenceWait();
  const nextStep = {
    look: name,
    trigger_type: "after",
    amount: wait.amount,
    unit: wait.unit,
    note: "",
  };
  if (isFirstEmpty) {
    steps[0] = nextStep;
    activeSequenceCueIndex = 0;
  } else {
    steps.push(nextStep);
    activeSequenceCueIndex = steps.length - 1;
  }
  renderSequenceRowsFromSteps(steps);
  markSequenceDirty();
}

function moveSequenceStep(index, direction) {
  const steps = collectShowSequenceSteps();
  const nextIndex = index + direction;
  if (nextIndex < 0 || nextIndex >= steps.length) return;
  const [step] = steps.splice(index, 1);
  steps.splice(nextIndex, 0, step);
  renderSequenceRowsFromSteps(steps);
  markSequenceDirty();
}

function removeSequenceStep(index) {
  const steps = collectShowSequenceSteps();
  steps.splice(index, 1);
  renderSequenceRowsFromSteps(steps);
  markSequenceDirty();
}

function currentSequenceBpm() {
  return Math.max(1, Number(bpmInput?.value || latestShow?.bpm || 120) || 120);
}

function sequenceStepDurationMs(step) {
  return durationMsForAmount(step?.amount, step?.unit || "bars");
}

function sequenceStepHasAction(step) {
  return Boolean(step?.look || step?.visual_id || step?.main_box_id || step?.pip_box_id || step?.background_id || step?.visuals_cams_id || step?.scene_id);
}

function sequenceStepLabel(step) {
  if (step?.look) return step.look;
  if (step?.visual_id) return optionLabel(appSettings?.visual_controls, step.visual_id, step.visual_id);
  const cameraConfig = appSettings?.camera_controls || {};
  if (step?.main_box_id) return optionLabel(cameraConfig.groups?.main_box, step.main_box_id, step.main_box_id);
  if (step?.pip_box_id) return optionLabel(cameraConfig.groups?.pip_box, step.pip_box_id, step.pip_box_id);
  if (step?.background_id) return optionLabel(cameraConfig.groups?.background, step.background_id, step.background_id);
  if (step?.visuals_cams_id) return optionLabel(cameraConfig.groups?.visuals_cams, step.visuals_cams_id, step.visuals_cams_id);
  if (step?.scene_id) return optionLabel(cameraConfig.scenes, step.scene_id, step.scene_id);
  return "Cue";
}

function delayBeforeSequenceStep(step) {
  const duration = sequenceStepDurationMs(step);
  if (step?.trigger_type === "at") {
    return Math.max(0, duration - Math.max(0, Date.now() - showSequenceStartedAt));
  }
  return duration;
}

function setSequenceTransport(label, detail = "") {
  if (showSequenceTransport) showSequenceTransport.textContent = label;
  if (showSequenceStatus) showSequenceStatus.textContent = detail || label;
}

function clearSequenceTimer() {
  if (showSequenceTimer) clearTimeout(showSequenceTimer);
  showSequenceTimer = null;
}

async function triggerSequenceStep(index, providedSteps = null, transportLabel = "Playing") {
  const steps = (providedSteps || collectShowSequenceSteps()).filter(sequenceStepHasAction);
  if (!steps.length) {
    stopShowSequencePlayback("No cue actions are ready to trigger.");
    return false;
  }
  const step = steps[index];
  if (!step) return false;
  showSequenceStepIndex = index;
  const detail = `${index + 1}/${steps.length}: ${sequenceStepLabel(step)}${step.note ? ` - ${step.note}` : ""}`;
  setSequenceTransport(showSequencePaused ? "Paused" : transportLabel, detail);
  if (step.look) await sendCommandForResult(linkedLookPayload(step.look));
  if (step.visual_id) await sendCommandForResult({ command: "visual_trigger", id: step.visual_id });
  if (step.main_box_id) await sendCommandForResult({ command: "camera_trigger", kind: "camera", group: "main_box", id: step.main_box_id });
  if (step.pip_box_id) await sendCommandForResult({ command: "camera_trigger", kind: "camera", group: "pip_box", id: step.pip_box_id });
  if (step.background_id) await sendCommandForResult({ command: "camera_trigger", kind: "camera", group: "background", id: step.background_id });
  if (step.visuals_cams_id) await sendCommandForResult({ command: "camera_trigger", kind: "camera", group: "visuals_cams", id: step.visuals_cams_id });
  if (step.scene_id) await sendCommandForResult({ command: "camera_trigger", kind: "scene", id: step.scene_id });
  await loadStatus();
  return true;
}

function scheduleSequenceAdvance(index) {
  clearSequenceTimer();
  const steps = collectShowSequenceSteps().filter(sequenceStepHasAction);
  if (!showSequenceRunning || showSequencePaused || !steps[index]) return;
  const nextIndex = index + 1;
  if (nextIndex >= steps.length) {
    if (!showSequenceLoop?.checked) {
      stopShowSequencePlayback("Show complete.");
      return;
    }
    const delay = Math.max(100, delayBeforeSequenceStep(steps[0]));
    showSequenceTimer = setTimeout(() => {
      showSequenceStartedAt = Date.now();
      runSequenceFrom(0);
    }, delay);
    return;
  }
  const delay = Math.max(100, delayBeforeSequenceStep(steps[nextIndex]));
  showSequenceTimer = setTimeout(() => {
    runSequenceFrom(nextIndex);
  }, delay);
}

async function runSequenceFrom(index) {
  const didTrigger = await triggerSequenceStep(index);
  if (didTrigger) scheduleSequenceAdvance(index);
}

function startShowSequencePlayback() {
  const steps = collectShowSequenceSteps().filter(sequenceStepHasAction);
  if (!steps.length) {
    setSequenceTransport("Stopped", "Add at least one cue action before playing the show.");
    return;
  }
  showSequenceRunning = true;
  showSequencePaused = false;
  const startIndex = showSequenceStepIndex < steps.length ? showSequenceStepIndex : 0;
  showSequenceStartedAt = Date.now() - (startIndex ? sequenceStepDurationMs(steps[startIndex]) : 0);
  runSequenceFrom(startIndex);
}

function pauseShowSequencePlayback() {
  if (!showSequenceRunning) return;
  clearSequenceTimer();
  showSequencePaused = true;
  setSequenceTransport("Paused", `Paused at step ${showSequenceStepIndex + 1}.`);
}

function stopShowSequencePlayback(message = "Stopped.") {
  clearSequenceTimer();
  showSequenceRunning = false;
  showSequencePaused = false;
  showSequenceStepIndex = 0;
  showSequenceStartedAt = 0;
  setSequenceTransport("Stopped", message);
}

function triggerNextShowSequenceStep() {
  const steps = collectShowSequenceSteps().filter(sequenceStepHasAction);
  if (!steps.length) {
    setSequenceTransport("Stopped", "Add at least one cue action before stepping.");
    return;
  }
  clearSequenceTimer();
  const nextIndex = showSequenceRunning && !showSequencePaused ? Math.min(showSequenceStepIndex + 1, steps.length - 1) : showSequenceStepIndex;
  showSequenceRunning = true;
  showSequencePaused = false;
  if (!showSequenceStartedAt) showSequenceStartedAt = Date.now();
  runSequenceFrom(nextIndex);
}

function renderQuickSettingsForm() {
  if (!appSettings || quickSettingsDirty) return;
  quickSettingsForm.replaceChildren();
  for (const [key, label, kind] of quickSettingFields) {
    quickSettingsForm.append(makeQuickField(key, label, kind));
  }
}

function renderArtworkOptions() {
  if (!appSettings) return;
  fillColorSelect(neutralArtworkPrimary, appSettings.neutral_artwork_primary || appSettings.neutral_artwork_color || "teal");
  fillColorSelect(neutralArtworkSecondary, appSettings.neutral_artwork_secondary || "blue");
  fillColorSelect(neutralArtworkAccent, appSettings.neutral_artwork_accent || "magenta");
  setToggleButton(keepPresetColorsToggle, Boolean(appSettings.preset_keep_current_colors), "Keep Preset Colors");
  setToggleButton(autoArtworkToggle, Boolean(appSettings.use_artwork_palette), "Auto Artwork Colors");
  renderLookLightsModeControls();
}

function renderLookLightsModeControls() {
  const enabled = lookApplyLights();
  lookLightsToggles.forEach((button) => {
    button.classList.toggle("active", enabled);
    button.ariaPressed = String(enabled);
    button.textContent = `Look Lights: ${enabled ? "ON" : "OFF"}`;
    button.title = enabled ? "Looks recall lighting plus media cues" : "Looks recall media cues and leave lights held";
  });
}

async function saveLookLightsMode(enabled) {
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ look_apply_lights: enabled }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    renderLookLightsModeControls();
    renderQuickSettingsForm();
    renderSettingsForm();
      renderObsSettingsForm();
    refreshLookDispatchSurfaces();
    showToast(enabled ? "Look lights on" : "Look lights held");
  } catch (error) {
    showToast(String(error.message || error), true);
    renderLookLightsModeControls();
  }
}

function fillColorSelect(select, selectedValue) {
  if (!select) return;
  const currentValue = select.value;
  select.replaceChildren();
  for (const name of appSettings.colors.names || []) {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = name;
    select.append(option);
  }
  select.value = selectedValue || currentValue || "blue";
}

function setToggleButton(button, enabled, label) {
  if (!button) return;
  button.classList.toggle("active", enabled);
  button.textContent = `${label}: ${enabled ? "ON" : "OFF"}`;
}

function makeQuickField(key, labelText, kind) {
  if (kind === "checks:bpm-rotation") {
    const field = document.createElement("div");
    field.className = "quick-field quick-checkset";
    const checks = makeBpmRotationChecks({
      className: "bpm-rotation-checks quick-bpm-rotation",
      name: key,
      title: labelText,
      value: appSettings[key],
      onChange: () => {
        quickSettingsDirty = true;
        quickSettingsStatus.textContent = "Unsaved quick settings.";
      },
    });
    field.append(checks);
    return field;
  }

  const label = document.createElement("label");
  label.className = kind === "checkbox" ? "quick-field quick-toggle" : "quick-field";
  const span = document.createElement("span");
  span.textContent = labelText;
  label.append(span);

  let input;
  if (kind === "select:color") {
    input = document.createElement("select");
    for (const name of appSettings.colors.names || []) {
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      input.append(option);
    }
  } else if (kind === "select:bpm") {
    input = document.createElement("select");
    for (const division of appSettings.bpm_divisions || []) {
      const option = document.createElement("option");
      option.value = division;
      option.textContent = division;
      input.append(option);
    }
  } else if (kind === "checkbox") {
    input = document.createElement("input");
    input.type = "checkbox";
  } else {
    input = document.createElement("input");
    input.type = "text";
  }

  input.name = key;
  if (kind === "number" && (key === "output_pixels" || key.endsWith("_artwork_width") || key.endsWith("_artwork_height"))) {
    input.min = "64";
    input.max = "4096";
    input.step = "1";
    input.inputMode = "numeric";
  }
  if (kind === "checkbox") {
    input.checked = Boolean(appSettings[key]);
  } else {
    input.value = appSettings[key] ?? "";
  }
  input.addEventListener("input", () => {
    quickSettingsDirty = true;
    quickSettingsStatus.textContent = "Unsaved quick settings.";
  });
  label.append(input);
  return label;
}

async function saveArtworkOptionPayload(payload, options = {}) {
  const statusEl = options.statusEl || paletteStatus;
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    renderArtworkOptions();
    if (appSettings?.use_artwork_palette) {
      if (statusEl) statusEl.textContent = "Auto artwork colors enabled. Applying current artwork now.";
      await refreshPalette(true, options);
    } else {
      await refreshPalette(false, options);
    }
  } catch (error) {
    if (statusEl) statusEl.textContent = String(error.message || error);
  }
}

function collectQuickSettingsPayload() {
  const data = new FormData(quickSettingsForm);
  const payload = {};
  for (const [key, _label, kind] of quickSettingFields) {
    if (kind === "checks:bpm-rotation") {
      payload[key] = collectBpmRotationSlots(quickSettingsForm);
      continue;
    }
    const field = quickSettingsForm.elements[key];
    payload[key] = kind === "checkbox" ? Boolean(field.checked) : data.get(key);
  }
  return payload;
}

async function saveQuickSettingsPayload() {
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectQuickSettingsPayload()),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    quickSettingsDirty = false;
    quickSettingsStatus.textContent = "Quick settings saved.";
    if (result.state) renderShowState(result.state);
    renderQuickSettingsForm();
    renderSettingsForm();
      renderObsSettingsForm();
    renderLocalOscForms();
    await loadStatus();
  } catch (error) {
    quickSettingsStatus.textContent = String(error.message || error);
  }
}

function markSettingsDirty() {
  settingsDirty = true;
  settingsStatus.textContent = "Unsaved settings changes.";
}

function makeBltOutputRow(output, onDirty = markSettingsDirty) {
  const row = document.createElement("div");
  row.className = "blt-output-row";
  row.dataset.outputKey = output.key;

  const enabled = document.createElement("input");
  enabled.type = "checkbox";
  enabled.name = `blt_enabled_${output.key}`;
  enabled.checked = Boolean(output.enabled);

  const label = document.createElement("input");
  label.name = `blt_label_${output.key}`;
  label.value = output.label || output.key;

  const field = document.createElement("select");
  field.name = `blt_field_${output.key}`;
  for (const fieldName of appSettings.blt_field_choices || []) {
    const option = document.createElement("option");
    option.value = fieldName;
    option.textContent = fieldName;
    field.append(option);
  }
  field.value = output.field || "full_track";

  const address = document.createElement("input");
  address.name = `blt_address_${output.key}`;
  address.value = output.address || "";
  address.placeholder = "/composition/layers/.../clips/.../video/source/.../text/params/lines";

  for (const input of [enabled, label, field, address]) {
    input.addEventListener("input", onDirty);
  }

  const addressCell = document.createElement("div");
  addressCell.className = "osc-address-cell";
  addressCell.append(address, makeOscAddressBuilder(address, onDirty));

  row.append(enabled, label, field, addressCell);
  return row;
}

function makeCameraOpacitySettingRow(groupKey, labelText, onDirty = markSettingsDirty) {
  const row = document.createElement("div");
  row.className = "camera-setting-row camera-opacity-setting-row";
  const label = document.createElement("input");
  label.name = `camera_opacity_label_${groupKey}`;
  label.value = appSettings?.camera_opacity_labels?.[groupKey] || labelText;
  label.addEventListener("input", onDirty);

  const address = document.createElement("input");
  address.name = `camera_opacity_${groupKey}`;
  address.value = appSettings?.camera_opacity_addresses?.[groupKey] || "";
  address.placeholder = "/composition/layers/.../video/opacity";
  address.addEventListener("input", onDirty);

  const addressCell = document.createElement("div");
  addressCell.className = "osc-address-cell";
  addressCell.append(address, makeOscAddressBuilder(address, onDirty));
  row.append(label, addressCell);
  return row;
}

function makeCameraSettingRow(kind, item, onDirty = markSettingsDirty) {
  const row = document.createElement("div");
  row.className = "camera-setting-row";
  const label = document.createElement("input");
  label.name = `camera_label_${item.id}`;
  label.value = item.label || item.name || item.id;

  const address = document.createElement("input");
  address.name = `camera_address_${item.id}`;
  address.value = item.address || "";
  address.placeholder = "/composition/layers/.../clips/.../connect";

  label.addEventListener("input", () => updateCameraControlDraft(kind, item.id, { name: label.value, label: label.value }));
  address.addEventListener("input", () => updateCameraControlDraft(kind, item.id, { address: address.value }));

  for (const input of [label, address]) {
    input.dataset.cameraKind = kind;
    input.addEventListener("input", onDirty);
  }

  const addressCell = document.createElement("div");
  addressCell.className = "osc-address-cell";
  addressCell.append(address, makeOscAddressBuilder(address, onDirty, (value) => updateCameraControlDraft(kind, item.id, { address: value })));

  row.append(label, addressCell);
  return row;
}

function makeVisualSettingRow(item, onDirty = markSettingsDirty) {
  const row = document.createElement("div");
  row.className = "visual-setting-row";
  row.classList.toggle("visual-off-setting-row", isVisualOffItem(item));
  row.dataset.visualControlId = item.id;
  row.dataset.visualKind = isVisualOffItem(item) ? "off" : "clip";
  const label = document.createElement("input");
  label.name = `visual_label_${item.id}`;
  label.value = item.label || item.name || item.id;
  label.dataset.visualControlId = item.id;

  const address = document.createElement("input");
  address.name = `visual_address_${item.id}`;
  address.value = item.address || "";
  address.placeholder = isVisualOffItem(item) ? "/composition/layers/.../clear" : "/composition/groups/.../columns/.../connect";
  address.dataset.visualAddressId = item.id;

  label.addEventListener("input", () => updateVisualControlDraft(item.id, { name: label.value, label: label.value }));
  address.addEventListener("input", () => updateVisualControlDraft(item.id, { address: address.value }));

  for (const input of [label, address]) {
    input.addEventListener("input", onDirty);
  }

  const addressCell = document.createElement("div");
  addressCell.className = "osc-address-cell";
  addressCell.append(address, makeOscAddressBuilder(address, onDirty, (value) => updateVisualControlDraft(item.id, { address: value })));

  row.append(label, addressCell);
  return row;
}
function makeVisualSliderSettingRow(item, onDirty = markSettingsDirty) {
  const row = document.createElement("div");
  row.className = "visual-slider-setting-row";
  const label = document.createElement("input");
  label.name = `visual_slider_label_${item.id}`;
  label.value = item.label || item.name || item.id;

  const address = document.createElement("input");
  address.name = `visual_slider_address_${item.id}`;
  address.value = item.address || "";
  address.placeholder = "/composition/layers/.../video/opacity";

  label.addEventListener("input", () => updateVisualSliderDraft(item.id, { name: label.value, label: label.value }));
  address.addEventListener("input", () => updateVisualSliderDraft(item.id, { address: address.value }));

  for (const input of [label, address]) {
    input.addEventListener("input", onDirty);
  }

  const addressCell = document.createElement("div");
  addressCell.className = "osc-address-cell";
  addressCell.append(address, makeOscAddressBuilder(address, onDirty, (value) => updateVisualSliderDraft(item.id, { address: value })));

  row.append(label, addressCell);
  return row;
}

function updateVisualControlDraft(id, patch) {
  const item = (appSettings?.visual_controls || []).find((candidate) => candidate.id === id);
  if (!item) return;
  Object.assign(item, patch);
  refreshCueLabelSurfaces();
}

function updateVisualSliderDraft(id, patch) {
  const item = (appSettings?.visual_slider_controls || []).find((candidate) => candidate.id === id);
  if (!item) return;
  Object.assign(item, patch);
}

function updateCameraControlDraft(kind, id, patch) {
  const cameraConfig = appSettings?.camera_controls || {};
  const items = kind === "scene"
    ? cameraConfig.scenes || []
    : Object.values(cameraConfig.groups || {}).flat();
  const item = items.find((candidate) => candidate.id === id);
  if (!item) return;
  Object.assign(item, patch);
  refreshCueLabelSurfaces();
}

function selectForItems(name, items, selectedId, emptyText = "None", onDirty = null) {
  const select = document.createElement("select");
  select.name = name;
  const empty = document.createElement("option");
  empty.value = "";
  empty.textContent = emptyText;
  select.append(empty);
  for (const item of items || []) {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.label || item.name || item.id;
    select.append(option);
  }
  select.value = selectedId || "";
  select.addEventListener("input", () => {
    if (onDirty) {
      onDirty();
    } else {
      settingsDirty = true;
      settingsStatus.textContent = "Unsaved settings changes.";
    }
  });
  return select;
}

function selectForPresetNames(name, presets, selectedName, emptyText = "No change", onDirty = null) {
  const select = document.createElement("select");
  select.name = name;
  const empty = document.createElement("option");
  empty.value = "";
  empty.textContent = emptyText;
  select.append(empty);
  for (const presetName of Object.keys(presets || {})) {
    const option = document.createElement("option");
    option.value = presetName;
    option.textContent = presetName;
    select.append(option);
  }
  select.value = selectedName || "";
  select.addEventListener("input", () => {
    if (onDirty) onDirty();
  });
  return select;
}

function selectForNowPlayingMode(name, selectedMode, onDirty = null) {
  const select = document.createElement("select");
  select.name = name;
  const modes = [
    ["", "No change"],
    ["cdj", "CDJ Beatlink"],
    ["vinyl", `Vinyl: ${manualModeText("vinyl") || "Record Playing"}`],
    ["studio", `Studio: ${manualModeText("studio") || "NO TALKING STUDIO"}`],
    ["videogame", `Videogames: ${manualModeText("videogame") || "Ravenswatch"}`],
  ];
  for (const [value, label] of modes) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    select.append(option);
  }
  select.value = selectedMode || "";
  select.addEventListener("input", () => {
    if (onDirty) {
      onDirty();
    } else {
      lookLinksDirty = true;
      lookLinksStatus.textContent = "Unsaved look link changes.";
    }
  });
  return select;
}

function selectForNowPlayingOpacity(name, selectedValue, onDirty = null) {
  const select = document.createElement("select");
  select.name = name;
  const current = selectedValue === 0 ? "0" : String(selectedValue || "");
  const options = [
    ["", "Hold current"],
    ["0", "Off"],
    ["25", "25%"],
    ["50", "50%"],
    ["75", "75%"],
    ["100", "On"],
  ];
  for (const [value, label] of options) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    select.append(option);
  }
  select.value = current;
  select.addEventListener("input", () => {
    if (onDirty) {
      onDirty();
    } else {
      lookLinksDirty = true;
      lookLinksStatus.textContent = "Unsaved look link changes.";
    }
  });
  return select;
}

function collectLookBuilderRoutingPayload(nameOverride = "") {
  const name = nameOverride || currentLookBuilderName();
  const links = { ...(appSettings.preset_links || {}) };
  const existingLink = links[name] || {};
  links[name] = {
    ...existingLink,
    enabled: true,
    section_preset: lookBuilderForm.elements.builder_section?.value || "",
    now_playing_mode: lookBuilderForm.elements.builder_now_playing?.value || "",
    now_playing_opacity: lookBuilderForm.elements.builder_now_playing_opacity?.value || "",
    visual_id: lookBuilderForm.elements.builder_visual?.value || "",
    generative_visual: existingLink.generative_visual || {},
    main_box_id: lookBuilderForm.elements.builder_main?.value || "",
    pip_box_id: lookBuilderForm.elements.builder_pip?.value || "",
    background_id: lookBuilderForm.elements.builder_background?.value || "",
    visuals_cams_id: lookBuilderForm.elements.builder_visuals_cams?.value || "",
    scene_id: lookBuilderForm.elements.builder_scene?.value || "",
  };
  return { preset_links: links };
}

async function saveLookFromBuilder() {
  const name = currentLookBuilderName();
  if (!name) {
    saveLookStatus.textContent = "Name the look first.";
    return;
  }
  saveLookStatus.textContent = `Saving ${name}...`;
  try {
    const saveResult = await sendCommandForResult({ command: "save_current_look", name }, { quiet: true });
    if (saveResult.config) {
      appSettings = saveResult.config;
      presetData = saveResult.config.preset_groups || presetData;
    }
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectLookBuilderRoutingPayload(name)),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    lookBuilderDirty = false;
    lookLinksDirty = false;
    activeShowSequence = activeShowSequence || "Main Show";
    saveLookStatus.textContent = `Saved ${name}.`;
    showToast(`Saved ${name}`);
    if (result.state) renderShowState(result.state);
    renderSaveLookPicker();
    if (saveCurrentLookSelect) saveCurrentLookSelect.value = name;
    if (lookBuilderName) lookBuilderName.value = name;
    renderLookBuilder();
    renderPresetLinks();
    renderLookLinkForm();
    renderSequencer();
    await loadStatus();
  } catch (error) {
    const message = String(error.message || error);
    saveLookStatus.textContent = message;
    showToast(message, true);
  }
}

const saveLookBuilderRouting = saveLookFromBuilder;

function collectPresetCardRoutingPayload(name, form) {
  const links = { ...(appSettings.preset_links || {}) };
  links[name] = {
    enabled: true,
    section_preset: form.elements.section_preset?.value || "",
    now_playing_mode: form.elements.now_playing_mode?.value || "",
    now_playing_opacity: form.elements.now_playing_opacity?.value || "",
    visual_id: form.elements.visual_id?.value || "",
    main_box_id: form.elements.main_box_id?.value || "",
    pip_box_id: form.elements.pip_box_id?.value || "",
    background_id: form.elements.background_id?.value || "",
    visuals_cams_id: form.elements.visuals_cams_id?.value || "",
    scene_id: form.elements.scene_id?.value || "",
  };
  return { preset_links: links };
}

async function savePresetCardRouting(name, form) {
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectPresetCardRoutingPayload(name, form)),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    lookBuilderDirty = false;
    lookLinksDirty = false;
    form.classList.remove("dirty");
    saveLookStatus.textContent = `Saved routing for ${name}.`;
    showToast(`Saved routing for ${name}`);
    if (result.state) renderShowState(result.state);
    renderLookBuilder();
    renderPresetLinks();
    renderLookLinkForm();
    await loadStatus();
  } catch (error) {
    const message = String(error.message || error);
    saveLookStatus.textContent = message;
    showToast(message, true);
  }
}

async function savePresetCard(originalName, requestedName, lightEditor, form) {
  const name = String(requestedName || "").trim();
  const oldName = String(originalName || "").trim();
  if (!name || !lightEditor || !form) {
    saveLookStatus.textContent = "Name the look first.";
    return false;
  }
  const performancePresets = { ...(presetData?.groups?.performance || {}) };
  if (oldName && oldName !== name) delete performancePresets[oldName];
  performancePresets[name] = collectLookLightValues(lightEditor);
  const routingPayload = collectPresetCardRoutingPayload(name, form);
  if (oldName && oldName !== name && routingPayload.preset_links) delete routingPayload.preset_links[oldName];
  saveLookStatus.textContent = `Saving ${name}...`;
  try {
    const presetResponse = await fetch("/api/presets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ group: "performance", presets: performancePresets }),
    });
    const presetResult = await presetResponse.json();
    if (!presetResponse.ok || !presetResult.ok) throw new Error(presetResult.message || `HTTP ${presetResponse.status}`);
    presetData = presetResult.presets;

    const configResponse = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(routingPayload),
    });
    const configResult = await configResponse.json();
    if (!configResponse.ok || !configResult.ok) throw new Error(configResult.message || `HTTP ${configResponse.status}`);
    appSettings = configResult.config;
    presetData = configResult.config.preset_groups || presetData;
    lookBuilderDirty = false;
    lookLinksDirty = false;
    form.classList.remove("dirty");
    lightEditor.closest(".preset-link-card")?.classList.remove("dirty");
    saveLookStatus.textContent = `Saved ${name} look.`;
    showToast(`Saved ${name} look`);
    if (configResult.state) renderShowState(configResult.state);
    renderPresetButtons(Object.keys(presetData?.groups?.performance || {}));
    renderPresetEditor();
    renderLookBuilder();
    renderPresetLinks();
    renderLookLinkForm();
    await loadStatus();
    return true;
  } catch (error) {
    const message = String(error.message || error);
    saveLookStatus.textContent = message;
    showToast(message, true);
    return false;
  }
}

function makePresetLinkSettingRow(presetName, index) {
  const row = document.createElement("div");
  row.className = "preset-link-setting-row";
  row.dataset.presetName = presetName;
  const link = appSettings.preset_links?.[presetName] || {};
  const cameraConfig = appSettings.camera_controls || {};
  const markDirty = () => {
    lookLinksDirty = true;
    lookLinksStatus.textContent = "Unsaved look link changes.";
  };

  const name = document.createElement("strong");
  name.textContent = presetName;

  const nowPlaying = selectForNowPlayingMode(`preset_link_now_playing_${index}`, link.now_playing_mode);
  const nowPlayingOpacity = selectForNowPlayingOpacity(`preset_link_now_playing_opacity_${index}`, link.now_playing_opacity, markDirty);
  const section = selectForPresetNames(`preset_link_section_${index}`, presetData.groups?.section || {}, link.section_preset, "No change", markDirty);
  const visual = selectForItems(`preset_link_visual_${index}`, appSettings.visual_controls || [], link.visual_id, "None", markDirty);
  const main = selectForItems(`preset_link_main_${index}`, cameraConfig.groups?.main_box || [], link.main_box_id, "None", markDirty);
  const pip = selectForItems(`preset_link_pip_${index}`, cameraConfig.groups?.pip_box || [], link.pip_box_id, "None", markDirty);
  const background = selectForItems(`preset_link_background_${index}`, cameraConfig.groups?.background || [], link.background_id, "None", markDirty);
  const visualsCams = selectForItems(`preset_link_visuals_cams_${index}`, cameraConfig.groups?.visuals_cams || [], link.visuals_cams_id, "None", markDirty);
  const scene = selectForItems(`preset_link_scene_${index}`, cameraConfig.scenes || [], link.scene_id, "None", markDirty);

  row.append(name, nowPlaying, nowPlayingOpacity, section, visual, main, pip, background, visualsCams, scene);
  return row;
}

function collectSettingsPayload() {
  const data = new FormData(settingsForm);
  const payload = {};
  for (const group of settingGroups) {
    for (const [key, _label, kind] of group.fields) {
      const field = settingsForm.elements[key];
      payload[key] = kind === "checkbox" ? Boolean(field.checked) : data.get(key);
    }
  }
  Object.assign(payload, collectNetworkRoutingPayload());
  Object.assign(payload, collectOscTargetsPayload());
  return payload;
}

function collectLightsOscPayload() {
  const data = new FormData(lightsOscForm);
  const payload = {
    link_labels: {},
    osc_addresses: {},
    osc_extra_addresses: {},
    osc_output_notes: {},
  };
  for (const control of liveLightControls()) {
    payload.link_labels[String(control.link)] = data.get(`label_${control.link}`);
    payload.osc_addresses[String(control.link)] = data.get(`address_${control.link}`);
    payload.osc_extra_addresses[String(control.link)] = [];
    payload.osc_output_notes[String(control.link)] = [];
    const outputSlots = lightOscOutputSlots(control);
    for (let index = 0; index < outputSlots; index += 1) {
      payload.osc_output_notes[String(control.link)].push(data.get(`output_note_${control.link}_${index}`) || "");
      if (index > 0) payload.osc_extra_addresses[String(control.link)].push(data.get(`extra_address_${control.link}_${index - 1}`) || "");
    }
  }
  for (const [key] of BPM_TIMING_OSC_FIELDS) {
    payload[key] = data.get(key) || "";
  }
  return payload;
}

function cleanOscAddressValue(value) {
  const text = String(value || "").trim();
  if (!text) return "";
  return text.startsWith("/") ? text : `/${text}`;
}

function findUnsavedBpmTimingOscKeys(payload, config) {
  if (!payload || !config) return [];
  return BPM_TIMING_OSC_FIELDS
    .map(([key, label]) => [key, label, cleanOscAddressValue(payload[key]), cleanOscAddressValue(config[key])])
    .filter(([_key, _label, posted, returned]) => posted && posted !== returned)
    .map(([_key, label]) => label);
}
function collectManualModePayload() {
  return {
    blt_params_url: beatlinkParamsUrl?.value || "",
    music_root: musicRoot?.value || "",
    artwork_output: artworkOutputPath?.value || "",
    fallback_artwork_path: fallbackArtworkPath?.value || "",
    default_fallback_template: defaultFallbackTemplate?.value || "",
    cdj_artwork_width: cdjArtworkWidth?.value || "",
    cdj_artwork_height: cdjArtworkHeight?.value || "",
    fallback_artwork_width: fallbackArtworkWidth?.value || "",
    fallback_artwork_height: fallbackArtworkHeight?.value || "",
    spotify_enabled: Boolean(spotifyEnabled?.checked),
    spotify_track_text: spotifyTrackText?.value || "Spotify Now Playing",
    spotify_artwork_path: spotifyArtworkPath?.value || "",
    spotify_artwork_width: spotifyArtworkWidth?.value || "",
    spotify_artwork_height: spotifyArtworkHeight?.value || "",
    spotify_client_id: spotifyClientId?.value || "",
    spotify_redirect_uri: spotifyRedirectUri?.value || "http://127.0.0.1:8080/spotify/callback",
    spotify_market: spotifyMarket?.value || "US",
    spotify_track_template: spotifyTrackTemplate?.value || "{artist} - {title}",
    vinyl_track_text: vinylTrackText?.value || "Record Playing",
    vinyl_logo_path: vinylArtworkPath?.value || "",
    vinyl_artwork_width: vinylArtworkWidth?.value || "",
    vinyl_artwork_height: vinylArtworkHeight?.value || "",
    studio_track_text: studioTrackText?.value || "NO TALKING STUDIO",
    studio_artwork_path: studioArtworkPath?.value || "",
    studio_artwork_width: studioArtworkWidth?.value || "",
    studio_artwork_height: studioArtworkHeight?.value || "",
    videogame_track_text: videogameTrackText?.value || "Ravenswatch",
    videogame_artwork_path: videogameArtworkPath?.value || "",
    videogame_artwork_width: videogameArtworkWidth?.value || "",
    videogame_artwork_height: videogameArtworkHeight?.value || "",
  };
}

async function saveManualModePayload() {
  if (!manualModeForm) return;
  try {
    if (manualModeStatus) manualModeStatus.textContent = "Saving Now Playing source settings...";
    if (beatlinkSourceStatus) beatlinkSourceStatus.textContent = "Saving BeatLink settings...";
    if (spotifyAuthStatus) spotifyAuthStatus.textContent = "Saving Spotify settings...";
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectManualModePayload()),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    manualModeDirty = false;
    if (manualModeStatus) manualModeStatus.textContent = result.message || "Now Playing source settings saved.";
    if (beatlinkSourceStatus) beatlinkSourceStatus.textContent = "BeatLink settings saved.";
    if (spotifyAuthStatus) renderSpotifyStatus(result);
    if (result.state) renderShowState(result.state);
    renderManualModeForm();
    renderSettingsForm();
      renderObsSettingsForm();
    await loadStatus({ full: true, force: true });
  } catch (error) {
    if (manualModeStatus) manualModeStatus.textContent = String(error.message || error);
  }
}

function applySpotifyApiResult(result = {}) {
  if (result.config) {
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    manualModeDirty = false;
    renderManualModeForm();
    renderSettingsForm();
    renderObsSettingsForm();
  }
  if (result.state) renderShowState(result.state);
  renderSpotifyStatus(result);
  if (spotifyAuthStatus && result.message) spotifyAuthStatus.textContent = result.message;
}

async function fetchSpotifyEndpoint(path, payload = null) {
  const options = payload === null
    ? { method: "GET" }
    : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) };
  const response = await fetch(path, options);
  let result = {};
  try {
    result = await response.json();
  } catch (_error) {
    result = { ok: false, message: `HTTP ${response.status}` };
  }
  if (!response.ok || result.ok === false) throw new Error(result.message || `HTTP ${response.status}`);
  return result;
}

async function runSpotifyAction(path, payload = null, workingText = "Updating Spotify...") {
  try {
    if (spotifyAuthStatus) spotifyAuthStatus.textContent = workingText;
    const result = await fetchSpotifyEndpoint(path, payload);
    if (result.authorization_url) {
      window.location.href = result.authorization_url;
      return;
    }
    applySpotifyApiResult(result);
    await loadStatus({ full: true, force: true });
  } catch (error) {
    const message = String(error.message || error);
    if (spotifyAuthStatus) spotifyAuthStatus.textContent = message;
    showToast(message, true);
  }
}
async function rebuildMusicIndexPayload() {
  if (!rebuildMusicIndex) return;
  const previousText = rebuildMusicIndex.textContent;
  try {
    rebuildMusicIndex.disabled = true;
    rebuildMusicIndex.textContent = "Saving...";
    if (manualModeStatus) manualModeStatus.textContent = "Saving BeatLink artwork settings...";
    const saveResponse = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectManualModePayload()),
    });
    const saveResult = await saveResponse.json();
    if (!saveResponse.ok || !saveResult.ok) throw new Error(saveResult.message || `HTTP ${saveResponse.status}`);
    appSettings = saveResult.config;
    presetData = saveResult.config.preset_groups || presetData;
    manualModeDirty = false;

    rebuildMusicIndex.textContent = "Indexing...";
    if (manualModeStatus) manualModeStatus.textContent = "Scanning Music Root for MP3 files...";
    const result = await sendCommandForResult({ command: "rebuild_music_index" }, { quiet: true });
    if (manualModeStatus) manualModeStatus.textContent = result.message || "Music index rebuild started.";
    if (result.state) renderShowState(result.state);

    for (let attempt = 0; attempt < 45; attempt += 1) {
      const status = await loadStatus({ full: true, force: true });
      const rebuild = status?.artwork?.index_rebuild;
      if (!rebuild?.running) {
        if (manualModeStatus) manualModeStatus.textContent = rebuild?.message || status?.artwork?.status || "Music index rebuilt.";
        break;
      }
      if (manualModeStatus) manualModeStatus.textContent = rebuild.message || "Rebuilding music index...";
      await new Promise((resolve) => window.setTimeout(resolve, 1000));
    }
  } catch (error) {
    if (manualModeStatus) manualModeStatus.textContent = String(error.message || error);
  } finally {
    rebuildMusicIndex.disabled = false;
    rebuildMusicIndex.textContent = previousText;
  }
}
function collectNowPlayingOscPayload() {
  const data = new FormData(nowPlayingOscForm);
  const payload = { blt_osc_outputs: [], now_playing_opacity_address: data.get("now_playing_opacity_address") || "" };
  payload.blt_osc_outputs = [];
  for (const output of appSettings.blt_osc_outputs || []) {
    payload.blt_osc_outputs.push({
      key: output.key,
      label: data.get(`blt_label_${output.key}`),
      field: data.get(`blt_field_${output.key}`),
      address: data.get(`blt_address_${output.key}`),
      enabled: Boolean(nowPlayingOscForm.elements[`blt_enabled_${output.key}`]?.checked),
    });
  }
  return payload;
}

function collectVisualsOscPayload() {
  const data = new FormData(visualsOscForm);
  const payload = { visual_controls: { items: {} }, visual_slider_controls: { items: {} } };
  payload.visual_controls = { items: {} };
  for (const item of visualControlsWithLayerOff()) {
    const label = data.get(`visual_label_${item.id}`) || item.label || item.name || item.id;
    payload.visual_controls.items[item.id] = {
      id: item.id,
      name: label,
      label,
      kind: item.kind || (isVisualOffItem(item) ? "off" : "clip"),
      layer: visualLayerNumber(item),
      clip: visualClipNumber(item),
      address: data.get(`visual_address_${item.id}`),
    };
  }
  payload.visual_slider_controls = { items: {} };
  for (const item of appSettings.visual_slider_controls || []) {
    const label = data.get(`visual_slider_label_${item.id}`) || item.label || item.name || item.id;
    payload.visual_slider_controls.items[item.id] = {
      id: item.id,
      name: label,
      label,
      address: data.get(`visual_slider_address_${item.id}`),
    };
  }
  return payload;
}

function collectCamerasOscPayload() {
  const data = new FormData(camerasOscForm);
  const payload = {
    camera_controls: { items: {} },
    camera_opacity_addresses: { ...(appSettings.camera_opacity_addresses || {}) },
    camera_opacity_labels: { ...(appSettings.camera_opacity_labels || {}) },
  };
  payload.camera_controls = { items: {} };
  for (const groupKey of Object.keys(cameraContainers)) {
    payload.camera_opacity_addresses[groupKey] = data.get(`camera_opacity_${groupKey}`) || "";
    payload.camera_opacity_labels[groupKey] = data.get(`camera_opacity_label_${groupKey}`) || cameraOpacityLabels[groupKey] || "Cam Mix";
  }

  const cameraConfig = appSettings.camera_controls || {};
  const cameraItems = [
    ...Object.values(cameraConfig.groups || {}).flat(),
    ...(cameraConfig.scenes || []),
  ];
  for (const item of cameraItems) {
    const label = data.get(`camera_label_${item.id}`) || item.label || item.name || item.id;
    payload.camera_controls.items[item.id] = {
      name: label,
      label,
      address: data.get(`camera_address_${item.id}`),
    };
  }
  return payload;
}

function collectLookLinksPayload() {
  const data = new FormData(lookLinkForm);
  const presetLinksPayload = {};
  const presetRows = lookLinkForm.querySelectorAll(".preset-link-setting-row[data-preset-name]");
  presetRows.forEach((row, index) => {
    const presetName = row.dataset.presetName;
    presetLinksPayload[presetName] = {
      enabled: true,
      now_playing_mode: data.get(`preset_link_now_playing_${index}`) || "",
      now_playing_opacity: data.get(`preset_link_now_playing_opacity_${index}`) || "",
      section_preset: data.get(`preset_link_section_${index}`) || "",
      visual_id: data.get(`preset_link_visual_${index}`) || "",
      main_box_id: data.get(`preset_link_main_${index}`) || "",
      pip_box_id: data.get(`preset_link_pip_${index}`) || "",
      background_id: data.get(`preset_link_background_${index}`) || "",
      visuals_cams_id: data.get(`preset_link_visuals_cams_${index}`) || "",
      scene_id: data.get(`preset_link_scene_${index}`) || "",
    };
  });
  return presetLinksPayload;
}

async function saveSettingsPayload() {
  try {
    const payload = collectSettingsPayload();
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    if (payload.osc_targets?.length && !Array.isArray(result.config?.osc_targets)) {
      throw new Error("Restart the app server once to enable multi-target OSC saving.");
    }
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    settingsDirty = false;
    settingsStatus.textContent = result.message || "Settings saved.";
    if (result.state) renderShowState(result.state);
    renderSettingsForm();
    renderObsSettingsForm();
    renderLocalOscForms();
    renderPresetEditor();
    await loadStatus();
  } catch (error) {
    settingsStatus.textContent = String(error.message || error);
  }
}

function collectObsSettingsPayload() {
  const data = new FormData(obsSettingsForm);
  const payload = {};
  for (const [key, _label, kind] of obsSettingFields) {
    const field = obsSettingsForm.elements[key];
    if (!field) continue;
    payload[key] = kind === "checkbox" ? Boolean(field.checked) : data.get(key);
  }
  return payload;
}

async function saveObsSettingsPayload() {
  if (!obsSettingsForm) return;
  try {
    if (obsSettingsStatus) obsSettingsStatus.textContent = "Saving OBS settings...";
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectObsSettingsPayload()),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    obsSettingsDirty = false;
    if (obsSettingsStatus) obsSettingsStatus.textContent = result.message || "OBS settings saved.";
    if (result.state) renderShowState(result.state);
    renderObsSettingsForm();
    await loadStatus({ full: true, force: true });
  } catch (error) {
    if (obsSettingsStatus) obsSettingsStatus.textContent = String(error.message || error);
  }
}
async function saveLocalOscPayload(collectPayload, setDirty, statusEl, successText) {
  try {
    const payload = collectPayload();
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    const unsavedBpmTiming = findUnsavedBpmTimingOscKeys(payload, result.config);
    if (unsavedBpmTiming.length) {
      throw new Error(`Restart the app server once to enable BPM Timing OSC saving. Not saved yet: ${unsavedBpmTiming.join(", ")}.`);
    }
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    setDirty(false);
    statusEl.textContent = successText;
    if (result.state) renderShowState(result.state);
    renderLocalOscForms();
    renderSettingsForm();
      renderObsSettingsForm();
    refreshCueLabelSurfaces();
    await loadStatus();
  } catch (error) {
    statusEl.textContent = String(error.message || error);
  }
}

function saveLightsOscPayload() {
  return saveLocalOscPayload(collectLightsOscPayload, (value) => { lightsOscDirty = value; }, lightsOscStatus, "Lights OSC settings saved.");
}

function saveVisualsOscPayload() {
  return saveLocalOscPayload(collectVisualsOscPayload, (value) => { visualsOscDirty = value; }, visualsOscStatus, "Visuals OSC settings saved.");
}

function saveCamerasOscPayload() {
  return saveLocalOscPayload(collectCamerasOscPayload, (value) => { camerasOscDirty = value; }, camerasOscStatus, "Camera OSC settings saved.");
}

function saveNowPlayingOscPayload() {
  return saveLocalOscPayload(collectNowPlayingOscPayload, (value) => { nowPlayingOscDirty = value; }, nowPlayingOscStatus, "Now Playing OSC settings saved.");
}

function cloneBackupValue(value) {
  if (value === undefined) return undefined;
  return JSON.parse(JSON.stringify(value));
}

function setOscBackupStatus(text) {
  if (oscBackupStatus) oscBackupStatus.textContent = text;
}

function collectOscBackupSettings(source = appSettings) {
  const settings = {};
  if (!source || typeof source !== "object") return settings;
  for (const key of OSC_BACKUP_KEYS) {
    if (Object.prototype.hasOwnProperty.call(source, key)) {
      settings[key] = cloneBackupValue(source[key]);
    }
  }
  return settings;
}

function buildOscBackupPayload() {
  const settings = collectOscBackupSettings();
  if (!Object.keys(settings).length) throw new Error("OSC settings are not loaded yet. Refresh once, then export again.");
  return {
    app: "NT Performance Hub",
    type: "osc-settings-backup",
    version: 1,
    exported_at: new Date().toISOString(),
    settings,
  };
}

function defaultOscBackupFileName() {
  const stamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  return `nt-performance-hub-osc-settings-${stamp}.json`;
}

function sanitizeOscBackupFileName(value) {
  const base = String(value || "").trim().split(/[\\/]/).pop().replace(/[^A-Za-z0-9._ -]+/g, "-").replace(/^[ .]+|[ .]+$/g, "");
  const name = base || defaultOscBackupFileName();
  return name.toLowerCase().endsWith(".json") ? name : `${name}.json`;
}

function oscBackupFileName() {
  if (!oscBackupFileNameInput) return defaultOscBackupFileName();
  if (!oscBackupFileNameInput.value.trim()) oscBackupFileNameInput.value = defaultOscBackupFileName();
  return sanitizeOscBackupFileName(oscBackupFileNameInput.value);
}

function renderOscBackupFiles(files = []) {
  if (!oscBackupFileList) return;
  oscBackupFileList.replaceChildren();
  files.forEach((file) => {
    const option = document.createElement("option");
    option.value = file.filename || "";
    option.label = file.relative_path || file.filename || "";
    oscBackupFileList.append(option);
  });
  if (oscImportFileNameInput && !oscImportFileNameInput.value && files[0]?.filename) {
    oscImportFileNameInput.placeholder = files[0].filename;
  }
}

async function loadOscBackupFiles() {
  try {
    const response = await fetch("/api/osc-backups");
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    renderOscBackupFiles(result.files || []);
    return result.files || [];
  } catch (_error) {
    return [];
  }
}

function downloadOscSettingsPayload() {
  try {
    const payload = buildOscBackupPayload();
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = oscBackupFileName();
    document.body.append(link);
    link.click();
    const objectUrl = link.href;
    link.remove();
    URL.revokeObjectURL(objectUrl);
    setOscBackupStatus(`Downloaded ${Object.keys(payload.settings).length} OSC setting groups as ${link.download}.`);
  } catch (error) {
    setOscBackupStatus(String(error.message || error));
  }
}

async function exportOscSettingsPayload() {
  try {
    setOscBackupStatus("Saving OSC backup into project...");
    const response = await fetch("/api/osc-backup/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename: oscBackupFileName() }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    if (oscBackupFileNameInput) oscBackupFileNameInput.value = result.filename || oscBackupFileNameInput.value;
    if (oscImportFileNameInput) oscImportFileNameInput.value = result.filename || "";
    renderOscBackupFiles(result.files || []);
    setOscBackupStatus(`${result.message} (${result.settings_count || 0} setting groups).`);
  } catch (error) {
    setOscBackupStatus(String(error.message || error));
  }
}

function applyOscImportResult(result, sourceName) {
  appSettings = result.config;
  presetData = result.config.preset_groups || presetData;
  lightsOscDirty = false;
  visualsOscDirty = false;
  camerasOscDirty = false;
  nowPlayingOscDirty = false;
  lookLinksDirty = false;
  showSequenceDirty = false;
  settingsDirty = false;
  obsSettingsDirty = false;
  if (result.state) renderShowState(result.state);
  renderSettingsForm();
  renderObsSettingsForm();
  renderLocalOscForms();
  refreshCueLabelSurfaces();
  renderOscBackupFiles(result.files || []);
  setOscBackupStatus(result.message || `Imported OSC setting groups from ${sourceName}.`);
}

async function importOscSettingsBackup(payload, sourceName) {
  const response = await fetch("/api/osc-backup/import", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const result = await response.json();
  if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
  applyOscImportResult(result, sourceName);
  await loadStatus({ full: true, force: true });
}

async function importOscSettingsPayload(file) {
  if (!file) return;
  try {
    setOscBackupStatus(`Reading ${file.name}...`);
    const raw = JSON.parse(await file.text());
    setOscBackupStatus(`Importing OSC settings from ${file.name}...`);
    await importOscSettingsBackup({ backup: raw, source_name: file.name }, file.name);
  } catch (error) {
    setOscBackupStatus(String(error.message || error));
  } finally {
    if (importOscSettings) importOscSettings.value = "";
  }
}

async function importProjectOscSettingsPayload() {
  const rawName = String(oscImportFileNameInput?.value || oscBackupFileNameInput?.value || "").trim();
  if (!rawName) {
    setOscBackupStatus("Choose or type a project OSC backup filename first.");
    return;
  }
  const filename = sanitizeOscBackupFileName(rawName);
  try {
    setOscBackupStatus(`Importing ${filename} from project backups...`);
    await importOscSettingsBackup({ filename }, filename);
  } catch (error) {
    setOscBackupStatus(String(error.message || error));
  }
}
async function saveLookLinksPayload() {
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ preset_links: collectLookLinksPayload() }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    appSettings = result.config;
    presetData = result.config.preset_groups || presetData;
    lookLinksDirty = false;
    lookLinksStatus.textContent = "Look links saved.";
    if (result.state) renderShowState(result.state);
    renderPresetLinks();
    renderLookLinkForm();
    await loadStatus();
  } catch (error) {
    lookLinksStatus.textContent = String(error.message || error);
  }
}

function renderPresetGroupTabs() {
  if (!presetData) return;
  presetGroupTabs.replaceChildren();
  for (const group of Object.keys(presetData.groups || {})) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "subtab-button";
    button.classList.toggle("active", activePresetGroup === group);
    button.textContent = presetData.labels?.[group] || group;
    button.addEventListener("click", () => {
      activePresetGroup = group;
      presetDirty = false;
      renderPresetEditor();
    });
    presetGroupTabs.append(button);
  }
}

function makePresetInput(name, key, value, kind) {
  let input = document.createElement("select");
  if (kind === "color") {
    for (const colorName of presetData.colors.names || []) {
      const option = document.createElement("option");
      option.value = colorName;
      option.textContent = colorName;
      input.append(option);
    }
  } else {
    for (const percent of presetData.percent_choices || []) {
      const option = document.createElement("option");
      option.value = String(percent);
      option.textContent = `${percent}`;
      input.append(option);
    }
  }
  input.name = `${name}::${key}`;
  input.dataset.presetName = name;
  input.dataset.presetKey = key;
  input.value = value ?? (kind === "color" ? "indigo" : "0");
  input.addEventListener("change", () => {
    presetDirty = true;
    presetStatus.textContent = "Unsaved preset changes.";
    renderPresetSwatch(input);
  });
  return input;
}

function renderPresetSwatch(input) {
  const chip = input.parentElement.querySelector(".preset-chip");
  if (chip) chip.style.background = colorHex(input.value);
}

function renderPresetEditor() {
  if (!presetData) return;
  renderPresetGroupTabs();
  if (presetDirty) return;
  presetEditor.replaceChildren();

  const groupPresets = presetData.groups?.[activePresetGroup] || {};
  const table = document.createElement("div");
  table.className = "preset-table";
  const header = document.createElement("div");
  header.className = "preset-row preset-header";
  header.append(cell("Preset"));
  for (const column of presetData.columns || []) header.append(cell(column.label));
  header.append(cell("Actions"));
  table.append(header);

  for (const [name, values] of Object.entries(groupPresets)) {
    const row = document.createElement("div");
    row.className = "preset-row";
    const nameInput = document.createElement("input");
    nameInput.value = name;
    nameInput.dataset.originalName = name;
    nameInput.className = "preset-name-input";
    nameInput.addEventListener("input", () => {
      presetDirty = true;
      presetStatus.textContent = "Unsaved preset changes.";
    });
    row.append(wrap(nameInput));

    for (const column of presetData.columns || []) {
      const wrapCell = document.createElement("div");
      wrapCell.className = "preset-cell";
      if (column.kind === "color") {
        const chip = document.createElement("span");
        chip.className = "preset-chip";
        chip.style.background = colorHex(values[column.key]);
        wrapCell.append(chip);
      }
      const input = makePresetInput(name, column.key, values[column.key], column.kind);
      wrapCell.append(input);
      row.append(wrapCell);
    }

    const actions = document.createElement("div");
    actions.className = "preset-actions";
    const apply = document.createElement("button");
    apply.type = "button";
    apply.textContent = "Apply";
    apply.addEventListener("click", () => sendCommand({ command: "preset", group: activePresetGroup, name }));
    const save = document.createElement("button");
    save.type = "button";
    save.textContent = "Save";
    save.addEventListener("click", savePresetGroup);
    const copy = document.createElement("button");
    copy.type = "button";
    copy.textContent = "Copy";
    copy.addEventListener("click", () => copyPresetComment(name, values));
    const reset = document.createElement("button");
    reset.type = "button";
    reset.textContent = "Reset";
    reset.addEventListener("click", () => {
      presetDirty = false;
      renderPresetEditor();
      presetStatus.textContent = `Reset ${name} editor row.`;
    });
    actions.append(apply, save, copy, reset);
    row.append(actions);
    table.append(row);
  }
  presetEditor.append(table);
}

async function copyPresetComment(name, values) {
  const parts = [];
  for (const column of presetData.columns || []) {
    if (values[column.key] !== undefined) parts.push(`${column.key}=${values[column.key]}`);
  }
  try {
    await navigator.clipboard.writeText(parts.join(";"));
    presetStatus.textContent = `Copied ${name} preset comment.`;
  } catch (_error) {
    presetStatus.textContent = "Clipboard was blocked by the browser.";
  }
}

function cell(text) {
  const div = document.createElement("div");
  div.className = "preset-cell";
  div.textContent = text;
  return div;
}

function wrap(node) {
  const div = document.createElement("div");
  div.className = "preset-cell";
  div.append(node);
  return div;
}

function collectPresetGroup() {
  const rows = presetEditor.querySelectorAll(".preset-row:not(.preset-header)");
  const presets = {};
  for (const row of rows) {
    const nameInput = row.querySelector(".preset-name-input");
    const name = nameInput.value.trim();
    if (!name) continue;
    presets[name] = {};
    row.querySelectorAll("select[data-preset-key]").forEach((input) => {
      const key = input.dataset.presetKey;
      presets[name][key] = input.value;
    });
  }
  return presets;
}

async function savePresetGroup() {
  try {
    const response = await fetch("/api/presets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ group: activePresetGroup, presets: collectPresetGroup() }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    presetData = result.presets;
    presetDirty = false;
    presetStatus.textContent = result.message || "Presets saved.";
    renderPresetEditor();
    renderLookLinkForm();
    renderPresetLinks();
    await loadStatus();
  } catch (error) {
    presetStatus.textContent = String(error.message || error);
  }
}

async function refreshPalette(apply = false, options = {}) {
  if (!apply && paletteRefreshInFlight) return;
  const statusEl = options.statusEl || paletteStatus;
  const previewEl = options.previewEl === undefined ? palettePreview : options.previewEl;
  if (!apply) paletteRefreshInFlight = true;
  try {
    const url = apply ? "/api/command" : "/api/artwork/palette";
    const requestOptions = apply
      ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ command: "artwork_palette" }) }
      : {};
    const response = await fetch(url, requestOptions);
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    const palette = result.palette;
    if (statusEl) statusEl.textContent = apply ? (result.message || "Applied artwork palette.") : (palette.message || result.message || "Palette updated.");
    if (previewEl) previewEl.replaceChildren();
    for (const item of palette.colors || []) {
      const swatch = document.createElement("div");
      swatch.className = "palette-swatch";
      const chip = document.createElement("span");
      chip.style.background = item.hex;
      const name = document.createElement("strong");
      name.textContent = item.name;
      const hex = document.createElement("small");
      const detail = item.coverage_ratio
        ? `${item.hex} - ${Math.round(Number(item.coverage_ratio) * 1000) / 10}% pixels`
        : item.source === "generated"
          ? `${item.hex} - generated match`
          : item.hex;
      hex.textContent = detail;
      const actions = document.createElement("div");
      actions.className = "palette-actions";
      [
        ["Color 1", "Color 1", "color1"],
        ["Color 2", "Color 2", "color2"],
        ["Color 3", "Color 3", "color3"],
        ["1 + 2", "Color 1 + Color 2", "color1_color2"],
        ["2 + 3", "Color 2 + Color 3", "color2_color3"],
        ["1 + 3", "Color 1 + Color 3", "color1_color3"],
        ["All", "Color 1 + Color 2 + Color 3", "all"],
      ].forEach(([label, title, target]) => {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = label;
        button.ariaLabel = `Send ${item.name} to ${title}`;
        button.title = `Send ${item.name} to ${title}`;
        button.addEventListener("click", () => applyPaletteColor(item.name, target));
        actions.append(button);
      });
      swatch.append(chip, name, hex, actions);
      if (previewEl) previewEl.append(swatch);
    }
    if (result.state) renderShowState(result.state);
    if (apply) await loadStatus();
  } catch (error) {
    if (statusEl) statusEl.textContent = String(error.message || error);
  } finally {
    if (!apply) paletteRefreshInFlight = false;
  }
}
function applyPaletteColor(color, target) {
  return sendCommand({ command: "set_palette_color", color, target });
}

async function sendCommand(payload, options = {}) {
  try {
    if (!options.quiet && options.manualOverride !== false) markManualOverride();
    const result = await sendCommandForResult(payload, { ...options, compact: true });
    if (!options.quiet) showToast(result.message || "Command sent");
    if (result.config) {
      appSettings = result.config;
      presetData = result.config.preset_groups || presetData;
      settingsDirty = false;
      quickSettingsDirty = false;
      lookLinksDirty = false;
      renderQuickSettingsForm();
      renderManualModeForm();
      renderSettingsForm();
      renderObsSettingsForm();
      renderLookLinkForm();
      renderLocalOscForms();
      renderSequencer();
      renderMathSceneGallery();
    }
    if (result.state) renderShowState(result.state);
    await loadStatus();
    return result;
  } catch (error) {
    optimisticNowPlayingMode = "";
    renderSelectedButtons(latestShow || {});
    showToast(String(error.message || error), true);
    return null;
  }
}

async function sendCommandForResult(payload, _options = {}) {
  const url = _options.compact ? "/api/command?compact=1" : "/api/command";
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const result = await response.json();
  if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
  return result;
}

async function saveCurrentLookByName(name) {
  if (!name) {
    saveLookStatus.textContent = "Choose a look first.";
    return;
  }
  try {
    const response = await fetch("/api/command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: "save_current_look", name }),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || `HTTP ${response.status}`);
    showToast(result.message || `Saved current state to ${name}`);
    saveLookStatus.textContent = result.message || `Saved current state to ${name}`;
    if (result.config) {
      appSettings = result.config;
      presetData = result.config.preset_groups || presetData;
      lookLinksDirty = false;
      lookBuilderDirty = false;
      renderLookLinkForm();
      renderLocalOscForms();
      renderSettingsForm();
      renderObsSettingsForm();
      renderSequencer();
    }
    if (result.presets) presetData = result.presets;
    if (result.state) renderShowState(result.state);
    renderPresetButtons(Object.keys(presetData?.groups?.performance || {}));
    renderLookBuilder();
    renderPresetEditor();
    renderPresetLinks();
    renderSequencer();
    await loadStatus();
  } catch (error) {
    const message = String(error.message || error);
    saveLookStatus.textContent = message;
    showToast(message, true);
  }
}

function scheduleStatusRefresh(show) {
  if (statusTimer) clearTimeout(statusTimer);
  if (document.hidden) return;
  const running = Boolean(show?.bpm_running);
  const interval = Number(show?.bpm_interval_ms || 500);
  const visibleDelay = running ? Math.max(650, Math.min(1200, Math.round(interval * 8))) : 2800;
  const settingsDelay = ["settingsSection", "nowPlayingSection", "obsSection", "macrosSection"].includes(activeSectionId) ? Math.max(visibleDelay, 5000) : visibleDelay;
  statusTimer = setTimeout(loadStatus, settingsDelay);
}

function statusPollOptions(options = {}) {
  const full = Boolean(options.full) || !appSettings || !presetData || statusPollCount % FULL_STATUS_POLL_EVERY === 0 || ["settingsSection", "nowPlayingSection", "obsSection", "macrosSection"].includes(activeSectionId);
  const blt = Boolean(options.full) || activeSectionId === "nowPlayingSection" || statusPollCount % BLT_STATUS_POLL_EVERY === 0;
  return { full, blt };
}

function formatBltAddressStatus(status) {
  const sources = status.blt?.sources || status.settings?.blt_sources || [];
  if (!sources.length) return status.config?.blt_params_url || "-";
  const live = sources.filter((source) => source.ok);
  if (live.length) return `Live: ${live.map((source) => source.label || source.url).join(" + ")}`;
  return `Polling: ${sources.map((source) => source.label || source.url).join(" + ")}`;
}

async function loadStatus(options = {}) {
  if (statusRequestInFlight && !options.force) return;
  statusRequestInFlight = true;
  const { full: requestFullStatus, blt: pollBlt } = statusPollOptions(options);
  try {
    const params = new URLSearchParams({ ts: String(Date.now()), settings: requestFullStatus ? "1" : "0", blt: pollBlt ? "1" : "0" });
    const response = await fetch(`/api/status?${params.toString()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const status = await response.json();
    const receivedSettings = Boolean(status.settings);
    const revision = status.config?.revision || "";
    if (!receivedSettings && latestConfigRevision && revision && revision !== latestConfigRevision) {
      statusRequestInFlight = false;
      await loadStatus({ full: true, force: true });
      return;
    }

    if (receivedSettings) {
      appSettings = status.settings;
      presetData = status.settings?.preset_groups || presetData;
      renderLookLightsModeControls();
      latestConfigRevision = revision || latestConfigRevision;
    } else if (revision && !latestConfigRevision) {
      latestConfigRevision = revision;
    }

    setConnection("online", "Online");
    renderSystemConfidence(status.confidence || []);
    if (connectionProfile) connectionProfile.textContent = status.config.profile || appSettings?.connection_profile_name || "-";
    serverAddress.textContent = `${location.hostname || "localhost"}:${status.server.port}`;
    const oscTargets = status.config.osc_targets || appSettings?.osc_targets || [];
    const enabledTargets = oscTargets.filter((target) => target.enabled !== false && target.host);
    resolumeAddress.textContent = enabledTargets.length > 1 ? `${enabledTargets.length} OSC targets` : `${status.config.resolume_ip || "-"}:${status.config.resolume_port || "-"}`;
    bltAddress.textContent = formatBltAddressStatus(status);
    configState.textContent = status.config.exists ? "Loaded" : "Defaults";
    artworkPath.textContent = status.artwork.path || "Artwork path unavailable";
    trackArtworkPath.textContent = status.artwork.path || "Artwork path unavailable";
    renderRemoteUrls(status.server.remote_urls || []);
    renderShowState(status.show, { full: receivedSettings });
    if (receivedSettings) {
      renderPresetButtons(status.presets || []);
      renderQuickSettingsForm();
      renderArtworkOptions();
      renderManualModeForm();
      renderSettingsForm();
      renderObsSettingsForm();
      renderLocalOscForms();
      renderSaveLookPicker();
      renderPresetEditor();
      renderSequencer();
      renderMathSceneGallery();
    }
    renderTrackMetadata(status);

    if (perfTrackDisplay) {
      const track = status.blt?.context || {};
      const mode = status.show?.manual_mode || "cdj";
      const spotify = currentSpotifyStatus(status) || {};
      const spotifyCurrent = spotify.current || null;
      const hasSpotifyTrack = Boolean(mode === "spotify" && spotifyCurrent && spotifyCurrent.item_type !== "none" && (spotifyCurrent.title || spotifyCurrent.track_id || spotifyCurrent.track_uri));
      perfTrackDisplay.textContent = mode === "cdj"
        ? track.full_track || track.title || status.show?.last_event || status.artwork.status || "Current display"
        : hasSpotifyTrack
          ? spotifyCurrentDisplay(spotifyCurrent).title
          : mode === "spotify"
            ? ""
            : manualModeText(mode) || status.show?.last_event || status.artwork.status || "Current display";
    }

    const artworkToken = status.artwork.exists ? `${status.artwork.url}|${status.artwork.updated || ""}` : "";
    if (status.artwork.exists) {
      previewArtworkImage.hidden = false;
      artworkImage.hidden = false;
      trackArtworkImage.hidden = false;
      if (artworkToken !== latestArtworkToken) {
        const artworkSrc = `${status.artwork.url}?v=${encodeURIComponent(status.artwork.updated || Date.now())}`;
        previewArtworkImage.src = artworkSrc;
        artworkImage.src = artworkSrc;
        trackArtworkImage.src = artworkSrc;
        latestArtworkToken = artworkToken;
      }
      previewArtworkEmpty.classList.add("hidden");
      artworkEmpty.classList.add("hidden");
      trackArtworkEmpty.classList.add("hidden");
    } else {
      latestArtworkToken = "";
      previewArtworkImage.hidden = true;
      previewArtworkImage.removeAttribute("src");
      previewArtworkEmpty.classList.remove("hidden");
      artworkImage.hidden = true;
      artworkImage.removeAttribute("src");
      artworkEmpty.classList.remove("hidden");
      trackArtworkImage.hidden = true;
      trackArtworkImage.removeAttribute("src");
      trackArtworkEmpty.classList.remove("hidden");
    }
    if (appSettings?.use_artwork_palette && status.artwork.exists && status.artwork.updated && status.artwork.updated !== latestPaletteArtworkUpdated) {
      latestPaletteArtworkUpdated = status.artwork.updated;
      refreshPalette(true);
    }
    statusPollCount += 1;
    scheduleStatusRefresh(status.show);
    return status;
  } catch (error) {
    setConnection("offline", "Offline");
    serverAddress.textContent = "-";
    resolumeAddress.textContent = "-";
    bltAddress.textContent = "-";
    configState.textContent = String(error.message || error);
    renderRemoteUrls([]);
    scheduleStatusRefresh(null);
  } finally {
    statusRequestInFlight = false;
  }
}

function scrollLiveSurfaceToTop() {
  const surface = document.querySelector(".app");
  if (!surface) return;
  const top = Math.max(0, surface.getBoundingClientRect().top + window.scrollY);
  window.scrollTo({ top, behavior: "auto" });
}

function scheduleLiveSurfaceScroll() {
  requestAnimationFrame(scrollLiveSurfaceToTop);
  window.setTimeout(scrollLiveSurfaceToTop, 80);
}

function activateSection(sectionId, { scroll = true } = {}) {
  const section = document.querySelector(`#${sectionId}`);
  if (!section) return;
  activeSectionId = sectionId;
  document.querySelectorAll(".tab-button").forEach((tab) => tab.classList.toggle("active", tab.dataset.section === sectionId));
  document.querySelectorAll(".section-view").forEach((view) => view.classList.toggle("active", view === section));
  if (window.location.hash !== `#${sectionId}`) history.replaceState(null, "", `#${sectionId}`);
  if (scroll) scheduleLiveSurfaceScroll();
  loadStatus({ force: true, full: ["settingsSection", "nowPlayingSection", "obsSection", "macrosSection"].includes(sectionId) });
}

document.querySelectorAll(".tab-button").forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.section) activateSection(button.dataset.section);
  });
});

document.querySelectorAll("[data-section-link]").forEach((link) => {
  link.addEventListener("click", (event) => {
    const sectionId = link.dataset.sectionLink;
    if (!document.querySelector(`#${sectionId}`)) return;
    event.preventDefault();
    activateSection(sectionId);
  });
});

liveDeckPanelToggles.forEach((input) => {
  input.addEventListener("change", () => {
    liveDeckVisiblePanels[input.dataset.livePanelToggle] = input.checked;
    saveLiveDeckVisiblePanels();
    applyLiveDeckVisibility();
  });
});

liveDeckHideButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setLiveDeckVisibility({ ...liveDeckVisiblePanels, [button.dataset.livePanelHide]: false });
  });
});

if (liveDeckLookName) {
  liveDeckLookName.addEventListener("input", () => {
    liveDeckLookNameDirty = true;
    setLiveDeckSaveStatus("Ready to save this label.");
  });
}
if (saveLiveDeckLook) saveLiveDeckLook.addEventListener("click", saveCurrentShowStateFromLiveDeck);

refreshButton.addEventListener("click", () => loadStatus({ full: true, force: true }));
if (favoriteBankSelect) favoriteBankSelect.addEventListener("change", () => persistPerformanceBanks(clonePerformanceBanks(), favoriteBankSelect.value, "Active favorite bank changed"));
if (panicSafeButton) {
  panicSafeButton.addEventListener("pointerdown", startPanicHold);
  ["pointerup", "pointercancel", "pointerleave"].forEach((eventName) => panicSafeButton.addEventListener(eventName, cancelPanicHold));
  panicSafeButton.addEventListener("keydown", (event) => { if (event.key === "Enter" || event.key === " ") startPanicHold(); });
  panicSafeButton.addEventListener("keyup", cancelPanicHold);
}

document.querySelectorAll("[data-command]").forEach((button) => {
  if (button.dataset.nowPlayingActionSource) return;
  button.addEventListener("click", () => sendCommand({ command: button.dataset.command }));
});
document.querySelectorAll("[data-relationship]").forEach((button) => {
  button.addEventListener("click", () => sendCommand({ command: "relationship", relationship: button.dataset.relationship }));
});
bpmStart.addEventListener("click", () => sendCommand({ command: "bpm_start", bpm: bpmInput.value, division: selectedDivision }));
bpmResync.addEventListener("click", () => sendCommand({ command: "bpm_resync", bpm: bpmInput.value, division: selectedDivision }));
bpmStop.addEventListener("click", () => sendCommand({ command: "bpm_stop" }));
bpmFollow.addEventListener("click", () => sendCommand({ command: "bpm_follow", enabled: !Boolean(latestShow?.bpm_follow_now_playing) }));
bpmDown.addEventListener("click", () => nudgeBpm(-1));
bpmUp.addEventListener("click", () => nudgeBpm(1));
bpmInput.addEventListener("change", () => {
  setBpmUiValue(bpmInput.value);
  sendBpmUpdate();
});
bpmInput.addEventListener("input", () => previewTypedBpm(bpmInput.value));
bpmSlider.addEventListener("input", () => {
  setBpmUiValue(bpmSlider.value);
  refreshBpmSurfaces();
});
bpmSlider.addEventListener("change", sendBpmUpdate);
if (addOscButtonMacro) addOscButtonMacro.addEventListener("click", () => addDraftMacro("osc_button"));
if (addOscClockMacro) addOscClockMacro.addEventListener("click", () => addDraftMacro("osc_clock"));
saveSettings.addEventListener("click", saveSettingsPayload);
saveSettingsSticky.addEventListener("click", saveSettingsPayload);
if (saveObsSettings) saveObsSettings.addEventListener("click", saveObsSettingsPayload);
saveQuickSettings.addEventListener("click", saveQuickSettingsPayload);
if (downloadOscSettings) downloadOscSettings.addEventListener("click", downloadOscSettingsPayload);
if (exportOscSettings) exportOscSettings.addEventListener("click", exportOscSettingsPayload);
if (importProjectOscSettings) importProjectOscSettings.addEventListener("click", importProjectOscSettingsPayload);
if (importOscSettings) {
  importOscSettings.addEventListener("change", () => importOscSettingsPayload(importOscSettings.files?.[0]));
}
saveLightsOsc.addEventListener("click", saveLightsOscPayload);
saveVisualsOsc.addEventListener("click", saveVisualsOscPayload);
saveCamerasOsc.addEventListener("click", saveCamerasOscPayload);
saveNowPlayingOsc.addEventListener("click", saveNowPlayingOscPayload);
[manualModeForm, beatlinkSourceForm, spotifySourceForm].forEach((form) => {
  if (!form) return;
  form.addEventListener("input", () => {
    manualModeDirty = true;
    if (manualModeStatus) manualModeStatus.textContent = "Unsaved Now Playing source settings.";
    if (beatlinkSourceStatus && form === beatlinkSourceForm) beatlinkSourceStatus.textContent = "Unsaved BeatLink settings.";
    if (spotifyAuthStatus && form === spotifySourceForm) spotifyAuthStatus.textContent = "Unsaved Spotify settings.";
  });
});
if (nowPlayingSourceTabs) {
  nowPlayingSourceTabs.addEventListener("click", (event) => {
    const button = event.target.closest("[data-now-playing-source]");
    if (!button) return;
    activeNowPlayingSource = button.dataset.nowPlayingSource || "beatlink";
    renderNowPlayingSourceTabs(latestShow);
  });
}
document.querySelectorAll("[data-now-playing-action-source]").forEach((button) => {
  button.addEventListener("click", () => {
    const command = button.dataset.command || "resume";
    if (command === "spotify" && spotifyNeedsConnection()) {
      optimisticNowPlayingMode = "";
      activeNowPlayingSource = "spotify";
      renderNowPlayingSourceTabs(latestShow);
      renderSelectedButtons(latestShow || {});
      runSpotifyAction("/spotify/login", null, "Preparing Spotify login...");
      return;
    }
    optimisticNowPlayingMode = nowPlayingModeForCommand(command);
    renderSelectedButtons({ ...(latestShow || {}), manual_mode: optimisticNowPlayingMode });
    sendCommand({ command });
  });
});
if (spotifyConnect) spotifyConnect.addEventListener("click", () => runSpotifyAction("/spotify/login", null, "Preparing Spotify login..."));if (spotifyUseNowPlaying) spotifyUseNowPlaying.addEventListener("click", () => runSpotifyAction("/api/spotify/activate", {}, "Activating Spotify source..."));
if (spotifyDisconnect) spotifyDisconnect.addEventListener("click", () => runSpotifyAction("/api/spotify/disconnect", {}, "Disconnecting Spotify..."));
if (saveManualModeText) saveManualModeText.addEventListener("click", saveManualModePayload);
if (rebuildMusicIndex) rebuildMusicIndex.addEventListener("click", rebuildMusicIndexPayload);
saveCurrentLook.addEventListener("click", saveLookFromBuilder);
launchSelectedLook.addEventListener("click", async () => {
  const name = currentLookBuilderName();
  if (!name) {
    saveLookStatus.textContent = "Name the look first.";
    return;
  }
  if (lookBuilderDirty || !presetData?.groups?.performance?.[name]) await saveLookFromBuilder();
  dispatchPerformanceLook(name, "look builder");
});
if (saveLookRouting) saveLookRouting.addEventListener("click", saveLookBuilderRouting);
saveCurrentLookSelect.addEventListener("change", () => {
  if (lookBuilderName) lookBuilderName.value = saveCurrentLookSelect.value;
  lookBuilderDirty = false;
  renderLookBuilder();
});
if (lookBuilderName) lookBuilderName.addEventListener("input", () => {
  lookBuilderDirty = true;
  saveLookStatus.textContent = "Unsaved look name or cue changes.";
});
saveLookLinks.addEventListener("click", saveLookLinksPayload);
savePresets.addEventListener("click", savePresetGroup);
if (saveShowSequence) saveShowSequence.addEventListener("click", saveShowSequencePayload);
if (addSequenceStep) addSequenceStep.addEventListener("click", addShowSequenceStep);
if (showSequenceLoop) showSequenceLoop.addEventListener("change", markSequenceDirty);
if (playShowSequence) playShowSequence.addEventListener("click", startShowSequencePlayback);
if (pauseShowSequence) pauseShowSequence.addEventListener("click", pauseShowSequencePlayback);
if (nextShowSequenceStep) nextShowSequenceStep.addEventListener("click", triggerNextShowSequenceStep);
if (stopShowSequence) stopShowSequence.addEventListener("click", () => stopShowSequencePlayback());
if (showSequenceSelect) showSequenceSelect.addEventListener("change", () => {
  stopShowSequencePlayback("Loaded another show.");
  activeShowSequence = showSequenceSelect.value;
  showSequenceDirty = false;
  renderSequencer();
});
if (showSequenceName) showSequenceName.addEventListener("input", markSequenceDirty);
extractPalette.addEventListener("click", () => refreshPalette(Boolean(appSettings?.use_artwork_palette)));
applyPalette.addEventListener("click", () => refreshPalette(true));
useCurrentColors.addEventListener("click", () => sendCommand({ command: "use_current_colors" }));
neutralArtworkPrimary.addEventListener("change", () => saveArtworkOptionPayload({ neutral_artwork_primary: neutralArtworkPrimary.value }));
neutralArtworkSecondary.addEventListener("change", () => saveArtworkOptionPayload({ neutral_artwork_secondary: neutralArtworkSecondary.value }));
neutralArtworkAccent.addEventListener("change", () => saveArtworkOptionPayload({ neutral_artwork_accent: neutralArtworkAccent.value }));
lookLightsToggles.forEach((button) => button.addEventListener("click", () => saveLookLightsMode(!lookApplyLights())));
keepPresetColorsToggle.addEventListener("click", () => saveArtworkOptionPayload({ preset_keep_current_colors: !Boolean(appSettings?.preset_keep_current_colors) }));
autoArtworkToggle.addEventListener("click", () => saveArtworkOptionPayload({ use_artwork_palette: !Boolean(appSettings?.use_artwork_palette) }));
if (copyColorComment && colorComment) {
  copyColorComment.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(colorComment.textContent);
      showToast("Copied color comment");
    } catch (_error) {
      showToast("Clipboard was blocked by the browser. The color comment is visible on Now Playing.", true);
    }
  });
}
if (sendAllLinks) sendAllLinks.addEventListener("click", () => sendCommand({ command: "send_all_links" }));
if (reapplyCurrentLook) reapplyCurrentLook.addEventListener("click", reapplyActivePerformanceLook);
if (applyDefaultLook) applyDefaultLook.addEventListener("click", applyDefaultPerformanceLook);
if (overviewReapplyLook) overviewReapplyLook.addEventListener("click", reapplyActivePerformanceLook);
if (overviewDefaultLook) overviewDefaultLook.addEventListener("click", applyDefaultPerformanceLook);
setupMomentaryControl(overviewPulseHold, "pulse", 100);
if (openGenerativeVisualizer) openGenerativeVisualizer.addEventListener("click", () => window.open("/visuals/generative", "_blank", "noopener"));
if (freezeGenerativeVisual) freezeGenerativeVisual.addEventListener("click", () => {
  const next = { ...collectGenerativeValues(), freeze: !Boolean(currentGenerativeVisual().freeze), blackout: false, enabled: true };
  sendCommand({ command: "generative_visual", values: next });
});
if (stopGenerativeVisual) stopGenerativeVisual.addEventListener("click", () => sendCommand({ command: "generative_visual_stop" }));
clearLog.addEventListener("click", () => sendCommand({ command: "clear_log" }));
trackUseCurrentColors.addEventListener("click", () => sendCommand({ command: "use_current_colors" }));
trackCopyColorComment.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(trackColorComment.textContent);
    showToast("Copied track color comment");
  } catch (_error) {
    showToast("Clipboard was blocked by the browser.", true);
  }
});

if (window.ResizeObserver) {
  const liveDeckResizeObserver = new ResizeObserver(scheduleLiveDeckResize);
  [liveDeckGrid, ...liveDeckPanelCards].filter((element) => element instanceof Element).forEach((element) => liveDeckResizeObserver.observe(element));
}
window.addEventListener("resize", scheduleLiveDeckResize);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    if (statusTimer) clearTimeout(statusTimer);
    statusTimer = null;
    return;
  }
  loadStatus({ full: true, force: true });
});

function initializeTabletSetupPanels() {
  const collapseForTablet = window.matchMedia("(max-width: 1180px)").matches;
  document.querySelectorAll("[data-tablet-collapse]").forEach((panel) => {
    panel.open = !collapseForTablet;
  });
}

async function initializeApp() {
  await bootstrapAdminSession();
  initializeTabletSetupPanels();
  renderDivisionButtons();
  applyLiveDeckVisibility();
  if (oscBackupFileNameInput && !oscBackupFileNameInput.value) oscBackupFileNameInput.value = defaultOscBackupFileName();
  loadOscBackupFiles();
  const initialSectionId = window.location.hash.slice(1);
  if (initialSectionId && document.querySelector(`#${initialSectionId}`)) activateSection(initialSectionId);
  loadStatus();
}

initializeApp();
