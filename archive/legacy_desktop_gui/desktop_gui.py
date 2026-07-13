"""
Legacy desktop GUI for NT Performance Hub.

Preserved for reference and compatibility while the browser app is the primary
live-control surface.
"""

from __future__ import annotations

import colorsys
import contextlib
import csv
import io
import json
import os
import queue
import socket
import struct
import sys
import threading
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Optional
import tkinter as tk

ARCHIVE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ARCHIVE_DIR.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PIL import Image, ImageOps, ImageTk

import beatlink_watcher_resolume_osc as watcher
import extract_album_artwork as artwork_module
from extract_album_artwork import DEFAULT_OUTPUT_PIXELS


SCRIPT_DIR = PROJECT_ROOT
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_PATH = CONFIG_DIR / "app_config.json"
LEGACY_CONFIG_PATH = PROJECT_ROOT / "performance_lighting_gui_config.json"
VISUAL_DEFAULTS_CONFIG = CONFIG_DIR / "visual_defaults.json"
LOG_DIR = PROJECT_ROOT / "logs"
MAX_COMMAND_OUTPUT_LINES = 2000
DAILY_LOG_FIELDS = [
    "timestamp",
    "track",
    "title",
    "artist",
    "album",
    "bpm",
    "matched_file",
    "match_score",
    "comment_found",
    "comment_to_add",
    "applied_source",
    "fallback_used",
    "note",
    "osc_values",
]
TRACK_HISTORY_LOG_FIELDS = [
    "timestamp",
    "action",
    "track",
    "artist",
    "title",
    "album",
    "bpm",
    "existing_mp3_comment",
    "used_color_comment",
    "suggested_color_comment",
    "primary",
    "secondary",
    "accent",
    "source",
    "note",
    "matched_file",
]

STROBE_SAFETY_MODES = ("OFF", "LOW ONLY", "FULL")
BLT_FIELD_CHOICES = (
    "full_track",
    "title",
    "artist",
    "album",
    "track_info",
    "bpm",
    "player_number",
    "device_name",
    "source_player",
    "player",
    "comment",
)
LINK_CONTROL_SPECS: tuple[tuple[int, str, str, str], ...] = (
    (1, "Primary Hue", "color1", "color"),
    (2, "Secondary Hue", "color2", "color"),
    (3, "Motion / Energy", "motion", "percent_buttons"),
    (4, "Accent Hue", "strobe_color", "color"),
    (5, "Saturation", "saturation", "percent_buttons"),
    (6, "Brightness", "brightness", "percent_buttons"),
    (7, "FX / Pattern", "fx", "percent_buttons"),
    (8, "Pulse / Accent", "pulse", "percent_buttons"),
)
CONTROL_TO_LINK = {key: link for link, _label, key, _kind in LINK_CONTROL_SPECS}
DEFAULT_LINK_LABELS = {str(link): label for link, label, _key, _kind in LINK_CONTROL_SPECS}
CONTROL_TO_DISPLAY_LINK = {
    "color1": 1,
    "color2": 2,
    "strobe": 3,
    "strobe_color": 4,
    "saturation": 5,
    "brightness": 6,
    "motion": 3,
    "fx": 7,
    "pulse": 8,
}
PRESET_CONTROL_COLUMNS: tuple[tuple[str, int, str], ...] = (
    ("PRIMARY", 1, ""),
    ("SECONDARY", 2, ""),
    ("STROBE", 4, ""),
    ("MOTION", 3, ""),
    ("STROBE_PERCENT", 3, " %"),
    ("SATURATION", 5, ""),
    ("BRIGHTNESS", 6, ""),
    ("FX", 7, ""),
    ("PULSE", 8, ""),
)

COLOR_HUE_VALUES = dict(watcher.COLOR_HUE_VALUES)
COLOR_HEX = {
    "red": "#ff3030",
    "orange": "#ff8a00",
    "amber": "#ffbf00",
    "yellow": "#fff04a",
    "lime": "#9cff00",
    "green": "#20d060",
    "teal": "#00b894",
    "cyan": "#00d8ff",
    "blue": "#2563ff",
    "indigo": "#4b3dff",
    "purple": "#7b2cff",
    "violet": "#9c4dff",
    "uv": "#6c2bff",
    "magenta": "#ff2bd6",
    "pink": "#ff6bb5",
}
SORTED_COLOR_NAMES = [name for name, _ in sorted(COLOR_HUE_VALUES.items(), key=lambda item: (item[1], item[0]))]
DEFAULT_NEUTRAL_ARTWORK_COLOR_NAME = "blue"
DEFAULT_VINYL_LOGO_PATH = r"C:\Users\ryant\Videos\Resolume Visuals\Branding\NO_TALKING_DOUGHNUT_LOGO_2.png"
DEFAULT_VINYL_TRACK_TEXT = "record playing"
DEFAULT_STUDIO_ARTWORK_PATH = r"C:\Users\ryant\Videos\Resolume Visuals\Branding\NO_TALKING_STUDIO.png"
DEFAULT_STUDIO_TRACK_TEXT = "NO TALKING STUDIO"

DEFAULT_TEMPLATE = (
    "PRIMARY=indigo;SECONDARY=magenta;MOOD=club;ENERGY=3;SECTION=GROOVE;"
    "STROBE_PERCENT=10;STROBE=purple;SATURATION=100;BRIGHTNESS=100;"
    "MOTION=50;FX=25;PULSE=0"
)
SELECTED_BUTTON_PREFIX = "✓ "
BPM_FLIP_MIN_BPM = 40.0
BPM_FLIP_MAX_BPM = 240.0
BPM_FLIP_DIVISIONS: tuple[tuple[str, float], ...] = (
    ("1/64", 4.0 / 64.0),
    ("1/32", 4.0 / 32.0),
    ("1/16", 4.0 / 16.0),
    ("1/8", 4.0 / 8.0),
    ("1/4", 4.0 / 4.0),
    ("1/2 bar", 2.0),
    ("1 bar", 4.0),
    ("2 bars", 8.0),
    ("4 bars", 16.0),
    ("8 bars", 32.0),
    ("16 bars", 64.0),
)
BPM_FLIP_DIVISION_MULTIPLIERS = dict(BPM_FLIP_DIVISIONS)
BPM_FLIP_DIVISION_ALIASES = {
    "Bar": "1 bar",
    "1/2x": "1/2 bar",
    "1x": "1/4",
    "2x": "1/8",
    "4x": "1/16",
    "1/4 beat": "1/16",
    "1/2 beat": "1/8",
    "1 beat": "1/4",
    "2 beats": "1/2 bar",
    "4 beats": "1 bar",
    "1/2": "1/2 bar",
}


@dataclass
class LightingState:
    color1_name: str = "indigo"
    color1_value: float = 0.708
    color2_name: str = "magenta"
    color2_value: float = 0.833
    strobe_color_name: str = "purple"
    strobe_color_value: float = 0.750
    strobe_percent: int = 0
    strobe_value: float = 0.0
    saturation_percent: int = 100
    saturation_value: float = 1.0
    brightness_percent: int = 100
    brightness_value: float = 1.0
    motion_value: float = 0.25
    fx_value: float = 0.0
    pulse_value: float = 0.0
    source: str = "default"
    mood: Optional[str] = None
    energy: Optional[int] = None
    section: Optional[str] = None
    notes: list[str] = field(default_factory=list)

    def clone(self) -> "LightingState":
        return LightingState(**asdict(self))


@dataclass
class PaletteColor:
    name: str = "-"
    hue: float = 0.0
    rgb: tuple[int, int, int] = (0, 0, 0)
    hex: str = "#000000"


@dataclass
class ArtworkPalette:
    dominant: PaletteColor = field(default_factory=PaletteColor)
    accent: PaletteColor = field(default_factory=PaletteColor)
    bright_accent: PaletteColor = field(default_factory=PaletteColor)
    available: bool = False
    source_path: str = ""


MOOD_PRESETS: dict[str, dict[str, Any]] = {
    "dark": {"PRIMARY": "indigo", "SECONDARY": "purple", "STROBE_PERCENT": 0, "SATURATION": 70, "BRIGHTNESS": 55, "MOTION": 20, "FX": 20, "PULSE": 10},
    "euphoric": {"PRIMARY": "magenta", "SECONDARY": "cyan", "STROBE_PERCENT": 10, "SATURATION": 100, "BRIGHTNESS": 100, "MOTION": 70, "FX": 55, "PULSE": 45},
    "acid": {"PRIMARY": "lime", "SECONDARY": "purple", "STROBE_PERCENT": 25, "SATURATION": 100, "BRIGHTNESS": 100, "MOTION": 80, "FX": 65, "PULSE": 50},
    "warm": {"PRIMARY": "amber", "SECONDARY": "pink", "STROBE_PERCENT": 10, "SATURATION": 85, "BRIGHTNESS": 90, "MOTION": 45, "FX": 35, "PULSE": 25},
    "icy": {"PRIMARY": "cyan", "SECONDARY": "blue", "STROBE_PERCENT": 10, "SATURATION": 80, "BRIGHTNESS": 85, "MOTION": 40, "FX": 30, "PULSE": 20},
    "warehouse": {"PRIMARY": "red", "SECONDARY": "blue", "STROBE_PERCENT": 25, "SATURATION": 100, "BRIGHTNESS": 80, "MOTION": 75, "FX": 65, "PULSE": 45},
    "disco": {"PRIMARY": "amber", "SECONDARY": "pink", "STROBE_PERCENT": 10, "SATURATION": 90, "BRIGHTNESS": 100, "MOTION": 55, "FX": 45, "PULSE": 35},
    "afterhours": {"PRIMARY": "blue", "SECONDARY": "indigo", "STROBE_PERCENT": 0, "SATURATION": 75, "BRIGHTNESS": 60, "MOTION": 20, "FX": 15, "PULSE": 10},
    "club": {"PRIMARY": "indigo", "SECONDARY": "magenta", "STROBE_PERCENT": 10, "SATURATION": 100, "BRIGHTNESS": 100, "MOTION": 60, "FX": 45, "PULSE": 30},
}

ENERGY_PRESETS: dict[str, dict[str, Any]] = {
    "1": {"BRIGHTNESS": 50, "SATURATION": 50, "STROBE_PERCENT": 0, "MOTION": 15, "FX": 10, "PULSE": 5},
    "2": {"BRIGHTNESS": 65, "SATURATION": 70, "STROBE_PERCENT": 0, "MOTION": 30, "FX": 20, "PULSE": 10},
    "3": {"BRIGHTNESS": 85, "SATURATION": 90, "STROBE_PERCENT": 10, "MOTION": 50, "FX": 40, "PULSE": 25},
    "4": {"BRIGHTNESS": 100, "SATURATION": 100, "STROBE_PERCENT": 25, "MOTION": 75, "FX": 65, "PULSE": 45},
    "5": {"BRIGHTNESS": 100, "SATURATION": 100, "STROBE_PERCENT": 50, "MOTION": 95, "FX": 90, "PULSE": 65},
}

SECTION_PRESETS: dict[str, dict[str, Any]] = {
    "INTRO": {"BRIGHTNESS": 55, "SATURATION": 60, "STROBE_PERCENT": 0, "MOTION": 20, "FX": 10, "PULSE": 5},
    "GROOVE": {"BRIGHTNESS": 85, "SATURATION": 85, "STROBE_PERCENT": 10, "MOTION": 50, "FX": 35, "PULSE": 20},
    "BUILD": {"BRIGHTNESS": 95, "SATURATION": 100, "STROBE_PERCENT": 25, "MOTION": 75, "FX": 60, "PULSE": 40},
    "DROP": {"BRIGHTNESS": 100, "SATURATION": 100, "STROBE_PERCENT": 50, "MOTION": 95, "FX": 80, "PULSE": 55},
    "BREAKDOWN": {"PRIMARY": "blue", "SECONDARY": "indigo", "BRIGHTNESS": 50, "SATURATION": 75, "STROBE_PERCENT": 0, "MOTION": 15, "FX": 10, "PULSE": 5},
    "OUTRO": {"BRIGHTNESS": 45, "SATURATION": 55, "STROBE_PERCENT": 0, "MOTION": 15, "FX": 10, "PULSE": 0},
}

PERFORMANCE_PRESETS: dict[str, dict[str, Any]] = {
    "Default": {"PRIMARY": "indigo", "SECONDARY": "magenta", "STROBE": "purple", "STROBE_PERCENT": 10, "SATURATION": 100, "BRIGHTNESS": 100, "MOTION": 35, "FX": 20, "PULSE": 10},
    "Warm": {"PRIMARY": "amber", "SECONDARY": "pink", "STROBE": "orange", "STROBE_PERCENT": 10, "SATURATION": 90, "BRIGHTNESS": 90, "MOTION": 45, "FX": 30, "PULSE": 20},
    "Cool": {"PRIMARY": "cyan", "SECONDARY": "blue", "STROBE": "cyan", "STROBE_PERCENT": 10, "SATURATION": 85, "BRIGHTNESS": 90, "MOTION": 40, "FX": 30, "PULSE": 15},
    "Club": {"PRIMARY": "indigo", "SECONDARY": "magenta", "STROBE": "purple", "STROBE_PERCENT": 25, "SATURATION": 100, "BRIGHTNESS": 100, "MOTION": 70, "FX": 60, "PULSE": 40},
    "Breakdown": {"PRIMARY": "blue", "SECONDARY": "indigo", "STROBE": "blue", "STROBE_PERCENT": 0, "SATURATION": 75, "BRIGHTNESS": 50, "MOTION": 15, "FX": 10, "PULSE": 5},
    "Drop": {"PRIMARY": "magenta", "SECONDARY": "cyan", "STROBE": "purple", "STROBE_PERCENT": 50, "SATURATION": 100, "BRIGHTNESS": 100, "MOTION": 95, "FX": 80, "PULSE": 55},
    "Dark / Minimal": {"PRIMARY": "indigo", "SECONDARY": "purple", "STROBE": "purple", "STROBE_PERCENT": 0, "SATURATION": 65, "BRIGHTNESS": 45, "MOTION": 15, "FX": 10, "PULSE": 0},
    "High Energy": {"PRIMARY": "lime", "SECONDARY": "magenta", "STROBE": "cyan", "STROBE_PERCENT": 50, "SATURATION": 100, "BRIGHTNESS": 100, "MOTION": 100, "FX": 90, "PULSE": 70},
    "Emergency Reset": {"PRIMARY": "blue", "SECONDARY": "purple", "STROBE": "blue", "STROBE_PERCENT": 0, "SATURATION": 100, "BRIGHTNESS": 100, "MOTION": 20, "FX": 0, "PULSE": 0},
    "Blackout / Safe": {"PRIMARY": "blue", "SECONDARY": "indigo", "STROBE": "blue", "STROBE_PERCENT": 0, "SATURATION": 60, "BRIGHTNESS": 0, "MOTION": 0, "FX": 0, "PULSE": 0},
}

DEFAULT_BLT_OSC_OUTPUTS: list[dict[str, Any]] = [
    {"key": "title", "label": "BLT Title", "field": "title", "address": watcher.OSC_TITLE_ADDRESS, "enabled": True},
    {"key": "artist", "label": "BLT Artist", "field": "artist", "address": watcher.OSC_ARTIST_ADDRESS, "enabled": True},
    {"key": "track", "label": "BLT Track", "field": "full_track", "address": watcher.OSC_TRACK_ADDRESS, "enabled": True},
    {"key": "track_info", "label": "BLT Track Info", "field": "track_info", "address": watcher.OSC_TRACK_INFO_ADDRESS, "enabled": True},
    {"key": "resolume_track_text", "label": "Resolume Track Text", "field": "full_track", "address": watcher.RESOLUME_TRACK_TEXT_ADDRESS, "enabled": True},
    {"key": "resolume_track_info", "label": "Resolume Track Info", "field": "track_info", "address": watcher.RESOLUME_TRACK_INFO_TEXT_ADDRESS, "enabled": True},
    {"key": "bpm", "label": "BPM", "field": "bpm", "address": "/blt/bpm", "enabled": False},
    {"key": "player", "label": "Player", "field": "player_number", "address": "/blt/player", "enabled": False},
    {"key": "device", "label": "Device", "field": "device_name", "address": "/blt/device", "enabled": False},
    {"key": "album", "label": "Album", "field": "album", "address": "/blt/album", "enabled": False},
    {"key": "custom_1", "label": "Custom 1", "field": "bpm", "address": "", "enabled": False},
    {"key": "custom_2", "label": "Custom 2", "field": "player_number", "address": "", "enabled": False},
    {"key": "custom_3", "label": "Custom 3", "field": "device_name", "address": "", "enabled": False},
    {"key": "custom_4", "label": "Custom 4", "field": "comment", "address": "", "enabled": False},
]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def percent_to_value(value: Any) -> float:
    return clamp(parse_percent(value) / 100.0)


def motion_percent(value: Any) -> int:
    return min(parse_percent(value), 95)


def parse_percent(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    text = str(value).strip().casefold().removesuffix("%")
    aliases = {
        "off": 0,
        "none": 0,
        "low": 25,
        "medium": 50,
        "med": 50,
        "high": 75,
        "full": 100,
        "slow": 20,
        "fast": 85,
    }
    if text in aliases:
        return aliases[text]
    try:
        return max(0, min(100, int(round(float(text)))))
    except ValueError:
        return default


def parse_int(value: Any, default: int, minimum: int = 1, maximum: int = 100000) -> int:
    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, parsed))


def parse_bpm(value: Any) -> float:
    text = str(value or "").strip()
    if not text:
        raise ValueError("Enter a BPM first.")
    try:
        bpm = float(text)
    except ValueError as exc:
        raise ValueError(f"BPM must be a number, not {text!r}.") from exc
    if not BPM_FLIP_MIN_BPM <= bpm <= BPM_FLIP_MAX_BPM:
        raise ValueError(f"BPM must be between {BPM_FLIP_MIN_BPM:.0f} and {BPM_FLIP_MAX_BPM:.0f}.")
    return bpm


def normalize_bpm_swap_rate(rate: Any) -> str:
    text = str(rate or "").strip()
    normalized = BPM_FLIP_DIVISION_ALIASES.get(text, text)
    if normalized not in BPM_FLIP_DIVISION_MULTIPLIERS:
        normalized = "1 beat"
    return normalized


def bpm_flip_interval_ms(bpm: float, division: str) -> int:
    division = normalize_bpm_swap_rate(division)
    multiplier = BPM_FLIP_DIVISION_MULTIPLIERS.get(division)
    if multiplier is None:
        raise ValueError(f"Unknown BPM division: {division}")
    return max(1, int(round((60000.0 / bpm) * multiplier)))


def clean_path_text(raw_path: Any) -> str:
    return str(raw_path or "").strip().strip('"').strip("'").strip()


def path_from_text(raw_path: Any, fallback: str | Path) -> Path:
    return Path(clean_path_text(raw_path) or fallback)


def nearest_percent_choice(value_percent: Any, allowed_values: list[int]) -> int:
    value = parse_percent(value_percent)
    return min(allowed_values, key=lambda allowed: (abs(allowed - value), allowed))


def normalized_key(raw_key: str) -> str:
    key = raw_key.strip().upper().replace(" ", "_").replace("-", "_")
    aliases = {
        "ACCENT": "STROBE",
        "STROBE_COLOR": "STROBE",
        "STROBECOLOUR": "STROBE",
        "STROBE_COLOUR": "STROBE",
        "COLOR1": "PRIMARY",
        "COLOR_A": "PRIMARY",
        "COLOUR1": "PRIMARY",
        "COLOR2": "SECONDARY",
        "COLOR_B": "SECONDARY",
        "COLOUR2": "SECONDARY",
        "STROBE%": "STROBE_PERCENT",
        "STROBEPERCENT": "STROBE_PERCENT",
        "STROBE_RATE": "STROBE_PERCENT",
        "SAT": "SATURATION",
        "SATURATION_PERCENT": "SATURATION",
        "BRIGHTNESS_PERCENT": "BRIGHTNESS",
        "DIMMER": "BRIGHTNESS",
        "MOVEMENT": "MOTION",
        "SHAPE": "FX",
        "PATTERN": "FX",
        "GRADIENT_POSITION": "FX",
        "ACCENT_AMOUNT": "PULSE",
        "AUDIO_REACTIVITY": "PULSE",
    }
    return aliases.get(key, key)


def parse_comment_tags(comment: str) -> dict[str, str]:
    tags: dict[str, str] = {}
    supported = {
        "PRIMARY",
        "SECONDARY",
        "STROBE",
        "STROBE_PERCENT",
        "SATURATION",
        "BRIGHTNESS",
        "MOOD",
        "ENERGY",
        "SECTION",
        "MOTION",
        "FX",
        "PULSE",
    }
    for part in (comment or "").split(";"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        key = normalized_key(key)
        if key in supported:
            tags[key] = value.strip().casefold() if key != "SECTION" else value.strip().upper()
    return tags


def nearest_color_name(hue: float) -> str:
    hue = hue % 1.0

    def distance(item: tuple[str, float]) -> float:
        diff = abs(item[1] - hue)
        return min(diff, 1.0 - diff)

    return min(COLOR_HUE_VALUES.items(), key=distance)[0]


def color_name_to_value(name: str, fallback: str = "indigo") -> tuple[str, float]:
    normalized = str(name or "").strip().casefold()
    if normalized not in COLOR_HUE_VALUES:
        normalized = fallback
    return normalized, COLOR_HUE_VALUES[normalized]


def rgb_to_palette_color(rgb: tuple[int, int, int]) -> PaletteColor:
    r, g, b = rgb
    hue, _sat, _val = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    return PaletteColor(
        name=nearest_color_name(hue),
        hue=hue,
        rgb=rgb,
        hex=f"#{r:02x}{g:02x}{b:02x}",
    )


def color_hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def make_state_from_template(template: str) -> LightingState:
    state = LightingState()
    apply_values_to_state(state, parse_comment_tags(template), exact=True)
    state.source = "default"
    return state


def apply_values_to_state(state: LightingState, values: dict[str, Any], exact: bool = False) -> None:
    if "PRIMARY" in values:
        state.color1_name, state.color1_value = color_name_to_value(str(values["PRIMARY"]), state.color1_name)
    if "SECONDARY" in values:
        state.color2_name, state.color2_value = color_name_to_value(str(values["SECONDARY"]), state.color2_name)
    if "STROBE" in values:
        state.strobe_color_name, state.strobe_color_value = color_name_to_value(str(values["STROBE"]), state.strobe_color_name)
    if "STROBE_PERCENT" in values:
        state.strobe_percent = parse_percent(values["STROBE_PERCENT"], state.strobe_percent)
        state.strobe_value = percent_to_value(state.strobe_percent)
    if "SATURATION" in values:
        state.saturation_percent = parse_percent(values["SATURATION"], state.saturation_percent)
        state.saturation_value = percent_to_value(state.saturation_percent)
    if "BRIGHTNESS" in values:
        state.brightness_percent = parse_percent(values["BRIGHTNESS"], state.brightness_percent)
        state.brightness_value = percent_to_value(state.brightness_percent)
    if "MOTION" in values:
        state.motion_value = percent_to_value(motion_percent(values["MOTION"]))
    if "FX" in values:
        state.fx_value = percent_to_value(values["FX"])
    if "PULSE" in values:
        state.pulse_value = percent_to_value(values["PULSE"])
    if exact:
        if "MOOD" in values:
            state.mood = str(values["MOOD"]).casefold()
        if "ENERGY" in values:
            with contextlib.suppress(ValueError):
                state.energy = int(str(values["ENERGY"]).strip())
        if "SECTION" in values:
            state.section = str(values["SECTION"]).upper()


class PerformanceLightingGui:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("NT Performance Hub - Legacy Desktop GUI")
        self.root.geometry("1500x930")
        self.root.minsize(1180, 760)
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        self.output_queue: queue.Queue[dict[str, Any]] = queue.Queue()
        self.stop_event = threading.Event()
        self.watch_thread: Optional[threading.Thread] = None
        self.rebuild_thread: Optional[threading.Thread] = None
        self.current_matched_file: Optional[Path] = None
        self.artwork_photo: Optional[ImageTk.PhotoImage] = None
        self.artwork_preview_labels: list[ttk.Label] = []
        self.visual_swatches: dict[str, tk.Canvas] = {}
        self.color_button_groups: dict[str, dict[str, tk.Button]] = {}
        self.percent_button_groups: dict[str, dict[int, tk.Button]] = {}
        self.percent_button_values: dict[str, list[int]] = {}
        self.toggle_buttons: dict[str, tk.Button] = {}
        self.control_vars: dict[str, tk.Variable] = {}
        self.control_readout_vars: dict[str, tk.StringVar] = {}
        self.output_vars: dict[str, tk.StringVar] = {}
        self.osc_vars: dict[int, tk.StringVar] = {}
        self.preset_editors: dict[str, dict[str, dict[str, Any]]] = {}
        self.dynamic_link_label_vars: list[tuple[tk.StringVar, int, str]] = []
        self.palette_labels: dict[str, tk.StringVar] = {}
        self.palette_swatches: dict[str, list[tk.Canvas]] = {}
        self.choice_button_groups: dict[str, dict[str, tk.Button]] = {}
        self.osc_address_vars: dict[int, tk.StringVar] = {}
        self.blt_osc_output_vars: dict[str, dict[str, tk.Variable]] = {}
        self.blt_osc_last_vars: dict[str, tk.StringVar] = {}
        self.output_color_canvases: dict[str, tk.Canvas] = {}
        self.latest_blt_context: dict[str, str] = {}
        self.latest_track_history_context: dict[str, str] = {}
        self.track_history_context: dict[str, str] = {}
        self.palette = ArtworkPalette()

        self.config = self.load_config()
        self.blt_osc_outputs = self.normalize_blt_osc_outputs(self.config.get("blt_osc_outputs", DEFAULT_BLT_OSC_OUTPUTS))
        self.performance_presets = dict(self.config.get("performance_presets", PERFORMANCE_PRESETS))
        self.mood_presets = dict(self.config.get("mood_presets", MOOD_PRESETS))
        self.energy_presets = dict(self.config.get("energy_presets", ENERGY_PRESETS))
        self.section_presets = dict(self.config.get("section_presets", SECTION_PRESETS))
        self.state = make_state_from_template(self.config["default_fallback_template"])
        self.last_safety_note = ""
        self.last_track_key = ""
        self.current_track_auto_key = ""
        self.manual_artwork_override_track_key = ""
        self.last_simple_history_signature = ""
        self.track_history_key = ""
        self.track_history_matched_file = ""
        self.track_history_existing_comment = ""
        self.track_history_final_written = True
        self.track_history_final_source = ""
        self.track_history_final_note = ""
        self.vinyl_mode_active = False
        self.manual_artwork_mode = ""
        self.bpm_flip_running = False
        self.bpm_flip_after_id: Optional[str] = None
        self.bpm_flip_token = 0
        self.bpm_flip_remaining: Optional[int] = None
        self.bpm_flip_trigger_button: Optional[ttk.Button] = None

        self.status_var = tk.StringVar(value="Stopped")
        self.last_event_var = tk.StringVar(value="Ready")
        self.blt_status_var = tk.StringVar(value="BLT not polled yet")
        self.output_size_var = tk.StringVar(value=str(self.config["output_pixels"]))
        self.bpm_flip_bpm_var = tk.StringVar(value=str(self.config.get("bpm_flip_bpm", "125")))
        bpm_division = normalize_bpm_swap_rate(self.config.get("bpm_flip_division", "1/4"))
        self.bpm_flip_division_var = tk.StringVar(value=bpm_division)
        self.bpm_flip_status_var = tk.StringVar(value="Auto Swap idle")
        self.rebuild_index_var = tk.BooleanVar(value=False)
        self.apply_preset_colors_var = tk.BooleanVar(value=not bool(self.config["preset_keep_current_colors"]))
        self.auto_artwork_palette_var = tk.BooleanVar(value=bool(self.config.get("use_artwork_palette", False)))
        neutral_color = str(self.config.get("neutral_artwork_color", DEFAULT_NEUTRAL_ARTWORK_COLOR_NAME)).casefold()
        if neutral_color not in COLOR_HUE_VALUES:
            neutral_color = DEFAULT_NEUTRAL_ARTWORK_COLOR_NAME
        self.neutral_artwork_color_var = tk.StringVar(value=neutral_color)
        self.template_var = tk.StringVar(value=self.config["default_fallback_template"])
        self.blt_url_var = tk.StringVar(value=self.config["blt_params_url"])
        self.osc_host_var = tk.StringVar(value=self.config["resolume_host"])
        self.osc_port_var = tk.StringVar(value=str(self.config["resolume_port"]))
        self.music_root_var = tk.StringVar(value=self.config["music_root"])
        self.artwork_output_var = tk.StringVar(value=self.config["artwork_output"])
        self.fallback_artwork_path_var = tk.StringVar(value=self.config["fallback_artwork_path"])
        self.vinyl_logo_path_var = tk.StringVar(value=self.config.get("vinyl_logo_path", DEFAULT_VINYL_LOGO_PATH))
        self.vinyl_track_text_var = tk.StringVar(value=self.config.get("vinyl_track_text", DEFAULT_VINYL_TRACK_TEXT))
        self.studio_artwork_path_var = tk.StringVar(value=self.config.get("studio_artwork_path", DEFAULT_STUDIO_ARTWORK_PATH))
        self.studio_track_text_var = tk.StringVar(value=self.config.get("studio_track_text", DEFAULT_STUDIO_TRACK_TEXT))
        self.default_template_var = tk.StringVar(value=self.config["default_fallback_template"])
        self.osc_address_vars = {
            link: tk.StringVar(value=self.config["osc_addresses"].get(str(link), watcher.RESOLUME_LINK_OSC_ADDRESSES[link]))
            for link in range(1, 9)
        }
        self.link_label_vars = {
            link: tk.StringVar(value=self.config.get("link_labels", DEFAULT_LINK_LABELS).get(str(link), DEFAULT_LINK_LABELS[str(link)]))
            for link in range(1, 9)
        }

        self.active_track_var = tk.StringVar(value="Waiting for track...")
        self.matched_file_var = tk.StringVar(value="-")
        self.comment_found_var = tk.StringVar(value="No track comment read yet.")
        self.parsed_tags_var = tk.StringVar(value="-")
        self.missing_tags_var = tk.StringVar(value="-")
        self.applied_source_var = tk.StringVar(value="default")
        self.fallback_var = tk.StringVar(value="-")
        self.artwork_status_var = tk.StringVar(value="-")
        self.daily_log_status_var = tk.StringVar(value=f"Daily log folder: {LOG_DIR}")
        self.ensure_daily_log_file()

        self._build_ui()
        self.update_bpm_flip_status()
        self.apply_state(self.state, source="default", send=False)
        self._poll_output_queue()
        self.root.after(0, self.maximize_window)
        self.root.after(500, self.start_watcher)

    def maximize_window(self) -> None:
        try:
            self.root.state("zoomed")
        except tk.TclError:
            with contextlib.suppress(tk.TclError):
                self.root.attributes("-zoomed", True)

    def load_config(self) -> dict[str, Any]:
        config = {
            "blt_params_url": watcher.BLT_PARAMS_URL,
            "resolume_host": watcher.RESOLUME_OSC_HOST,
            "resolume_port": watcher.RESOLUME_OSC_PORT,
            "music_root": str(watcher.MUSIC_ROOT),
            "artwork_output": str(artwork_module.OUTPUT_IMAGE),
            "fallback_artwork_path": str(artwork_module.FALLBACK_ARTWORK_IMAGE),
            "vinyl_logo_path": DEFAULT_VINYL_LOGO_PATH,
            "vinyl_track_text": DEFAULT_VINYL_TRACK_TEXT,
            "studio_artwork_path": DEFAULT_STUDIO_ARTWORK_PATH,
            "studio_track_text": DEFAULT_STUDIO_TRACK_TEXT,
            "output_pixels": DEFAULT_OUTPUT_PIXELS,
            "bpm_flip_bpm": "125",
            "bpm_flip_division": "1/4",
            "default_fallback_template": DEFAULT_TEMPLATE,
            "preset_keep_current_colors": False,
            "use_artwork_palette": False,
            "neutral_artwork_color": DEFAULT_NEUTRAL_ARTWORK_COLOR_NAME,
            "osc_addresses": {str(link): watcher.RESOLUME_LINK_OSC_ADDRESSES[link] for link in range(1, 9)},
            "link_labels": DEFAULT_LINK_LABELS,
            "blt_osc_outputs": DEFAULT_BLT_OSC_OUTPUTS,
            "performance_presets": PERFORMANCE_PRESETS,
            "mood_presets": MOOD_PRESETS,
            "energy_presets": ENERGY_PRESETS,
            "section_presets": SECTION_PRESETS,
        }
        config_source = CONFIG_PATH if CONFIG_PATH.exists() else LEGACY_CONFIG_PATH
        if config_source.exists():
            try:
                loaded = json.loads(config_source.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    config.update(loaded)
            except Exception:
                pass
        return config

    def save_config(self) -> None:
        self.config.update(
            {
                "blt_params_url": self.blt_url_var.get().strip(),
                "resolume_host": self.osc_host_var.get().strip(),
                "resolume_port": parse_int(self.osc_port_var.get(), watcher.RESOLUME_OSC_PORT, 1, 65535),
                "music_root": clean_path_text(self.music_root_var.get()),
                "artwork_output": clean_path_text(self.artwork_output_var.get()),
                "fallback_artwork_path": clean_path_text(self.fallback_artwork_path_var.get()) or str(artwork_module.FALLBACK_ARTWORK_IMAGE),
                "vinyl_logo_path": clean_path_text(self.vinyl_logo_path_var.get()) or DEFAULT_VINYL_LOGO_PATH,
                "vinyl_track_text": self.vinyl_track_text_var.get().strip() or DEFAULT_VINYL_TRACK_TEXT,
                "studio_artwork_path": clean_path_text(self.studio_artwork_path_var.get()) or DEFAULT_STUDIO_ARTWORK_PATH,
                "studio_track_text": self.studio_track_text_var.get().strip() or DEFAULT_STUDIO_TRACK_TEXT,
                "output_pixels": parse_int(self.output_size_var.get(), DEFAULT_OUTPUT_PIXELS, 64, 4096),
                "bpm_flip_bpm": self.bpm_flip_bpm_var.get().strip() or "125",
                "bpm_flip_division": normalize_bpm_swap_rate(self.bpm_flip_division_var.get()),
                "default_fallback_template": self.default_template_var.get().strip() or DEFAULT_TEMPLATE,
                "preset_keep_current_colors": not self.apply_preset_colors_var.get(),
                "use_artwork_palette": self.auto_artwork_palette_var.get(),
                "neutral_artwork_color": self.current_neutral_artwork_color(),
                "osc_addresses": self.current_osc_addresses(),
                "link_labels": self.current_link_labels(),
                "blt_osc_outputs": self.current_blt_osc_outputs(),
                "performance_presets": self.performance_presets,
                "mood_presets": self.mood_presets,
                "energy_presets": self.energy_presets,
                "section_presets": self.section_presets,
            }
        )
        try:
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.write_text(json.dumps(self.config, indent=2), encoding="utf-8")
            self.configure_runtime_modules()
            self.refresh_dynamic_link_labels()
            self.last_event_var.set("Saved performance GUI settings")
        except OSError as exc:
            messagebox.showerror("Could Not Save Settings", str(exc))

    def current_osc_addresses(self) -> dict[str, str]:
        return {
            str(link): self.clean_osc_address(self.osc_address_vars[link].get(), watcher.RESOLUME_LINK_OSC_ADDRESSES[link])
            for link in range(1, 9)
        }

    def current_link_labels(self) -> dict[str, str]:
        return {
            str(link): self.clean_link_label(self.link_label_vars[link].get(), DEFAULT_LINK_LABELS[str(link)])
            for link in range(1, 9)
        }

    def clean_link_label(self, raw_label: str, fallback: str) -> str:
        return str(raw_label or "").strip() or fallback

    def link_label(self, link: int, suffix: str = "") -> str:
        return f"{self.clean_link_label(self.link_label_vars[link].get(), DEFAULT_LINK_LABELS[str(link)])}{suffix}"

    def make_link_label_var(self, link: int, suffix: str = "") -> tk.StringVar:
        variable = tk.StringVar(value=self.link_label(link, suffix))
        self.dynamic_link_label_vars.append((variable, link, suffix))
        return variable

    def refresh_dynamic_link_labels(self) -> None:
        for variable, link, suffix in self.dynamic_link_label_vars:
            variable.set(self.link_label(link, suffix))

    def clean_osc_address(self, raw_address: str, fallback: str = "") -> str:
        address = str(raw_address or "").strip()
        if "=" in address:
            address = address.split("=", 1)[0].strip()
        for link in range(1, 9):
            address = address.replace(f"/Link{link}", f"/link{link}")
            address = address.replace(f"/LINK{link}", f"/link{link}")
        return address or fallback

    def current_neutral_artwork_color(self) -> str:
        selected = self.neutral_artwork_color_var.get().strip().casefold()
        if selected not in COLOR_HUE_VALUES:
            selected = DEFAULT_NEUTRAL_ARTWORK_COLOR_NAME
            self.neutral_artwork_color_var.set(selected)
        return selected

    def track_auto_key(self, track: dict[str, Any]) -> str:
        identity = {
            "title": track.get("title", ""),
            "artist": track.get("artist", ""),
            "album": track.get("album", ""),
            "player": track.get("player", ""),
            "player_number": track.get("player_number", ""),
        }
        return json.dumps(identity, sort_keys=True, ensure_ascii=False)

    def mark_manual_artwork_override(self, reason: str = "manual") -> None:
        if not self.current_track_auto_key:
            return
        self.manual_artwork_override_track_key = self.current_track_auto_key
        self.track_history_final_source = "manual"
        self.track_history_final_note = "Manual color changes during track"
        self.fallback_var.set("Manual until next track")
        self.last_event_var.set(f"Manual color change active until next track ({reason})")

    def normalize_blt_osc_outputs(self, outputs: Any) -> list[dict[str, Any]]:
        by_key = {str(item["key"]): dict(item) for item in DEFAULT_BLT_OSC_OUTPUTS}
        if isinstance(outputs, list):
            for item in outputs:
                if not isinstance(item, dict):
                    continue
                key = str(item.get("key") or "").strip()
                if not key:
                    continue
                base = by_key.get(key, {"key": key, "label": key, "field": "full_track", "address": "", "enabled": False})
                base.update(item)
                by_key[key] = base
        return list(by_key.values())

    def current_blt_osc_outputs(self) -> list[dict[str, Any]]:
        if not self.blt_osc_output_vars:
            return self.blt_osc_outputs
        outputs = []
        for output in self.blt_osc_outputs:
            key = output["key"]
            variables = self.blt_osc_output_vars.get(key)
            if not variables:
                outputs.append(dict(output))
                continue
            outputs.append(
                {
                    "key": key,
                    "label": variables["label"].get().strip() or key,
                    "field": variables["field"].get().strip() or "full_track",
                    "address": variables["address"].get().strip(),
                    "enabled": bool(variables["enabled"].get()),
                }
            )
        return outputs

    def save_blt_osc_outputs(self) -> None:
        self.blt_osc_outputs = self.current_blt_osc_outputs()
        self.save_config()
        self.last_event_var.set("Saved BLT OSC outputs")

    def get_osc_address(self, link: int) -> str:
        return self.current_osc_addresses()[str(link)]

    def save_osc_addresses(self) -> None:
        self.config["osc_addresses"] = self.current_osc_addresses()
        self.config["link_labels"] = self.current_link_labels()
        for link, address in self.config["osc_addresses"].items():
            self.osc_address_vars[int(link)].set(address)
        for link, label in self.config["link_labels"].items():
            self.link_label_vars[int(link)].set(label)
        self.save_config()
        self.refresh_dynamic_link_labels()
        self.refresh_osc_address_status()
        self.last_event_var.set("Saved OSC dashboard link labels and addresses")

    def refresh_osc_address_status(self) -> None:
        for link, variable in self.osc_vars.items():
            current = variable.get()
            variable.set(current if current and current != self.get_osc_address(link) else "-")

    def _build_ui(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Muted.TLabel", foreground="#555555")
        style.configure("Big.TButton", font=("Segoe UI", 10, "bold"), padding=(8, 5))
        style.configure("Safe.TButton", font=("Segoe UI", 11, "bold"), padding=(10, 7))
        style.configure("TButton", padding=(7, 4))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        header = ttk.Frame(self.root, padding=(16, 12, 16, 8))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="NT Performance Hub - Legacy Desktop GUI", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        self.status_badge = tk.Label(header, textvariable=self.status_var, font=("Segoe UI", 11, "bold"), padx=12, pady=4, bg="#666666", fg="white")
        self.status_badge.grid(row=0, column=1, sticky="e")
        ttk.Label(header, textvariable=self.last_event_var, style="Muted.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 0))
        ttk.Label(header, textvariable=self.blt_status_var, style="Muted.TLabel").grid(row=2, column=0, columnspan=2, sticky="w", pady=(2, 0))

        tabs = ttk.Notebook(self.root)
        tabs.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

        self.performance_tab = ttk.Frame(tabs, padding=10)
        self.presets_tab = ttk.Frame(tabs, padding=10)
        self.track_tab = ttk.Frame(tabs, padding=10)
        self.settings_tab = ttk.Frame(tabs, padding=10)
        self.command_tab = ttk.Frame(tabs, padding=10)
        for tab in (self.performance_tab, self.presets_tab, self.track_tab, self.settings_tab, self.command_tab):
            tab.columnconfigure(0, weight=1)
        tabs.add(self.performance_tab, text="Performance")
        tabs.add(self.presets_tab, text="Presets")
        tabs.add(self.track_tab, text="Track / Metadata")
        tabs.add(self.settings_tab, text="Settings / OSC")
        tabs.add(self.command_tab, text="Command Output")

        self._build_performance_tab()
        self._build_presets_tab()
        self._build_track_tab()
        self._build_settings_tab()
        self._build_command_output_tab()

    def _create_choice_button_strip(
        self,
        parent: ttk.Frame,
        group_key: str,
        variable: tk.StringVar,
        values: tuple[str, ...],
        callback: Any,
    ) -> None:
        buttons: dict[str, tk.Button] = {}
        for col, value in enumerate(values):
            button = tk.Button(
                parent,
                text=value,
                height=1,
                relief="raised",
                bd=1,
                padx=4,
                pady=1,
                command=lambda current=value: self._select_choice_button(group_key, variable, current, callback),
            )
            button.grid(row=0, column=col, sticky="ew", padx=2, pady=1)
            parent.columnconfigure(col, weight=1)
            buttons[value] = button
        self.choice_button_groups[group_key] = buttons
        self._refresh_choice_button_group(group_key, variable.get())

    def _select_choice_button(self, group_key: str, variable: tk.StringVar, value: str, callback: Any) -> None:
        variable.set(value)
        self._refresh_choice_button_group(group_key, value)
        callback()

    def _refresh_choice_button_group(self, group_key: str, selected_value: str) -> None:
        for value, button in self.choice_button_groups.get(group_key, {}).items():
            selected = value == selected_value
            self._configure_selected_button(button, selected)
            button.configure(
                text=f"{SELECTED_BUTTON_PREFIX}{value}" if selected else value,
            )

    def _configure_selected_button(self, button: tk.Button, selected: bool) -> None:
        button.configure(
            relief="solid" if selected else "raised",
            bd=2 if selected else 1,
            highlightthickness=1 if selected else 0,
            highlightbackground="#ffffff" if selected else button.cget("bg"),
            highlightcolor="#ffffff" if selected else button.cget("bg"),
        )

    def _create_toggle_button(
        self,
        parent: ttk.Frame,
        key: str,
        label: str,
        variable: tk.BooleanVar,
        command: Any,
    ) -> tk.Button:
        button = tk.Button(
            parent,
            height=1,
            bd=1,
            padx=8,
            pady=1,
            command=lambda: self._toggle_boolean_button(key, variable, command),
        )
        self.toggle_buttons[key] = button
        self._refresh_toggle_button(key, label, variable.get())
        return button

    def _toggle_boolean_button(self, key: str, variable: tk.BooleanVar, command: Any) -> None:
        variable.set(not variable.get())
        command()
        self._refresh_toggle_button(key, self._toggle_button_label(key), variable.get())

    def _toggle_button_label(self, key: str) -> str:
        labels = {
            "apply_preset_colors": "Apply Preset Colors",
            "auto_artwork_palette": "Auto Artwork",
        }
        return labels.get(key, key.replace("_", " ").title())

    def _refresh_toggle_button(self, key: str, label: str, enabled: bool) -> None:
        button = self.toggle_buttons.get(key)
        if button is None:
            return
        button.configure(
            text=f"{label}: {'ON' if enabled else 'OFF'}",
            bg="#245f35" if enabled else "#eeeeee",
            fg="#ffffff" if enabled else "#222222",
            activebackground="#2f7a45" if enabled else "#dddddd",
            activeforeground="#ffffff" if enabled else "#222222",
            relief="solid" if enabled else "raised",
        )

    def _create_scrollable_frame(self, parent: ttk.Frame, row: int, column: int = 0, pady: Any = 0) -> ttk.Frame:
        parent.rowconfigure(row, weight=1)
        parent.columnconfigure(column, weight=1)
        canvas = tk.Canvas(parent, highlightthickness=0, takefocus=1)
        canvas.grid(row=row, column=column, sticky="nsew", pady=pady)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=row, column=column + 1, sticky="ns", pady=pady)
        canvas.configure(yscrollcommand=scrollbar.set)

        content = ttk.Frame(canvas)
        content.columnconfigure(0, weight=1)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        def update_scroll_region(_event: tk.Event) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))

        def update_width(event: tk.Event) -> None:
            canvas.itemconfigure(window_id, width=event.width)

        def on_mousewheel(event: tk.Event) -> None:
            if event.delta == 0:
                return
            units = -1 if event.delta > 0 else 1
            if abs(event.delta) >= 120:
                units = int(-1 * (event.delta / 120))
            canvas.yview_scroll(units, "units")

        def on_page_up(_event: tk.Event) -> None:
            canvas.yview_scroll(-1, "pages")

        def on_page_down(_event: tk.Event) -> None:
            canvas.yview_scroll(1, "pages")

        def on_home(_event: tk.Event) -> None:
            canvas.yview_moveto(0.0)

        def on_end(_event: tk.Event) -> None:
            canvas.yview_moveto(1.0)

        content.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", update_width)
        canvas.bind("<MouseWheel>", on_mousewheel)
        content.bind("<MouseWheel>", on_mousewheel)
        canvas.bind(
            "<Enter>",
            lambda _event: (
                canvas.focus_set(),
                canvas.bind_all("<MouseWheel>", on_mousewheel),
            ),
        )
        canvas.bind("<Leave>", lambda _event: canvas.unbind_all("<MouseWheel>"))
        canvas.bind("<Prior>", on_page_up)
        canvas.bind("<Next>", on_page_down)
        canvas.bind("<Home>", on_home)
        canvas.bind("<End>", on_end)
        return content

    def _build_performance_tab(self) -> None:
        content = self._create_scrollable_frame(self.performance_tab, 0)

        presets = ttk.LabelFrame(content, text="Performance Preset Buttons", padding=6)
        presets.grid(row=0, column=0, sticky="ew")
        self.performance_preset_frame = presets
        self._build_performance_preset_buttons(presets)

        self._build_performance_palette_panel(content, 1)
        self._build_vinyl_mode_panel(content, 2)

        color_tools = ttk.LabelFrame(content, text="Color Relationships", padding=6)
        color_tools.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        color_actions: tuple[tuple[str, Any], ...] = (
            (f"Swap {self.link_label(1)} / {self.link_label(2)}", self.swap_primary_secondary),
            *(
                (label, lambda current_offset=offset: self.apply_color_relationship(current_offset))
                for label, offset in (
                    ("Make Complement", 0.500),
                    ("Make Analogous", 0.083),
                    ("Make Triad", 0.333),
                    ("Split Complement A", 0.416),
                    ("Split Complement B", 0.583),
                )
            ),
        )
        for index, (label, command) in enumerate(color_actions):
            color_tools.columnconfigure(index, weight=1)
            ttk.Button(color_tools, text=label, command=command).grid(row=0, column=index, sticky="ew", padx=2)
        self._build_bpm_flip_panel(color_tools, 1, len(color_actions))

        self._build_output_strip(content, 4)

        controls = ttk.LabelFrame(content, text="8-Link Dashboard Controls", padding=6)
        controls.grid(row=5, column=0, sticky="ew", pady=(6, 0))
        controls.columnconfigure(2, weight=1)
        self._build_link_controls(controls)

        ttk.Button(content, text="SAFE LIGHT LOOK / RESET LIGHT CLIP", style="Safe.TButton", command=self.safe_reset).grid(row=6, column=0, sticky="ew", pady=(8, 0))

    def _build_bpm_flip_panel(self, parent: ttk.Frame, row: int, columnspan: int) -> None:
        panel = ttk.Frame(parent)
        panel.grid(row=row, column=0, columnspan=columnspan, sticky="ew", pady=(6, 0))
        for col in range(8):
            panel.columnconfigure(col, weight=1 if col == 7 else 0)

        ttk.Label(panel, text="Auto Swap").grid(row=0, column=0, sticky="w", padx=(4, 10))
        ttk.Label(panel, text="BPM").grid(row=0, column=1, sticky="w", padx=(0, 4))
        bpm_entry = ttk.Entry(panel, textvariable=self.bpm_flip_bpm_var, width=8)
        bpm_entry.grid(row=0, column=2, sticky="w", padx=(0, 8))
        bpm_entry.bind("<Return>", lambda _event: self.update_bpm_flip_status())
        ttk.Button(panel, text="Use Track BPM", command=self.use_latest_track_bpm).grid(row=0, column=3, sticky="w", padx=(0, 12))
        ttk.Button(panel, text="Start", command=self.trigger_bpm_flip).grid(row=0, column=4, sticky="ew", padx=(0, 4))
        self.bpm_flip_trigger_button = ttk.Button(panel, text="Stop", command=self.stop_bpm_flip, state="disabled")
        self.bpm_flip_trigger_button.grid(row=0, column=5, sticky="ew", padx=(4, 12))

        division_frame = ttk.Frame(panel)
        division_frame.grid(row=0, column=7, sticky="ew")
        division_frame.columnconfigure(0, weight=1)
        fast_frame = ttk.Frame(division_frame)
        fast_frame.grid(row=0, column=0, sticky="ew")
        bar_frame = ttk.Frame(division_frame)
        bar_frame.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        fast_rates = ("1/64", "1/32", "1/16", "1/8", "1/4")
        bar_rates = ("1/2 bar", "1 bar", "2 bars", "4 bars", "8 bars", "16 bars")
        self._create_choice_button_strip(
            fast_frame,
            "bpm_flip_division_fast",
            self.bpm_flip_division_var,
            fast_rates,
            self.on_bpm_flip_division_changed,
        )
        self._create_choice_button_strip(
            bar_frame,
            "bpm_flip_division_bars",
            self.bpm_flip_division_var,
            bar_rates,
            self.on_bpm_flip_division_changed,
        )

        ttk.Label(panel, textvariable=self.bpm_flip_status_var, style="Muted.TLabel").grid(row=1, column=0, columnspan=8, sticky="w", padx=4, pady=(3, 0))

    def _build_performance_preset_buttons(self, parent: ttk.Frame) -> None:
        for child in parent.winfo_children():
            child.destroy()
        parent.columnconfigure(0, weight=1)
        options = ttk.Frame(parent)
        options.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        preset_toggle = self._create_toggle_button(
            options,
            "apply_preset_colors",
            "Apply Preset Colors",
            variable=self.apply_preset_colors_var,
            command=self.on_apply_preset_colors_changed,
        )
        preset_toggle.grid(row=0, column=0, sticky="w")
        ttk.Label(options, text="OFF keeps current colors when preset changes", style="Muted.TLabel").grid(row=0, column=1, sticky="w", padx=(8, 0))
        button_grid = ttk.Frame(parent)
        button_grid.grid(row=1, column=0, sticky="ew")
        for col in range(5):
            button_grid.columnconfigure(col, weight=1)
        for index, name in enumerate(self.performance_presets):
            button = ttk.Button(
                button_grid,
                text=str(name),
                style="Big.TButton",
                command=lambda current_name=name: self.apply_named_preset("performance", current_name),
            )
            button.grid(row=index // 5, column=index % 5, sticky="ew", padx=3, pady=2)

    def _build_performance_palette_panel(self, parent: ttk.Frame, row: int) -> None:
        panel = ttk.LabelFrame(parent, text="Album Artwork Color Matcher", padding=6)
        panel.grid(row=row, column=0, sticky="ew", pady=(6, 0))
        panel.columnconfigure(0, weight=0)
        panel.columnconfigure(1, weight=1)
        controls = ttk.Frame(panel)
        controls.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        ttk.Button(controls, text="Extract Current Artwork", command=self.extract_palette_from_current_artwork).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(controls, text="Apply Palette to Links 1 / 2 / 4", command=self.force_apply_artwork_palette).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(controls, text="Copy Color Comment", command=self.copy_template).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(controls, text="Use Current Colors", command=self.update_template_from_state).grid(row=0, column=3, padx=(0, 5))
        auto_artwork_toggle = self._create_toggle_button(
            controls,
            "auto_artwork_palette",
            "Auto Artwork",
            variable=self.auto_artwork_palette_var,
            command=self.on_auto_artwork_palette_changed,
        )
        auto_artwork_toggle.grid(row=0, column=4, padx=(0, 8))
        ttk.Label(controls, text="Neutral").grid(row=0, column=5, padx=(0, 4))
        neutral_combo = ttk.Combobox(
            controls,
            textvariable=self.neutral_artwork_color_var,
            values=SORTED_COLOR_NAMES,
            state="readonly",
            width=10,
        )
        neutral_combo.grid(row=0, column=6, padx=(0, 8))
        neutral_combo.bind("<<ComboboxSelected>>", lambda _event: self.on_neutral_artwork_color_changed())
        ttk.Button(controls, text="Open Artwork Folder", command=self.open_artwork_folder).grid(row=0, column=7, padx=(0, 5))
        ttk.Button(controls, text="Open Track Folder", command=self.open_track_folder).grid(row=0, column=8)

        preview_frame = ttk.Frame(panel)
        preview_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview = ttk.Label(preview_frame, text="Artwork appears after first save", anchor="center")
        preview.grid(row=0, column=0, sticky="nsew")
        self.artwork_preview_labels.append(preview)
        ttk.Label(preview_frame, textvariable=self.artwork_status_var, style="Muted.TLabel", anchor="center").grid(row=1, column=0, sticky="ew", pady=(3, 0))

        swatches = ttk.Frame(panel)
        swatches.grid(row=1, column=1, sticky="ew")
        for col in range(3):
            swatches.columnconfigure(col, weight=1)
        for col, key in enumerate(("dominant", "accent", "bright_accent")):
            self._add_palette_action_card(swatches, col, key)

        comment = ttk.Frame(panel)
        comment.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        comment.columnconfigure(0, weight=1)
        ttk.Entry(comment, textvariable=self.template_var).grid(row=0, column=0, sticky="ew")

    def _build_vinyl_mode_panel(self, parent: ttk.Frame, row: int) -> None:
        panel = ttk.LabelFrame(parent, text="Manual Artwork Modes", padding=6)
        panel.grid(row=row, column=0, sticky="ew", pady=(6, 0))
        panel.columnconfigure(3, weight=1)
        panel.columnconfigure(5, weight=2)
        ttk.Button(panel, text="Start Vinyl / Show Logo", command=self.enter_vinyl_mode).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(panel, text="Resume CDJ Artwork", command=self.exit_vinyl_mode).grid(row=0, column=1, padx=(0, 8))
        ttk.Label(panel, text="Track Text").grid(row=0, column=2, sticky="e", padx=(0, 4))
        ttk.Entry(panel, textvariable=self.vinyl_track_text_var, width=22).grid(row=0, column=3, sticky="ew", padx=(0, 12))
        ttk.Label(panel, text="Logo").grid(row=0, column=4, sticky="e", padx=(0, 4))
        ttk.Entry(panel, textvariable=self.vinyl_logo_path_var).grid(row=0, column=5, sticky="ew")
        ttk.Button(panel, text="NO TALKING STUDIO", command=self.enter_studio_mode).grid(row=1, column=0, padx=(0, 5), pady=(5, 0))
        ttk.Label(panel, text="Track Text").grid(row=1, column=2, sticky="e", padx=(0, 4), pady=(5, 0))
        ttk.Entry(panel, textvariable=self.studio_track_text_var, width=22).grid(row=1, column=3, sticky="ew", padx=(0, 12), pady=(5, 0))
        ttk.Label(panel, text="Artwork").grid(row=1, column=4, sticky="e", padx=(0, 4), pady=(5, 0))
        ttk.Entry(panel, textvariable=self.studio_artwork_path_var).grid(row=1, column=5, sticky="ew", pady=(5, 0))

    def _add_palette_action_card(self, parent: ttk.Frame, col: int, key: str) -> None:
        card = ttk.Frame(parent)
        card.grid(row=0, column=col, sticky="ew", padx=4)
        card.columnconfigure(0, weight=1)
        self._add_palette_swatch(card, 0, key)
        actions = ttk.Frame(card)
        actions.grid(row=3, column=0, sticky="ew", padx=1, pady=(1, 0))
        for action_col in range(3):
            actions.columnconfigure(action_col, weight=1)
        ttk.Button(actions, text="Link 1", command=lambda: self.apply_palette_color_to_control(key, "color1")).grid(row=0, column=0, sticky="ew", padx=1)
        ttk.Button(actions, text="Link 2", command=lambda: self.apply_palette_color_to_control(key, "color2")).grid(row=0, column=1, sticky="ew", padx=1)
        ttk.Button(actions, text="Link 4", command=lambda: self.apply_palette_color_to_control(key, "strobe_color")).grid(row=0, column=2, sticky="ew", padx=1)

    def _build_output_strip(self, parent: ttk.Frame, row: int) -> None:
        strip = ttk.LabelFrame(parent, text="Current Output", padding=6)
        strip.grid(row=row, column=0, sticky="ew")
        for col in range(9):
            strip.columnconfigure(col, weight=1)
        labels = ["color1", "color2", "strobe", "strobe_color", "saturation", "brightness", "motion", "fx", "pulse"]
        for col, key in enumerate(labels):
            link = CONTROL_TO_DISPLAY_LINK[key]
            suffix = " %" if key == "strobe" else ""
            ttk.Label(strip, textvariable=self.make_link_label_var(link, suffix), style="Muted.TLabel").grid(row=0, column=col, sticky="w", padx=4)
            var = tk.StringVar(value="-")
            self.output_vars[key] = var
            ttk.Label(strip, textvariable=var, font=("Segoe UI", 10, "bold")).grid(row=1, column=col, sticky="w", padx=4)
            if key in {"color1", "color2", "strobe_color"}:
                chip = tk.Canvas(strip, width=34, height=12, highlightthickness=1, highlightbackground="#777777")
                chip.grid(row=2, column=col, sticky="w", padx=4, pady=(4, 0))
                self.output_color_canvases[key] = chip
        self.gradient_canvas = tk.Canvas(strip, width=180, height=12, highlightthickness=1, highlightbackground="#999999")
        self.gradient_canvas.grid(row=2, column=3, columnspan=2, sticky="w", padx=4, pady=(4, 0))
        self.gradient_canvas.bind("<Configure>", lambda _event: self.refresh_output_strip())

    def _build_link_controls(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Link").grid(row=0, column=0, sticky="w")
        ttk.Label(parent, text="Control").grid(row=0, column=1, sticky="w")
        ttk.Label(parent, text="Value").grid(row=0, column=2, sticky="ew")
        ttk.Label(parent, text="Actions").grid(row=0, column=3, sticky="w")
        for row, (link, _label, key, kind) in enumerate(LINK_CONTROL_SPECS, start=1):
            ttk.Label(parent, text=f"Link {link}").grid(row=row, column=0, sticky="w", pady=4)
            ttk.Label(parent, textvariable=self.make_link_label_var(link)).grid(row=row, column=1, sticky="w", padx=(8, 10), pady=4)
            if kind == "color":
                default_color = {"color1": "indigo", "color2": "magenta", "strobe_color": "purple"}[key]
                var = tk.StringVar(value=default_color)
                self.control_vars[key] = var
                color_frame = ttk.Frame(parent)
                color_frame.grid(row=row, column=2, sticky="ew", padx=(0, 34), pady=4)
                self._create_color_button_strip(
                    color_frame,
                    key,
                    var,
                    lambda current_key=key: self.on_manual_control_changed(current_key),
                )
                swatch = tk.Canvas(parent, width=18, height=18, highlightthickness=1, highlightbackground="#999999")
                swatch.grid(row=row, column=2, sticky="e", padx=(0, 8))
                self.visual_swatches[key] = swatch
            elif kind in {"percent_buttons", "strobe_buttons"}:
                values = [0, 10, 25, 50, 75, 90, 95] if key == "motion" or kind == "strobe_buttons" else [0, 10, 25, 50, 75, 90, 100]
                var = tk.IntVar(value=0)
                self.control_vars[key] = var
                value_frame = ttk.Frame(parent)
                value_frame.grid(row=row, column=2, sticky="ew", pady=4)
                value_frame.columnconfigure(0, weight=1)
                self._create_percent_button_strip(
                    value_frame,
                    key,
                    var,
                    values,
                    lambda current_key=key: self.on_manual_control_changed(current_key),
                )
                readout = tk.StringVar(value="Current: 0% / 0.000")
                self.control_readout_vars[key] = readout
                ttk.Label(value_frame, textvariable=readout, style="Muted.TLabel").grid(row=0, column=1, sticky="e", padx=(10, 0))
            actions = ttk.Frame(parent)
            actions.grid(row=row, column=3, sticky="w", pady=4)
            ttk.Button(actions, text="Send", command=lambda current=key: self.send_one_control(current)).grid(row=0, column=0, padx=2)
            ttk.Button(actions, text="Resend", command=lambda current=key: self.resend_one_control(current)).grid(row=0, column=1, padx=2)
            ttk.Button(actions, text="Reset", command=lambda current=key: self.reset_one_control(current)).grid(row=0, column=2, padx=2)

    def _build_presets_tab(self) -> None:
        self.presets_tab.rowconfigure(0, weight=1)
        notebook = ttk.Notebook(self.presets_tab)
        notebook.grid(row=0, column=0, sticky="nsew")
        self._build_preset_editor_page(notebook, "Performance Presets", "performance", self.performance_presets)
        self._build_preset_editor_page(notebook, "Mood Presets", "mood", self.mood_presets)
        self._build_preset_editor_page(notebook, "Energy Presets", "energy", self.energy_presets)
        self._build_preset_editor_page(notebook, "Section Presets", "section", self.section_presets)

    def _build_preset_editor_page(
        self,
        notebook: ttk.Notebook,
        title: str,
        group: str,
        presets: dict[str, dict[str, Any]],
    ) -> None:
        page = ttk.Frame(notebook, padding=8)
        page.columnconfigure(0, weight=1)
        page.rowconfigure(0, weight=1)
        canvas = tk.Canvas(page, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(page, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)
        inner = ttk.Frame(canvas)
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def update_scroll_region(_event: tk.Event) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))

        def update_width(event: tk.Event) -> None:
            canvas.itemconfigure(window_id, width=event.width)

        inner.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", update_width)
        canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        inner.columnconfigure(0, weight=1)

        top = ttk.Frame(inner)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top.columnconfigure(0, weight=1)
        ttk.Label(top, text=f"Edit names and dashboard values. Save writes them to the app config.", style="Muted.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(top, text="Save All Presets", command=lambda current=group: self.save_preset_editor(current)).grid(row=0, column=1, sticky="e")

        table = ttk.Frame(inner)
        table.grid(row=1, column=0, sticky="ew")
        column_weights = (2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2)
        for col, weight in enumerate(column_weights):
            table.columnconfigure(col, weight=weight)
        ttk.Label(table, text="Preset", style="Muted.TLabel").grid(row=0, column=0, sticky="w", padx=3, pady=(0, 4))
        for col, (_key, link, suffix) in enumerate(PRESET_CONTROL_COLUMNS, start=1):
            ttk.Label(table, textvariable=self.make_link_label_var(link, suffix), style="Muted.TLabel").grid(row=0, column=col, sticky="w", padx=3, pady=(0, 4))
        ttk.Label(table, text="Actions", style="Muted.TLabel").grid(row=0, column=10, sticky="w", padx=3, pady=(0, 4))

        self.preset_editors[group] = {}
        for row, (name, values) in enumerate(presets.items(), start=1):
            self._add_preset_row(table, row, group, name, values)

        notebook.add(page, text=title)

    def _add_preset_row(
        self,
        parent: ttk.Frame,
        row: int,
        group: str,
        name: str,
        values: dict[str, Any],
    ) -> None:
        editor: dict[str, Any] = {}
        self.preset_editors[group][name] = editor

        defaults = self.default_preset_values()
        name_var = tk.StringVar(value=str(name))
        editor["NAME"] = name_var
        ttk.Entry(parent, textvariable=name_var, width=18).grid(row=row, column=0, sticky="ew", padx=3, pady=3)

        color_choices = [""] + SORTED_COLOR_NAMES
        for col, key in enumerate(("PRIMARY", "SECONDARY", "STROBE"), start=1):
            var = tk.StringVar(value=str(values.get(key, "")).casefold())
            editor[key] = var
            cell = ttk.Frame(parent)
            cell.grid(row=row, column=col, sticky="ew", padx=3, pady=3)
            cell.columnconfigure(0, weight=1)
            combo = ttk.Combobox(cell, textvariable=var, values=color_choices, state="readonly", width=10)
            combo.grid(row=0, column=0, sticky="ew")
            swatch = tk.Canvas(cell, width=18, height=18, highlightthickness=1, highlightbackground="#777777")
            swatch.grid(row=0, column=1, sticky="e", padx=(4, 0))
            editor[f"{key}_SWATCH"] = swatch
            combo.bind("<<ComboboxSelected>>", lambda _event, current_group=group, current_name=name, current_key=key: self.refresh_preset_color_swatch(current_group, current_name, current_key))
            swatch.bind("<Configure>", lambda _event, current_group=group, current_name=name, current_key=key: self.refresh_preset_color_swatch(current_group, current_name, current_key))
            self.refresh_preset_color_swatch(group, name, key)

        numeric_fields = (
            ("MOTION", [0, 10, 25, 50, 75, 90, 95]),
            ("STROBE_PERCENT", [0, 10, 25, 50, 75, 90, 95]),
            ("SATURATION", [0, 10, 25, 50, 75, 90, 100]),
            ("BRIGHTNESS", [0, 10, 25, 50, 75, 90, 100]),
            ("FX", [0, 10, 25, 50, 75, 90, 100]),
            ("PULSE", [0, 10, 25, 50, 75, 90, 100]),
        )
        for col, (key, allowed) in enumerate(numeric_fields, start=4):
            default_value = defaults[key]
            var = tk.StringVar(value=str(parse_percent(values.get(key, default_value), parse_percent(default_value))))
            editor[key] = var
            combo = ttk.Combobox(parent, textvariable=var, values=[str(value) for value in allowed], state="readonly", width=6)
            combo.grid(row=row, column=col, sticky="ew", padx=3, pady=3)

        actions = ttk.Frame(parent)
        actions.grid(row=row, column=10, sticky="ew", padx=3, pady=3)
        for col in range(4):
            actions.columnconfigure(col, weight=1)
        ttk.Button(actions, text="Apply", command=lambda: self.apply_preset_from_editor(group, name)).grid(row=0, column=0, sticky="ew", padx=1)
        ttk.Button(actions, text="Save", command=lambda: self.save_preset_editor(group)).grid(row=0, column=1, sticky="ew", padx=1)
        ttk.Button(actions, text="Copy", command=lambda: self.copy_preset_tag(group, name)).grid(row=0, column=2, sticky="ew", padx=1)
        ttk.Button(actions, text="Reset", command=lambda: self.reset_preset_editor(group, name)).grid(row=0, column=3, sticky="ew", padx=1)

    def _create_color_button_strip(
        self,
        parent: ttk.Frame,
        group_key: str,
        variable: tk.StringVar,
        callback: Any,
        include_none: bool = False,
    ) -> None:
        buttons: dict[str, tk.Button] = {}
        values = [""] if include_none else []
        values.extend(SORTED_COLOR_NAMES)
        for col, color_name in enumerate(values):
            label = "No change" if color_name == "" else color_name
            bg = "#eeeeee" if color_name == "" else COLOR_HEX[color_name]
            fg = "#111111" if color_name == "" else self._button_text_for_color(color_name)
            button = tk.Button(
                parent,
                text=label,
                width=7 if color_name else 9,
                height=1,
                relief="raised",
                bd=1,
                padx=2,
                pady=1,
                bg=bg,
                fg=fg,
                command=lambda current=color_name: self._select_color_button(group_key, variable, current, callback),
            )
            button.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
            parent.columnconfigure(col, weight=1)
            buttons[color_name] = button
        self.color_button_groups[group_key] = buttons
        self._refresh_color_button_group(group_key, variable.get())

    def _select_color_button(self, group_key: str, variable: tk.StringVar, color_name: str, callback: Any) -> None:
        variable.set(color_name)
        self._refresh_color_button_group(group_key, color_name)
        callback()

    def _refresh_color_button_group(self, group_key: str, selected_color: str) -> None:
        buttons = self.color_button_groups.get(group_key, {})
        for color_name, button in buttons.items():
            selected = color_name == selected_color
            label = color_name or "No change"
            text = f"{SELECTED_BUTTON_PREFIX}{label}" if selected else label
            self._configure_selected_button(button, selected)
            button.configure(text=text)

    def _button_text_for_color(self, color_name: str) -> str:
        return "#111111" if color_name in {"amber", "yellow", "lime", "cyan", "pink"} else "#ffffff"

    def _create_percent_button_strip(
        self,
        parent: ttk.Frame,
        group_key: str,
        variable: tk.IntVar,
        values: list[int],
        callback: Any,
    ) -> None:
        buttons: dict[int, tk.Button] = {}
        strip = ttk.Frame(parent)
        strip.grid(row=0, column=0, sticky="ew")
        for col, percent in enumerate(values):
            button = tk.Button(
                strip,
                text=self._percent_button_text(percent, selected=False),
                width=6,
                height=1,
                relief="raised",
                bd=1,
                padx=2,
                pady=1,
                bg=self._percent_button_bg(group_key, percent),
                fg=self._percent_button_fg(group_key, percent),
                command=lambda current=percent: self._select_percent_button(group_key, variable, current, callback),
            )
            button.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
            strip.columnconfigure(col, weight=1)
            buttons[percent] = button
        self.percent_button_groups[group_key] = buttons
        self.percent_button_values[group_key] = list(values)
        self._refresh_percent_button_group(group_key, variable.get())

    def _select_percent_button(self, group_key: str, variable: tk.IntVar, percent: int, callback: Any) -> None:
        variable.set(percent)
        self._refresh_percent_button_group(group_key, percent)
        callback()

    def _refresh_percent_button_group(self, group_key: str, selected_percent: Any) -> None:
        buttons = self.percent_button_groups.get(group_key, {})
        values = self.percent_button_values.get(group_key, list(buttons))
        if not buttons or not values:
            return
        selected_choice = nearest_percent_choice(selected_percent, values)
        for percent, button in buttons.items():
            selected = percent == selected_choice
            self._configure_selected_button(button, selected)
            button.configure(text=self._percent_button_text(percent, selected))

    def _percent_button_text(self, percent: int, selected: bool) -> str:
        label = f"{SELECTED_BUTTON_PREFIX}{percent}" if selected else str(percent)
        return f"{label} / {percent_to_value(percent):.2f}"

    def _percent_button_bg(self, group_key: str, percent: int) -> str:
        if group_key == "strobe":
            if percent == 0:
                return "#252525"
            if percent <= 25:
                return "#6b6b6b"
            if percent <= 75:
                return "#b8a15a"
            return "#d48a3a"
        level = int(45 + (percent / 100) * 165)
        return f"#{level:02x}{level:02x}{level:02x}"

    def _percent_button_fg(self, group_key: str, percent: int) -> str:
        if group_key == "strobe":
            return "#ffffff" if percent <= 50 else "#111111"
        return "#ffffff" if percent < 65 else "#111111"

    def default_preset_values(self) -> dict[str, Any]:
        return {
            "PRIMARY": self.state.color1_name,
            "SECONDARY": self.state.color2_name,
            "STROBE": self.state.strobe_color_name,
            "STROBE_PERCENT": self.state.strobe_percent,
            "SATURATION": self.state.saturation_percent,
            "BRIGHTNESS": self.state.brightness_percent,
            "MOTION": round(self.state.motion_value * 100),
            "FX": round(self.state.fx_value * 100),
            "PULSE": round(self.state.pulse_value * 100),
        }

    def _current_preset_values(self, group: str, name: str) -> dict[str, Any]:
        editor = self.preset_editors[group][name]
        values: dict[str, Any] = {}
        for key, variable in editor.items():
            if key == "NAME" or key.endswith("_SWATCH"):
                continue
            raw_value = variable.get()
            if key in {"PRIMARY", "SECONDARY", "STROBE"}:
                if str(raw_value).strip():
                    values[key] = str(raw_value).strip().casefold()
            else:
                values[key] = parse_percent(raw_value)
        return values

    def _current_preset_name(self, group: str, name: str) -> str:
        editor = self.preset_editors[group][name]
        variable = editor.get("NAME")
        if not variable:
            return name
        return str(variable.get()).strip() or name

    def refresh_preset_color_swatch(self, group: str, name: str, key: str) -> None:
        editor = self.preset_editors.get(group, {}).get(name, {})
        variable = editor.get(key)
        canvas = editor.get(f"{key}_SWATCH")
        if not variable or not canvas:
            return
        color_name = str(variable.get()).strip().casefold()
        fill = COLOR_HEX.get(color_name, "#eeeeee")
        canvas.delete("all")
        canvas.create_rectangle(
            1,
            1,
            max(canvas.winfo_width(), 18) - 1,
            max(canvas.winfo_height(), 18) - 1,
            fill=fill,
            outline="#333333",
        )

    def preset_dict_for_group(self, group: str) -> dict[str, dict[str, Any]]:
        if group == "performance":
            return self.performance_presets
        if group == "mood":
            return self.mood_presets
        if group == "energy":
            return self.energy_presets
        return self.section_presets

    def set_preset_dict_for_group(self, group: str, data: dict[str, dict[str, Any]]) -> None:
        if group == "performance":
            self.performance_presets = data
        elif group == "mood":
            self.mood_presets = data
        elif group == "energy":
            self.energy_presets = data
        else:
            self.section_presets = data

    def apply_preset_from_editor(self, group: str, name: str) -> None:
        values = self._current_preset_values(group, name)
        preset_name = self._current_preset_name(group, name)
        self.apply_preset_values(group, preset_name, values)

    def apply_named_preset(self, group: str, name: str) -> None:
        values = self.preset_dict_for_group(group).get(name)
        if values is None:
            return
        self.apply_preset_values(group, name, values)

    def apply_preset_values(self, group: str, name: str, values: dict[str, Any]) -> None:
        if self.apply_preset_colors_var.get() and {"PRIMARY", "SECONDARY", "STROBE"}.intersection(values):
            self.mark_manual_artwork_override(f"{name} preset")
        state = self.state.clone()
        current_colors = (
            state.color1_name,
            state.color1_value,
            state.color2_name,
            state.color2_value,
            state.strobe_color_name,
            state.strobe_color_value,
        )
        apply_values_to_state(state, values, exact=True)
        if not self.apply_preset_colors_var.get():
            (
                state.color1_name,
                state.color1_value,
                state.color2_name,
                state.color2_value,
                state.strobe_color_name,
                state.strobe_color_value,
            ) = current_colors
        state.source = f"{group}:{name}"
        self.sync_strobe_value(state)
        self.apply_state(state, "preset", send=True)
        if not self.apply_preset_colors_var.get():
            self.last_event_var.set(f"Applied {name} preset energy with current colors")

    def on_apply_preset_colors_changed(self) -> None:
        self.save_config()
        self._refresh_toggle_button("apply_preset_colors", "Apply Preset Colors", self.apply_preset_colors_var.get())
        mode = "apply full color looks" if self.apply_preset_colors_var.get() else "keep current colors"
        self.last_event_var.set(f"Preset buttons now {mode}")

    def on_auto_artwork_palette_changed(self) -> None:
        self.save_config()
        self._refresh_toggle_button("auto_artwork_palette", "Auto Artwork", self.auto_artwork_palette_var.get())
        if self.auto_artwork_palette_var.get():
            self.last_event_var.set("Auto artwork colors enabled for tracks without MP3 color comments")
        else:
            self.last_event_var.set("Auto artwork colors off; artwork colors are manual")

    def on_neutral_artwork_color_changed(self) -> None:
        selected = self.current_neutral_artwork_color()
        self.save_config()
        self.last_event_var.set(f"Neutral artwork fallback set to {selected}")

    def copy_preset_tag(self, group: str, name: str) -> None:
        preset_name = self._current_preset_name(group, name)
        tag = self.template_from_state(
            self.state_from_preset_values(self._current_preset_values(group, name), source=f"{group}:{preset_name}")
        )
        self.root.clipboard_clear()
        self.root.clipboard_append(tag)
        self.last_event_var.set(f"Copied color comment for {preset_name} to clipboard")

    def state_from_preset_values(self, values: dict[str, Any], source: str = "preset") -> LightingState:
        state = self.state.clone()
        apply_values_to_state(state, values, exact=True)
        state.source = source
        self.sync_strobe_value(state)
        return state

    def reset_preset_editor(self, group: str, name: str) -> None:
        defaults = {
            "performance": PERFORMANCE_PRESETS,
            "mood": MOOD_PRESETS,
            "energy": ENERGY_PRESETS,
            "section": SECTION_PRESETS,
        }[group]
        values = defaults.get(name, {})
        editor = self.preset_editors[group][name]
        for key, variable in editor.items():
            if key.endswith("_SWATCH"):
                continue
            if key == "NAME":
                variable.set(name)
                continue
            if key in {"PRIMARY", "SECONDARY", "STROBE"}:
                variable.set(str(values.get(key, "")).casefold())
                self.refresh_preset_color_swatch(group, name, key)
            else:
                variable.set(str(parse_percent(values.get(key, self.default_preset_values().get(key, 0)), 0)))
                self._refresh_percent_button_group(f"preset:{group}:{name}:{key}", variable.get())
        self.last_event_var.set(f"Reset {name} preset controls from built-in defaults")

    def _build_track_tab(self) -> None:
        self.track_tab.columnconfigure(1, weight=1)
        self._add_value_row(self.track_tab, 0, "Now Playing", self.active_track_var)
        self._add_value_row(self.track_tab, 1, "Matched File", self.matched_file_var)
        self._add_value_row(self.track_tab, 2, "Track Comment Found", self.comment_found_var)
        self._add_value_row(self.track_tab, 3, "Parsed Values", self.parsed_tags_var)
        self._add_value_row(self.track_tab, 4, "Missing Color Values", self.missing_tags_var)
        self._add_value_row(self.track_tab, 5, "Applied From", self.applied_source_var)
        self._add_value_row(self.track_tab, 6, "Auto Send", self.fallback_var)
        self._add_value_row(self.track_tab, 7, "Daily Log", self.daily_log_status_var)
        template = ttk.LabelFrame(self.track_tab, text="Color Comment for MP3", padding=10)
        template.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        template.columnconfigure(0, weight=1)
        ttk.Entry(template, textvariable=self.template_var).grid(row=0, column=0, sticky="ew")
        ttk.Button(template, text="Use Current Colors", command=self.update_template_from_state).grid(row=0, column=1, padx=(8, 0))
        ttk.Button(template, text="Copy Color Comment", command=self.copy_template).grid(row=0, column=2, padx=(8, 0))

    def _add_palette_swatch(self, parent: ttk.Frame, col: int, key: str) -> None:
        label = {
            "dominant": "Primary Color",
            "accent": "Secondary Color",
            "bright_accent": "Accent Color",
        }.get(key, key.replace("_", " ").title())
        ttk.Label(parent, text=label, font=("Segoe UI", 9, "bold")).grid(row=0, column=col, sticky="w")
        canvas = tk.Canvas(parent, height=20, highlightthickness=1, highlightbackground="#777777", bg="#f5f5f5")
        canvas.grid(row=1, column=col, sticky="ew", padx=2, pady=2)
        if key not in self.palette_labels:
            self.palette_labels[key] = tk.StringVar(value="-")
        self.palette_swatches.setdefault(key, []).append(canvas)
        canvas.bind("<Configure>", lambda _event, current_key=key, current_canvas=canvas: self.draw_palette_swatch(current_key, current_canvas))
        ttk.Label(parent, textvariable=self.palette_labels[key], style="Muted.TLabel").grid(row=2, column=col, sticky="w", padx=2)

    def _build_command_output_tab(self) -> None:
        self.command_tab.columnconfigure(0, weight=1)
        self.command_tab.rowconfigure(0, weight=1)
        log_frame = ttk.LabelFrame(self.command_tab, text="Command Prompt Output / Sent OSC Messages", padding=10)
        log_frame.grid(row=0, column=0, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.log_text = tk.Text(log_frame, wrap="word", font=("Consolas", 10), height=16)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)
        ttk.Button(log_frame, text="Clear Log", command=self.clear_log).grid(row=1, column=0, sticky="e", pady=(8, 0))

    def _build_blt_osc_editor(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(2, weight=1)
        parent.columnconfigure(3, weight=2)
        parent.columnconfigure(4, weight=2)
        headers = ("On", "Label", "Field", "OSC Address", "Last Sent")
        for col, header in enumerate(headers):
            ttk.Label(parent, text=header).grid(row=0, column=col, sticky="w", padx=4, pady=(0, 4))
        for row, output in enumerate(self.blt_osc_outputs, start=1):
            key = output["key"]
            enabled_var = tk.BooleanVar(value=bool(output.get("enabled", False)))
            label_var = tk.StringVar(value=str(output.get("label", key)))
            field_var = tk.StringVar(value=str(output.get("field", "full_track")))
            address_var = tk.StringVar(value=str(output.get("address", "")))
            last_var = tk.StringVar(value="-")
            self.blt_osc_output_vars[key] = {
                "enabled": enabled_var,
                "label": label_var,
                "field": field_var,
                "address": address_var,
            }
            self.blt_osc_last_vars[key] = last_var
            ttk.Checkbutton(parent, variable=enabled_var).grid(row=row, column=0, sticky="w", padx=4, pady=2)
            ttk.Entry(parent, textvariable=label_var, width=24).grid(row=row, column=1, sticky="ew", padx=4, pady=2)
            ttk.Combobox(parent, textvariable=field_var, values=BLT_FIELD_CHOICES, width=18).grid(row=row, column=2, sticky="ew", padx=4, pady=2)
            ttk.Entry(parent, textvariable=address_var).grid(row=row, column=3, sticky="ew", padx=4, pady=2)
            ttk.Label(parent, textvariable=last_var, wraplength=520).grid(row=row, column=4, sticky="ew", padx=4, pady=2)
        actions = ttk.Frame(parent)
        actions.grid(row=len(self.blt_osc_outputs) + 1, column=0, columnspan=5, sticky="ew", pady=(8, 0))
        ttk.Button(actions, text="Save BLT OSC Outputs", command=self.save_blt_osc_outputs).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(actions, text="Test Enabled BLT Outputs", command=self.test_blt_osc_outputs).grid(row=0, column=1, padx=(0, 8))

    def _build_settings_tab(self) -> None:
        content = self._create_scrollable_frame(self.settings_tab, 0)

        core = ttk.LabelFrame(content, text="Runtime Settings", padding=10)
        core.grid(row=0, column=0, sticky="ew")
        core.columnconfigure(1, weight=1)
        row = 0
        for label, var in (
            ("BLT params URL", self.blt_url_var),
            ("Resolume IP", self.osc_host_var),
            ("Resolume Port", self.osc_port_var),
            ("Music Root", self.music_root_var),
            ("Artwork Output File", self.artwork_output_var),
            ("Fallback Artwork File", self.fallback_artwork_path_var),
            ("Vinyl Logo File", self.vinyl_logo_path_var),
            ("Vinyl Track Text", self.vinyl_track_text_var),
            ("NO TALKING STUDIO Artwork", self.studio_artwork_path_var),
            ("NO TALKING STUDIO Text", self.studio_track_text_var),
            ("Default Fallback Template", self.default_template_var),
            ("Artwork Size", self.output_size_var),
        ):
            ttk.Label(core, text=label).grid(row=row, column=0, sticky="w", pady=4)
            ttk.Entry(core, textvariable=var).grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=4)
            row += 1
        osc_frame = ttk.LabelFrame(content, text="Editable Resolume Dashboard Link Addresses", padding=10)
        osc_frame.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        osc_frame.columnconfigure(1, weight=1)
        osc_frame.columnconfigure(2, weight=2)
        osc_frame.columnconfigure(3, weight=2)
        ttk.Label(osc_frame, text="Link").grid(row=0, column=0, sticky="w", pady=(0, 4))
        ttk.Label(osc_frame, text="Label").grid(row=0, column=1, sticky="w", pady=(0, 4))
        ttk.Label(osc_frame, text="Editable OSC Address").grid(row=0, column=2, sticky="w", pady=(0, 4))
        ttk.Label(osc_frame, text="Last Sent").grid(row=0, column=3, sticky="w", pady=(0, 4))
        for link in range(1, 9):
            var = tk.StringVar(value="-")
            self.osc_vars[link] = var
            ttk.Label(osc_frame, text=f"Link {link}:").grid(row=link, column=0, sticky="w", pady=3)
            ttk.Entry(osc_frame, textvariable=self.link_label_vars[link]).grid(row=link, column=1, sticky="ew", padx=(8, 12), pady=3)
            ttk.Entry(osc_frame, textvariable=self.osc_address_vars[link]).grid(row=link, column=2, sticky="ew", padx=(0, 12), pady=3)
            ttk.Label(osc_frame, textvariable=var, wraplength=720, justify="left").grid(row=link, column=3, sticky="ew", pady=3)
        osc_buttons = ttk.Frame(osc_frame)
        osc_buttons.grid(row=9, column=0, columnspan=4, sticky="ew", pady=(8, 0))
        ttk.Button(osc_buttons, text="Save Link Labels / OSC Addresses", command=self.save_osc_addresses).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(osc_buttons, text="Test Send All Links", command=lambda: self.send_state_osc(self.state, "test")).grid(row=0, column=1, padx=(0, 8))
        for link in range(1, 9):
            ttk.Button(osc_buttons, text=f"L{link}", command=lambda current=link: self.test_link_number(current)).grid(row=0, column=link + 1, padx=2)

        blt_frame = ttk.LabelFrame(content, text="BLT / Track Text OSC Outputs", padding=10)
        blt_frame.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        self._build_blt_osc_editor(blt_frame)

        buttons = ttk.Frame(content)
        buttons.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        ttk.Button(buttons, text="Save Settings", command=self.save_config).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(buttons, text="Start Watcher", command=self.start_watcher).grid(row=0, column=1, padx=4)
        ttk.Button(buttons, text="Stop Watcher", command=self.stop_watcher).grid(row=0, column=2, padx=4)
        ttk.Button(buttons, text="Rebuild Library Index", command=self.rebuild_library_index).grid(row=0, column=3, padx=4)
        ttk.Button(buttons, text="Open Artwork Folder", command=self.open_artwork_folder).grid(row=0, column=4, padx=4)
        ttk.Button(buttons, text="Open Track Folder", command=self.open_track_folder).grid(row=0, column=5, padx=4)
        ttk.Checkbutton(buttons, text="Rebuild index on start", variable=self.rebuild_index_var).grid(row=0, column=6, padx=(12, 0))
        ttk.Button(buttons, text="Browse Fallback Artwork", command=self.browse_fallback_artwork).grid(row=1, column=0, padx=(0, 8), pady=(8, 0))
        ttk.Button(buttons, text="Open Fallback Folder", command=self.open_fallback_artwork_folder).grid(row=1, column=1, padx=4, pady=(8, 0))

    def _add_value_row(self, parent: ttk.Frame, row: int, label: str, variable: tk.StringVar) -> None:
        ttk.Label(parent, text=f"{label}:").grid(row=row, column=0, sticky="nw", pady=3)
        ttk.Label(parent, textvariable=variable, wraplength=960, justify="left").grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=3)

    def log(self, text: str) -> None:
        self.log_text.insert("end", text)
        line_count = int(self.log_text.index("end-1c").split(".", 1)[0])
        if line_count > MAX_COMMAND_OUTPUT_LINES:
            self.log_text.delete("1.0", f"{line_count - MAX_COMMAND_OUTPUT_LINES}.0")
        self.log_text.see("end")

    def clear_log(self) -> None:
        self.log_text.delete("1.0", "end")
        self.last_event_var.set("Log cleared")

    def configure_runtime_modules(self) -> None:
        watcher.BLT_PARAMS_URL = self.blt_url_var.get().strip() or watcher.BLT_PARAMS_URL
        watcher.RESOLUME_OSC_HOST = self.osc_host_var.get().strip() or watcher.RESOLUME_OSC_HOST
        watcher.RESOLUME_OSC_PORT = parse_int(self.osc_port_var.get(), watcher.RESOLUME_OSC_PORT, 1, 65535)
        watcher.MUSIC_ROOT = path_from_text(self.music_root_var.get(), watcher.MUSIC_ROOT)
        artwork_module.OUTPUT_IMAGE = path_from_text(self.artwork_output_var.get(), artwork_module.OUTPUT_IMAGE)
        artwork_module.FALLBACK_ARTWORK_IMAGE = path_from_text(
            self.fallback_artwork_path_var.get(),
            artwork_module.FALLBACK_ARTWORK_IMAGE,
        )

    def start_watcher(self) -> None:
        if self.watch_thread and self.watch_thread.is_alive():
            self.last_event_var.set("Watcher already running")
            return
        self.configure_runtime_modules()
        self.save_config()
        self.stop_event.clear()
        self.watch_thread = threading.Thread(target=self._watch_loop, args=(self.rebuild_index_var.get(),), daemon=True)
        self.watch_thread.start()
        self.status_var.set("Running")
        self.status_badge.configure(bg="#2b7a3d")
        self.last_event_var.set("Watcher started")
        self.blt_status_var.set("Starting BLT poll...")

    def stop_watcher(self) -> None:
        self.stop_event.set()
        self.status_var.set("Stopping")
        self.status_badge.configure(bg="#946200")
        self.last_event_var.set("Stopping watcher after current poll")

    def _load_music_index_in_thread(self, rebuild_index: bool, index_queue: queue.Queue[dict[str, Any]]) -> None:
        try:
            index = watcher.load_music_index(rebuild=rebuild_index)
            index_queue.put({"type": "index", "index": index})
        except Exception as exc:
            index_queue.put({"type": "index_error", "text": str(exc)})

    def _watch_loop(self, rebuild_index: bool) -> None:
        try:
            self.output_queue.put({"type": "log", "text": "\nPerformance watcher started.\n"})
            index: Optional[list[watcher.TrackIndexEntry]] = None
            index_queue: queue.Queue[dict[str, Any]] = queue.Queue()
            index_thread = threading.Thread(
                target=self._load_music_index_in_thread,
                args=(rebuild_index, index_queue),
                daemon=True,
            )
            index_thread.start()
            self.output_queue.put({"type": "status", "text": "Loading music library index; polling BLT now"})
            last_active_track_key = ""
            last_payload_track_key = ""
            last_track_info = ""
            last_waiting_message_time = 0.0
            last_blt_error_time = 0.0
            last_index_wait_message_time = 0.0
            output_pixels = parse_int(self.config.get("output_pixels", DEFAULT_OUTPUT_PIXELS), DEFAULT_OUTPUT_PIXELS, 64, 4096)
            while not self.stop_event.is_set():
                try:
                    while True:
                        index_event = index_queue.get_nowait()
                        if index_event.get("type") == "index":
                            index = index_event["index"]
                            last_active_track_key = ""
                            self.output_queue.put({"type": "log", "text": f"Loaded {len(index)} indexed tracks.\n"})
                            self.output_queue.put({"type": "status", "text": f"Music index ready: {len(index)} tracks"})
                        elif index_event.get("type") == "index_error":
                            index = []
                            self.output_queue.put({"type": "error", "text": f"Music index failed: {index_event['text']}"})
                except queue.Empty:
                    pass

                params = watcher.fetch_blt_params()
                if not params:
                    now = time.time()
                    if now - last_blt_error_time >= 10:
                        self.output_queue.put({"type": "status", "text": f"BLT params unavailable at {watcher.BLT_PARAMS_URL}"})
                        last_blt_error_time = now
                    time.sleep(watcher.POLL_SECONDS)
                    continue
                track = watcher.select_active_track(params)
                if not track:
                    now = time.time()
                    if now - last_waiting_message_time >= 10:
                        self.output_queue.put({"type": "status", "text": "BLT connected; waiting for a playing master deck"})
                        last_waiting_message_time = now
                    time.sleep(watcher.POLL_SECONDS)
                    continue
                if self.vinyl_mode_active:
                    last_active_track_key = ""
                    last_payload_track_key = ""
                    last_track_info = ""
                    time.sleep(watcher.POLL_SECONDS)
                    continue
                track_info = watcher.build_track_info(track)
                if track_info and track_info != last_track_info:
                    last_track_info = track_info
                    self.output_queue.put({"type": "track_info", "track_info": track_info})
                auto_track_key = self.track_auto_key(track)
                track_identity = {
                    "title": track.get("title", ""),
                    "artist": track.get("artist", ""),
                    "album": track.get("album", ""),
                    "player": track.get("player", ""),
                    "bpm": track.get("bpm", ""),
                    "player_number": track.get("player_number", ""),
                    "device_name": track.get("device_name", ""),
                    "source_player": track.get("source_player", ""),
                }
                track_key = json.dumps(track_identity, sort_keys=True, ensure_ascii=False)
                if track_key != last_active_track_key:
                    last_active_track_key = track_key
                    self.output_queue.put(
                        {
                            "type": "active_track",
                            "track": track,
                            "track_info": track_info,
                            "description": watcher.describe_track(track),
                            "auto_track_key": auto_track_key,
                        }
                    )
                if index is None:
                    now = time.time()
                    if now - last_index_wait_message_time >= 10:
                        self.output_queue.put({"type": "status", "text": "BLT active; waiting for music index before artwork/comment matching"})
                        last_index_wait_message_time = now
                    time.sleep(watcher.POLL_SECONDS)
                    continue
                if track_key == last_payload_track_key:
                    time.sleep(watcher.POLL_SECONDS)
                    continue
                last_payload_track_key = track_key
                match = watcher.find_best_match(track, index)
                if not match:
                    self.output_queue.put({"type": "log", "text": "Could not confidently match this track to a local MP3.\n"})
                    self.output_queue.put({"type": "status", "text": "BLT active; no confident local MP3 match yet"})
                    time.sleep(watcher.POLL_SECONDS)
                    continue
                entry, score = match
                mp3_path = Path(entry["path"])
                comment, comment_source = watcher.read_mp3_comment(mp3_path)
                artwork_log = self._process_artwork_in_thread(mp3_path, output_pixels)
                if self.vinyl_mode_active:
                    self.output_queue.put({"type": "vinyl_refresh"})
                    time.sleep(watcher.POLL_SECONDS)
                    continue
                self.output_queue.put(
                    {
                        "type": "track_payload",
                        "track": track,
                        "description": watcher.describe_track(track),
                        "auto_track_key": auto_track_key,
                        "path": str(mp3_path),
                        "score": score,
                        "comment": comment,
                        "comment_source": comment_source,
                        "artwork_log": artwork_log,
                    }
                )
                time.sleep(watcher.POLL_SECONDS)
        except Exception as exc:
            self.output_queue.put({"type": "error", "text": f"Watcher crashed: {exc}", "fatal": True})
        finally:
            if self.stop_event.is_set():
                self.output_queue.put({"type": "stopped"})

    def _process_artwork_in_thread(self, mp3_path: Path, output_pixels: int) -> str:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                artwork_module.process_mp3(mp3_path, output_pixels)
            except Exception as exc:
                print(f"ERROR: Artwork extraction failed: {exc}")
        return output.getvalue()

    def _poll_output_queue(self) -> None:
        try:
            while True:
                event = self.output_queue.get_nowait()
                self.handle_event(event)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_output_queue)

    def handle_event(self, event: dict[str, Any]) -> None:
        event_type = event.get("type")
        if event_type == "log":
            self.log(event["text"])
        elif event_type == "status":
            self.last_event_var.set(event["text"])
            self.blt_status_var.set(event["text"])
        elif event_type == "error":
            self.log(f"ERROR: {event['text']}\n")
            self.last_event_var.set(event["text"])
            if event.get("fatal"):
                self.status_var.set("Error")
            self.status_badge.configure(bg="#a83232")
        elif event_type == "stopped":
            self.status_var.set("Stopped")
            self.status_badge.configure(bg="#666666")
            self.last_event_var.set("Watcher stopped")
        elif event_type == "track_info":
            if self.vinyl_mode_active:
                return
            self.latest_blt_context["track_info"] = event["track_info"]
            self.send_blt_osc_outputs(self.latest_blt_context, fields={"track_info"})
        elif event_type == "active_track":
            if self.vinyl_mode_active:
                return
            auto_track_key = event.get("auto_track_key") or self.track_auto_key(event.get("track", {}))
            if auto_track_key != self.current_track_auto_key:
                self.flush_track_history_end("next track loaded")
                self.current_track_auto_key = auto_track_key
                self.manual_artwork_override_track_key = ""
            self.active_track_var.set(event["description"])
            self.last_event_var.set(f"Active track: {event['description']}")
            self.blt_status_var.set(f"BLT active: {event['description']}")
            self.latest_blt_context = self.build_blt_context(event["track"], event.get("track_info", ""))
            self.latest_track_history_context = dict(self.latest_blt_context)
            self.send_blt_osc_outputs(self.latest_blt_context)
        elif event_type == "track_payload":
            if self.vinyl_mode_active:
                return
            self.handle_track_payload(event)
        elif event_type == "vinyl_refresh":
            if self.vinyl_mode_active:
                if self.manual_artwork_mode == "studio":
                    self.write_studio_artwork_to_artwork_file()
                else:
                    self.write_vinyl_logo_to_artwork_file()

    def handle_track_payload(self, event: dict[str, Any]) -> None:
        auto_track_key = event.get("auto_track_key") or self.track_auto_key(event.get("track", {}))
        if auto_track_key != self.current_track_auto_key:
            self.flush_track_history_end("next track loaded")
            self.current_track_auto_key = auto_track_key
            self.manual_artwork_override_track_key = ""
        self.current_matched_file = Path(event["path"])
        self.matched_file_var.set(f"{event['path']} ({event['score']:.0%})")
        self.latest_track_history_context = self.build_blt_context(event.get("track", {}), event.get("track_info", ""), event.get("comment", ""))
        self.log(event.get("artwork_log", ""))
        self.refresh_artwork_preview()
        self.extract_palette_from_current_artwork(update_only=True)

        comment = event.get("comment", "")
        self.latest_blt_context["comment"] = comment
        self.send_blt_osc_outputs(self.latest_blt_context, fields={"comment"})
        tags = parse_comment_tags(comment)
        self.update_comment_feedback(comment, event.get("comment_source", ""), tags)

        if self.manual_artwork_override_track_key == auto_track_key:
            self.applied_source_var.set("Manual override")
            self.fallback_var.set("Manual until next track")
            self.last_event_var.set("Manual color change held; track color automation resumes next track")
            self.log_daily_track_decision(
                event,
                self.state,
                {"source": "manual", "fallback": "Manual until next track", "note": "Manual color change paused track color automation for this track."},
                comment,
            )
            return

        if not {"PRIMARY", "SECONDARY", "STROBE"}.intersection(tags):
            if self.auto_artwork_palette_var.get() and self.palette.available:
                state = self.state.clone()
                self.apply_palette_to_state(state)
                state.source = "artwork"
                self.apply_state(state, "artwork", send=False)
                self.send_color_controls_only(source="artwork-auto")
                self.applied_source_var.set("Artwork palette")
                self.fallback_var.set("Auto artwork")
                details = {
                    "source": "artwork",
                    "fallback": "Sent from album artwork auto mode",
                    "note": "No MP3 color comment; auto artwork colors enabled.",
                }
                self.last_event_var.set("No MP3 color comment; sent album artwork colors")
                self.log_daily_track_decision(event, state, details, comment)
                return

            if self.auto_artwork_palette_var.get():
                self.applied_source_var.set("No artwork palette")
                self.fallback_var.set("Auto artwork unavailable")
                self.last_event_var.set("No MP3 color comment; auto artwork on but no usable palette")
                self.log_daily_track_decision(
                    event,
                    self.state,
                    {"source": "none", "fallback": "Auto artwork unavailable", "note": "No MP3 color comment and no usable artwork palette; OSC not sent."},
                    comment,
                )
                return

            self.applied_source_var.set("No color comment")
            self.fallback_var.set("Manual artwork")
            self.last_event_var.set("No MP3 color comment found; auto artwork off, lights unchanged")
            self.log_daily_track_decision(
                event,
                self.state,
                {"source": "none", "fallback": "Manual artwork", "note": "No MP3 color comment; auto artwork colors off, OSC not sent."},
                comment,
            )
            return

        state, details = self.resolve_state_for_track(comment, tags)
        self.apply_state(state, source=state.source, send=True)
        self.applied_source_var.set(details["source"])
        self.fallback_var.set(details["fallback"])
        self.log_daily_track_decision(event, state, details, comment)

    def update_comment_feedback(self, comment: str, comment_source: str, tags: dict[str, str]) -> None:
        expected = ["PRIMARY", "SECONDARY", "STROBE"]
        missing = [key for key in expected if key not in tags]
        color_tags = {key: tags[key] for key in expected if key in tags}
        if color_tags:
            pretty = "\n".join(f"{key}={value}" for key, value in color_tags.items())
            self.comment_found_var.set(f"Yes ({comment_source}):\n{pretty}")
        elif comment.strip():
            self.comment_found_var.set(f"No color tags found ({comment_source}).")
        else:
            self.comment_found_var.set(f"No color comment found ({comment_source}).")
        self.parsed_tags_var.set(", ".join(f"{key}={value}" for key, value in color_tags.items()) if color_tags else "-")
        self.missing_tags_var.set(", ".join(missing) if missing else "None")

    def resolve_state_for_track(self, comment: str, tags: dict[str, str]) -> tuple[LightingState, dict[str, str]]:
        exact_keys = {"PRIMARY", "SECONDARY", "STROBE"}
        exact = {key: value for key, value in tags.items() if key in exact_keys}
        state = self.state.clone()
        apply_values_to_state(state, exact, exact=True)

        state.source = "comment"
        self.sync_strobe_value(state)
        return state, {
            "source": state.source,
            "fallback": "Sent from MP3 color comment",
            "note": "",
        }

    def sync_strobe_value(self, state: LightingState) -> None:
        state.strobe_value = percent_to_value(state.strobe_percent)

    def apply_palette_to_state(self, state: LightingState) -> None:
        if not self.palette.available:
            return
        state.color1_name = self.palette.dominant.name
        state.color1_value = self.palette.dominant.hue
        state.color2_name = self.palette.accent.name
        state.color2_value = self.palette.accent.hue
        state.strobe_color_name = self.palette.bright_accent.name
        state.strobe_color_value = self.palette.bright_accent.hue

    def send_color_controls_only(self, source: str) -> None:
        for control_key in ("color1", "color2", "strobe_color"):
            self.resend_one_control(control_key, source=source)

    def apply_state(self, state: LightingState, source: str, send: bool = True) -> None:
        self.state = state
        self.sync_controls_from_state()
        self.refresh_output_strip()
        self.template_var.set(self.template_from_state(state))
        self.write_visual_defaults_config(state)
        if send:
            self.send_state_osc(state, source)
        self.last_event_var.set(f"Applied lighting state from {source}")

    def sync_controls_from_state(self) -> None:
        self.control_vars["color1"].set(self.state.color1_name)
        self.control_vars["color2"].set(self.state.color2_name)
        self.control_vars["strobe_color"].set(self.state.strobe_color_name)
        self._refresh_color_button_group("color1", self.state.color1_name)
        self._refresh_color_button_group("color2", self.state.color2_name)
        self._refresh_color_button_group("strobe_color", self.state.strobe_color_name)
        self._sync_percent_control("motion", round(self.state.motion_value * 100), self.state.motion_value)
        self._sync_percent_control("saturation", self.state.saturation_percent, self.state.saturation_value)
        self._sync_percent_control("brightness", self.state.brightness_percent, self.state.brightness_value)
        self._sync_percent_control("fx", round(self.state.fx_value * 100), self.state.fx_value)
        self._sync_percent_control("pulse", round(self.state.pulse_value * 100), self.state.pulse_value)
        self.refresh_control_swatches()

    def _sync_percent_control(self, key: str, percent: int, normalized_value: float) -> None:
        allowed_values = self.percent_button_values.get(key)
        if allowed_values:
            visual_percent = nearest_percent_choice(percent, allowed_values)
        else:
            visual_percent = percent
        self.control_vars[key].set(percent)
        self._refresh_percent_button_group(key, visual_percent)
        readout = self.control_readout_vars.get(key)
        if readout:
            readout.set(f"Current: {percent}% / {normalized_value:.3f}")

    def refresh_control_swatches(self) -> None:
        for key, color_name in (
            ("color1", self.state.color1_name),
            ("color2", self.state.color2_name),
            ("strobe_color", self.state.strobe_color_name),
        ):
            canvas = self.visual_swatches.get(key)
            if canvas:
                canvas.delete("all")
                canvas.create_rectangle(2, 2, 22, 22, fill=COLOR_HEX.get(color_name, "#777777"), outline="#333333")

    def refresh_output_strip(self) -> None:
        self.output_vars["color1"].set(f"{self.state.color1_name} {self.state.color1_value:.3f}")
        self.output_vars["color2"].set(f"{self.state.color2_name} {self.state.color2_value:.3f}")
        self.output_vars["strobe"].set(f"{self.state.strobe_percent}% {self.state.strobe_value:.3f}")
        self.output_vars["strobe_color"].set(f"{self.state.strobe_color_name} {self.state.strobe_color_value:.3f}")
        self.output_vars["saturation"].set(f"{self.state.saturation_percent}% {self.state.saturation_value:.3f}")
        self.output_vars["brightness"].set(f"{self.state.brightness_percent}% {self.state.brightness_value:.3f}")
        self.output_vars["motion"].set(f"{self.state.motion_value:.3f}")
        self.output_vars["fx"].set(f"{self.state.fx_value:.3f}")
        self.output_vars["pulse"].set(f"{self.state.pulse_value:.3f}")
        self.refresh_output_color_chips()
        self.draw_gradient()

    def refresh_output_color_chips(self) -> None:
        color_names = {
            "color1": self.state.color1_name,
            "color2": self.state.color2_name,
            "strobe_color": self.state.strobe_color_name,
        }
        for key, canvas in self.output_color_canvases.items():
            canvas.delete("all")
            canvas.create_rectangle(
                1,
                1,
                max(canvas.winfo_width(), 34) - 1,
                max(canvas.winfo_height(), 12) - 1,
                fill=COLOR_HEX.get(color_names.get(key, ""), "#777777"),
                outline="",
            )

    def draw_gradient(self) -> None:
        canvas = self.gradient_canvas
        width = max(canvas.winfo_width(), 2)
        height = max(canvas.winfo_height(), 2)
        canvas.delete("all")
        left = self.hex_to_rgb(COLOR_HEX.get(self.state.color1_name, "#4b3dff"))
        right = self.hex_to_rgb(COLOR_HEX.get(self.state.color2_name, "#ff2bd6"))
        for x in range(width):
            t = x / max(width - 1, 1)
            rgb = tuple(int(left[i] + (right[i] - left[i]) * t) for i in range(3))
            canvas.create_line(x, 0, x, height, fill=f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")

    def hex_to_rgb(self, value: str) -> tuple[int, int, int]:
        return color_hex_to_rgb(value)

    def on_manual_control_changed(self, key: str, live: bool = False) -> None:
        if live and key not in {"motion", "strobe", "saturation", "brightness", "fx", "pulse"}:
            return
        if key in {"color1", "color2", "strobe_color"}:
            self.mark_manual_artwork_override("color button")
        state = self.state.clone()
        if key == "color1":
            state.color1_name, state.color1_value = color_name_to_value(self.control_vars[key].get())
        elif key == "color2":
            state.color2_name, state.color2_value = color_name_to_value(self.control_vars[key].get())
        elif key == "strobe_color":
            state.strobe_color_name, state.strobe_color_value = color_name_to_value(
                self.control_vars[key].get(),
                state.strobe_color_name,
            )
        elif key == "motion":
            motion = motion_percent(self.control_vars[key].get())
            state.motion_value = percent_to_value(motion)
            state.strobe_percent = motion
            self.sync_strobe_value(state)
            state.motion_value = state.strobe_value
        elif key == "strobe":
            state.strobe_percent = parse_percent(self.control_vars[key].get())
            self.sync_strobe_value(state)
        elif key == "saturation":
            state.saturation_percent = parse_percent(self.control_vars[key].get(), 100)
            state.saturation_value = percent_to_value(state.saturation_percent)
        elif key == "brightness":
            state.brightness_percent = parse_percent(self.control_vars[key].get(), 100)
            state.brightness_value = percent_to_value(state.brightness_percent)
        elif key == "fx":
            state.fx_value = percent_to_value(self.control_vars[key].get())
        elif key == "pulse":
            state.pulse_value = percent_to_value(self.control_vars[key].get())
        state.source = "manual"
        self.apply_state(state, "manual", send=False)
        if key in {"color1", "color2", "strobe_color"}:
            self.resend_one_control(key)
        else:
            self.send_one_control(key)
        self.last_event_var.set(f"Updated {key.replace('_', ' ')} and sent one OSC value")

    def apply_performance_preset(self, name: str) -> None:
        state = make_state_from_template(self.default_template_var.get() or DEFAULT_TEMPLATE)
        apply_values_to_state(state, self.performance_presets[name], exact=True)
        state.source = f"preset:{name}"
        self.sync_strobe_value(state)
        self.apply_state(state, "preset", send=True)

    def safe_reset(self) -> None:
        state = make_state_from_template("PRIMARY=blue;SECONDARY=purple;STROBE=blue;STROBE_PERCENT=0;SATURATION=100;BRIGHTNESS=100;MOTION=20;FX=0;PULSE=0")
        state.source = "safe reset"
        self.apply_state(state, "safe reset", send=True)

    def apply_color_relationship(self, offset: float) -> None:
        self.mark_manual_artwork_override("color relationship")
        state = self.state.clone()
        hue = (state.color1_value + offset) % 1.0
        state.color2_value = hue
        state.color2_name = nearest_color_name(hue)
        state.source = "manual color relationship"
        self.apply_state(state, "manual", send=False)
        self.send_one_control("color2")

    def swap_primary_secondary(self, source: str = "swap", resend: bool = True) -> None:
        self.mark_manual_artwork_override("color swap")
        state = self.state.clone()
        state.color1_name, state.color2_name = state.color2_name, state.color1_name
        state.color1_value, state.color2_value = state.color2_value, state.color1_value
        state.source = "manual color swap"
        self.apply_state(state, "manual", send=False)
        if resend:
            self.resend_one_control("color1", source=source)
            self.resend_one_control("color2", source=source)
        else:
            self.send_one_control("color1", source=source)
            self.send_one_control("color2", source=source)
        self.template_var.set(self.template_from_state(state))
        self.last_event_var.set("Swapped primary and secondary colors")

    def on_bpm_flip_division_changed(self) -> None:
        self.refresh_bpm_flip_rate_buttons()
        self.save_config()
        if self.bpm_flip_running:
            self.reschedule_bpm_flip()
        else:
            self.update_bpm_flip_status()

    def refresh_bpm_flip_rate_buttons(self) -> None:
        rate = normalize_bpm_swap_rate(self.bpm_flip_division_var.get())
        self.bpm_flip_division_var.set(rate)
        self._refresh_choice_button_group("bpm_flip_division_fast", rate)
        self._refresh_choice_button_group("bpm_flip_division_bars", rate)

    def use_latest_track_bpm(self) -> None:
        bpm = str(self.latest_blt_context.get("bpm", "")).strip()
        if not bpm:
            messagebox.showinfo("No Track BPM", "No active track BPM is available yet.")
            return
        try:
            parsed = parse_bpm(bpm)
        except ValueError as exc:
            messagebox.showerror("Invalid Track BPM", str(exc))
            return
        self.bpm_flip_bpm_var.set(f"{parsed:g}")
        self.save_config()
        self.update_bpm_flip_status()
        self.last_event_var.set(f"Auto Swap set to active track BPM: {parsed:g}")

    def current_bpm_flip_interval_ms(self) -> int:
        bpm = parse_bpm(self.bpm_flip_bpm_var.get())
        division = normalize_bpm_swap_rate(self.bpm_flip_division_var.get())
        return bpm_flip_interval_ms(bpm, division)

    def update_bpm_flip_status(self) -> None:
        try:
            bpm = parse_bpm(self.bpm_flip_bpm_var.get())
            division = normalize_bpm_swap_rate(self.bpm_flip_division_var.get())
            self.bpm_flip_division_var.set(division)
            self.refresh_bpm_flip_rate_buttons()
            interval_ms = bpm_flip_interval_ms(bpm, division)
        except ValueError as exc:
            self.bpm_flip_status_var.set(str(exc))
            return
        state = "running" if self.bpm_flip_running else "idle"
        self.bpm_flip_status_var.set(f"{state}: {bpm:g} BPM, {division}, swap every {interval_ms} ms")

    def trigger_bpm_flip(self) -> None:
        try:
            bpm = parse_bpm(self.bpm_flip_bpm_var.get())
            division = normalize_bpm_swap_rate(self.bpm_flip_division_var.get())
            self.bpm_flip_division_var.set(division)
            self.refresh_bpm_flip_rate_buttons()
            interval_ms = bpm_flip_interval_ms(bpm, division)
        except ValueError as exc:
            messagebox.showerror("Invalid Auto Swap", str(exc))
            self.bpm_flip_status_var.set(str(exc))
            return

        self.stop_bpm_flip(update_status=False)
        self.save_config()
        self.bpm_flip_running = True
        self.bpm_flip_token += 1
        self.bpm_flip_remaining = None
        if self.bpm_flip_trigger_button is not None:
            self.bpm_flip_trigger_button.configure(state="normal")
        self.bpm_flip_status_var.set(f"running: {bpm:g} BPM, {division}, swap every {interval_ms} ms")
        self.last_event_var.set(f"Auto Swap started at {bpm:g} BPM {division}")
        self._run_bpm_flip_step(self.bpm_flip_token)

    def _run_bpm_flip_step(self, token: int) -> None:
        if token != self.bpm_flip_token or not self.bpm_flip_running:
            return
        self.swap_primary_secondary(source="auto swap", resend=False)
        self.schedule_next_bpm_flip(token)

    def schedule_next_bpm_flip(self, token: int) -> None:
        if token != self.bpm_flip_token or not self.bpm_flip_running:
            return
        try:
            interval_ms = self.current_bpm_flip_interval_ms()
            bpm = parse_bpm(self.bpm_flip_bpm_var.get())
        except ValueError as exc:
            self.stop_bpm_flip(update_status=False)
            self.bpm_flip_status_var.set(str(exc))
            return
        rate = normalize_bpm_swap_rate(self.bpm_flip_division_var.get())
        self.bpm_flip_after_id = self.root.after(interval_ms, lambda current_token=token: self._run_bpm_flip_step(current_token))
        self.bpm_flip_status_var.set(f"running: {bpm:g} BPM, {rate}, next swap in {interval_ms} ms")

    def reschedule_bpm_flip(self) -> None:
        if not self.bpm_flip_running:
            self.update_bpm_flip_status()
            return
        if self.bpm_flip_after_id is not None:
            with contextlib.suppress(tk.TclError):
                self.root.after_cancel(self.bpm_flip_after_id)
        self.bpm_flip_after_id = None
        self.bpm_flip_token += 1
        token = self.bpm_flip_token
        self.schedule_next_bpm_flip(token)
        rate = normalize_bpm_swap_rate(self.bpm_flip_division_var.get())
        self.last_event_var.set(f"Auto Swap rate changed to {rate}")

    def stop_bpm_flip(self, update_status: bool = True) -> None:
        self.bpm_flip_token += 1
        if self.bpm_flip_after_id is not None:
            with contextlib.suppress(tk.TclError):
                self.root.after_cancel(self.bpm_flip_after_id)
        self.bpm_flip_after_id = None
        was_running = self.bpm_flip_running
        self.bpm_flip_running = False
        self.bpm_flip_remaining = None
        if self.bpm_flip_trigger_button is not None:
            self.bpm_flip_trigger_button.configure(state="disabled")
        if update_status:
            self.update_bpm_flip_status()
            if was_running:
                self.last_event_var.set("Auto Swap stopped")

    def send_one_control(self, key: str, source: str = "manual") -> None:
        link, value, label = self.control_to_link_value_label(key)
        address = self.get_osc_address(link)
        self.send_osc_float(address, value, source, label)
        self.osc_vars[link].set(f"{value:.3f}")

    def resend_one_control(self, key: str, source: str = "resend") -> None:
        self.send_one_control(key, source=source)
        self.root.after(75, lambda current=key, current_source=source: self.send_one_control(current, source=current_source))
        self.last_event_var.set(f"Resent steady {key.replace('_', ' ')} value")

    def test_pulse(self, key: str) -> None:
        self.resend_one_control(key)

    def reset_one_control(self, key: str) -> None:
        if key in {"color1", "color2", "strobe_color"}:
            self.mark_manual_artwork_override("color reset")
        state = self.state.clone()
        default = make_state_from_template(self.default_template_var.get() or DEFAULT_TEMPLATE)
        if key == "color1":
            state.color1_name, state.color1_value = default.color1_name, default.color1_value
        elif key == "color2":
            state.color2_name, state.color2_value = default.color2_name, default.color2_value
        elif key == "strobe_color":
            state.strobe_color_name, state.strobe_color_value = default.strobe_color_name, default.strobe_color_value
        elif key == "motion":
            state.motion_value = default.motion_value
            state.strobe_percent = round(default.motion_value * 100)
            self.sync_strobe_value(state)
            state.motion_value = state.strobe_value
        elif key == "strobe":
            state.strobe_percent, state.strobe_value = default.strobe_percent, default.strobe_value
            self.sync_strobe_value(state)
        elif key == "saturation":
            state.saturation_percent, state.saturation_value = default.saturation_percent, default.saturation_value
        elif key == "brightness":
            state.brightness_percent, state.brightness_value = default.brightness_percent, default.brightness_value
        elif key == "fx":
            state.fx_value = default.fx_value
        elif key == "pulse":
            state.pulse_value = default.pulse_value
        self.apply_state(state, "reset", send=False)
        self.send_one_control(key)

    def control_to_link_value_label(self, key: str) -> tuple[int, float, str]:
        link = 3 if key == "strobe" else CONTROL_TO_LINK[key]
        if key == "color1":
            return link, self.state.color1_value, f"{self.link_label(link)} {self.state.color1_name}"
        if key == "color2":
            return link, self.state.color2_value, f"{self.link_label(link)} {self.state.color2_name}"
        if key == "motion":
            return link, self.state.motion_value, self.link_label(link)
        if key == "strobe":
            return link, self.state.strobe_value, f"{self.link_label(link)} {self.state.strobe_percent}%"
        if key == "strobe_color":
            return link, self.state.strobe_color_value, f"{self.link_label(link)} {self.state.strobe_color_name}"
        if key == "saturation":
            return link, self.state.saturation_value, f"{self.link_label(link)} {self.state.saturation_percent}%"
        if key == "brightness":
            return link, self.state.brightness_value, f"{self.link_label(link)} {self.state.brightness_percent}%"
        if key == "fx":
            return link, self.state.fx_value, self.link_label(link)
        if key == "pulse":
            return link, self.state.pulse_value, self.link_label(link)
        raise KeyError(key)

    def state_control_value_label(self, state: LightingState, key: str) -> tuple[float, str]:
        link = CONTROL_TO_LINK[key]
        if key == "color1":
            return state.color1_value, f"{self.link_label(link)} {state.color1_name}"
        if key == "color2":
            return state.color2_value, f"{self.link_label(link)} {state.color2_name}"
        if key == "motion":
            return state.motion_value, self.link_label(link)
        if key == "strobe_color":
            return state.strobe_color_value, f"{self.link_label(link)} {state.strobe_color_name}"
        if key == "saturation":
            return state.saturation_value, f"{self.link_label(link)} {state.saturation_percent}%"
        if key == "brightness":
            return state.brightness_value, f"{self.link_label(link)} {state.brightness_percent}%"
        if key == "fx":
            return state.fx_value, self.link_label(link)
        if key == "pulse":
            return state.pulse_value, self.link_label(link)
        raise KeyError(key)

    def state_link_values(self, state: LightingState) -> list[tuple[int, float, str]]:
        values = []
        for link, _label, key, _kind in LINK_CONTROL_SPECS:
            value, label = self.state_control_value_label(state, key)
            values.append((link, value, label))
        return values

    def send_state_osc(self, state: LightingState, source: str) -> None:
        for link, value, label in self.state_link_values(state):
            address = self.get_osc_address(link)
            self.send_osc_float(address, value, source, label)
            self.osc_vars[link].set(f"{value:.3f}")

    def osc_pad(self, value: bytes) -> bytes:
        padding = (4 - (len(value) % 4)) % 4
        return value + (b"\x00" * padding)

    def osc_string(self, value: str) -> bytes:
        return self.osc_pad(value.encode("utf-8") + b"\x00")

    def send_osc_float(self, address: str, value: float, source: str, label: str) -> None:
        address = self.clean_osc_address(address)
        packet = self.osc_string(address) + self.osc_string(",f") + struct.pack(">f", float(value))
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(packet, (self.osc_host_var.get().strip(), parse_int(self.osc_port_var.get(), watcher.RESOLUME_OSC_PORT, 1, 65535)))
            self.log_osc(source, address, value, label)
        except OSError as exc:
            self.log(f"ERROR: Could not send OSC {address}: {exc}\n")

    def send_osc_string(self, address: str, value: str, source: str, label: str) -> None:
        packet = self.osc_string(address) + self.osc_string(",s") + self.osc_string(value)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(packet, (self.osc_host_var.get().strip(), parse_int(self.osc_port_var.get(), watcher.RESOLUME_OSC_PORT, 1, 65535)))
            self.log_osc(source, address, 0.0, f"{label}: {value}")
        except OSError as exc:
            self.log(f"ERROR: Could not send OSC {address}: {exc}\n")

    def log_osc(self, source: str, address: str, value: float, label: str) -> None:
        timestamp = time.strftime("%H:%M:%S")
        self.log(f"{timestamp} | {source} | {address} | {value:.3f} | {label}\n")

    def daily_log_path(self) -> Path:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        return LOG_DIR / f"performance_lighting_{datetime.now().strftime('%Y-%m-%d')}.csv"

    def track_history_log_path(self) -> Path:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        date_text = datetime.now().strftime("%Y-%m-%d")
        path = LOG_DIR / f"track_color_history_{date_text}.csv"
        if path.exists():
            try:
                with path.open("r", newline="", encoding="utf-8") as handle:
                    header = next(csv.reader(handle), [])
                if header and header != TRACK_HISTORY_LOG_FIELDS:
                    return LOG_DIR / f"track_color_history_{date_text}_v2.csv"
            except OSError:
                pass
        return path

    def ensure_daily_log_file(self) -> Path:
        path = self.daily_log_path()
        if not path.exists():
            try:
                with path.open("w", newline="", encoding="utf-8") as handle:
                    csv.DictWriter(handle, fieldnames=DAILY_LOG_FIELDS).writeheader()
                self.daily_log_status_var.set(f"Created daily log: {path.name}")
            except OSError as exc:
                self.daily_log_status_var.set(f"Daily log failed: {exc}")
        return path

    def ensure_track_history_log_file(self) -> Path:
        path = self.track_history_log_path()
        if not path.exists():
            try:
                with path.open("w", newline="", encoding="utf-8") as handle:
                    csv.DictWriter(handle, fieldnames=TRACK_HISTORY_LOG_FIELDS).writeheader()
            except OSError as exc:
                self.daily_log_status_var.set(f"Track history log failed: {exc}")
        return path

    def state_osc_values_for_log(self, state: LightingState) -> list[dict[str, Any]]:
        values = []
        for link, value, label in self.state_link_values(state):
            values.append(
                {
                    "link": link,
                    "address": self.get_osc_address(link),
                    "value": round(float(value), 3),
                    "label": label,
                }
            )
        return values

    def track_history_row(
        self,
        action: str,
        state: LightingState,
        context: dict[str, str],
        source: str,
        note: str,
        matched_file: str = "",
        existing_comment: str = "",
    ) -> dict[str, str]:
        used_comment = self.template_from_state(state)
        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "action": action,
            "track": context.get("full_track", "-"),
            "artist": context.get("artist", ""),
            "title": context.get("title", ""),
            "album": context.get("album", ""),
            "bpm": context.get("bpm", ""),
            "existing_mp3_comment": existing_comment if existing_comment else context.get("comment", ""),
            "used_color_comment": used_comment,
            "suggested_color_comment": used_comment,
            "primary": state.color1_name,
            "secondary": state.color2_name,
            "accent": state.strobe_color_name,
            "source": source,
            "note": note,
            "matched_file": matched_file,
        }

    def write_track_history_row(self, row: dict[str, str], dedupe: bool = False) -> None:
        signature = json.dumps(
            {key: row.get(key, "") for key in ("action", "track", "used_color_comment", "source", "note")},
            sort_keys=True,
            ensure_ascii=False,
        )
        if dedupe and signature == self.last_simple_history_signature:
            return
        path = self.ensure_track_history_log_file()
        try:
            with path.open("a", newline="", encoding="utf-8") as handle:
                csv.DictWriter(handle, fieldnames=TRACK_HISTORY_LOG_FIELDS).writerow(row)
            self.last_simple_history_signature = signature
        except OSError as exc:
            self.daily_log_status_var.set(f"Track history log failed: {exc}")
            self.log(f"ERROR: Could not write track history log {path}: {exc}\n")

    def start_track_history(
        self,
        track_key: str,
        context: dict[str, str],
        matched_file: str,
        existing_comment: str,
        source: str,
        note: str,
    ) -> None:
        self.track_history_key = track_key
        self.track_history_context = dict(context)
        self.track_history_matched_file = matched_file
        self.track_history_existing_comment = existing_comment
        self.track_history_final_written = False
        self.track_history_final_source = source
        self.track_history_final_note = note

    def flush_track_history_end(self, reason: str = "track ended") -> None:
        if not self.track_history_key or self.track_history_final_written or not self.track_history_context:
            return
        source = self.track_history_final_source or self.state.source
        note = self.track_history_final_note or reason
        row = self.track_history_row(
            "track end",
            self.state,
            self.track_history_context,
            source,
            note,
            self.track_history_matched_file,
            self.track_history_existing_comment,
        )
        self.write_track_history_row(row)
        self.track_history_final_written = True

    def log_daily_track_decision(
        self,
        event: dict[str, Any],
        state: LightingState,
        details: dict[str, str],
        original_comment: str,
    ) -> None:
        path = self.ensure_daily_log_file()
        track = event.get("track", {})
        context = self.build_blt_context(track, event.get("track_info", ""), original_comment)
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "track": context.get("full_track", "-"),
            "title": context.get("title", ""),
            "artist": context.get("artist", ""),
            "album": context.get("album", ""),
            "bpm": context.get("bpm", ""),
            "matched_file": str(event.get("path", "")),
            "match_score": f"{float(event.get('score', 0.0)):.3f}",
            "comment_found": original_comment,
            "comment_to_add": self.template_from_state(state),
            "applied_source": details.get("source", state.source),
            "fallback_used": details.get("fallback", ""),
            "note": details.get("note", ""),
            "osc_values": json.dumps(self.state_osc_values_for_log(state), ensure_ascii=False),
        }
        simple_row = self.track_history_row(
            "track load",
            state,
            context,
            details.get("source", state.source),
            details.get("fallback", "") or details.get("note", ""),
            str(event.get("path", "")),
            original_comment,
        )
        try:
            with path.open("a", newline="", encoding="utf-8") as handle:
                csv.DictWriter(handle, fieldnames=DAILY_LOG_FIELDS).writerow(row)
            self.write_track_history_row(simple_row, dedupe=True)
            self.start_track_history(
                event.get("auto_track_key") or self.track_auto_key(track),
                context,
                str(event.get("path", "")),
                original_comment,
                details.get("source", state.source),
                "End state at next track load.",
            )
            self.daily_log_status_var.set(f"Wrote {path.name}: {row['track']}")
        except OSError as exc:
            self.daily_log_status_var.set(f"Daily log failed: {exc}")
            self.log(f"ERROR: Could not write daily track log {path}: {exc}\n")

    def build_blt_context(self, track: dict[str, str], track_info: str = "", comment: str = "") -> dict[str, str]:
        title = track.get("title", "").strip()
        artist = track.get("artist", "").strip()
        full_track = " - ".join(part for part in (artist, title) if part) or title or artist or "-"
        return {
            "title": title,
            "artist": artist,
            "album": track.get("album", "").strip(),
            "full_track": full_track,
            "track_info": track_info,
            "bpm": track.get("bpm", "").strip(),
            "player_number": track.get("player_number", "").strip(),
            "device_name": track.get("device_name", "").strip(),
            "source_player": track.get("source_player", "").strip(),
            "player": track.get("player", "").strip(),
            "comment": comment,
        }

    def send_blt_osc_outputs(
        self,
        context: dict[str, str],
        source: str = "track",
        fields: Optional[set[str]] = None,
    ) -> None:
        if not context:
            return
        for output in self.current_blt_osc_outputs():
            if not output.get("enabled"):
                continue
            field = str(output.get("field", "full_track"))
            if fields is not None and field not in fields:
                continue
            address = str(output.get("address", "")).strip()
            if not address:
                continue
            value = str(context.get(field, ""))
            label = str(output.get("label", field))
            self.send_osc_string(address, value, source, label)
            key = str(output.get("key", ""))
            if key in self.blt_osc_last_vars:
                self.blt_osc_last_vars[key].set(f"{address} = {value or '-'}")

    def test_blt_osc_outputs(self) -> None:
        context = self.latest_blt_context or {
            "title": "Test Title",
            "artist": "Test Artist",
            "album": "Test Album",
            "full_track": "Test Artist - Test Title",
            "track_info": "128 BPM | Player 1 CDJ",
            "bpm": "128",
            "player_number": "Player 1",
            "device_name": "CDJ",
            "source_player": "Player 1",
            "player": "1",
            "comment": "PRIMARY=indigo;SECONDARY=magenta",
        }
        self.send_blt_osc_outputs(context, source="test")

    def vinyl_blt_context(self) -> dict[str, str]:
        text = self.vinyl_track_text_var.get().strip() or DEFAULT_VINYL_TRACK_TEXT
        return self.manual_mode_blt_context(text, "vinyl", "turntable")

    def studio_blt_context(self) -> dict[str, str]:
        text = self.studio_track_text_var.get().strip() or DEFAULT_STUDIO_TRACK_TEXT
        return self.manual_mode_blt_context(text, "studio", "studio")

    def manual_mode_blt_context(self, text: str, player: str, device_name: str) -> dict[str, str]:
        return {
            "title": text,
            "artist": "",
            "album": player,
            "full_track": text,
            "track_info": text,
            "bpm": "",
            "player_number": player,
            "device_name": device_name,
            "source_player": player,
            "player": player,
            "comment": "",
        }

    def write_placeholder_artwork_to_output(
        self,
        source_path: Path,
        status_label: str,
        path_var: Optional[tk.StringVar] = None,
    ) -> bool:
        output_path = path_from_text(self.artwork_output_var.get(), artwork_module.OUTPUT_IMAGE)
        output_pixels = parse_int(self.output_size_var.get(), DEFAULT_OUTPUT_PIXELS, 64, 4096)
        temp_output_path = output_path.with_name(f"{output_path.stem}.tmp{output_path.suffix}")
        try:
            if path_var is not None:
                path_var.set(str(source_path))
            self.artwork_output_var.set(str(output_path))
            with Image.open(source_path) as source_image:
                source_image.load()
                image = ImageOps.exif_transpose(source_image).convert("RGBA")
                contained = ImageOps.contain(image, (output_pixels, output_pixels), method=Image.Resampling.LANCZOS)
                square = Image.new("RGBA", (output_pixels, output_pixels), (0, 0, 0, 255))
                left = (output_pixels - contained.width) // 2
                top = (output_pixels - contained.height) // 2
                square.alpha_composite(contained, dest=(left, top))
                output_path.parent.mkdir(parents=True, exist_ok=True)
                square.convert("RGB").save(temp_output_path, format="JPEG", quality=95, optimize=False, progressive=False, subsampling=0)
            temp_output_path.replace(output_path)
            with contextlib.suppress(OSError):
                os.utime(output_path, None)
            self.artwork_status_var.set(f"{status_label} active: {source_path.name}")
            self.refresh_artwork_preview(f"{status_label}: {source_path.name}")
            return True
        except Exception as exc:
            self.artwork_status_var.set(f"{status_label} failed: {exc}")
            self.log(f"ERROR: Could not write {status_label} artwork: {exc}\n")
            return False

    def write_vinyl_logo_to_artwork_file(self) -> bool:
        logo_path = path_from_text(self.vinyl_logo_path_var.get(), DEFAULT_VINYL_LOGO_PATH)
        return self.write_placeholder_artwork_to_output(logo_path, "Vinyl logo", self.vinyl_logo_path_var)

    def write_studio_artwork_to_artwork_file(self) -> bool:
        studio_path = path_from_text(self.studio_artwork_path_var.get(), DEFAULT_STUDIO_ARTWORK_PATH)
        return self.write_placeholder_artwork_to_output(studio_path, "NO TALKING STUDIO", self.studio_artwork_path_var)

    def enter_vinyl_mode(self) -> None:
        self.vinyl_mode_active = True
        self.manual_artwork_mode = "vinyl"
        self.save_config()
        self.flush_track_history_end("vinyl mode started")
        if self.write_vinyl_logo_to_artwork_file():
            self.palette = ArtworkPalette()
            self.refresh_palette_display()
        context = self.vinyl_blt_context()
        self.latest_blt_context = context
        self.latest_track_history_context = context
        self.active_track_var.set(context["full_track"])
        self.blt_status_var.set("Vinyl mode active; BLT/CDJ artwork paused")
        self.send_blt_osc_outputs(context, source="vinyl")
        self.last_event_var.set("Vinyl mode active; lights left unchanged")

    def enter_studio_mode(self) -> None:
        self.vinyl_mode_active = True
        self.manual_artwork_mode = "studio"
        self.save_config()
        self.flush_track_history_end("NO TALKING STUDIO mode started")
        if self.write_studio_artwork_to_artwork_file():
            self.palette = ArtworkPalette()
            self.refresh_palette_display()
        context = self.studio_blt_context()
        self.latest_blt_context = context
        self.latest_track_history_context = context
        self.active_track_var.set(context["full_track"])
        self.blt_status_var.set("NO TALKING STUDIO active; BLT/CDJ artwork paused")
        self.send_blt_osc_outputs(context, source="studio")
        self.last_event_var.set("NO TALKING STUDIO active; lights left unchanged")

    def exit_vinyl_mode(self) -> None:
        self.vinyl_mode_active = False
        self.manual_artwork_mode = ""
        self.save_config()
        self.current_track_auto_key = ""
        self.manual_artwork_override_track_key = ""
        self.last_event_var.set("CDJ mode resumed; waiting for next BLT poll")
        self.blt_status_var.set("CDJ mode resumed; BLT polling active")

    def test_link_number(self, link: int) -> None:
        for current_link, value, label in self.state_link_values(self.state):
            if current_link == link:
                address = self.get_osc_address(link)
                self.send_osc_float(address, value, "test", label)
                self.osc_vars[link].set(f"{value:.3f}")
                return

    def extract_palette_from_current_artwork(self, update_only: bool = False) -> None:
        path = path_from_text(self.artwork_output_var.get(), artwork_module.OUTPUT_IMAGE)
        if not path.exists():
            self.artwork_status_var.set("No current artwork file yet.")
            return
        try:
            with Image.open(path) as image:
                image = image.convert("RGB")
                small = image.resize((120, 120))
                colors = small.quantize(colors=48, method=Image.Quantize.MEDIANCUT).convert("RGB").getcolors(120 * 120)
        except Exception as exc:
            self.artwork_status_var.set(f"Palette unavailable: {exc}")
            return
        if not colors:
            return
        palette_colors = self.select_artwork_palette_colors(colors)
        if not palette_colors:
            self.artwork_status_var.set(f"No usable color palette found in {path.name}")
            return
        while len(palette_colors) < 3:
            palette_colors.append(palette_colors[-1])
        primary, secondary, accent = palette_colors[:3]
        self.palette = ArtworkPalette(
            dominant=rgb_to_palette_color(primary),
            accent=rgb_to_palette_color(secondary),
            bright_accent=rgb_to_palette_color(accent),
            available=True,
            source_path=str(path),
        )
        self.refresh_palette_display()
        self.artwork_status_var.set(f"Extracted palette from {path.name}")

    def select_artwork_palette_colors(self, colors: list[tuple[int, tuple[int, int, int]]]) -> list[tuple[int, int, int]]:
        candidates: list[tuple[float, int, tuple[int, int, int], float]] = []
        for count, rgb in colors:
            r, g, b = rgb
            hue, sat, val = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if val < 0.16 or sat < 0.22:
                continue
            score = (count ** 0.58) * (sat ** 2.8) * (val ** 1.45)
            candidates.append((score, count, rgb, hue))

        if not candidates:
            neutral_name = self.current_neutral_artwork_color()
            neutral_rgb = color_hex_to_rgb(COLOR_HEX[neutral_name])
            return [neutral_rgb, neutral_rgb, neutral_rgb]

        candidates.sort(reverse=True, key=lambda item: item[0])
        selected: list[tuple[int, int, int]] = []
        selected_hues: list[float] = []
        for _score, _count, rgb, hue in candidates:
            if all(PerformanceLightingGui.hue_distance(hue, other) >= 0.055 for other in selected_hues):
                selected.append(rgb)
                selected_hues.append(hue)
            if len(selected) == 3:
                return selected

        for _score, _count, rgb, _hue in candidates:
            if rgb not in selected:
                selected.append(rgb)
            if len(selected) == 3:
                break
        return selected

    @staticmethod
    def hue_distance(a: float, b: float) -> float:
        diff = abs(a - b) % 1.0
        return min(diff, 1.0 - diff)

    def draw_palette_swatch(self, key: str, canvas: tk.Canvas) -> None:
        color = getattr(self.palette, key, PaletteColor())
        width = max(canvas.winfo_width(), 2)
        height = max(canvas.winfo_height(), 2)
        canvas.delete("all")
        canvas.create_rectangle(2, 2, width - 2, height - 2, fill=color.hex, outline="#333333")

    def refresh_palette_display(self) -> None:
        for key in ("dominant", "accent", "bright_accent"):
            color = getattr(self.palette, key)
            self.palette_labels[key].set(f"{color.name}  {color.hue:.3f}  {color.hex}")
            for canvas in self.palette_swatches.get(key, []):
                self.draw_palette_swatch(key, canvas)

    def apply_palette_color_to_control(self, palette_key: str, control_key: str) -> None:
        if not self.palette.available:
            self.extract_palette_from_current_artwork(update_only=True)
        if not self.palette.available:
            return
        self.mark_manual_artwork_override("artwork color button")
        color = getattr(self.palette, palette_key)
        state = self.state.clone()
        if control_key == "color1":
            state.color1_name = color.name
            state.color1_value = color.hue
        elif control_key == "color2":
            state.color2_name = color.name
            state.color2_value = color.hue
        elif control_key == "strobe_color":
            state.strobe_color_name = color.name
            state.strobe_color_value = color.hue
        else:
            return
        state.source = "artwork"
        self.apply_state(state, "artwork", send=False)
        self.resend_one_control(control_key, source="artwork")
        self.last_event_var.set(f"Sent artwork {palette_key.replace('_', ' ')} to {control_key.replace('_', ' ')}")

    def force_apply_artwork_palette(self) -> None:
        if not self.palette.available:
            self.extract_palette_from_current_artwork(update_only=True)
        if not self.palette.available:
            return
        self.mark_manual_artwork_override("artwork palette apply")
        state = self.state.clone()
        self.apply_palette_to_state(state)
        state.source = "artwork"
        self.apply_state(state, "artwork", send=False)
        self.send_color_controls_only(source="artwork")
        self.last_event_var.set("Applied artwork palette colors only")

    def refresh_artwork_preview(self, status_text: str = "Saved current_artwork.jpg") -> None:
        path = path_from_text(self.artwork_output_var.get(), artwork_module.OUTPUT_IMAGE)
        if not path.exists():
            for label in self.artwork_preview_labels:
                label.configure(text="Artwork appears after first save", image="")
            return
        try:
            with Image.open(path) as image:
                image = image.convert("RGB")
                image.thumbnail((130, 130), Image.Resampling.LANCZOS)
                self.artwork_photo = ImageTk.PhotoImage(image)
            for label in self.artwork_preview_labels:
                label.configure(image=self.artwork_photo, text="")
            self.artwork_status_var.set(status_text)
        except Exception as exc:
            for label in self.artwork_preview_labels:
                label.configure(text=f"Preview unavailable: {exc}", image="")

    def template_from_state(self, state: LightingState) -> str:
        return ";".join(
            [
                f"PRIMARY={state.color1_name}",
                f"SECONDARY={state.color2_name}",
                f"STROBE={state.strobe_color_name}",
            ]
        )

    def update_template_from_state(self) -> None:
        self.template_var.set(self.template_from_state(self.state))
        self.last_event_var.set("Filled color comment with current primary, secondary, and accent")

    def copy_template(self) -> None:
        template = self.template_var.get().strip() or self.template_from_state(self.state)
        self.root.clipboard_clear()
        self.root.clipboard_append(template)
        self.last_event_var.set("Copied color comment to clipboard")

    def write_visual_defaults_config(self, state: LightingState) -> None:
        old_defaults = {
            "PRIMARY": state.color1_name,
            "SECONDARY": state.color2_name,
            "STROBE_PERCENT": str(state.strobe_percent),
            "STROBE": state.strobe_color_name,
            "SATURATION": str(state.saturation_percent),
            "BRIGHTNESS": str(state.brightness_percent),
        }
        try:
            VISUAL_DEFAULTS_CONFIG.parent.mkdir(parents=True, exist_ok=True)
            VISUAL_DEFAULTS_CONFIG.write_text(json.dumps(old_defaults, indent=2), encoding="utf-8")
        except OSError:
            pass

    def save_preset_editor(self, group: str) -> None:
        data = {
            self._current_preset_name(group, name): self._current_preset_values(group, name)
            for name in self.preset_editors.get(group, {})
        }
        self.set_preset_dict_for_group(group, data)
        self.save_config()
        frame = getattr(self, "performance_preset_frame", None)
        if frame is not None and group == "performance":
            self._build_performance_preset_buttons(frame)
        self.last_event_var.set(f"Saved {group} presets")

    def rebuild_library_index(self) -> None:
        if self.rebuild_thread and self.rebuild_thread.is_alive():
            self.last_event_var.set("Library index rebuild already running")
            return
        self.configure_runtime_modules()
        self.rebuild_thread = threading.Thread(target=self._rebuild_index_thread, daemon=True)
        self.rebuild_thread.start()
        self.last_event_var.set("Rebuilding music library index")

    def _rebuild_index_thread(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                entries = watcher.build_music_index()
                watcher.INDEX_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
                print(f"Indexed {len(entries)} tracks.")
            except Exception as exc:
                print(f"ERROR: Rebuild failed: {exc}")
        self.output_queue.put({"type": "log", "text": output.getvalue()})

    def open_artwork_folder(self) -> None:
        try:
            import subprocess

            output_path = path_from_text(self.artwork_output_var.get(), artwork_module.OUTPUT_IMAGE)
            subprocess.Popen(["explorer", str(output_path.parent)])
            self.last_event_var.set("Opened artwork output folder")
        except OSError as exc:
            messagebox.showerror("Could Not Open Folder", str(exc))

    def browse_fallback_artwork(self) -> None:
        current_path = path_from_text(self.fallback_artwork_path_var.get(), artwork_module.FALLBACK_ARTWORK_IMAGE)
        selected = filedialog.askopenfilename(
            title="Choose Fallback Artwork",
            initialdir=str(current_path.parent if current_path.parent.exists() else SCRIPT_DIR),
            filetypes=(
                ("Image files", "*.jpg *.jpeg *.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*"),
            ),
        )
        if not selected:
            return
        self.fallback_artwork_path_var.set(selected)
        self.configure_runtime_modules()
        self.save_config()
        self.last_event_var.set("Fallback artwork file updated")

    def open_fallback_artwork_folder(self) -> None:
        try:
            import subprocess

            fallback_path = path_from_text(self.fallback_artwork_path_var.get(), artwork_module.FALLBACK_ARTWORK_IMAGE)
            subprocess.Popen(["explorer", str(fallback_path.parent)])
            self.last_event_var.set("Opened fallback artwork folder")
        except OSError as exc:
            messagebox.showerror("Could Not Open Folder", str(exc))

    def open_track_folder(self) -> None:
        if not self.current_matched_file:
            messagebox.showinfo("No Track Yet", "No matched track file is available yet.")
            return
        try:
            import subprocess

            subprocess.Popen(["explorer", str(self.current_matched_file.parent)])
            self.last_event_var.set("Opened current track folder")
        except OSError as exc:
            messagebox.showerror("Could Not Open Folder", str(exc))

    def on_close(self) -> None:
        if self.watch_thread and self.watch_thread.is_alive():
            if not messagebox.askyesno("Quit", "The watcher is still running. Stop it and quit?"):
                return
            self.stop_event.set()
        self.stop_bpm_flip(update_status=False)
        self.flush_track_history_end("app closed")
        self.save_config()
        self.root.destroy()


def main() -> int:
    root = tk.Tk()
    app = PerformanceLightingGui(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
