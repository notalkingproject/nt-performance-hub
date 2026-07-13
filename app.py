"""Local web control surface for NT Performance Hub.

Serves the browser performance UI, local status/config APIs, OSC commands,
album-artwork helpers, linked looks, cameras, visuals, and show sequencing.
"""

from __future__ import annotations

import argparse
import colorsys
import contextlib
import io
import json
import mimetypes
import os
import re
import shutil
import socket
import struct
import subprocess
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from difflib import SequenceMatcher
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen


APP_VERSION = "nt-performance-hub"

PROJECT_ROOT = Path(__file__).resolve().parent
WEB_ROOT = PROJECT_ROOT / "web"
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_PATH = CONFIG_DIR / "app_config.json"
LEGACY_CONFIG_GLOB = "performance_lighting_gui*_config.json"
INDEX_PATH = DATA_DIR / "music_library_index.json"
LEGACY_INDEX_PATH = PROJECT_ROOT / "music_library_index.json"
DEFAULT_ARTWORK_OUTPUT = DATA_DIR / "current_artwork.jpg"
DEFAULT_OUTPUT_PIXELS = 1024
ARTWORK_SIZE_MIN = 64
ARTWORK_SIZE_MAX = 4096
ARTWORK_SIZE_SOURCES = ("cdj", "fallback", "vinyl", "studio", "videogame")
DEFAULT_VINYL_LOGO_PATH = str(ASSETS_DIR / "NO_TALKING_DOUGHNUT_LOGO_2.png")
DEFAULT_VINYL_TRACK_TEXT = "Record Playing"
DEFAULT_STUDIO_ARTWORK_PATH = str(ASSETS_DIR / "NO_TALKING_STUDIO.png")
DEFAULT_STUDIO_TRACK_TEXT = "NO TALKING STUDIO"
DEFAULT_VIDEOGAME_ARTWORK_PATH = str(ASSETS_DIR / "NO_TALKING_DOUGHNUT_LOGO_2.png")
DEFAULT_VIDEOGAME_TRACK_TEXT = "Ravenswatch"
BLT_SOURCE_TIMEOUT_SECONDS = 0.45
BLT_POLL_TIMEOUT_SECONDS = 0.9
STATIC_ASSET_CACHE_SECONDS = 120
SERVER_START_TIME = time.time()
DEFAULT_TEMPLATE = (
    "COLOR1=indigo;COLOR2=magenta;MOOD=club;ENERGY=3;SECTION=GROOVE;"
    "STROBE_PERCENT=10;COLOR3=purple;SATURATION=100;BRIGHTNESS=100;"
    "MOTION=50;FX=25;PULSE=0"
)
COLOR_HUE_VALUES = {
    "red": 0 / 360,
    "scarlet": 15 / 360,
    "orange": 30 / 360,
    "amber": 45 / 360,
    "yellow": 60 / 360,
    "chartreuse": 75 / 360,
    "lime": 90 / 360,
    "spring": 105 / 360,
    "green": 120 / 360,
    "emerald": 135 / 360,
    "mint": 150 / 360,
    "teal": 165 / 360,
    "cyan": 180 / 360,
    "sky": 195 / 360,
    "azure": 210 / 360,
    "royal": 225 / 360,
    "blue": 240 / 360,
    "indigo": 255 / 360,
    "violet": 270 / 360,
    "purple": 285 / 360,
    "magenta": 300 / 360,
    "fuchsia": 315 / 360,
    "pink": 330 / 360,
    "rose": 345 / 360,
}
COLOR_HEX = {
    "red": "#ff0000",
    "scarlet": "#ff4000",
    "orange": "#ff8000",
    "amber": "#ffbf00",
    "yellow": "#ffff00",
    "chartreuse": "#bfff00",
    "lime": "#80ff00",
    "spring": "#40ff00",
    "green": "#00ff00",
    "emerald": "#00ff40",
    "mint": "#00ff80",
    "teal": "#00ffbf",
    "cyan": "#00ffff",
    "sky": "#00bfff",
    "azure": "#0080ff",
    "royal": "#0040ff",
    "blue": "#0000ff",
    "indigo": "#4000ff",
    "violet": "#8000ff",
    "purple": "#bf00ff",
    "magenta": "#ff00ff",
    "fuchsia": "#ff00bf",
    "pink": "#ff0080",
    "rose": "#ff0040",
}
ARTWORK_MIN_SATURATION = 0.22
ARTWORK_MIN_USABLE_VALUE = 0.24
ARTWORK_MIN_BRIGHT_VALUE = 0.36
ARTWORK_MIN_COLORFUL_RATIO = 0.08
ARTWORK_MIN_BRIGHT_RATIO = 0.045
ARTWORK_PRIMARY_HUE_SEPARATION = 0.075
ARTWORK_ACCENT_HUE_SEPARATION = 0.045
GEN_VISUAL_PRESET_DEFS = {
    "lissajous_orbit": {
        "name": "Lissajous Orbit",
        "renderer": "canvas2d",
        "base": "lissajous_orbit",
        "intensity": 0.72,
        "complexity": 0.48,
        "motion": 0.62,
        "beat_response": 0.52,
        "color_source": "look",
        "quality": "medium",
        "category": "Line Geometry",
        "mood": "Elegant / Hypnotic",
        "best_for": "melodic sections, intro loops, smooth transitions",
        "notes": "Parametric sine/cosine orbit lines for beat-aware motion.",
    },
    "moire_grid": {
        "name": "Moire Grid",
        "renderer": "canvas2d",
        "base": "moire_grid",
        "intensity": 0.58,
        "complexity": 0.58,
        "motion": 0.38,
        "beat_response": 0.46,
        "color_source": "look",
        "quality": "medium",
        "category": "Interference",
        "mood": "Tense / Technical",
        "best_for": "builds, minimal techno, texture beds",
        "notes": "Rotating grid interference for projected texture.",
    },
    "superformula_mandala": {
        "name": "Superformula Mandala",
        "renderer": "canvas2d",
        "base": "superformula_mandala",
        "intensity": 0.68,
        "complexity": 0.6,
        "motion": 0.42,
        "beat_response": 0.5,
        "color_source": "look",
        "quality": "medium",
        "category": "Polar Form",
        "mood": "Sacred / Focused",
        "best_for": "breakdowns, held moments, centered stage looks",
        "notes": "Polar flower and mandala lines with phrase morphing.",
    },
    "particle_vortex": {
        "name": "Particle Vortex",
        "renderer": "canvas2d",
        "base": "particle_vortex",
        "intensity": 0.68,
        "complexity": 0.64,
        "motion": 0.74,
        "beat_response": 0.62,
        "color_source": "look",
        "quality": "medium",
        "category": "Particles",
        "mood": "Kinetic / Airy",
        "best_for": "drops, high-energy passages, motion-heavy looks",
        "notes": "Particles following a polar sine vector field.",
    },
    "shader_plasma": {
        "name": "Shader Plasma",
        "renderer": "webgl-shader",
        "base": "shader_plasma",
        "intensity": 0.64,
        "complexity": 0.52,
        "motion": 0.46,
        "beat_response": 0.5,
        "color_source": "look",
        "quality": "medium",
        "category": "Shader",
        "mood": "Electric / Fluid",
        "best_for": "ambient fills, color washes, continuous motion",
        "notes": "Stable fragment shader plasma with Beat Link uniforms.",
    },
    "harmonic_tunnel": {
        "name": "Harmonic Tunnel",
        "renderer": "canvas2d",
        "base": "harmonic_tunnel",
        "intensity": 0.7,
        "complexity": 0.58,
        "motion": 0.58,
        "beat_response": 0.6,
        "color_source": "look",
        "quality": "medium",
        "category": "Perspective",
        "mood": "Deep / Driving",
        "best_for": "forward momentum, tunnels, long transitions",
        "notes": "Beat-pulsed nested rings with rotational tunnel depth.",
    },
    "vector_field": {
        "name": "Vector Field",
        "renderer": "canvas2d",
        "base": "vector_field",
        "intensity": 0.62,
        "complexity": 0.72,
        "motion": 0.55,
        "beat_response": 0.54,
        "color_source": "look",
        "quality": "medium",
        "category": "Field Lines",
        "mood": "Scientific / Nervous",
        "best_for": "glitchy sections, analytical textures, mid-song motion",
        "notes": "Curved directional strokes from a sine/cosine force field.",
    },
    "crystal_rings": {
        "name": "Crystal Rings",
        "renderer": "canvas2d",
        "base": "crystal_rings",
        "intensity": 0.66,
        "complexity": 0.5,
        "motion": 0.34,
        "beat_response": 0.48,
        "color_source": "look",
        "quality": "medium",
        "category": "Radial",
        "mood": "Clean / Ceremonial",
        "best_for": "symmetrical lighting looks, stings, logo moments",
        "notes": "Facet rings and mirrored spokes for clean geometric looks.",
    },
    "wave_ribbons": {
        "name": "Wave Ribbons",
        "renderer": "canvas2d",
        "base": "wave_ribbons",
        "intensity": 0.64,
        "complexity": 0.58,
        "motion": 0.5,
        "beat_response": 0.46,
        "color_source": "look",
        "quality": "medium",
        "category": "Ribbons",
        "mood": "Smooth / Liquid",
        "best_for": "vocals, house grooves, soft color blending",
        "notes": "Layered sine ribbons that drift and braid across the frame.",
    },
    "starfield_gate": {
        "name": "Starfield Gate",
        "renderer": "canvas2d",
        "base": "starfield_gate",
        "intensity": 0.66,
        "complexity": 0.62,
        "motion": 0.7,
        "beat_response": 0.58,
        "color_source": "look",
        "quality": "medium",
        "category": "Depth",
        "mood": "Expansive / Cosmic",
        "best_for": "openers, breakdown lifts, spacey transitions",
        "notes": "Perspective particles rushing through a geometric gate.",
    },
    "kaleido_mesh": {
        "name": "Kaleido Mesh",
        "renderer": "canvas2d",
        "base": "kaleido_mesh",
        "intensity": 0.7,
        "complexity": 0.68,
        "motion": 0.48,
        "beat_response": 0.52,
        "color_source": "look",
        "quality": "medium",
        "category": "Kaleido",
        "mood": "Prismatic / Busy",
        "best_for": "choruses, peak sections, maximal color looks",
        "notes": "Mirrored triangular mesh with rotating color facets.",
    },
    "liquid_topo": {
        "name": "Liquid Topo",
        "renderer": "canvas2d",
        "base": "liquid_topo",
        "intensity": 0.58,
        "complexity": 0.56,
        "motion": 0.36,
        "beat_response": 0.42,
        "color_source": "look",
        "quality": "medium",
        "category": "Contour",
        "mood": "Organic / Subtle",
        "best_for": "ambient holds, lower-energy sections, background layers",
        "notes": "Contour-line topology that breathes around the beat.",
    },
    "pulse_bars": {
        "name": "Pulse Bars",
        "renderer": "canvas2d",
        "base": "pulse_bars",
        "intensity": 0.74,
        "complexity": 0.45,
        "motion": 0.4,
        "beat_response": 0.72,
        "color_source": "look",
        "quality": "medium",
        "category": "Rhythm",
        "mood": "Direct / Punchy",
        "best_for": "beat drops, simple stage hits, strong rhythm sections",
        "notes": "Stacked bars and gates that breathe with beat energy.",
    },
    "constellation_web": {
        "name": "Constellation Web",
        "renderer": "canvas2d",
        "base": "constellation_web",
        "intensity": 0.6,
        "complexity": 0.7,
        "motion": 0.46,
        "beat_response": 0.48,
        "color_source": "look",
        "quality": "medium",
        "category": "Network",
        "mood": "Delicate / Intelligent",
        "best_for": "bridges, tech visuals, detailed projector texture",
        "notes": "Animated point network with short glowing link lines.",
    },
    "scanline_bloom": {
        "name": "Scanline Bloom",
        "renderer": "canvas2d",
        "base": "scanline_bloom",
        "intensity": 0.7,
        "complexity": 0.52,
        "motion": 0.58,
        "beat_response": 0.56,
        "color_source": "look",
        "quality": "medium",
        "category": "Retro",
        "mood": "Analog / Neon",
        "best_for": "retro sections, darker looks, stylized transitions",
        "notes": "Horizontal scanlines with soft bloom and beat shimmer.",
    },
    "orbital_dust": {
        "name": "Orbital Dust",
        "renderer": "canvas2d",
        "base": "orbital_dust",
        "intensity": 0.64,
        "complexity": 0.6,
        "motion": 0.64,
        "beat_response": 0.5,
        "color_source": "look",
        "quality": "medium",
        "category": "Particles",
        "mood": "Dreamy / Circular",
        "best_for": "melodic grooves, soft transitions, background motion",
        "notes": "Dust points orbit in layered ellipses with glowing trails.",
    },
}
GEN_VISUAL_PRESET_ORDER = tuple(GEN_VISUAL_PRESET_DEFS.keys())
GEN_VISUAL_COLOR_SOURCES = {"look", "album", "track", "manual"}
GEN_VISUAL_QUALITIES = {"low", "medium", "high"}
GEN_VISUAL_AUTOMATION_TARGETS = {"intensity", "complexity", "motion", "beat_response", "scale", "zoom", "rotation", "symmetry", "warp", "line_width", "trail", "opacity"}
GEN_VISUAL_AUTOMATION_MODES = {"bpm", "seconds"}
GEN_VISUAL_AUTOMATION_SHAPES = {"sine", "triangle", "saw", "pulse"}
GEN_VISUAL_LAYER_STYLES = {"none", "glow_grid", "scanlines", "vignette", "echo", "sparkle"}
DEFAULT_GENERATIVE_VISUAL = {
    "enabled": True,
    "preset": "lissajous_orbit",
    "color_source": "look",
    "intensity": 0.72,
    "complexity": 0.48,
    "motion": 0.62,
    "beat_response": 0.52,
    "scale": 0.54,
    "zoom": 0.5,
    "rotation": 0.42,
    "symmetry": 0.5,
    "warp": 0.38,
    "line_width": 0.42,
    "trail": 0.56,
    "automation_enabled": False,
    "automation_target": "warp",
    "automation_mode": "bpm",
    "automation_division": "1 bar",
    "automation_shape": "sine",
    "automation_depth": 0.35,
    "automation_offset": 0.5,
    "layer_enabled": True,
    "layer_style": "glow_grid",
    "layer_mix": 0.32,
    "layer_speed": 0.4,
    "phrase_morph": True,
    "auto_seed": True,
    "quality": "medium",
    "opacity": 1.0,
    "freeze": False,
    "blackout": False,
    "seed": 1,
}
GEN_VISUAL_PRESET_RECIPES = {
    "lissajous_orbit": {"scale": 0.58, "zoom": 0.46, "rotation": 0.36, "symmetry": 0.42, "warp": 0.32, "line_width": 0.48, "trail": 0.68, "automation_target": "rotation", "automation_division": "4 bars", "automation_depth": 0.18, "automation_offset": 0.36},
    "moire_grid": {"scale": 0.44, "zoom": 0.52, "rotation": 0.64, "symmetry": 0.82, "warp": 0.24, "line_width": 0.28, "trail": 0.42, "automation_target": "rotation", "automation_division": "8 bars", "automation_depth": 0.24, "automation_offset": 0.64},
    "superformula_mandala": {"scale": 0.62, "zoom": 0.48, "rotation": 0.5, "symmetry": 0.86, "warp": 0.46, "line_width": 0.52, "trail": 0.58, "automation_target": "symmetry", "automation_division": "16 bars", "automation_depth": 0.2, "automation_offset": 0.86},
    "particle_vortex": {"scale": 0.7, "zoom": 0.62, "rotation": 0.58, "symmetry": 0.48, "warp": 0.62, "line_width": 0.22, "trail": 0.82, "automation_target": "warp", "automation_division": "2 bars", "automation_depth": 0.32, "automation_offset": 0.62},
    "shader_plasma": {"scale": 0.5, "zoom": 0.58, "rotation": 0.48, "symmetry": 0.36, "warp": 0.72, "line_width": 0.42, "trail": 0.5, "automation_target": "warp", "automation_division": "4 bars", "automation_depth": 0.3, "automation_offset": 0.72},
    "harmonic_tunnel": {"scale": 0.66, "zoom": 0.76, "rotation": 0.54, "symmetry": 0.58, "warp": 0.42, "line_width": 0.46, "trail": 0.64, "automation_target": "zoom", "automation_division": "2 bars", "automation_depth": 0.28, "automation_offset": 0.76},
    "vector_field": {"scale": 0.54, "zoom": 0.45, "rotation": 0.4, "symmetry": 0.62, "warp": 0.72, "line_width": 0.3, "trail": 0.5, "automation_target": "warp", "automation_division": "1 bar", "automation_depth": 0.34, "automation_offset": 0.72},
    "crystal_rings": {"scale": 0.6, "zoom": 0.5, "rotation": 0.46, "symmetry": 0.92, "warp": 0.24, "line_width": 0.5, "trail": 0.54, "automation_target": "scale", "automation_division": "4 bars", "automation_depth": 0.2, "automation_offset": 0.6},
    "wave_ribbons": {"scale": 0.48, "zoom": 0.56, "rotation": 0.34, "symmetry": 0.46, "warp": 0.64, "line_width": 0.58, "trail": 0.72, "automation_target": "warp", "automation_division": "8 bars", "automation_depth": 0.26, "automation_offset": 0.64},
    "starfield_gate": {"scale": 0.72, "zoom": 0.82, "rotation": 0.56, "symmetry": 0.5, "warp": 0.38, "line_width": 0.24, "trail": 0.5, "automation_target": "zoom", "automation_division": "1 bar", "automation_depth": 0.35, "automation_offset": 0.82},
    "kaleido_mesh": {"scale": 0.58, "zoom": 0.52, "rotation": 0.6, "symmetry": 0.95, "warp": 0.52, "line_width": 0.34, "trail": 0.48, "automation_target": "rotation", "automation_division": "2 bars", "automation_depth": 0.28, "automation_offset": 0.6},
    "liquid_topo": {"scale": 0.42, "zoom": 0.48, "rotation": 0.42, "symmetry": 0.5, "warp": 0.7, "line_width": 0.42, "trail": 0.78, "automation_target": "warp", "automation_division": "16 bars", "automation_depth": 0.24, "automation_offset": 0.7},
    "pulse_bars": {"scale": 0.52, "zoom": 0.44, "rotation": 0.5, "symmetry": 0.36, "warp": 0.26, "line_width": 0.32, "trail": 0.38, "automation_target": "scale", "automation_division": "1/2 bar", "automation_shape": "pulse", "automation_depth": 0.36, "automation_offset": 0.52},
    "constellation_web": {"scale": 0.56, "zoom": 0.62, "rotation": 0.52, "symmetry": 0.7, "warp": 0.44, "line_width": 0.22, "trail": 0.66, "automation_target": "symmetry", "automation_division": "4 bars", "automation_depth": 0.22, "automation_offset": 0.7},
    "scanline_bloom": {"scale": 0.33, "zoom": 0.57, "rotation": 1.0, "symmetry": 0.5, "warp": 0.38, "line_width": 0.25, "trail": 0.56, "automation_target": "warp", "automation_division": "1 bar", "automation_depth": 0.2, "automation_offset": 0.38},
    "orbital_dust": {"scale": 0.68, "zoom": 0.58, "rotation": 0.62, "symmetry": 0.55, "warp": 0.5, "line_width": 0.2, "trail": 0.86, "automation_target": "rotation", "automation_division": "8 bars", "automation_depth": 0.2, "automation_offset": 0.62},
}
SORTED_COLOR_NAMES = [name for name, _value in sorted(COLOR_HUE_VALUES.items(), key=lambda item: (item[1], item[0]))]
PERCENT_CHOICES = [0, 10, 25, 50, 75, 90, 95, 100]
PRESET_GROUP_KEYS = {
    "performance": "performance_presets",
    "mood": "mood_presets",
    "energy": "energy_presets",
    "section": "section_presets",
}
PRESET_GROUP_LABELS = {
    "performance": "Performance Presets",
    "mood": "Mood Presets",
    "energy": "Energy Presets",
    "section": "Section Presets",
}
LINK_CONTROL_SPECS: tuple[tuple[int, str, str, str], ...] = (
    (1, "Color 1", "color1", "color"),
    (2, "Color 2", "color2", "color"),
    (3, "Motion / Energy", "motion", "percent_buttons"),
    (4, "Color 3", "strobe_color", "color"),
    (5, "Saturation", "saturation", "percent_buttons"),
    (6, "Brightness", "brightness", "percent_buttons"),
    (7, "FX / Pattern", "fx", "percent_buttons"),
    (8, "Pulse / Color 3", "pulse", "percent_buttons"),
)
COLOR_SLOT_KEYS = ("color1", "color2", "strobe_color")
COLOR_SLOT_LABELS = {"color1": "Color 1", "color2": "Color 2", "strobe_color": "Color 3"}
DEFAULT_BPM_ROTATION_SLOTS = list(COLOR_SLOT_KEYS)
CONTROL_TO_LINK = {key: link for link, _label, key, _kind in LINK_CONTROL_SPECS}
COLOR_LINK_NUMBERS = {CONTROL_TO_LINK[key] for key in COLOR_SLOT_KEYS}
DEFAULT_LINK_LABELS = {str(link): label for link, label, _key, _kind in LINK_CONTROL_SPECS}
DEFAULT_OSC_ADDRESSES = {
    str(link): f"/composition/layers/1/clips/2/dashboard/link{link}"
    for link in range(1, 9)
}
DEFAULT_OSC_OUTPUT_SLOTS = 3
COLOR_OSC_OUTPUT_SLOTS = 10
EXTRA_OSC_ADDRESS_SLOTS = DEFAULT_OSC_OUTPUT_SLOTS - 1


def osc_output_slots_for_link(link: Any) -> int:
    try:
        link_number = int(str(link).strip())
    except (TypeError, ValueError):
        return DEFAULT_OSC_OUTPUT_SLOTS
    return COLOR_OSC_OUTPUT_SLOTS if link_number in COLOR_LINK_NUMBERS else DEFAULT_OSC_OUTPUT_SLOTS


def extra_osc_address_slots_for_link(link: Any) -> int:
    return max(0, osc_output_slots_for_link(link) - 1)
DEFAULT_BLT_OSC_OUTPUTS: list[dict[str, Any]] = [
    {"key": "title", "label": "BLT Title", "field": "title", "address": "/blt/title", "enabled": True},
    {"key": "artist", "label": "BLT Artist", "field": "artist", "address": "/blt/artist", "enabled": True},
    {"key": "track", "label": "BLT Track", "field": "full_track", "address": "/blt/track", "enabled": True},
    {"key": "track_info", "label": "BLT Track Info", "field": "track_info", "address": "/blt/track-info", "enabled": True},
    {
        "key": "resolume_track_text",
        "label": "Resolume Track Text",
        "field": "full_track",
        "address": "/composition/layers/28/clips/2/video/source/blocktextgenerator/text/params/lines",
        "enabled": True,
    },
    {
        "key": "resolume_track_info",
        "label": "Resolume Track Info",
        "field": "track_info",
        "address": "/composition/layers/27/clips/2/video/source/blocktextgenerator/text/params/lines",
        "enabled": True,
    },
]
CAMERA_GROUP_SPECS = (
    ("main_box", "Main Box Cams"),
    ("pip_box", "PIP Box Cams"),
    ("background", "Background Cams"),
)
DEFAULT_CAMERA_OPACITY_LABELS = {
    "main_box": "Main Box Mix",
    "pip_box": "PIP Box Mix",
    "background": "BG Cam Mix",
}
DEFAULT_NOW_PLAYING_OPACITY_LABEL = "Now Playing Opacity"
CAMERA_COLUMN_LABELS = ("Set 1", "Set 2", "Set 3", "Set 4")
SCENE_BUTTON_COUNT = 15
VISUAL_LAYER_COUNT = 3
VISUAL_CLIPS_PER_LAYER = 10
VISUAL_BUTTON_COUNT = VISUAL_LAYER_COUNT * VISUAL_CLIPS_PER_LAYER
BLT_FIELD_CHOICES = [
    "title",
    "artist",
    "album",
    "full_track",
    "track_info",
    "bpm",
    "player_number",
    "device_name",
    "source_player",
    "player",
    "comment",
]
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
    ("32 bars", 128.0),
)
BPM_FLIP_DIVISION_MULTIPLIERS = dict(BPM_FLIP_DIVISIONS)
BPM_FLIP_MIN_SECONDS = 0.1
BPM_FLIP_MAX_SECONDS = 3600.0

DEFAULT_CONNECTION_PROFILES: list[dict[str, Any]] = [
    {
        "id": "show_pc_local",
        "name": "Show PC Local",
        "mode": "Local",
        "app_bind_host": "127.0.0.1",
        "app_port": 8080,
        "public_control_url": "http://127.0.0.1:8080/",
        "beatlink_host": "127.0.0.1",
        "beatlink_port": 8088,
        "beatlink_base_url": "http://127.0.0.1:8088/",
        "resolume_host": "127.0.0.1",
        "resolume_port": 7000,
        "visualizer_url": "/visuals/generative",
    },
    {
        "id": "laptop_dev_to_pc",
        "name": "Laptop Dev to PC",
        "mode": "Development",
        "app_bind_host": "0.0.0.0",
        "app_port": 8080,
        "public_control_url": "",
        "beatlink_host": "",
        "beatlink_port": 8088,
        "beatlink_base_url": "",
        "resolume_host": "",
        "resolume_port": 7000,
        "visualizer_url": "/visuals/generative",
    },
    {
        "id": "pc_server_tablet",
        "name": "PC Server + Tablet Control",
        "mode": "LAN",
        "app_bind_host": "0.0.0.0",
        "app_port": 8080,
        "public_control_url": "",
        "beatlink_host": "",
        "beatlink_port": 8088,
        "beatlink_base_url": "",
        "resolume_host": "127.0.0.1",
        "resolume_port": 7000,
        "visualizer_url": "/visuals/generative",
    },
    {
        "id": "manual_advanced",
        "name": "Manual Advanced",
        "mode": "Manual",
        "app_bind_host": "0.0.0.0",
        "app_port": 8080,
        "public_control_url": "",
        "beatlink_host": "",
        "beatlink_port": 8088,
        "beatlink_base_url": "",
        "resolume_host": "",
        "resolume_port": 7000,
        "visualizer_url": "/visuals/generative",
    },
]

MATH_SCENE_TEMPLATES: list[dict[str, Any]] = [
    {
        "id": "complex_domain_bloom",
        "name": "Complex Domain Bloom",
        "category": "Fractal Field",
        "math_family": "Complex functions",
        "description": "A luminous complex-plane bloom that curls around roots, poles, and color bands.",
        "mood": "Electric, fluid, dimensional",
        "best_for": "color washes, atmospheric intros, album-art driven palettes",
        "renderer": "webgl-shader",
        "performance_cost": "Medium",
        "style_tags": ["complex", "bloom", "shader"],
        "preset": "shader_plasma",
        "recommended_controls": ["warp", "intensity", "color_source", "automation_depth"],
        "scene": {"intensity": 0.68, "complexity": 0.64, "motion": 0.52, "beat_response": 0.5, "warp": 0.78, "trail": 0.58, "automation_enabled": True, "automation_target": "warp", "automation_division": "4 bars"},
    },
    {
        "id": "fourier_epicycle_signal",
        "name": "Fourier Epicycle Signal",
        "category": "Signal Motion",
        "math_family": "Fourier series",
        "description": "Nested rotating circles trace a clean waveform path, like a musical signal becoming geometry.",
        "mood": "Elegant, precise, musical",
        "best_for": "melodic loops, breakdowns, smooth transitions",
        "renderer": "canvas2d",
        "performance_cost": "Low",
        "style_tags": ["signal", "epicycle", "line"],
        "preset": "lissajous_orbit",
        "recommended_controls": ["rotation", "line_width", "symmetry", "automation_division"],
        "scene": {"intensity": 0.7, "complexity": 0.56, "motion": 0.58, "beat_response": 0.56, "line_width": 0.52, "automation_enabled": True, "automation_target": "rotation", "automation_division": "2 bars"},
    },
    {
        "id": "ode_lorenz_trace",
        "name": "Lorenz Trace",
        "category": "Chaos Trail",
        "math_family": "ODE attractor",
        "description": "A chaotic attractor-style particle trail with long memory and orbiting motion.",
        "mood": "Unstable, hypnotic, airy",
        "best_for": "tension builds, deep grooves, evolving background motion",
        "renderer": "canvas2d",
        "performance_cost": "Medium",
        "style_tags": ["chaos", "particles", "trail"],
        "preset": "particle_vortex",
        "recommended_controls": ["trail", "motion", "warp", "beat_response"],
        "scene": {"intensity": 0.66, "complexity": 0.74, "motion": 0.76, "beat_response": 0.58, "trail": 0.88, "warp": 0.62, "automation_enabled": True, "automation_target": "warp", "automation_division": "2 bars"},
    },
    {
        "id": "vector_spiral_flow",
        "name": "Spiral Flow",
        "category": "Vector Field",
        "math_family": "Divergence/curl fields",
        "description": "Curved vector strokes spiral through a force field with beat-aware flow strength.",
        "mood": "Scientific, nervous, propulsive",
        "best_for": "glitchy sections, analytical textures, mid-song motion",
        "renderer": "canvas2d",
        "performance_cost": "Low",
        "style_tags": ["field", "spiral", "strokes"],
        "preset": "vector_field",
        "recommended_controls": ["complexity", "warp", "motion", "scale"],
        "scene": {"intensity": 0.62, "complexity": 0.78, "motion": 0.58, "beat_response": 0.54, "warp": 0.76, "automation_enabled": True, "automation_target": "warp", "automation_division": "1 bar"},
    },
    {
        "id": "fractal_julia_tunnel",
        "name": "Julia Tunnel",
        "category": "Fractal Depth",
        "math_family": "Julia sets",
        "description": "A tunnel-like fractal mood with mirrored structure and a pulsing zoom center.",
        "mood": "Deep, prismatic, immersive",
        "best_for": "long transitions, peak tunnels, projected depth",
        "renderer": "webgl-shader",
        "performance_cost": "High",
        "style_tags": ["fractal", "tunnel", "depth"],
        "preset": "harmonic_tunnel",
        "recommended_controls": ["zoom", "symmetry", "rotation", "quality"],
        "scene": {"intensity": 0.72, "complexity": 0.68, "motion": 0.62, "beat_response": 0.62, "zoom": 0.8, "warp": 0.5, "automation_enabled": True, "automation_target": "zoom", "automation_division": "2 bars"},
    },
    {
        "id": "oscilloscope_stack",
        "name": "Oscilloscope Stack",
        "category": "Rhythm Signal",
        "math_family": "Wave synthesis",
        "description": "Layered signal lines and scan bands that read like an audio scope on stage.",
        "mood": "Analog, neon, direct",
        "best_for": "retro sections, beat drops, clearly rhythmic cues",
        "renderer": "canvas2d",
        "performance_cost": "Low",
        "style_tags": ["wave", "scanline", "rhythm"],
        "preset": "scanline_bloom",
        "recommended_controls": ["beat_response", "line_width", "trail", "motion"],
        "scene": {"intensity": 0.72, "complexity": 0.54, "motion": 0.58, "beat_response": 0.68, "line_width": 0.3, "automation_enabled": True, "automation_target": "scale", "automation_shape": "pulse", "automation_division": "1/2 bar"},
    },
    {
        "id": "liquid_topography",
        "name": "Liquid Topography",
        "category": "Contour Field",
        "math_family": "Scalar fields",
        "description": "Breathing contour lines suggest terrain, water, and slow pressure changes.",
        "mood": "Organic, subtle, liquid",
        "best_for": "ambient holds, lower-energy sections, texture layers",
        "renderer": "canvas2d",
        "performance_cost": "Low",
        "style_tags": ["contour", "topography", "liquid"],
        "preset": "liquid_topo",
        "recommended_controls": ["warp", "trail", "scale", "automation_depth"],
        "scene": {"intensity": 0.6, "complexity": 0.58, "motion": 0.38, "beat_response": 0.44, "warp": 0.72, "trail": 0.8, "automation_enabled": True, "automation_target": "warp", "automation_division": "16 bars"},
    },
    {
        "id": "superformula_organism",
        "name": "Superformula Organism",
        "category": "Organic Geometry",
        "math_family": "Superformula",
        "description": "Mandala-like polar organisms that bloom, fold, and hold a strong center.",
        "mood": "Sacred, focused, alive",
        "best_for": "breakdowns, centered stage looks, held moments",
        "renderer": "canvas2d",
        "performance_cost": "Medium",
        "style_tags": ["polar", "mandala", "organism"],
        "preset": "superformula_mandala",
        "recommended_controls": ["symmetry", "scale", "line_width", "phrase_morph"],
        "scene": {"intensity": 0.72, "complexity": 0.64, "motion": 0.42, "beat_response": 0.52, "symmetry": 0.9, "line_width": 0.54, "automation_enabled": True, "automation_target": "symmetry", "automation_division": "16 bars"},
    },
    {
        "id": "orbital_mechanics",
        "name": "Orbital Mechanics",
        "category": "Particle Orbit",
        "math_family": "N-body inspired",
        "description": "Orbiting dust and elliptical paths create a celestial motion layer with long trails.",
        "mood": "Dreamy, circular, expansive",
        "best_for": "melodic grooves, soft transitions, spacey openers",
        "renderer": "canvas2d",
        "performance_cost": "Medium",
        "style_tags": ["orbit", "particles", "space"],
        "preset": "orbital_dust",
        "recommended_controls": ["rotation", "trail", "zoom", "motion"],
        "scene": {"intensity": 0.66, "complexity": 0.64, "motion": 0.66, "beat_response": 0.5, "trail": 0.88, "automation_enabled": True, "automation_target": "rotation", "automation_division": "8 bars"},
    },
    {
        "id": "eigenvector_grid",
        "name": "Eigenvector Grid",
        "category": "Linear Algebra",
        "math_family": "Matrix fields",
        "description": "A transformed grid of directional structure, good for crisp technical texture.",
        "mood": "Tense, architectural, technical",
        "best_for": "minimal techno, builds, structured background beds",
        "renderer": "canvas2d",
        "performance_cost": "Low",
        "style_tags": ["grid", "matrix", "interference"],
        "preset": "moire_grid",
        "recommended_controls": ["rotation", "symmetry", "line_width", "complexity"],
        "scene": {"intensity": 0.6, "complexity": 0.62, "motion": 0.4, "beat_response": 0.46, "symmetry": 0.86, "line_width": 0.28, "automation_enabled": True, "automation_target": "rotation", "automation_division": "8 bars"},
    },
]


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
    mood: str | None = None
    energy: int | None = None
    section: str | None = None
    notes: list[str] = field(default_factory=list)


PERFORMANCE_PRESETS: dict[str, dict[str, Any]] = {
    "Look 1": {"PRIMARY": "indigo", "SECONDARY": "magenta", "STROBE": "purple"},
    "Look 2": {"PRIMARY": "amber", "SECONDARY": "pink", "STROBE": "orange"},
    "Look 3": {"PRIMARY": "cyan", "SECONDARY": "blue", "STROBE": "cyan"},
    "Look 4": {"PRIMARY": "red", "SECONDARY": "amber", "STROBE": "yellow"},
    "Look 5": {"PRIMARY": "blue", "SECONDARY": "indigo", "STROBE": "blue"},
    "Look 6": {"PRIMARY": "magenta", "SECONDARY": "cyan", "STROBE": "purple"},
    "Look 7": {"PRIMARY": "green", "SECONDARY": "teal", "STROBE": "lime"},
    "Look 8": {"PRIMARY": "violet", "SECONDARY": "purple", "STROBE": "fuchsia"},
    "Look 9": {"PRIMARY": "rose", "SECONDARY": "orange", "STROBE": "pink"},
    "Look 10": {"PRIMARY": "blue", "SECONDARY": "purple", "STROBE": "royal"},
}


def osc_pad(value: bytes) -> bytes:
    padding = (4 - (len(value) % 4)) % 4
    return value + (b"\x00" * padding)


def osc_string(value: str) -> bytes:
    return osc_pad(value.encode("utf-8") + b"\x00")


def clean_osc_address(address: Any) -> str:
    text = str(address or "").strip()
    if not text:
        return ""
    if not text.startswith("/"):
        text = f"/{text}"
    return text


def default_camera_controls() -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for group_key, group_label in CAMERA_GROUP_SPECS:
        groups[group_key] = []
        for index, column_label in enumerate(CAMERA_COLUMN_LABELS, start=1):
            groups[group_key].append(
                {
                    "id": f"{group_key}_{index}",
                    "group": group_key,
                    "group_label": group_label,
                    "column": index,
                    "name": f"{group_label} {column_label}",
                    "label": column_label,
                    "address": "",
                }
            )
    scenes = [
        {
            "id": f"scene_{index}",
            "index": index,
            "name": f"Scene {index}",
            "label": f"Scene {index}",
            "address": "",
        }
        for index in range(1, SCENE_BUTTON_COUNT + 1)
    ]
    return {"groups": groups, "scenes": scenes}


def normalize_camera_controls(raw: Any) -> dict[str, Any]:
    defaults = default_camera_controls()
    raw_items: dict[str, Any] = {}
    if isinstance(raw, dict):
        explicit_items = raw.get("items", {})
        if isinstance(explicit_items, dict):
            raw_items.update(explicit_items)
        raw_groups = raw.get("groups", {})
        if isinstance(raw_groups, dict):
            for group_items in raw_groups.values():
                if isinstance(group_items, list):
                    for raw_item in group_items:
                        if isinstance(raw_item, dict) and raw_item.get("id"):
                            raw_items[str(raw_item["id"])] = raw_item
        for collection_key in ("scenes",):
            raw_collection = raw.get(collection_key, [])
            if isinstance(raw_collection, list):
                for raw_item in raw_collection:
                    if isinstance(raw_item, dict) and raw_item.get("id"):
                        raw_items[str(raw_item["id"])] = raw_item

    def apply_item(item: dict[str, Any]) -> dict[str, Any]:
        override = raw_items.get(item["id"], {})
        if not isinstance(override, dict):
            override = {}
        merged = dict(item)
        merged["name"] = text_value(override.get("name", item["name"])) or item["name"]
        merged["label"] = text_value(override.get("label", item["label"])) or item["label"]
        merged["address"] = clean_osc_address(override.get("address", item.get("address", "")))
        return merged

    return {
        "groups": {
            group_key: [apply_item(item) for item in items]
            for group_key, items in defaults["groups"].items()
        },
        "scenes": [apply_item(item) for item in defaults["scenes"]],
    }


def visual_layer_clip(index: int) -> tuple[int, int]:
    safe_index = max(1, int(index or 1))
    return ((safe_index - 1) // VISUAL_CLIPS_PER_LAYER) + 1, ((safe_index - 1) % VISUAL_CLIPS_PER_LAYER) + 1


def visual_clip_name(index: int) -> str:
    layer, clip = visual_layer_clip(index)
    return f"Layer {layer} Clip {clip}"


def visual_clip_label(index: int) -> str:
    layer, clip = visual_layer_clip(index)
    return f"L{layer} C{clip}"


def is_default_visual_label(value: Any, index: int, item_id: str = "") -> bool:
    text = text_value(value)
    if not text:
        return True
    layer, clip = visual_layer_clip(index)
    defaults = {
        item_id,
        f"V{index}",
        f"Visual {index}",
        f"Layer {layer} Clip {clip}",
        f"L{layer} C{clip}",
        f"C{clip}",
    }
    return text.casefold() in {item.casefold() for item in defaults if item}


def default_visual_controls() -> list[dict[str, Any]]:
    return [
        {
            "id": f"visual_{index}",
            "index": index,
            "layer": visual_layer_clip(index)[0],
            "clip": visual_layer_clip(index)[1],
            "name": visual_clip_name(index),
            "label": visual_clip_label(index),
            "address": "",
        }
        for index in range(1, VISUAL_BUTTON_COUNT + 1)
    ]


def default_visual_slider_controls(config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    config = config or {}
    legacy_address = clean_osc_address(config.get("visual_opacity_address", ""))
    return [
        {
            "id": f"visual_slider_{index}",
            "index": index,
            "name": "Visual Opacity" if index == 1 else f"Visual Slider {index}",
            "label": "Visual Opacity" if index == 1 else f"Slider {index}",
            "address": legacy_address if index == 1 else "",
        }
        for index in range(1, 6)
    ]


def normalize_visual_slider_controls(raw: Any, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    defaults = default_visual_slider_controls(config)
    raw_items: dict[str, Any] = {}
    if isinstance(raw, dict):
        explicit_items = raw.get("items", raw)
        if isinstance(explicit_items, dict):
            for item_id, item in explicit_items.items():
                if isinstance(item, dict):
                    raw_items[text_value(item.get("id", item_id))] = item
        elif isinstance(explicit_items, list):
            for item in explicit_items:
                if isinstance(item, dict) and item.get("id"):
                    raw_items[text_value(item.get("id"))] = item
    elif isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and item.get("id"):
                raw_items[text_value(item.get("id"))] = item

    normalized = []
    for item in defaults:
        override = raw_items.get(item["id"], {})
        if not isinstance(override, dict):
            override = {}
        merged = dict(item)
        merged["name"] = text_value(override.get("name", item["name"])) or item["name"]
        merged["label"] = text_value(override.get("label", item["label"])) or item["label"]
        merged["address"] = clean_osc_address(override.get("address", item["address"]))
        normalized.append(merged)
    return normalized


def normalize_visual_controls(raw: Any) -> list[dict[str, Any]]:
    defaults = default_visual_controls()
    raw_items: dict[str, Any] = {}
    if isinstance(raw, dict):
        explicit_items = raw.get("items", {})
        if isinstance(explicit_items, dict):
            raw_items.update(explicit_items)
        raw_list = raw.get("items", [])
        if isinstance(raw_list, list):
            for raw_item in raw_list:
                if isinstance(raw_item, dict) and raw_item.get("id"):
                    raw_items[str(raw_item["id"])] = raw_item
    elif isinstance(raw, list):
        for raw_item in raw:
            if isinstance(raw_item, dict) and raw_item.get("id"):
                raw_items[str(raw_item["id"])] = raw_item

    normalized = []
    for item in defaults:
        override = raw_items.get(item["id"], {})
        if not isinstance(override, dict):
            override = {}
        merged = dict(item)
        item_id = text_value(item.get("id", ""))
        item_index = int(item.get("index", 1) or 1)
        override_name = override.get("name", item["name"])
        override_label = override.get("label", item["label"])
        merged["name"] = item["name"] if is_default_visual_label(override_name, item_index, item_id) else text_value(override_name)
        merged["label"] = item["label"] if is_default_visual_label(override_label, item_index, item_id) else text_value(override_label)
        merged["address"] = clean_osc_address(override.get("address", item.get("address", "")))
        normalized.append(merged)
    return normalized


def parse_unit_interval(value: Any, default: float = 0.0, low: float = 0.0, high: float = 1.0) -> float:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return default
    return max(low, min(high, parsed))


def normalize_generative_visual_presets(raw: Any) -> dict[str, dict[str, Any]]:
    source = raw if isinstance(raw, dict) else {}
    normalized: dict[str, dict[str, Any]] = {}
    for key, defaults in GEN_VISUAL_PRESET_DEFS.items():
        recipe = GEN_VISUAL_PRESET_RECIPES.get(key, {})
        item = source.get(key, {})
        if not isinstance(item, dict):
            item = {}
        renderer = text_value(item.get("renderer", defaults["renderer"]))
        if renderer not in {"canvas2d", "webgl-shader"}:
            renderer = defaults["renderer"]
        color_source = text_value(item.get("color_source", defaults["color_source"])).casefold()
        if color_source not in GEN_VISUAL_COLOR_SOURCES:
            color_source = defaults["color_source"]
        quality = text_value(item.get("quality", defaults["quality"])).casefold()
        if quality not in GEN_VISUAL_QUALITIES:
            quality = defaults["quality"]
        normalized[key] = {
            "id": key,
            "name": text_value(item.get("name", defaults["name"])) or defaults["name"],
            "renderer": renderer,
            "base": text_value(item.get("base", defaults["base"])) or defaults["base"],
            "default_intensity": parse_unit_interval(item.get("default_intensity", item.get("intensity", recipe.get("intensity", defaults["intensity"]))), recipe.get("intensity", defaults["intensity"])),
            "default_complexity": parse_unit_interval(item.get("default_complexity", item.get("complexity", recipe.get("complexity", defaults["complexity"]))), recipe.get("complexity", defaults["complexity"])),
            "default_motion": parse_unit_interval(item.get("default_motion", item.get("motion", recipe.get("motion", defaults["motion"]))), recipe.get("motion", defaults["motion"])),
            "default_beat_response": parse_unit_interval(item.get("default_beat_response", item.get("beat_response", recipe.get("beat_response", defaults["beat_response"]))), recipe.get("beat_response", defaults["beat_response"])),
            "default_scale": parse_unit_interval(item.get("default_scale", item.get("scale", recipe.get("scale", DEFAULT_GENERATIVE_VISUAL["scale"]))), float(recipe.get("scale", DEFAULT_GENERATIVE_VISUAL["scale"]))),
            "default_zoom": parse_unit_interval(item.get("default_zoom", item.get("zoom", recipe.get("zoom", DEFAULT_GENERATIVE_VISUAL["zoom"]))), float(recipe.get("zoom", DEFAULT_GENERATIVE_VISUAL["zoom"]))),
            "default_rotation": parse_unit_interval(item.get("default_rotation", item.get("rotation", recipe.get("rotation", DEFAULT_GENERATIVE_VISUAL["rotation"]))), float(recipe.get("rotation", DEFAULT_GENERATIVE_VISUAL["rotation"]))),
            "default_symmetry": parse_unit_interval(item.get("default_symmetry", item.get("symmetry", recipe.get("symmetry", DEFAULT_GENERATIVE_VISUAL["symmetry"]))), float(recipe.get("symmetry", DEFAULT_GENERATIVE_VISUAL["symmetry"]))),
            "default_warp": parse_unit_interval(item.get("default_warp", item.get("warp", recipe.get("warp", DEFAULT_GENERATIVE_VISUAL["warp"]))), float(recipe.get("warp", DEFAULT_GENERATIVE_VISUAL["warp"]))),
            "default_line_width": parse_unit_interval(item.get("default_line_width", item.get("line_width", recipe.get("line_width", DEFAULT_GENERATIVE_VISUAL["line_width"]))), float(recipe.get("line_width", DEFAULT_GENERATIVE_VISUAL["line_width"]))),
            "default_trail": parse_unit_interval(item.get("default_trail", item.get("trail", recipe.get("trail", DEFAULT_GENERATIVE_VISUAL["trail"]))), float(recipe.get("trail", DEFAULT_GENERATIVE_VISUAL["trail"]))),
            "default_color_source": color_source,
            "default_quality": quality,
            "default_automation_enabled": bool_from_payload(item.get("default_automation_enabled", item.get("automation_enabled", recipe.get("automation_enabled", DEFAULT_GENERATIVE_VISUAL["automation_enabled"]))), DEFAULT_GENERATIVE_VISUAL["automation_enabled"]),
            "default_automation_target": text_value(item.get("default_automation_target", item.get("automation_target", recipe.get("automation_target", DEFAULT_GENERATIVE_VISUAL["automation_target"])))) or DEFAULT_GENERATIVE_VISUAL["automation_target"],
            "default_automation_mode": text_value(item.get("default_automation_mode", item.get("automation_mode", recipe.get("automation_mode", DEFAULT_GENERATIVE_VISUAL["automation_mode"])))) or DEFAULT_GENERATIVE_VISUAL["automation_mode"],
            "default_automation_division": normalize_generator_division(item.get("default_automation_division", item.get("automation_division", recipe.get("automation_division", DEFAULT_GENERATIVE_VISUAL["automation_division"])))),
            "default_automation_shape": text_value(item.get("default_automation_shape", item.get("automation_shape", recipe.get("automation_shape", DEFAULT_GENERATIVE_VISUAL["automation_shape"])))) or DEFAULT_GENERATIVE_VISUAL["automation_shape"],
            "default_automation_depth": parse_unit_interval(item.get("default_automation_depth", item.get("automation_depth", recipe.get("automation_depth", DEFAULT_GENERATIVE_VISUAL["automation_depth"]))), float(recipe.get("automation_depth", DEFAULT_GENERATIVE_VISUAL["automation_depth"]))),
            "default_automation_offset": parse_unit_interval(item.get("default_automation_offset", item.get("automation_offset", recipe.get("automation_offset", DEFAULT_GENERATIVE_VISUAL["automation_offset"]))), float(recipe.get("automation_offset", DEFAULT_GENERATIVE_VISUAL["automation_offset"]))),
            "category": text_value(item.get("category", defaults["category"])) or defaults["category"],
            "mood": text_value(item.get("mood", defaults.get("mood", ""))) or defaults.get("mood", ""),
            "best_for": text_value(item.get("best_for", defaults.get("best_for", ""))) or defaults.get("best_for", ""),
            "notes": text_value(item.get("notes", defaults["notes"])) or defaults["notes"],
        }
    return normalized


def normalize_generator_division(value: Any) -> str:
    text = text_value(value)
    return text if text in BPM_FLIP_DIVISION_MULTIPLIERS else "1 bar"


def normalize_generative_visual(raw: Any, base: dict[str, Any] | None = None) -> dict[str, Any]:
    source = raw if isinstance(raw, dict) else {}
    defaults = dict(DEFAULT_GENERATIVE_VISUAL if base is None else base)
    preset = text_value(source.get("preset", defaults.get("preset", "lissajous_orbit")))
    if preset not in GEN_VISUAL_PRESET_DEFS:
        preset = "lissajous_orbit"
    color_source = text_value(source.get("color_source", defaults.get("color_source", "look"))).casefold()
    if color_source not in GEN_VISUAL_COLOR_SOURCES:
        color_source = "look"
    quality = text_value(source.get("quality", defaults.get("quality", "medium"))).casefold()
    if quality not in GEN_VISUAL_QUALITIES:
        quality = "medium"
    automation_target = text_value(source.get("automation_target", defaults.get("automation_target", "warp"))).casefold()
    if automation_target not in GEN_VISUAL_AUTOMATION_TARGETS:
        automation_target = "warp"
    automation_mode = text_value(source.get("automation_mode", defaults.get("automation_mode", "bpm"))).casefold()
    if automation_mode not in GEN_VISUAL_AUTOMATION_MODES:
        automation_mode = "bpm"
    automation_division = normalize_generator_division(source.get("automation_division", defaults.get("automation_division", "1 bar")))
    automation_shape = text_value(source.get("automation_shape", defaults.get("automation_shape", "sine"))).casefold()
    if automation_shape not in GEN_VISUAL_AUTOMATION_SHAPES:
        automation_shape = "sine"
    layer_style = text_value(source.get("layer_style", defaults.get("layer_style", "glow_grid"))).casefold()
    if layer_style not in GEN_VISUAL_LAYER_STYLES:
        layer_style = "glow_grid"
    return {
        "enabled": bool_from_payload(source.get("enabled", defaults.get("enabled", True)), True),
        "preset": preset,
        "color_source": color_source,
        "intensity": parse_unit_interval(source.get("intensity", defaults.get("intensity", 0.72)), float(defaults.get("intensity", 0.72))),
        "complexity": parse_unit_interval(source.get("complexity", defaults.get("complexity", 0.48)), float(defaults.get("complexity", 0.48))),
        "motion": parse_unit_interval(source.get("motion", defaults.get("motion", 0.62)), float(defaults.get("motion", 0.62))),
        "beat_response": parse_unit_interval(source.get("beat_response", defaults.get("beat_response", 0.52)), float(defaults.get("beat_response", 0.52))),
        "scale": parse_unit_interval(source.get("scale", defaults.get("scale", 0.54)), float(defaults.get("scale", 0.54))),
        "zoom": parse_unit_interval(source.get("zoom", defaults.get("zoom", 0.5)), float(defaults.get("zoom", 0.5))),
        "rotation": parse_unit_interval(source.get("rotation", defaults.get("rotation", 0.42)), float(defaults.get("rotation", 0.42))),
        "symmetry": parse_unit_interval(source.get("symmetry", defaults.get("symmetry", 0.5)), float(defaults.get("symmetry", 0.5))),
        "warp": parse_unit_interval(source.get("warp", defaults.get("warp", 0.38)), float(defaults.get("warp", 0.38))),
        "line_width": parse_unit_interval(source.get("line_width", defaults.get("line_width", 0.42)), float(defaults.get("line_width", 0.42))),
        "trail": parse_unit_interval(source.get("trail", defaults.get("trail", 0.56)), float(defaults.get("trail", 0.56))),
        "automation_enabled": bool_from_payload(source.get("automation_enabled", defaults.get("automation_enabled", False)), False),
        "automation_target": automation_target,
        "automation_mode": automation_mode,
        "automation_division": automation_division,
        "automation_shape": automation_shape,
        "automation_depth": parse_unit_interval(source.get("automation_depth", defaults.get("automation_depth", 0.35)), float(defaults.get("automation_depth", 0.35))),
        "automation_offset": parse_unit_interval(source.get("automation_offset", defaults.get("automation_offset", 0.5)), float(defaults.get("automation_offset", 0.5))),
        "layer_enabled": bool_from_payload(source.get("layer_enabled", defaults.get("layer_enabled", True)), True),
        "layer_style": layer_style,
        "layer_mix": parse_unit_interval(source.get("layer_mix", defaults.get("layer_mix", 0.32)), float(defaults.get("layer_mix", 0.32))),
        "layer_speed": parse_unit_interval(source.get("layer_speed", defaults.get("layer_speed", 0.4)), float(defaults.get("layer_speed", 0.4))),
        "phrase_morph": bool_from_payload(source.get("phrase_morph", defaults.get("phrase_morph", True)), True),
        "auto_seed": bool_from_payload(source.get("auto_seed", defaults.get("auto_seed", True)), True),
        "quality": quality,
        "opacity": parse_unit_interval(source.get("opacity", defaults.get("opacity", 1.0)), float(defaults.get("opacity", 1.0))),
        "freeze": bool_from_payload(source.get("freeze", defaults.get("freeze", False)), False),
        "blackout": bool_from_payload(source.get("blackout", defaults.get("blackout", False)), False),
        "seed": parse_int(source.get("seed", defaults.get("seed", 1)), 1, 1, 999999999),
    }


def normalize_camera_opacity_addresses(raw: Any) -> dict[str, str]:
    source = raw if isinstance(raw, dict) else {}
    return {
        group_key: clean_osc_address(source.get(group_key, ""))
        for group_key, _group_label in CAMERA_GROUP_SPECS
    }


def normalize_camera_opacity_labels(raw: Any) -> dict[str, str]:
    source = raw if isinstance(raw, dict) else {}
    return {
        group_key: text_value(source.get(group_key, DEFAULT_CAMERA_OPACITY_LABELS[group_key])) or DEFAULT_CAMERA_OPACITY_LABELS[group_key]
        for group_key, _group_label in CAMERA_GROUP_SPECS
    }


def normalize_preset_link_rotation_slots(value: Any) -> list[str]:
    if isinstance(value, dict):
        raw_items = [key for key, enabled in value.items() if bool_from_payload(enabled)]
    elif isinstance(value, str):
        raw_items = [part for part in re.split(r"[,;\s]+", value) if part]
    elif isinstance(value, (list, tuple, set)):
        raw_items = list(value)
    else:
        raw_items = []
    aliases = {
        "1": "color1",
        "color1": "color1",
        "color_1": "color1",
        "2": "color2",
        "color2": "color2",
        "color_2": "color2",
        "3": "strobe_color",
        "color3": "strobe_color",
        "color_3": "strobe_color",
        "strobe": "strobe_color",
        "strobe_color": "strobe_color",
    }
    selected: list[str] = []
    for item in raw_items:
        key = aliases.get(text_value(item).casefold(), "")
        if key and key not in selected:
            selected.append(key)
    return selected if len(selected) >= 2 else []


def normalize_preset_link_float(value: Any, default: float, minimum: float, maximum: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = default
    return max(minimum, min(maximum, number))


def normalize_preset_link_opacity(value: Any) -> int | str:
    text = text_value(value)
    if not text:
        return ""
    return parse_percent(text, 100)


def normalize_preset_link_bpm(item: dict[str, Any]) -> dict[str, Any]:
    mode = text_value(item.get("bpm_flip_mode", "bars")).casefold()
    if mode not in {"bars", "seconds"}:
        mode = "bars"
    division = text_value(item.get("bpm_division", item.get("bpm_flip_division", "1/4")))
    if division not in BPM_FLIP_DIVISION_MULTIPLIERS:
        division = "1/4"
    return {
        "bpm_enabled": bool_from_payload(item.get("bpm_enabled", False)),
        "bpm_running": bool_from_payload(item.get("bpm_running", False)),
        "bpm_follow_now_playing": bool_from_payload(item.get("bpm_follow_now_playing", False)),
        "bpm": normalize_preset_link_float(item.get("bpm", item.get("bpm_flip_bpm", 125)), 125.0, BPM_FLIP_MIN_BPM, BPM_FLIP_MAX_BPM),
        "bpm_division": division,
        "bpm_flip_mode": mode,
        "bpm_seconds": normalize_preset_link_float(item.get("bpm_seconds", item.get("bpm_flip_seconds", 8)), 8.0, BPM_FLIP_MIN_SECONDS, BPM_FLIP_MAX_SECONDS),
        "bpm_rotation_slots": normalize_preset_link_rotation_slots(item.get("bpm_rotation_slots", [])),
    }


def normalize_preset_links(raw: Any, preset_names: list[str]) -> dict[str, dict[str, Any]]:
    source = raw if isinstance(raw, dict) else {}
    normalized: dict[str, dict[str, Any]] = {}
    for name in preset_names:
        item = source.get(name, {})
        if not isinstance(item, dict):
            item = {}
        now_playing_mode = text_value(item.get("now_playing_mode", item.get("mode", ""))).casefold()
        if now_playing_mode not in {"", "cdj", "vinyl", "studio", "videogame"}:
            now_playing_mode = ""
        generative_visual = item.get("generative_visual", {})
        if not isinstance(generative_visual, dict):
            generative_visual = {}
        normalized[name] = {
            "enabled": bool_from_payload(item.get("enabled", False)),
            "section_preset": text_value(item.get("section_preset", item.get("section", ""))).upper(),
            "now_playing_mode": now_playing_mode,
            "now_playing_opacity": normalize_preset_link_opacity(item.get("now_playing_opacity", "")),
            "visual_id": text_value(item.get("visual_id", "")),
            "main_box_id": text_value(item.get("main_box_id", "")),
            "pip_box_id": text_value(item.get("pip_box_id", "")),
            "background_id": text_value(item.get("background_id", "")),
            "scene_id": text_value(item.get("scene_id", "")),
            "generative_visual": normalize_generative_visual(generative_visual, DEFAULT_GENERATIVE_VISUAL) if generative_visual else {},
            **normalize_preset_link_bpm(item),
        }
    return normalized


PERFORMANCE_BANK_CATEGORIES = (
    "looks",
    "visuals",
    "main_box",
    "pip_box",
    "background",
    "scenes",
    "generator",
)
SONG_MOMENT_KEYS = ("intro", "build", "drop", "outro")


def _limited_known_ids(raw: Any, allowed: list[str], limit: int = 8) -> list[str]:
    values = raw if isinstance(raw, list) else []
    selected: list[str] = []
    for value in values:
        item_id = text_value(value)
        if item_id in allowed and item_id not in selected:
            selected.append(item_id)
        if len(selected) >= limit:
            break
    return selected


def normalize_performance_banks(
    raw: Any,
    preset_names: list[str],
    visual_controls: list[dict[str, Any]],
    camera_controls: dict[str, Any],
    generative_presets: dict[str, Any],
) -> list[dict[str, Any]]:
    source = raw if isinstance(raw, list) else raw.get("banks", []) if isinstance(raw, dict) else []
    visual_ids = [text_value(item.get("id")) for item in visual_controls]
    camera_groups = camera_controls.get("groups", {}) if isinstance(camera_controls, dict) else {}
    camera_ids = {
        group: [text_value(item.get("id")) for item in camera_groups.get(group, [])]
        for group in ("main_box", "pip_box", "background")
    }
    scene_ids = [text_value(item.get("id")) for item in camera_controls.get("scenes", [])] if isinstance(camera_controls, dict) else []
    generator_ids = list(generative_presets.keys())
    defaults = {
        "looks": preset_names[:8],
        "visuals": visual_ids[:8],
        "main_box": camera_ids["main_box"][:8],
        "pip_box": camera_ids["pip_box"][:8],
        "background": camera_ids["background"][:8],
        "scenes": scene_ids[:8],
        "generator": generator_ids[:8],
    }
    allowed = {
        "looks": preset_names,
        "visuals": visual_ids,
        "main_box": camera_ids["main_box"],
        "pip_box": camera_ids["pip_box"],
        "background": camera_ids["background"],
        "scenes": scene_ids,
        "generator": generator_ids,
    }
    normalized: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    for index, item in enumerate(source[:12]):
        if not isinstance(item, dict):
            continue
        name = text_value(item.get("name")) or f"Bank {index + 1}"
        raw_id = text_value(item.get("id")) or name.casefold()
        bank_id = re.sub(r"[^a-z0-9_-]+", "-", raw_id.casefold()).strip("-") or f"bank-{index + 1}"
        if bank_id in used_ids:
            bank_id = f"{bank_id}-{index + 1}"
        used_ids.add(bank_id)
        favorites = item.get("favorites", {}) if isinstance(item.get("favorites"), dict) else {}
        favorite_fallback = [] if "favorites" in item else None
        normalized_favorites = {
            category: _limited_known_ids(
                favorites.get(category, defaults[category] if favorite_fallback is None else favorite_fallback),
                allowed[category],
            )
            for category in PERFORMANCE_BANK_CATEGORIES
        }
        moments_raw = item.get("song_moments", item.get("moments", {}))
        moments_raw = moments_raw if isinstance(moments_raw, dict) else {}
        moments = {
            moment: text_value(moments_raw.get(moment, ""))
            if text_value(moments_raw.get(moment, "")) in preset_names
            else ""
            for moment in SONG_MOMENT_KEYS
        }
        normalized.append({"id": bank_id, "name": name[:48], "favorites": normalized_favorites, "song_moments": moments})
    if not normalized:
        normalized.append({"id": "main-set", "name": "Main Set", "favorites": defaults, "song_moments": {moment: "" for moment in SONG_MOMENT_KEYS}})
    return normalized


def normalize_panic_safe(
    raw: Any,
    preset_names: list[str],
    visual_controls: list[dict[str, Any]],
    camera_controls: dict[str, Any],
) -> dict[str, Any]:
    source = raw if isinstance(raw, dict) else {}
    safe_look = next((name for name in ("Look 1", "Look 10") if name in preset_names), preset_names[0] if preset_names else "")
    visual_ids = {text_value(item.get("id")) for item in visual_controls}
    groups = camera_controls.get("groups", {}) if isinstance(camera_controls, dict) else {}
    group_ids = {
        group: {text_value(item.get("id")) for item in groups.get(group, [])}
        for group in ("main_box", "pip_box", "background")
    }
    scene_ids = {text_value(item.get("id")) for item in camera_controls.get("scenes", [])} if isinstance(camera_controls, dict) else set()
    defaults = {
        "visual_id": next((text_value(item.get("id")) for item in visual_controls if text_value(item.get("id")) in visual_ids), ""),
        "main_box_id": next((text_value(item.get("id")) for item in groups.get("main_box", []) if text_value(item.get("id")) in group_ids["main_box"]), ""),
        "pip_box_id": next((text_value(item.get("id")) for item in groups.get("pip_box", []) if text_value(item.get("id")) in group_ids["pip_box"]), ""),
        "background_id": next((text_value(item.get("id")) for item in groups.get("background", []) if text_value(item.get("id")) in group_ids["background"]), ""),
        "scene_id": next((text_value(item.get("id")) for item in camera_controls.get("scenes", []) if text_value(item.get("id")) in scene_ids), ""),
    }
    requested_look = text_value(source.get("look", safe_look))
    return {
        "look": requested_look if requested_look in preset_names else safe_look,
        "visual_id": text_value(source.get("visual_id", defaults["visual_id"])) if text_value(source.get("visual_id", defaults["visual_id"])) in visual_ids else defaults["visual_id"],
        "main_box_id": text_value(source.get("main_box_id", defaults["main_box_id"])) if text_value(source.get("main_box_id", defaults["main_box_id"])) in group_ids["main_box"] else defaults["main_box_id"],
        "pip_box_id": text_value(source.get("pip_box_id", defaults["pip_box_id"])) if text_value(source.get("pip_box_id", defaults["pip_box_id"])) in group_ids["pip_box"] else defaults["pip_box_id"],
        "background_id": text_value(source.get("background_id", defaults["background_id"])) if text_value(source.get("background_id", defaults["background_id"])) in group_ids["background"] else defaults["background_id"],
        "scene_id": text_value(source.get("scene_id", defaults["scene_id"])) if text_value(source.get("scene_id", defaults["scene_id"])) in scene_ids else defaults["scene_id"],
        "stop_generator": bool_from_payload(source.get("stop_generator", True), True),
    }


def normalize_show_sequences(raw: Any, preset_names: list[str]) -> dict[str, dict[str, Any]]:
    source = raw if isinstance(raw, dict) else {}
    normalized: dict[str, dict[str, Any]] = {}
    allowed_units = {"bars", "beats", "seconds", "minutes"}
    for raw_name, raw_sequence in source.items():
        name = text_value(raw_name)
        if not name or not isinstance(raw_sequence, dict):
            continue
        steps: list[dict[str, Any]] = []
        for raw_step in raw_sequence.get("steps", []):
            if not isinstance(raw_step, dict):
                continue
            look = text_value(raw_step.get("look", ""))
            if look and look not in preset_names:
                continue
            unit = text_value(raw_step.get("unit", "bars")).casefold()
            if unit not in allowed_units:
                unit = "bars"
            trigger_type = text_value(raw_step.get("trigger_type", "after")).casefold()
            if trigger_type not in {"after", "at"}:
                trigger_type = "after"
            steps.append(
                {
                    "look": look,
                    "trigger_type": trigger_type,
                    "amount": parse_int(raw_step.get("amount", 1), 1, 0, 9999),
                    "unit": unit,
                    "note": text_value(raw_step.get("note", "")),
                    "visual_id": text_value(raw_step.get("visual_id", "")),
                    "main_box_id": text_value(raw_step.get("main_box_id", "")),
                    "pip_box_id": text_value(raw_step.get("pip_box_id", "")),
                    "background_id": text_value(raw_step.get("background_id", "")),
                    "scene_id": text_value(raw_step.get("scene_id", "")),
                }
            )
        normalized[name] = {"name": name, "loop": bool_from_payload(raw_sequence.get("loop", False)), "steps": steps}
    if not normalized:
        normalized["Main Show"] = {
            "name": "Main Show",
            "loop": False,
            "steps": [
                {"look": preset_names[0] if preset_names else "", "trigger_type": "after", "amount": 0, "unit": "bars", "note": "Opening look"},
            ],
        }
    return normalized


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


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


def percent_to_value(value: Any) -> float:
    return clamp(parse_percent(value) / 100.0)


def motion_percent(value: Any) -> int:
    return min(parse_percent(value), 95)


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
    return text if text in BPM_FLIP_DIVISION_MULTIPLIERS else "1/4"


def bpm_flip_interval_ms(bpm: float, division: str) -> int:
    division = normalize_bpm_swap_rate(division)
    multiplier = BPM_FLIP_DIVISION_MULTIPLIERS[division]
    return max(1, int(round((60000.0 / bpm) * multiplier)))


def parse_bpm_flip_seconds(value: Any) -> float:
    text = str(value or "").strip()
    if not text:
        raise ValueError("Enter seconds first.")
    try:
        seconds = float(text)
    except ValueError as exc:
        raise ValueError(f"Seconds must be a number, not {text!r}.") from exc
    if not BPM_FLIP_MIN_SECONDS <= seconds <= BPM_FLIP_MAX_SECONDS:
        raise ValueError(f"Seconds must be between {BPM_FLIP_MIN_SECONDS:g} and {BPM_FLIP_MAX_SECONDS:g}.")
    return seconds


def bpm_seconds_interval_ms(seconds: float) -> int:
    return max(1, int(round(seconds * 1000.0)))


def normalize_bpm_flip_mode(value: Any) -> str:
    text = str(value or "").strip().casefold()
    return text if text in {"bars", "seconds"} else "bars"


def normalize_bpm_rotation_slots(value: Any, *, require_multiple: bool = False, default_on_empty: bool = True) -> list[str]:
    aliases = {
        "1": "color1",
        "color1": "color1",
        "color_1": "color1",
        "primary": "color1",
        "primary_color": "color1",
        "2": "color2",
        "color2": "color2",
        "color_2": "color2",
        "secondary": "color2",
        "secondary_color": "color2",
        "3": "strobe_color",
        "color3": "strobe_color",
        "color_3": "strobe_color",
        "tertiary": "strobe_color",
        "tertiary_color": "strobe_color",
        "accent": "strobe_color",
        "accent_color": "strobe_color",
        "strobe": "strobe_color",
        "strobe_color": "strobe_color",
    }
    if isinstance(value, dict):
        raw_items = [key for key, enabled in value.items() if bool_from_payload(enabled)]
    elif isinstance(value, str):
        raw_items = [part for part in re.split(r"[,;\s]+", value) if part]
    elif isinstance(value, (list, tuple, set)):
        raw_items = list(value)
    elif value is None:
        raw_items = []
    else:
        raw_items = [value]

    selected: list[str] = []
    for item in raw_items:
        token = str(item or "").strip().casefold().replace(" ", "_").replace("-", "_")
        key = aliases.get(token)
        if key and key not in selected:
            selected.append(key)
    selected = [key for key in COLOR_SLOT_KEYS if key in selected]
    if not selected and default_on_empty:
        selected = list(DEFAULT_BPM_ROTATION_SLOTS)
    if require_multiple and len(selected) < 2:
        raise ValueError("Choose at least two colors for BPM rotation.")
    return selected


def normalized_key(raw_key: str) -> str:
    key = raw_key.strip().upper().replace(" ", "_").replace("-", "_")
    aliases = {
        "ACCENT": "STROBE",
        "STROBE_COLOR": "STROBE",
        "STROBE_COLOUR": "STROBE",
        "COLOR1": "PRIMARY",
        "COLOR_1": "PRIMARY",
        "PRIMARY_COLOR": "PRIMARY",
        "COLOR2": "SECONDARY",
        "COLOR_2": "SECONDARY",
        "SECONDARY_COLOR": "SECONDARY",
        "COLOR3": "STROBE",
        "COLOR_3": "STROBE",
        "TERTIARY": "STROBE",
        "TERTIARY_COLOR": "STROBE",
        "STROBE%": "STROBE_PERCENT",
        "STROBE_RATE": "STROBE_PERCENT",
        "SAT": "SATURATION",
        "DIMMER": "BRIGHTNESS",
        "MOVEMENT": "MOTION",
        "PATTERN": "FX",
        "ACCENT_AMOUNT": "PULSE",
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


def color_name_to_value(name: str, fallback: str = "indigo") -> tuple[str, float]:
    normalized = str(name or "").strip().casefold()
    if normalized not in COLOR_HUE_VALUES:
        normalized = fallback
    return normalized, COLOR_HUE_VALUES[normalized]


def color_hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = str(value or "").lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def nearest_color_name(hue: float) -> str:
    hue = hue % 1.0

    def distance(item: tuple[str, float]) -> float:
        diff = abs(item[1] - hue)
        return min(diff, 1.0 - diff)

    return min(COLOR_HUE_VALUES.items(), key=distance)[0]


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


def make_state_from_template(template: str) -> LightingState:
    state = LightingState()
    apply_values_to_state(state, parse_comment_tags(template), exact=True)
    state.source = "default"
    return state


def load_config() -> dict[str, Any]:
    config_path = CONFIG_PATH
    if not config_path.exists():
        legacy_paths = sorted(PROJECT_ROOT.glob(LEGACY_CONFIG_GLOB), key=lambda path: path.stat().st_mtime, reverse=True)
        config_path = legacy_paths[0] if legacy_paths else CONFIG_PATH
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_config(config: dict[str, Any]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = CONFIG_PATH.with_name(f"{CONFIG_PATH.stem}.tmp{CONFIG_PATH.suffix}")
    temp_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    temp_path.replace(CONFIG_PATH)


def bool_from_payload(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    text = str(value).strip().casefold()
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False
    return default


def text_value(value: Any) -> str:
    return str(value or "").strip()


def config_revision() -> str:
    try:
        return str(CONFIG_PATH.stat().st_mtime_ns) if CONFIG_PATH.exists() else "defaults"
    except OSError:
        return "unknown"


def local_ipv4_addresses() -> list[str]:
    addresses: set[str] = set()
    hostname = socket.gethostname()
    try:
        for family, _socktype, _proto, _canonname, sockaddr in socket.getaddrinfo(hostname, None):
            if family == socket.AF_INET:
                addresses.add(sockaddr[0])
    except OSError:
        pass

    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("8.8.8.8", 80))
        addresses.add(probe.getsockname()[0])
    except OSError:
        pass
    finally:
        probe.close()

    return sorted(address for address in addresses if not address.startswith("127."))


def normalize_connection_profiles(raw: Any, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    config = config or {}
    active_id = text_value(config.get("active_connection_profile", "pc_server_tablet")) or "pc_server_tablet"
    raw_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and item.get("id"):
                raw_by_id[text_value(item.get("id"))] = item
    elif isinstance(raw, dict):
        items = raw.get("items", raw)
        if isinstance(items, dict):
            for item_id, item in items.items():
                if isinstance(item, dict):
                    raw_by_id[text_value(item.get("id", item_id))] = item
        elif isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and item.get("id"):
                    raw_by_id[text_value(item.get("id"))] = item

    text_keys = (
        "name",
        "mode",
        "app_bind_host",
        "public_control_url",
        "beatlink_host",
        "beatlink_base_url",
        "blt_params_url",
        "resolume_host",
        "visualizer_url",
    )
    normalized = []
    for defaults in DEFAULT_CONNECTION_PROFILES:
        profile_id = defaults["id"]
        override = raw_by_id.get(profile_id, {})
        merged = dict(defaults)
        for key in text_keys:
            fallback = config.get(key, merged.get(key, "")) if profile_id in {active_id, "manual_advanced"} else merged.get(key, "")
            merged[key] = text_value(override.get(key, fallback))
        merged["app_port"] = parse_int(override.get("app_port", config.get("app_port", merged["app_port"])), int(merged["app_port"]), 1, 65535)
        merged["beatlink_port"] = parse_int(override.get("beatlink_port", config.get("beatlink_port", merged["beatlink_port"])), int(merged["beatlink_port"]), 1, 65535)
        merged["resolume_port"] = parse_int(
            override.get("resolume_port", override.get("resolume_osc_port", config.get("resolume_port", merged["resolume_port"]))),
            int(merged["resolume_port"]),
            1,
            65535,
        )
        normalized.append(merged)
    default_ids = {profile["id"] for profile in DEFAULT_CONNECTION_PROFILES}
    for profile_id, override in raw_by_id.items():
        if not profile_id or profile_id in default_ids:
            continue
        merged = {
            "id": profile_id,
            "name": profile_id.replace("_", " ").title(),
            "mode": "LAN",
            "app_bind_host": "0.0.0.0",
            "app_port": 8080,
            "public_control_url": "",
            "beatlink_host": "",
            "beatlink_port": 8088,
            "beatlink_base_url": "",
            "blt_params_url": "",
            "resolume_host": "",
            "resolume_port": 7000,
            "visualizer_url": "/visuals/generative",
        }
        for key in text_keys:
            merged[key] = text_value(override.get(key, merged.get(key, "")))
        merged["name"] = merged["name"] or profile_id
        merged["app_port"] = parse_int(override.get("app_port", merged["app_port"]), int(merged["app_port"]), 1, 65535)
        merged["beatlink_port"] = parse_int(override.get("beatlink_port", merged["beatlink_port"]), int(merged["beatlink_port"]), 1, 65535)
        merged["resolume_port"] = parse_int(
            override.get("resolume_port", override.get("resolume_osc_port", merged["resolume_port"])),
            int(merged["resolume_port"]),
            1,
            65535,
        )
        normalized.append(merged)
    return normalized


def active_connection_profile(config: dict[str, Any]) -> dict[str, Any]:
    profiles = normalize_connection_profiles(config.get("connection_profiles", []), config)
    active_id = text_value(config.get("active_connection_profile", "pc_server_tablet")) or "pc_server_tablet"
    for profile in profiles:
        if profile["id"] == active_id:
            return profile
    return profiles[0]


def profile_blt_url(config: dict[str, Any]) -> str:
    profile = active_connection_profile(config)
    profile_url = text_value(profile.get("blt_params_url", ""))
    if profile_url:
        return normalize_blt_params_url(profile_url)
    url = text_value(config.get("blt_params_url", config.get("blt_url", "")))
    if url:
        return normalize_blt_params_url(url)
    base = text_value(profile.get("beatlink_base_url", ""))
    if base:
        return normalize_blt_params_url(base)
    host = text_value(profile.get("beatlink_host", ""))
    if not host:
        return ""
    port = parse_int(profile.get("beatlink_port", 8088), 8088, 1, 65535)
    return blt_url_for_host(host, port)


def connection_payload(config: dict[str, Any], port: int | None = None) -> dict[str, Any]:
    profiles = normalize_connection_profiles(config.get("connection_profiles", []), config)
    active = active_connection_profile(config)
    app_port = parse_int(port or active.get("app_port") or config.get("app_port", 8080), 8080, 1, 65535)
    lan_ips = local_ipv4_addresses()
    local_url = f"http://127.0.0.1:{app_port}/"
    lan_urls = [f"http://{ip}:{app_port}/" for ip in lan_ips]
    public_url = text_value(active.get("public_control_url")) or (lan_urls[0] if lan_urls else local_url)
    return {
        "profiles": profiles,
        "active": active,
        "active_id": active["id"],
        "active_name": active["name"],
        "show_machine_name": text_value(config.get("show_machine_name", socket.gethostname())) or socket.gethostname(),
        "lan_ip": text_value(config.get("show_machine_lan_ip", lan_ips[0] if lan_ips else "")),
        "local_control_url": local_url,
        "lan_control_urls": lan_urls,
        "public_control_url": public_url,
        "visualizer_url": text_value(active.get("visualizer_url", "/visuals/generative")) or "/visuals/generative",
        "blt_params_url": profile_blt_url(config),
        "resolume_host": text_value(active.get("resolume_host", config.get("resolume_host", config.get("resolume_ip", "")))),
        "resolume_port": parse_int(active.get("resolume_port", config.get("resolume_port", 7000)), 7000, 1, 65535),
    }


def host_from_url(raw_url: Any) -> str:
    try:
        parsed = urlparse(text_value(raw_url))
    except Exception:
        return ""
    return text_value(parsed.hostname or "")


def port_from_url(raw_url: Any, fallback: int) -> int:
    try:
        parsed = urlparse(text_value(raw_url))
        return parse_int(parsed.port, fallback, 1, 65535)
    except Exception:
        return fallback


def normalize_blt_params_url(raw_url: Any) -> str:
    url = text_value(raw_url)
    if not url:
        return ""
    try:
        parsed = urlparse(url)
    except Exception:
        return url
    if not parsed.scheme or not parsed.netloc:
        return url
    path = parsed.path or "/"
    if path in {"", "/"}:
        path = "/params.json"
    return parsed._replace(path=path).geturl()


def blt_url_for_host(host: Any, port: Any = 17081) -> str:
    clean_host = text_value(host)
    if not clean_host:
        return ""
    clean_port = parse_int(port, 17081, 1, 65535)
    return f"http://{clean_host}:{clean_port}/params.json"


def normalize_network_host(raw: Any) -> str:
    value = text_value(raw).strip()
    if not value:
        return ""
    if "://" in value:
        host = host_from_url(value)
        return host or value
    value = value.strip().strip("/")
    if "/" in value:
        value = value.split("/", 1)[0]
    if value.count(":") == 1:
        host_part, port_part = value.rsplit(":", 1)
        if port_part.isdigit():
            value = host_part
    return value.strip()


def normalize_machine_addresses(item: Any, fallback_host: Any = "") -> list[str]:
    raw_values: list[Any] = []
    if isinstance(item, dict):
        raw_values.append(item.get("host", ""))
        raw_addresses = item.get("addresses", [])
        if isinstance(raw_addresses, str):
            raw_values.extend(re.split(r"[,;\n]+", raw_addresses))
        elif isinstance(raw_addresses, list):
            raw_values.extend(raw_addresses)
        for key in ("wifi_host", "wifi_ip", "wifi", "ethernet_host", "ethernet_ip", "ethernet", "lan_host", "lan_ip"):
            raw_values.append(item.get(key, ""))
    elif isinstance(item, str):
        raw_values.append(item)
    if fallback_host:
        raw_values.append(fallback_host)

    addresses: list[str] = []
    seen: set[str] = set()
    for raw in raw_values:
        address = normalize_network_host(raw)
        if not address:
            continue
        key = address.casefold()
        if key in seen:
            continue
        seen.add(key)
        addresses.append(address)
    return addresses


def machine_primary_host(machine: dict[str, Any]) -> str:
    addresses = normalize_machine_addresses(machine)
    return addresses[0] if addresses else text_value(machine.get("host", ""))


def normalize_network_machines(raw: Any, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    config = config or {}
    remote_host = text_value(config.get("resolume_host", ""))
    if remote_host.casefold() in {"127.0.0.1", "localhost"}:
        remote_host = host_from_url(config.get("blt_params_url", ""))
    if remote_host.casefold() in {"127.0.0.1", "localhost"}:
        remote_host = ""
    defaults = [
        {"id": "laptop", "label": "Laptop", "host": "127.0.0.1"},
        {"id": "pc", "label": "PC", "host": remote_host},
        {"id": "third", "label": "Third Machine", "host": ""},
    ]
    raw_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and text_value(item.get("id")):
                raw_by_id[text_value(item.get("id"))] = item
    elif isinstance(raw, dict):
        for item_id, item in raw.items():
            if isinstance(item, dict):
                raw_by_id[text_value(item.get("id", item_id))] = item

    normalized: list[dict[str, Any]] = []
    for defaults_item in defaults:
        override = raw_by_id.get(defaults_item["id"], {})
        addresses = normalize_machine_addresses(override, defaults_item["host"])
        normalized.append(
            {
                "id": defaults_item["id"],
                "label": text_value(override.get("label", defaults_item["label"])) or defaults_item["label"],
                "host": addresses[0] if addresses else "",
                "addresses": addresses,
            }
        )
    return normalized


def normalize_network_routes(raw: Any, machines: list[dict[str, Any]], config: dict[str, Any] | None = None) -> dict[str, Any]:
    config = config or {}
    raw = raw if isinstance(raw, dict) else {}
    machine_ids = {machine["id"] for machine in machines}

    def machine_for_host(host: str, fallback: str = "laptop") -> str:
        clean_host = normalize_network_host(host).casefold()
        if not clean_host:
            return fallback
        for machine in machines:
            machine_hosts = {address.casefold() for address in normalize_machine_addresses(machine)}
            if clean_host in machine_hosts:
                return machine["id"]
        return fallback

    beatlink_machine = text_value(raw.get("beatlink_machine")) or machine_for_host(host_from_url(config.get("blt_params_url", "")))
    resolume_machine = text_value(raw.get("resolume_machine")) or machine_for_host(config.get("resolume_host", ""))
    if beatlink_machine not in machine_ids:
        beatlink_machine = "laptop"
    if resolume_machine not in machine_ids:
        resolume_machine = "laptop"
    return {
        "beatlink_machine": beatlink_machine,
        "beatlink_port": parse_int(raw.get("beatlink_port", port_from_url(config.get("blt_params_url", ""), 17081)), 17081, 1, 65535),
        "resolume_machine": resolume_machine,
        "resolume_port": parse_int(raw.get("resolume_port", config.get("resolume_port", 7000)), 7000, 1, 65535),
    }


def blt_sources(config: dict[str, Any]) -> list[dict[str, Any]]:
    machines = normalize_network_machines(config.get("network_machines", []), config)
    routes = normalize_network_routes(config.get("network_routes", {}), machines, config)
    machines_by_id = {machine["id"]: machine for machine in machines}
    preferred_machine_id = text_value(routes.get("beatlink_machine", "laptop")) or "laptop"
    preferred_port = parse_int(routes.get("beatlink_port", port_from_url(config.get("blt_params_url", ""), 17081)), 17081, 1, 65535)
    sources: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add_source(source_id: str, label: str, url: str, preferred: bool = False) -> None:
        clean_url = normalize_blt_params_url(url)
        if not clean_url or clean_url in seen:
            return
        seen.add(clean_url)
        sources.append(
            {
                "id": source_id,
                "label": label or source_id,
                "url": clean_url,
                "preferred": preferred,
            }
        )

    def add_machine_sources(machine: dict[str, Any], preferred: bool = False) -> None:
        addresses = normalize_machine_addresses(machine)
        for index, host in enumerate(addresses):
            label = machine["label"] if index == 0 else f"{machine['label']} {index + 1}"
            add_source(
                f"{machine['id']}_{index + 1}",
                label,
                blt_url_for_host(host, preferred_port),
                preferred=preferred,
            )

    preferred_machine = machines_by_id.get(preferred_machine_id)
    if preferred_machine:
        add_machine_sources(preferred_machine, preferred=True)

    add_source("active_profile", "Active profile", profile_blt_url(config), preferred=not sources)

    for machine in machines:
        if machine["id"] == preferred_machine_id:
            continue
        add_machine_sources(machine)

    add_source("configured", "Configured URL", config.get("blt_params_url", ""))
    return sources


def normalize_osc_targets(raw: Any, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    config = config or {}
    default_host = text_value(config.get("resolume_host", config.get("resolume_ip", "")))
    default_port = parse_int(config.get("resolume_port", 7000), 7000, 1, 65535)
    try:
        profile = active_connection_profile(config)
        default_host = text_value(profile.get("resolume_host", default_host)) or default_host
        default_port = parse_int(profile.get("resolume_port", default_port), default_port, 1, 65535)
    except Exception:
        pass

    machines = normalize_network_machines(config.get("network_machines", []), config)
    routes = normalize_network_routes(config.get("network_routes", {}), machines, config)
    fanout_port = parse_int(routes.get("resolume_port", default_port), default_port, 1, 65535)
    primary_machine_id = text_value(routes.get("resolume_machine", ""))

    raw_items: list[Any] = []
    if isinstance(raw, list):
        raw_items = raw
    elif isinstance(raw, dict):
        items = raw.get("items", raw)
        raw_items = list(items.values()) if isinstance(items, dict) else items if isinstance(items, list) else []

    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()

    def add_target(item: Any, fallback_label: str = "OSC Target", primary: bool = False, source: str = "manual") -> None:
        if not isinstance(item, dict):
            return
        host = normalize_network_host(item.get("host", item.get("resolume_host", "")))
        port = parse_int(item.get("port", item.get("resolume_port", fanout_port)), fanout_port, 1, 65535)
        if not host:
            return
        key = (host.casefold(), port)
        if key in seen:
            return
        seen.add(key)
        target_id = text_value(item.get("id")) or re.sub(r"[^a-z0-9]+", "_", f"{host}_{port}".casefold()).strip("_")
        normalized.append(
            {
                "id": target_id or f"target_{len(normalized) + 1}",
                "label": text_value(item.get("label", item.get("name", fallback_label))) or fallback_label,
                "host": host,
                "port": port,
                "enabled": bool_from_payload(item.get("enabled", True)),
                "primary": bool_from_payload(item.get("primary", primary)),
                "source": text_value(item.get("source", source)) or source,
            }
        )

    for index, item in enumerate(raw_items):
        add_target(item, f"OSC Target {index + 1}", primary=index == 0, source="manual")

    route_names = ["Main", "Wi-Fi", "Ethernet"]
    for machine in machines:
        for index, host in enumerate(normalize_machine_addresses(machine)):
            route_name = route_names[index] if index < len(route_names) else f"Route {index + 1}"
            add_target(
                {
                    "id": f"auto_{machine['id']}_{index + 1}",
                    "label": f"{machine['label']} OSC {route_name}",
                    "host": host,
                    "port": fanout_port,
                    "enabled": True,
                    "primary": machine["id"] == primary_machine_id and index == 0,
                    "source": "auto",
                },
                f"{machine['label']} OSC {route_name}",
                primary=machine["id"] == primary_machine_id and index == 0,
                source="auto",
            )

    if default_host:
        add_target(
            {
                "id": "active_resolume",
                "label": "Active Resolume",
                "host": default_host,
                "port": default_port,
                "enabled": True,
                "primary": True,
                "source": "active",
            },
            "Active Resolume",
            primary=True,
            source="active",
        )

    if normalized and not any(target["primary"] for target in normalized):
        normalized[0]["primary"] = True
    return normalized

def normalize_math_scene_templates(raw: Any = None) -> list[dict[str, Any]]:
    overrides: dict[str, dict[str, Any]] = {}
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and item.get("id"):
                overrides[text_value(item.get("id"))] = item
    elif isinstance(raw, dict):
        for key, item in raw.items():
            if isinstance(item, dict):
                overrides[text_value(item.get("id", key))] = item

    normalized = []
    for defaults in MATH_SCENE_TEMPLATES:
        item = overrides.get(defaults["id"], {})
        preset = text_value(item.get("preset", defaults["preset"]))
        if preset not in GEN_VISUAL_PRESET_DEFS:
            preset = defaults["preset"] if defaults["preset"] in GEN_VISUAL_PRESET_DEFS else "lissajous_orbit"
        scene = item.get("scene", defaults.get("scene", {}))
        if not isinstance(scene, dict):
            scene = defaults.get("scene", {})
        normalized.append(
            {
                **defaults,
                "name": text_value(item.get("name", defaults["name"])) or defaults["name"],
                "category": text_value(item.get("category", defaults["category"])) or defaults["category"],
                "math_family": text_value(item.get("math_family", defaults["math_family"])) or defaults["math_family"],
                "description": text_value(item.get("description", defaults["description"])) or defaults["description"],
                "mood": text_value(item.get("mood", defaults["mood"])) or defaults["mood"],
                "best_for": text_value(item.get("best_for", defaults["best_for"])) or defaults["best_for"],
                "renderer": text_value(item.get("renderer", defaults["renderer"])) or defaults["renderer"],
                "performance_cost": text_value(item.get("performance_cost", defaults["performance_cost"])) or defaults["performance_cost"],
                "style_tags": [text_value(tag) for tag in item.get("style_tags", defaults.get("style_tags", [])) if text_value(tag)]
                if isinstance(item.get("style_tags", defaults.get("style_tags", [])), list)
                else list(defaults.get("style_tags", [])),
                "recommended_controls": [
                    text_value(control)
                    for control in item.get("recommended_controls", defaults.get("recommended_controls", []))
                    if text_value(control)
                ]
                if isinstance(item.get("recommended_controls", defaults.get("recommended_controls", [])), list)
                else list(defaults.get("recommended_controls", [])),
                "preset": preset,
                "scene": normalize_generative_visual({"preset": preset, **scene}, {**DEFAULT_GENERATIVE_VISUAL, **GEN_VISUAL_PRESET_RECIPES.get(preset, {})}),
            }
        )
    return normalized


def portable_project_path(value: Any) -> Path:
    path = Path(str(value or "").strip())
    return path if path.is_absolute() else PROJECT_ROOT / path


def artwork_output_path(config: dict[str, Any]) -> Path:
    configured = str(config.get("artwork_output", "")).strip()
    if configured:
        return portable_project_path(configured)
    return DEFAULT_ARTWORK_OUTPUT


def normalize_match_text(text: str) -> str:
    text = str(text or "").casefold()
    text = re.sub(r"\([^)]*\)|\[[^]]*\]", " ", text)
    text = re.sub(r"\b(original|extended|radio|edit|mix|remix|club|dub|version|remaster(ed)?)\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def make_match_key(artist: str, title: str) -> str:
    return normalize_match_text(f"{artist} {title}")


def score_track_match(track: dict[str, str], entry: dict[str, str]) -> float:
    query_key = make_match_key(track.get("artist", ""), track.get("title", "")) or normalize_match_text(track.get("title", ""))
    metadata_score = SequenceMatcher(None, query_key, entry.get("match_key", "")).ratio()
    filename_score = SequenceMatcher(None, query_key, entry.get("fallback_key", "")).ratio()
    title_score = SequenceMatcher(
        None,
        normalize_match_text(track.get("title", "")),
        normalize_match_text(entry.get("title", "") or entry.get("filename", "")),
    ).ratio()
    return max(metadata_score, filename_score * 0.96, title_score * 0.88)


def find_best_track_match(track: dict[str, str], index: list[dict[str, str]]) -> tuple[dict[str, str], float] | None:
    best_entry: dict[str, str] | None = None
    best_score = 0.0
    for entry in index:
        score = score_track_match(track, entry)
        if score > best_score:
            best_entry = entry
            best_score = score
    if best_entry and best_score >= 0.72:
        return best_entry, best_score
    return None


def resolve_indexed_mp3_path(entry: dict[str, str], config: dict[str, Any]) -> Path:
    indexed_path = Path(text_value(entry.get("path")))
    if indexed_path.exists():
        return indexed_path

    music_root = Path(text_value(config.get("music_root", "")))
    if music_root.exists():
        indexed_parts = indexed_path.parts
        root_parts = music_root.parts
        if root_parts:
            root_name = root_parts[-1].casefold()
            for index, part in enumerate(indexed_parts):
                if part.casefold() == root_name:
                    remapped = music_root.joinpath(*indexed_parts[index + 1 :])
                    if remapped.exists():
                        return remapped
                    break
        filename = text_value(entry.get("filename")) or indexed_path.stem
        direct_matches = list(music_root.rglob(f"{filename}.mp3"))
        if direct_matches:
            return direct_matches[0]

    return indexed_path


def first_tag_value(tags: Any, *keys: str) -> str:
    for key in keys:
        values = tags.get(key) if hasattr(tags, "get") else None
        if not values:
            continue
        if isinstance(values, (list, tuple)):
            return text_value(values[0])
        return text_value(values)
    return ""


def build_music_library_index(music_root: Path) -> list[dict[str, str]]:
    try:
        from mutagen import File as MutagenFile
    except ImportError as exc:
        raise RuntimeError("mutagen is required to build the music index. Install requirements.txt for this Python.") from exc

    entries: list[dict[str, str]] = []
    for mp3_path in music_root.rglob("*.mp3"):
        title = ""
        artist = ""
        album = ""
        comment = ""
        try:
            audio = MutagenFile(mp3_path, easy=True)
            tags = audio.tags if audio is not None and audio.tags is not None else {}
            title = first_tag_value(tags, "title")
            artist = first_tag_value(tags, "artist", "albumartist")
            album = first_tag_value(tags, "album")
            comment = first_tag_value(tags, "comment", "description")
        except Exception:
            pass
        filename = mp3_path.stem
        title = title or filename
        entries.append(
            {
                "path": str(mp3_path),
                "filename": filename,
                "title": title,
                "artist": artist,
                "album": album,
                "comment": comment,
                "match_key": make_match_key(artist, title),
                "fallback_key": normalize_match_text(filename),
            }
        )
    entries.sort(key=lambda item: item["path"].casefold())
    return entries

def synchsafe_to_int(raw: bytes) -> int:
    value = 0
    for byte in raw:
        value = (value << 7) | (byte & 0x7F)
    return value


def extract_apic_image(mp3_path: Path) -> tuple[bytes, str] | None:
    mutagen_error: Exception | None = None
    try:
        from mutagen.id3 import APIC, ID3, ID3NoHeaderError

        try:
            tags = ID3(mp3_path)
        except ID3NoHeaderError:
            return None
        artwork_frames = tags.getall("APIC")
        if not artwork_frames:
            return None
        front_cover = next((frame for frame in artwork_frames if isinstance(frame, APIC) and frame.type == 3), None)
        selected_frame = front_cover or artwork_frames[0]
        image_data = bytes(selected_frame.data or b"")
        if image_data:
            mime = text_value(selected_frame.mime).casefold()
            if mime in {"image/jpg", "image/jpeg", "jpg", "jpeg"}:
                return image_data, "image/jpeg"
            if mime in {"image/png", "png"}:
                return image_data, "image/png"
            return image_data, mime or "application/octet-stream"
    except ImportError:
        pass
    except FileNotFoundError:
        raise
    except Exception as exc:
        mutagen_error = exc

    data = mp3_path.read_bytes()
    if len(data) < 10 or data[:3] != b"ID3":
        if mutagen_error is not None:
            raise RuntimeError(f"Could not read ID3 artwork: {mutagen_error}") from mutagen_error
        return None
    major = data[3]
    tag_size = synchsafe_to_int(data[6:10])
    position = 10
    end = min(len(data), 10 + tag_size)
    while position + 10 <= end:
        frame_id = data[position : position + 4].decode("latin1", errors="ignore")
        if not frame_id.strip("\x00") or not re.match(r"^[A-Z0-9]{4}$", frame_id):
            break
        size_raw = data[position + 4 : position + 8]
        frame_size = synchsafe_to_int(size_raw) if major == 4 else int.from_bytes(size_raw, "big")
        position += 10
        frame_data = data[position : position + frame_size]
        position += frame_size
        if frame_id != "APIC" or len(frame_data) < 5:
            continue
        encoding = frame_data[0]
        mime_end = frame_data.find(b"\x00", 1)
        if mime_end < 0:
            continue
        mime = frame_data[1:mime_end].decode("latin1", errors="ignore").casefold().strip()
        cursor = mime_end + 2
        if cursor >= len(frame_data):
            continue
        if encoding in {1, 2}:
            desc_end = frame_data.find(b"\x00\x00", cursor)
            cursor = len(frame_data) if desc_end < 0 else desc_end + 2
        else:
            desc_end = frame_data.find(b"\x00", cursor)
            cursor = len(frame_data) if desc_end < 0 else desc_end + 1
        image_data = frame_data[cursor:]
        if image_data:
            if mime in {"image/jpg", "image/jpeg", "jpg", "jpeg"}:
                return image_data, "image/jpeg"
            if mime in {"image/png", "png"}:
                return image_data, "image/png"
    if mutagen_error is not None:
        raise RuntimeError(f"Could not read ID3 artwork: {mutagen_error}") from mutagen_error
    return None


def normalize_artwork_size(value: Any, default: int = DEFAULT_OUTPUT_PIXELS) -> int:
    return parse_int(value, default, ARTWORK_SIZE_MIN, ARTWORK_SIZE_MAX)


def artwork_dimensions(config: dict[str, Any], source: str = "cdj") -> tuple[int, int]:
    source_key = text_value(source).casefold()
    if source_key not in ARTWORK_SIZE_SOURCES:
        source_key = "cdj"
    legacy = normalize_artwork_size(config.get("output_pixels", DEFAULT_OUTPUT_PIXELS))
    width = normalize_artwork_size(config.get(f"{source_key}_artwork_width", legacy), legacy)
    height = normalize_artwork_size(config.get(f"{source_key}_artwork_height", legacy), legacy)
    return width, height


def artwork_size_label(size: tuple[int, int]) -> str:
    return f"{size[0]}x{size[1]}"


def render_artwork_canvas(source_image: Any, output_size: tuple[int, int]) -> Any:
    from PIL import Image, ImageOps

    width, height = output_size
    image = ImageOps.exif_transpose(source_image).convert("RGBA")
    contained = ImageOps.contain(image, (width, height), method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    left = (width - contained.width) // 2
    top = (height - contained.height) // 2
    canvas.alpha_composite(contained, dest=(left, top))
    return canvas.convert("RGB")


def save_image_bytes_as_jpeg(image_data: bytes, output_path: Path, output_size: tuple[int, int]) -> bool:
    from PIL import Image

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_handle = tempfile.NamedTemporaryFile(
        prefix=f"{output_path.stem}.",
        suffix=f".tmp{output_path.suffix}",
        dir=output_path.parent,
        delete=False,
    )
    temp_path = Path(temp_handle.name)
    temp_handle.close()
    try:
        with Image.open(io.BytesIO(image_data)) as source_image:
            source_image.load()
            canvas = render_artwork_canvas(source_image, output_size)
            canvas.save(temp_path, format="JPEG", quality=95, optimize=False, progressive=False, subsampling=0)
        last_error: PermissionError | None = None
        for attempt in range(6):
            try:
                temp_path.replace(output_path)
                last_error = None
                break
            except PermissionError as exc:
                last_error = exc
                time.sleep(0.12 * (attempt + 1))
        if last_error is not None:
            raise last_error
        os.utime(output_path, None)
        return True
    finally:
        with contextlib.suppress(OSError):
            if temp_path.exists():
                temp_path.unlink()


def extract_ffmpeg_attached_picture(mp3_path: Path) -> tuple[bytes, str] | None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return None
    with tempfile.TemporaryDirectory(prefix="blt-artwork-") as temp_dir:
        cover_path = Path(temp_dir) / "cover.png"
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(mp3_path),
            "-an",
            "-map",
            "0:v:0",
            "-frames:v",
            "1",
            str(cover_path),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=8, check=False)
        if result.returncode != 0 or not cover_path.exists():
            return None
        return cover_path.read_bytes(), "image/png"


def extract_mp3_artwork_to_output(
    mp3_path: Path,
    output_path: Path,
    fallback_path: Path | None,
    output_size: tuple[int, int],
    fallback_size: tuple[int, int] | None = None,
) -> bool:
    artwork = extract_apic_image(mp3_path)
    if artwork is None:
        artwork = extract_ffmpeg_attached_picture(mp3_path)
    if artwork is not None:
        image_data, _mime = artwork
        return save_image_bytes_as_jpeg(image_data, output_path, output_size)
    if fallback_path and fallback_path.exists():
        return save_image_bytes_as_jpeg(fallback_path.read_bytes(), output_path, fallback_size or output_size)
    return False


def normalize_blt_osc_outputs(outputs: Any) -> list[dict[str, Any]]:
    by_key: dict[str, dict[str, Any]] = {}
    if isinstance(outputs, list):
        for item in outputs:
            if not isinstance(item, dict):
                continue
            key = text_value(item.get("key"))
            if key:
                by_key[key] = item

    normalized = []
    for default in DEFAULT_BLT_OSC_OUTPUTS:
        key = default["key"]
        item = by_key.get(key, {})
        field = text_value(item.get("field", default["field"])) or default["field"]
        if field not in BLT_FIELD_CHOICES:
            field = default["field"]
        normalized.append(
            {
                "key": key,
                "label": text_value(item.get("label", default["label"])) or default["label"],
                "field": field,
                "address": clean_osc_address(item.get("address", default["address"])),
                "enabled": bool_from_payload(item.get("enabled", default["enabled"]), bool(default["enabled"])),
            }
        )

    for key, item in by_key.items():
        if any(output["key"] == key for output in normalized):
            continue
        field = text_value(item.get("field", "full_track")) or "full_track"
        if field not in BLT_FIELD_CHOICES:
            field = "full_track"
        normalized.append(
            {
                "key": key,
                "label": text_value(item.get("label", key)) or key,
                "field": field,
                "address": clean_osc_address(item.get("address", "")),
                "enabled": bool_from_payload(item.get("enabled", False)),
            }
        )
    return normalized


class ShowEngine:
    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.state = make_state_from_template(DEFAULT_TEMPLATE)
        self.manual_mode = "cdj"
        self.last_event = "app server ready"
        self.last_command_time = ""
        self.command_log: list[str] = []
        self.bpm_running = False
        self.bpm = 125.0
        self.bpm_follow_now_playing = False
        self.bpm_division = "1/4"
        self.bpm_flip_mode = "bars"
        self.bpm_seconds = 8.0
        self.bpm_rotation_slots = list(DEFAULT_BPM_ROTATION_SLOTS)
        self.bpm_interval_ms = bpm_flip_interval_ms(self.bpm, self.bpm_division)
        self.bpm_thread: threading.Thread | None = None
        self.bpm_stop_event = threading.Event()
        self.bpm_resync_event = threading.Event()
        self.bpm_flip_count = 0
        self.bpm_last_flip_time = ""
        self.bpm_last_flip_monotonic = 0.0
        self.last_camera_buttons = {"main_box": "", "pip_box": "", "background": "", "scene": ""}
        self.last_visual_button = ""
        self.delivery_status = {"lights": {"last_sent": "", "count": 0}, "visuals": {"last_sent": "", "count": 0}, "cameras": {"last_sent": "", "count": 0}}
        self.active_generative_visual = dict(DEFAULT_GENERATIVE_VISUAL)
        self.active_look_name = ""
        self.active_show_step = ""
        self.camera_opacity = {"main_box": 100, "pip_box": 100, "background": 100}
        self.visual_opacity = 100
        self.now_playing_opacity = 100
        self.visual_slider_values: dict[str, int] = {}
        self.latest_blt_context: dict[str, str] = {}
        self.latest_blt_status = "Waiting for BeatLink watcher data"
        self.latest_blt_error = ""
        self.latest_blt_key = ""
        self.latest_blt_sources: list[dict[str, Any]] = []
        self.last_blt_poll_time = ""
        self.music_index: list[dict[str, str]] | None = None
        self.music_index_mtime = 0.0
        self.latest_matched_file = ""
        self.latest_match_score = 0.0
        self.latest_artwork_status = "Artwork waits for matched track"
        self.latest_artwork_track_key = ""
        self.latest_auto_palette_key = ""
        self.music_index_rebuild_status = {"running": False, "message": "Music index has not been rebuilt this session.", "count": 0, "path": str(INDEX_PATH), "started": "", "finished": ""}
        self.music_index_rebuild_thread: threading.Thread | None = None
        self.reload_from_config()

    def reload_from_config(self) -> None:
        config = load_config()
        with self.lock:
            template = config.get("default_fallback_template", DEFAULT_TEMPLATE)
            self.state = make_state_from_template(str(template))
            self.bpm = self.parse_bpm(config.get("bpm_flip_bpm", self.bpm))
            self.bpm_follow_now_playing = bool(config.get("bpm_follow_now_playing", False))
            self.bpm_division = normalize_bpm_swap_rate(config.get("bpm_flip_division", self.bpm_division))
            self.bpm_flip_mode = normalize_bpm_flip_mode(config.get("bpm_flip_mode", self.bpm_flip_mode))
            self.bpm_rotation_slots = normalize_bpm_rotation_slots(config.get("bpm_rotation_slots", self.bpm_rotation_slots), require_multiple=True)
            with contextlib.suppress(ValueError):
                self.bpm_seconds = parse_bpm_flip_seconds(config.get("bpm_flip_seconds", self.bpm_seconds))
            self.bpm_interval_ms = (
                bpm_seconds_interval_ms(self.bpm_seconds)
                if self.bpm_flip_mode == "seconds"
                else bpm_flip_interval_ms(self.bpm, self.bpm_division)
            )
            self.active_generative_visual = normalize_generative_visual(config.get("current_generative_visual", {}))
            slider_controls = normalize_visual_slider_controls(config.get("visual_slider_controls", []), config)
            existing_values = getattr(self, "visual_slider_values", {})
            self.visual_slider_values = {
                item["id"]: parse_percent(existing_values.get(item["id"], 100), 100)
                for item in slider_controls
            }
            self.visual_opacity = self.visual_slider_values.get("visual_slider_1", self.visual_opacity)
            self.now_playing_opacity = parse_percent(getattr(self, "now_playing_opacity", 100), 100)

    def parse_bpm(self, value: Any) -> float:
        try:
            return parse_bpm(value)
        except ValueError:
            return 125.0

    def config(self) -> dict[str, Any]:
        return load_config()

    def record_delivery(self, channel: str, sent: list[dict[str, Any]]) -> None:
        if not sent or channel not in {"lights", "visuals", "cameras"}:
            return
        with self.lock:
            self.delivery_status[channel] = {
                "last_sent": datetime.now().isoformat(timespec="seconds"),
                "count": len(sent),
            }

    def osc_target(self, config: dict[str, Any]) -> tuple[str, int]:
        targets = self.osc_targets(config)
        if targets:
            return targets[0]
        profile = active_connection_profile(config)
        host = text_value(profile.get("resolume_host", config.get("resolume_host", config.get("resolume_ip", "")))) or "127.0.0.1"
        port = parse_int(profile.get("resolume_port", config.get("resolume_port", 7000)), 7000, 1, 65535)
        return host, port

    def osc_targets(self, config: dict[str, Any]) -> list[tuple[str, int]]:
        targets = normalize_osc_targets(config.get("osc_targets", []), config)
        enabled = [
            (target["host"], int(target["port"]))
            for target in targets
            if target.get("enabled") and target.get("host")
        ]
        enabled.sort(key=lambda item: (
            not next((target.get("primary", False) for target in targets if target["host"] == item[0] and int(target["port"]) == item[1]), False),
            item[0],
            item[1],
        ))
        return enabled

    def link_label(self, config: dict[str, Any], link: int) -> str:
        labels = config.get("link_labels", {})
        default = DEFAULT_LINK_LABELS.get(str(link), f"Link {link}")
        return str(labels.get(str(link), default)).strip() or default

    def link_address(self, config: dict[str, Any], link: int) -> str:
        addresses = config.get("osc_addresses", {})
        default = DEFAULT_OSC_ADDRESSES[str(link)]
        return clean_osc_address(addresses.get(str(link), default))

    def link_extra_address_slots(self, config: dict[str, Any], link: int) -> list[str]:
        extras = config.get("osc_extra_addresses", {})
        raw = extras.get(str(link), []) if isinstance(extras, dict) else []
        if not isinstance(raw, list):
            raw = []
        slot_count = extra_osc_address_slots_for_link(link)
        cleaned = [clean_osc_address(address) for address in raw[:slot_count]]
        return [*cleaned, *( [""] * slot_count )][:slot_count]

    def link_extra_addresses(self, config: dict[str, Any], link: int) -> list[str]:
        return [address for address in self.link_extra_address_slots(config, link) if address]

    def link_output_notes(self, config: dict[str, Any], link: int) -> list[str]:
        notes = config.get("osc_output_notes", {})
        raw = notes.get(str(link), []) if isinstance(notes, dict) else []
        if not isinstance(raw, list):
            raw = []
        slot_count = osc_output_slots_for_link(link)
        cleaned = [text_value(note) for note in raw[:slot_count]]
        return [*cleaned, *( [""] * slot_count )][:slot_count]

    def link_addresses(self, config: dict[str, Any], link: int) -> list[str]:
        return [self.link_address(config, link), *self.link_extra_addresses(config, link)]

    def send_osc_float(self, config: dict[str, Any], address: str, value: float, log_send: bool = True) -> None:
        address = clean_osc_address(address)
        if not address:
            return
        targets = self.osc_targets(config)
        packet = osc_string(address) + osc_string(",f") + struct.pack(">f", float(value))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(0.05)
            sent_count = 0
            for target in targets:
                try:
                    sock.sendto(packet, target)
                    sent_count += 1
                except OSError as exc:
                    self.log_command(f"OSC send failed {target[0]}:{target[1]} {address}: {exc}")
        if log_send:
            self.log_command(f"OSC float {address} -> {value:.3f} ({sent_count} targets)")

    def send_osc_string(self, config: dict[str, Any], address: str, value: str) -> None:
        address = clean_osc_address(address)
        if not address:
            return
        targets = self.osc_targets(config)
        packet = osc_string(address) + osc_string(",s") + osc_string(str(value))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(0.05)
            sent_count = 0
            for target in targets:
                try:
                    sock.sendto(packet, target)
                    sent_count += 1
                except OSError as exc:
                    self.log_command(f"OSC send failed {target[0]}:{target[1]} {address}: {exc}")
        self.log_command(f"OSC text {address} -> {value} ({sent_count} targets)")

    def state_control_value_label(self, config: dict[str, Any], key: str) -> tuple[int, float, str]:
        link = CONTROL_TO_LINK[key]
        label = self.link_label(config, link)
        if key == "color1":
            return link, self.state.color1_value, f"{label} {self.state.color1_name}"
        if key == "color2":
            return link, self.state.color2_value, f"{label} {self.state.color2_name}"
        if key == "motion":
            return link, self.state.motion_value, f"{label} {round(self.state.motion_value * 100)}%"
        if key == "strobe_color":
            return link, self.state.strobe_color_value, f"{label} {self.state.strobe_color_name}"
        if key == "saturation":
            return link, self.state.saturation_value, f"{label} {self.state.saturation_percent}%"
        if key == "brightness":
            return link, self.state.brightness_value, f"{label} {self.state.brightness_percent}%"
        if key == "fx":
            return link, self.state.fx_value, f"{label} {round(self.state.fx_value * 100)}%"
        if key == "pulse":
            return link, self.state.pulse_value, f"{label} {round(self.state.pulse_value * 100)}%"
        raise KeyError(key)

    def send_state(self, source: str) -> list[dict[str, Any]]:
        sent = []
        config = self.config()
        with self.lock:
            for link, _label, key, _kind in LINK_CONTROL_SPECS:
                _link, value, label = self.state_control_value_label(config, key)
                for index, address in enumerate(self.link_addresses(config, link)):
                    self.send_osc_float(config, address, value)
                    sent.append({"link": link, "label": label, "address": address, "value": value, "slot": index})
            self.set_event(f"Sent {source} to Resolume")
        self.record_delivery("lights", sent)
        return sent

    def send_color_pair(self, source: str, config: dict[str, Any] | None = None, log_event: bool = True) -> list[dict[str, Any]]:
        sent = []
        config = config or self.config()
        pending: list[tuple[int, str, str, float, int]] = []
        with self.lock:
            for key in ("color1", "color2"):
                link, value, label = self.state_control_value_label(config, key)
                for index, address in enumerate(self.link_addresses(config, link)):
                    pending.append((link, label, address, value, index))
        for link, label, address, value, index in pending:
            self.send_osc_float(config, address, value, log_send=log_event)
            sent.append({"link": link, "label": label, "address": address, "value": value, "slot": index})
        if log_event:
            with self.lock:
                self.set_event(f"Sent {source} color rotation")
        return sent

    def send_color_links(self, source: str, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        sent = []
        config = config or self.config()
        pending: list[tuple[int, str, str, float, int]] = []
        with self.lock:
            for key in ("color1", "color2", "strobe_color"):
                link, value, label = self.state_control_value_label(config, key)
                for index, address in enumerate(self.link_addresses(config, link)):
                    pending.append((link, label, address, value, index))
        for link, label, address, value, index in pending:
            self.send_osc_float(config, address, value)
            sent.append({"link": link, "label": label, "address": address, "value": value, "slot": index})
        with self.lock:
            self.set_event(f"Sent {source} color links")
        return sent

    def send_control_keys(self, keys: list[str], source: str, config: dict[str, Any] | None = None, log_event: bool = True) -> list[dict[str, Any]]:
        sent = []
        config = config or self.config()
        pending: list[tuple[int, str, str, float, int]] = []
        with self.lock:
            for key in keys:
                link, value, label = self.state_control_value_label(config, key)
                for index, address in enumerate(self.link_addresses(config, link)):
                    pending.append((link, label, address, value, index))
        for link, label, address, value, index in pending:
            self.send_osc_float(config, address, value, log_send=log_event)
            sent.append({"link": link, "label": label, "address": address, "value": value, "slot": index})
        if log_event:
            with self.lock:
                self.set_event(f"Sent {source}")
        return sent

    def preset_groups(self) -> dict[str, dict[str, Any]]:
        config = self.config()
        return {
            "performance": dict(config.get("performance_presets", PERFORMANCE_PRESETS)),
            "mood": dict(config.get("mood_presets", {})),
            "energy": dict(config.get("energy_presets", {})),
            "section": dict(config.get("section_presets", {})),
        }

    def preset_payload(self) -> dict[str, Any]:
        return {
            "groups": self.preset_groups(),
            "labels": PRESET_GROUP_LABELS,
            "columns": [
                {"key": "PRIMARY", "kind": "color", "label": "Color 1"},
                {"key": "SECONDARY", "kind": "color", "label": "Color 2"},
                {"key": "STROBE", "kind": "color", "label": "Color 3"},
            ],
            "colors": {"names": SORTED_COLOR_NAMES, "hex": COLOR_HEX},
            "percent_choices": PERCENT_CHOICES,
        }

    def save_preset_group(self, group: str, presets: dict[str, Any]) -> dict[str, Any]:
        group = str(group or "").strip().casefold()
        if group not in PRESET_GROUP_KEYS:
            raise ValueError(f"Unknown preset group: {group}")
        if not isinstance(presets, dict):
            raise ValueError("Presets must be an object.")
        config = self.config()
        cleaned: dict[str, dict[str, Any]] = {}
        is_performance_group = group == "performance"
        for raw_name, raw_values in presets.items():
            name = text_value(raw_name)
            if not name or not isinstance(raw_values, dict):
                continue
            values: dict[str, Any] = {}
            for key, value in raw_values.items():
                normalized = normalized_key(str(key))
                if normalized in {"PRIMARY", "SECONDARY", "STROBE"}:
                    values[normalized] = color_name_to_value(str(value), "indigo")[0]
                elif not is_performance_group and normalized in {"MOTION", "STROBE_PERCENT", "SATURATION", "BRIGHTNESS", "FX", "PULSE"}:
                    values[normalized] = parse_percent(value)
                elif normalized in {"MOOD", "ENERGY", "SECTION"}:
                    values[normalized] = text_value(value)
            cleaned[name] = values
        config[PRESET_GROUP_KEYS[group]] = cleaned
        save_config(config)
        self.set_event(f"Saved {PRESET_GROUP_LABELS[group]}")
        return {"ok": True, "message": f"Saved {PRESET_GROUP_LABELS[group]}", "presets": self.preset_payload(), "state": self.snapshot()}

    def current_performance_values(self) -> dict[str, Any]:
        with self.lock:
            return {
                "PRIMARY": self.state.color1_name,
                "SECONDARY": self.state.color2_name,
                "STROBE": self.state.strobe_color_name,
            }

    def save_current_look(self, name: str) -> dict[str, Any]:
        name = text_value(name)
        if not name:
            raise ValueError("Choose a look to save.")
        config = self.config()
        presets = dict(config.get("performance_presets", PERFORMANCE_PRESETS))

        presets[name] = self.current_performance_values()
        config["performance_presets"] = presets

        links = normalize_preset_links(config.get("preset_links", {}), list(presets.keys()))
        with self.lock:
            links[name] = {
                "enabled": True,
                "section_preset": self.state.section if self.state.section in dict(config.get("section_presets", {})) else "",
                "now_playing_mode": self.manual_mode if self.manual_mode in {"cdj", "vinyl", "studio", "videogame"} else "",
                "now_playing_opacity": self.now_playing_opacity,
                "visual_id": self.last_visual_button,
                "generative_visual": dict(self.active_generative_visual),
                "bpm_enabled": True,
                "bpm_running": self.bpm_running,
                "bpm_follow_now_playing": self.bpm_follow_now_playing,
                "bpm": self.bpm,
                "bpm_division": self.bpm_division,
                "bpm_flip_mode": self.bpm_flip_mode,
                "bpm_seconds": self.bpm_seconds,
                "bpm_rotation_slots": list(self.bpm_rotation_slots),
                "main_box_id": self.last_camera_buttons.get("main_box", ""),
                "pip_box_id": self.last_camera_buttons.get("pip_box", ""),
                "background_id": self.last_camera_buttons.get("background", ""),
                "scene_id": self.last_camera_buttons.get("scene", ""),
            }
            self.state.source = f"performance:{name}"
        config["preset_links"] = links

        save_config(config)
        self.set_event(f"Saved current show state to {name}")
        return {
            "ok": True,
            "message": f"Saved current show state to {name}",
            "config": self.config_payload(),
            "presets": self.preset_payload(),
            "state": self.snapshot(),
        }

    def apply_preset(self, name: str, group: str = "performance", apply_lights: Any = None) -> dict[str, Any]:
        group = str(group or "performance").strip().casefold()
        if group not in PRESET_GROUP_KEYS:
            raise ValueError(f"Unknown preset group: {group}")
        config = self.config()
        presets = self.preset_groups()[group]
        if name not in presets:
            raise ValueError(f"Unknown preset: {name}")
        apply_light_state = True
        if group == "performance":
            apply_light_state = bool(config.get("look_apply_lights", True)) if apply_lights is None else bool_from_payload(apply_lights)
        sent: list[dict[str, Any]] = []
        if apply_light_state:
            with self.lock:
                keep_colors = bool(config.get("preset_keep_current_colors", False)) and group == "performance"
                current_colors = {
                    "PRIMARY": self.state.color1_name,
                    "SECONDARY": self.state.color2_name,
                    "STROBE": self.state.strobe_color_name,
                }
                apply_values_to_state(self.state, presets[name], exact=True)
                if keep_colors:
                    apply_values_to_state(self.state, current_colors, exact=False)
                self.state.source = f"{group}:{name}"
                if group == "performance":
                    self.active_look_name = name
            sent = self.send_state(f"{group} preset {name}")
        elif group == "performance":
            with self.lock:
                self.active_look_name = name
                self.set_event(f"{name} media look recalled; lights held")
        linked_sent = self.send_preset_link_actions(config, name, apply_lights=apply_light_state) if group == "performance" else []
        auto_palette_sent: list[dict[str, Any]] = []
        if apply_light_state and bool(config.get("use_artwork_palette", False)):
            auto_palette_sent = self.maybe_auto_apply_artwork_palette(fallback_used=False, track_key=f"look:{name}", force=True)
        if linked_sent:
            if apply_light_state:
                self.set_event(f"Applied {name} with linked visual/camera look")
            else:
                self.set_event(f"Applied {name} media look; lights held")
        message = f"Applied {name}" if apply_light_state else f"Applied {name}; lights held"
        return {"ok": True, "message": message, "sent": [*sent, *linked_sent, *auto_palette_sent], "state": self.snapshot()}

    def color_comment(self) -> str:
        with self.lock:
            return (
                f"COLOR1={self.state.color1_name};"
                f"COLOR2={self.state.color2_name};"
                f"COLOR3={self.state.strobe_color_name};"
                f"STROBE_PERCENT={self.state.strobe_percent};"
                f"SATURATION={self.state.saturation_percent};"
                f"BRIGHTNESS={self.state.brightness_percent};"
                f"MOTION={round(self.state.motion_value * 100)};"
                f"FX={round(self.state.fx_value * 100)};"
                f"PULSE={round(self.state.pulse_value * 100)}"
            )

    def rotate_selected_colors(self, slots: Any = None, source: str = "manual rotation") -> dict[str, Any]:
        config = self.config()
        keys = normalize_bpm_rotation_slots(slots if slots is not None else config.get("bpm_rotation_slots", self.bpm_rotation_slots), require_multiple=True)
        with self.lock:
            self.bpm_rotation_slots = list(keys)
            self.rotate_color_slots(keys)
            self.state.source = source
        label = " + ".join(COLOR_SLOT_LABELS.get(key, key) for key in keys)
        sent = self.send_control_keys(keys, source)
        if bool(config.get("use_artwork_palette", False)):
            sent.extend(self.maybe_auto_apply_artwork_palette(fallback_used=False, track_key=f"manual:{source}", force=True))
        return {"ok": True, "message": f"Rotated {label}", "sent": sent, "state": self.snapshot()}

    def swap_primary_secondary(self, source: str = "manual rotation") -> dict[str, Any]:
        return self.rotate_selected_colors(["color1", "color2"], source)

    def apply_color_relationship(self, relationship: str) -> dict[str, Any]:
        relationship = str(relationship or "").strip().casefold().replace("_", "-")
        with self.lock:
            primary = self.state.color1_value
            if relationship == "complement":
                secondary = (primary + 0.5) % 1.0
                accent = primary
            elif relationship == "analogous":
                secondary = (primary + 1.0 / 12.0) % 1.0
                accent = (primary - 1.0 / 12.0) % 1.0
            elif relationship == "triad":
                secondary = (primary + 1.0 / 3.0) % 1.0
                accent = (primary + 2.0 / 3.0) % 1.0
            elif relationship == "split-a":
                secondary = (primary + 5.0 / 12.0) % 1.0
                accent = (primary - 5.0 / 12.0) % 1.0
            elif relationship == "split-b":
                secondary = (primary - 5.0 / 12.0) % 1.0
                accent = (primary + 5.0 / 12.0) % 1.0
            else:
                raise ValueError(f"Unknown color relationship: {relationship}")
            secondary_name = nearest_color_name(secondary)
            accent_name = nearest_color_name(accent)
            self.state.color2_name, self.state.color2_value = color_name_to_value(secondary_name, self.state.color2_name)
            self.state.strobe_color_name, self.state.strobe_color_value = color_name_to_value(accent_name, self.state.strobe_color_name)
            self.state.source = f"relationship:{relationship}"
        sent = self.send_state(f"color relationship {relationship}")
        if bool(self.config().get("use_artwork_palette", False)):
            sent.extend(self.maybe_auto_apply_artwork_palette(fallback_used=False, track_key=f"relationship:{relationship}", force=True))
        return {"ok": True, "message": f"Applied {relationship}", "sent": sent, "state": self.snapshot()}

    def apply_artwork_palette(self) -> dict[str, Any]:
        palette = self.extract_artwork_palette()
        sent = self.set_state_from_artwork_palette(palette, "artwork palette", send=True)
        return {"ok": True, "message": "Applied artwork palette", "palette": palette, "sent": sent, "state": self.snapshot()}

    def set_state_from_artwork_palette(self, palette: dict[str, Any], source: str, send: bool) -> list[dict[str, Any]]:
        with self.lock:
            if not palette["colors"]:
                raise ValueError("No usable artwork colors found.")
            colors = palette["colors"]
            color1 = colors[0]["name"]
            color2 = colors[1]["name"] if len(colors) > 1 else color1
            color3 = colors[2]["name"] if len(colors) > 2 else color2
            self.state.color1_name, self.state.color1_value = color_name_to_value(color1, self.state.color1_name)
            self.state.color2_name, self.state.color2_value = color_name_to_value(color2, self.state.color2_name)
            self.state.strobe_color_name, self.state.strobe_color_value = color_name_to_value(color3, self.state.strobe_color_name)
            self.state.source = source
        if send:
            return self.send_color_links(source)
        return []

    def maybe_auto_apply_artwork_palette(self, fallback_used: bool, track_key: str = "", force: bool = False) -> list[dict[str, Any]]:
        config = self.config()
        if not bool(config.get("use_artwork_palette", False)):
            return []
        path = artwork_output_path(config)
        try:
            artwork_stamp = path.stat().st_mtime_ns if path.exists() else 0
        except OSError:
            artwork_stamp = 0
        neutral_key = "|".join(
            text_value(config.get(key, config.get("neutral_artwork_color", "")))
            for key in ("neutral_artwork_primary", "neutral_artwork_secondary", "neutral_artwork_accent")
        )
        auto_key = f"{track_key}|artwork={artwork_stamp}|fallback={fallback_used}|neutral={neutral_key}"
        if not force and auto_key == self.latest_auto_palette_key:
            return []
        try:
            palette = self.extract_artwork_palette()
            sent = self.set_state_from_artwork_palette(palette, "artwork-auto", send=True)
            self.latest_auto_palette_key = auto_key
            self.log_command(f"Auto artwork colors applied: {palette.get('message', 'palette')}")
            return sent
        except Exception as exc:
            self.log_command(f"Auto artwork colors skipped: {exc}")
            return []

    def extract_artwork_palette(self) -> dict[str, Any]:
        config = self.config()
        path = artwork_output_path(config)
        if not path.exists():
            return {"available": False, "path": str(path), "colors": [], "message": "Current artwork file not found."}
        try:
            from PIL import Image
        except ModuleNotFoundError:
            return {"available": False, "path": str(path), "colors": [], "message": "Pillow is required for palette extraction."}
        try:
            with Image.open(path) as image:
                image = image.convert("RGB")
                image.thumbnail((180, 180))
                small = image.resize((120, 120))
                colors = small.quantize(colors=64, method=Image.Quantize.MEDIANCUT).convert("RGB").getcolors(120 * 120) or []
        except Exception as exc:
            return {"available": False, "path": str(path), "colors": [], "message": f"Palette unavailable: {exc}"}

        def neutral_items() -> list[dict[str, Any]]:
            fallback = text_value(config.get("neutral_artwork_color", "blue")).casefold()
            names = [
                text_value(config.get("neutral_artwork_primary", fallback or "blue")).casefold(),
                text_value(config.get("neutral_artwork_secondary", "blue")).casefold(),
                text_value(config.get("neutral_artwork_accent", "magenta")).casefold(),
            ]
            cleaned = []
            for index, (name, fallback_name) in enumerate(zip(names, ("blue", "teal", "magenta")), start=1):
                if name not in COLOR_HEX:
                    name = fallback_name
                r, g, b = color_hex_to_rgb(COLOR_HEX[name])
                cleaned.append({"name": name, "hex": f"#{r:02x}{g:02x}{b:02x}", "rgb": [r, g, b], "source": "neutral", "role": f"Color {index}"})
            return cleaned

        neutral_palette = neutral_items()
        total_count = sum(count for count, _rgb in colors) or 1
        colorful_count = 0
        bright_count = 0
        candidates: list[dict[str, Any]] = []
        for count, rgb in colors:
            r, g, b = rgb
            hue, saturation, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            luma = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
            if saturation < ARTWORK_MIN_SATURATION or value < ARTWORK_MIN_USABLE_VALUE:
                continue
            colorful_count += count
            if value < ARTWORK_MIN_BRIGHT_VALUE:
                continue
            bright_count += count
            population = (count / total_count) ** 0.46
            vividness = saturation ** 2.4
            brightness = value ** 3.0
            luma_bonus = 0.72 + (0.28 * luma)
            score = population * vividness * brightness * luma_bonus
            candidates.append(
                {
                    "score": score,
                    "count": count,
                    "rgb": rgb,
                    "hue": hue,
                    "saturation": saturation,
                    "value": value,
                    "luma": luma,
                    "name": self.rgb_to_color_name(rgb),
                }
            )

        colorful_ratio = colorful_count / total_count
        bright_ratio = bright_count / total_count
        if not candidates or colorful_ratio < ARTWORK_MIN_COLORFUL_RATIO or bright_ratio < ARTWORK_MIN_BRIGHT_RATIO:
            return {
                "available": True,
                "path": str(path),
                "colors": neutral_palette,
                "message": "Neutral palette: artwork is mostly dark, white, black, or low saturation.",
                "neutral": True,
            }

        candidates.sort(key=lambda item: item["score"], reverse=True)
        selected: list[dict[str, Any]] = []
        selected_hues: list[float] = []
        used_names: set[str] = set()

        def add_candidate(candidate: dict[str, Any], role: str) -> bool:
            name = str(candidate["name"])
            if name in used_names:
                return False
            r, g, b = candidate["rgb"]
            selected.append(
                {
                    "name": name,
                    "hex": f"#{r:02x}{g:02x}{b:02x}",
                    "rgb": [r, g, b],
                    "source": "artwork",
                    "role": role,
                    "brightness": round(float(candidate["value"]), 3),
                    "saturation": round(float(candidate["saturation"]), 3),
                }
            )
            selected_hues.append(float(candidate["hue"]))
            used_names.add(name)
            return True

        add_candidate(candidates[0], "Color 1")
        for role, separation in (("Color 2", ARTWORK_PRIMARY_HUE_SEPARATION), ("Color 3", ARTWORK_ACCENT_HUE_SEPARATION)):
            best = None
            best_score = -1.0
            for candidate in candidates[1:]:
                if str(candidate["name"]) in used_names:
                    continue
                distance = min(self.hue_distance(float(candidate["hue"]), hue) for hue in selected_hues)
                if distance < separation:
                    continue
                role_score = float(candidate["score"]) * (1.0 + min(distance, 0.5))
                if role == "Color 3":
                    role_score *= 0.82 + (0.42 * float(candidate["saturation"]))
                if role_score > best_score:
                    best = candidate
                    best_score = role_score
            if best and add_candidate(best, role):
                continue
            for candidate in candidates[1:]:
                if str(candidate["name"]) not in used_names and add_candidate(candidate, role):
                    break

        if len(selected) < 3:
            for index in range(len(selected), 3):
                selected.append(dict(neutral_palette[index]))
        message = "Bright artwork palette extracted" if all(item.get("source") == "artwork" for item in selected) else "Bright artwork palette extracted with neutral fallback roles"
        return {"available": bool(selected), "path": str(path), "colors": selected, "message": message, "neutral": False}

    def rgb_to_color_name(self, rgb: tuple[int, int, int]) -> str:
        r, g, b = rgb
        hue, _sat, _value = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        return nearest_color_name(hue)

    @staticmethod
    def hue_distance(a: float, b: float) -> float:
        diff = abs(a - b) % 1.0
        return min(diff, 1.0 - diff)

    def write_placeholder_artwork(self, source_path: Path, status_label: str, size_source: str = "fallback") -> None:
        config = self.config()
        output_path = artwork_output_path(config)
        output_size = artwork_dimensions(config, size_source)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_handle = tempfile.NamedTemporaryFile(
            prefix=f"{output_path.stem}.",
            suffix=f".tmp{output_path.suffix}",
            dir=output_path.parent,
            delete=False,
        )
        temp_output_path = Path(temp_handle.name)
        temp_handle.close()
        try:
            try:
                from PIL import Image, ImageOps
            except ModuleNotFoundError:
                if source_path.suffix.casefold() != output_path.suffix.casefold():
                    raise RuntimeError(
                        "Pillow is required to convert this artwork format. Install requirements.txt for the Python used by the app server."
                    )
                shutil.copyfile(source_path, temp_output_path)
            else:
                with Image.open(source_path) as source_image:
                    source_image.load()
                    canvas = render_artwork_canvas(source_image, output_size)
                    canvas.save(
                        temp_output_path,
                        format="JPEG",
                        quality=95,
                        optimize=False,
                        progressive=False,
                        subsampling=0,
                    )
            last_error: OSError | None = None
            for attempt in range(6):
                try:
                    temp_output_path.replace(output_path)
                    last_error = None
                    break
                except PermissionError as exc:
                    last_error = exc
                    time.sleep(0.12 * (attempt + 1))
            if last_error is not None:
                raise PermissionError(
                    f"Could not update {output_path}. Resolume or another preview may be holding the file open; try again in a moment."
                ) from last_error
        finally:
            with contextlib.suppress(OSError):
                if temp_output_path.exists():
                    temp_output_path.unlink()
        with contextlib.suppress(OSError):
            os.utime(output_path, None)
        self.set_event(f"{status_label} artwork active: {source_path.name} ({artwork_size_label(output_size)})")

    def manual_context(self, text: str, mode: str) -> dict[str, str]:
        return {
            "title": text,
            "artist": mode,
            "album": mode,
            "full_track": text,
            "track_info": text,
            "bpm": "",
            "player_number": mode,
            "device_name": "remote",
            "source_player": mode,
            "player": mode,
            "comment": "",
        }

    def player_track_context(self, player: dict[str, Any]) -> dict[str, str]:
        track = player.get("track") if isinstance(player.get("track"), dict) else {}
        title = text_value(track.get("title", ""))
        artist = text_value(track.get("artist", ""))
        album = text_value(track.get("album", ""))
        comment = text_value(track.get("comment", ""))
        bpm = text_value(player.get("track-bpm", track.get("starting-tempo", "")))
        tempo = text_value(player.get("tempo", ""))
        player_number = text_value(player.get("number", ""))
        device_name = text_value(player.get("name", ""))
        source_player = text_value(player.get("track-source-player", player_number))
        player_label = f"Player {player_number}".strip()
        full_track = " - ".join(part for part in (artist, title) if part) or title or "Loaded track"
        track_info_parts = []
        if bpm:
            track_info_parts.append(f"{bpm} BPM")
        if player_label:
            track_info_parts.append(player_label)
        if device_name:
            track_info_parts.append(device_name)
        if tempo and tempo != bpm:
            track_info_parts.append(f"tempo {tempo}")
        return {
            "title": title,
            "artist": artist,
            "album": album,
            "full_track": full_track,
            "track_info": " | ".join(track_info_parts),
            "bpm": bpm,
            "tempo": tempo,
            "player_number": player_number,
            "device_name": device_name,
            "source_player": source_player,
            "player": player_label,
            "comment": comment,
            "track_id": text_value(track.get("id", "")),
            "track_number": text_value(player.get("track-number", "")),
        }

    def is_active_master_player(self, player: dict[str, Any]) -> bool:
        return (
            bool(player.get("is-track-loaded"))
            and bool(player.get("is-playing"))
            and not bool(player.get("is-paused"))
            and not bool(player.get("is-at-end"))
        )

    def choose_blt_player(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        master = payload.get("master")
        if isinstance(master, dict) and self.is_active_master_player(master):
            return master
        return None

    def blt_track_key(self, context: dict[str, str]) -> str:
        return "|".join(
            [
                context.get("source_player", ""),
                context.get("track_id", ""),
                context.get("track_number", ""),
                context.get("artist", ""),
                context.get("title", ""),
            ]
        )

    def fetch_blt_context(self, source: dict[str, Any] | None = None) -> dict[str, str]:
        config = self.config()
        source = source or {"id": "active_profile", "label": "Active profile", "url": profile_blt_url(config)}
        url = text_value(source.get("url", ""))
        if not url:
            raise RuntimeError("BLT params URL is not configured.")
        with urlopen(url, timeout=BLT_SOURCE_TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeError("BLT params response was not a JSON object.")
        player = self.choose_blt_player(payload)
        if not player:
            raise RuntimeError("BLT connected; waiting for the current master deck to be playing.")
        context = self.player_track_context(player)
        context["blt_source_id"] = text_value(source.get("id", ""))
        context["blt_source_label"] = text_value(source.get("label", ""))
        context["blt_source_url"] = url
        return context

    def load_music_index(self) -> list[dict[str, str]]:
        index_path = INDEX_PATH if INDEX_PATH.exists() else LEGACY_INDEX_PATH
        try:
            mtime = index_path.stat().st_mtime
        except FileNotFoundError:
            with self.lock:
                self.latest_artwork_status = f"Music index not found: {INDEX_PATH}"
            return []
        if self.music_index is not None and self.music_index_mtime == mtime:
            return self.music_index
        try:
            entries = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception as exc:
            with self.lock:
                self.latest_artwork_status = f"Could not read music index: {exc}"
            return []
        if not isinstance(entries, list):
            with self.lock:
                self.latest_artwork_status = "Music index has an unexpected format"
            return []
        self.music_index = entries
        self.music_index_mtime = mtime
        self.log_command(f"Loaded music index: {len(entries)} tracks")
        return entries

    def write_fallback_artwork(self, reason: str, track_key: str = "", matched_file: str = "", match_score: float = 0.0) -> None:
        config = self.config()
        fallback_path = text_value(config.get("fallback_artwork_path", ""))
        if not fallback_path:
            with self.lock:
                self.latest_artwork_status = f"{reason}; fallback artwork is not configured"
                self.latest_artwork_track_key = track_key
                self.latest_matched_file = matched_file
                self.latest_match_score = match_score
            return
        fallback = portable_project_path(fallback_path)
        if not fallback.exists():
            with self.lock:
                self.latest_artwork_status = f"{reason}; fallback artwork missing: {fallback}"
                self.latest_artwork_track_key = track_key
                self.latest_matched_file = matched_file
                self.latest_match_score = match_score
            return
        try:
            self.write_placeholder_artwork(fallback, "Fallback artwork", "fallback")
            status = f"{reason}; showing fallback artwork: {fallback.name}"
        except Exception as exc:
            status = f"{reason}; fallback artwork failed: {exc}"
        with self.lock:
            self.latest_matched_file = matched_file
            self.latest_match_score = match_score
            self.latest_artwork_status = status
            self.latest_artwork_track_key = track_key
        self.maybe_auto_apply_artwork_palette(fallback_used=True, track_key=track_key, force=True)

    def update_track_artwork(self, context: dict[str, str], track_key: str, force: bool = False) -> dict[str, str]:
        if not force and track_key and track_key == self.latest_artwork_track_key:
            return context
        index = self.load_music_index()
        if not index:
            self.write_fallback_artwork("Music index unavailable for artwork", track_key)
            return context
        match = find_best_track_match(context, index)
        if not match:
            self.write_fallback_artwork("No confident local MP3 match for artwork", track_key)
            self.log_command("No confident local MP3 match for current BeatLink track")
            return context

        entry, score = match
        config = self.config()
        mp3_path = resolve_indexed_mp3_path(entry, config)
        indexed_path = Path(entry["path"])
        output_path = artwork_output_path(config)
        fallback_path = text_value(config.get("fallback_artwork_path", ""))
        fallback_artwork = portable_project_path(fallback_path) if fallback_path else None
        output_size = artwork_dimensions(config, "cdj")
        fallback_size = artwork_dimensions(config, "fallback")
        try:
            if not mp3_path.exists():
                raise FileNotFoundError(f"matched MP3 is not available: {indexed_path}")
            ok = extract_mp3_artwork_to_output(mp3_path, output_path, fallback_artwork, output_size, fallback_size)
            artwork_status = f"Artwork extracted from {mp3_path.name} to {output_path.name} ({artwork_size_label(output_size)})" if ok else f"No embedded artwork for {mp3_path.name}"
        except Exception as exc:
            ok = False
            artwork_status = f"Artwork extraction failed for {mp3_path.name}: {exc}"
        if not ok:
            self.write_fallback_artwork(artwork_status, track_key, str(mp3_path), score)
            artwork_status = self.latest_artwork_status
        else:
            self.maybe_auto_apply_artwork_palette(fallback_used=False, track_key=track_key, force=force)
        comment = text_value(entry.get("comment", ""))
        comment_source = "music index comment" if comment else "no cached comment"
        context.update(
            {
                "comment": comment,
                "comment_source": comment_source,
                "matched_file": str(mp3_path),
                "match_score": f"{score:.0%}",
            }
        )
        with self.lock:
            self.latest_matched_file = str(mp3_path)
            self.latest_match_score = score
            self.latest_artwork_status = artwork_status
            self.latest_artwork_track_key = track_key
        self.log_command(f"Matched artwork MP3 {mp3_path.name} ({score:.0%})")
        return context

    def _run_music_index_rebuild(self, music_root: Path) -> None:
        try:
            entries = build_music_library_index(music_root)
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            temp_path = INDEX_PATH.with_suffix(".tmp")
            temp_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
            temp_path.replace(INDEX_PATH)
            with self.lock:
                self.music_index = entries
                self.music_index_mtime = INDEX_PATH.stat().st_mtime
                self.latest_artwork_status = f"Music index rebuilt: {len(entries)} tracks"
                self.latest_artwork_track_key = ""
                self.music_index_rebuild_status = {
                    "running": False,
                    "message": f"Music index rebuilt: {len(entries)} tracks",
                    "count": len(entries),
                    "path": str(INDEX_PATH),
                    "started": self.music_index_rebuild_status.get("started", ""),
                    "finished": datetime.now().isoformat(timespec="seconds"),
                }
            if self.manual_mode == "cdj" and self.latest_blt_context:
                track_key = self.blt_track_key(self.latest_blt_context)
                context = self.update_track_artwork(dict(self.latest_blt_context), track_key, force=True)
                self.send_blt_outputs(context, "BeatLink after music index rebuild")
                with self.lock:
                    self.latest_blt_context = context
            self.set_event(f"Music index rebuilt: {len(entries)} tracks")
        except Exception as exc:
            message = f"Music index rebuild failed: {exc}"
            with self.lock:
                self.latest_artwork_status = message
                self.music_index_rebuild_status = {
                    "running": False,
                    "message": message,
                    "count": 0,
                    "path": str(INDEX_PATH),
                    "started": self.music_index_rebuild_status.get("started", ""),
                    "finished": datetime.now().isoformat(timespec="seconds"),
                }
            self.set_event(message)

    def rebuild_music_index(self) -> dict[str, Any]:
        config = self.config()
        music_root = portable_project_path(config.get("music_root", ""))
        if not text_value(config.get("music_root", "")):
            raise ValueError("Set Music Root before rebuilding the music index.")
        if not music_root.exists() or not music_root.is_dir():
            raise ValueError(f"Music Root is not available: {music_root}")
        with self.lock:
            if self.music_index_rebuild_status.get("running"):
                return {"ok": True, "message": self.music_index_rebuild_status.get("message", "Music index rebuild already running."), "rebuild": dict(self.music_index_rebuild_status), "state": self.snapshot()}
            started = datetime.now().isoformat(timespec="seconds")
            self.music_index_rebuild_status = {
                "running": True,
                "message": f"Rebuilding music index from {music_root}...",
                "count": 0,
                "path": str(INDEX_PATH),
                "started": started,
                "finished": "",
            }
            self.latest_artwork_status = self.music_index_rebuild_status["message"]
            self.music_index_rebuild_thread = threading.Thread(target=self._run_music_index_rebuild, args=(music_root,), daemon=True)
            self.music_index_rebuild_thread.start()
        self.set_event("Music index rebuild started")
        return {"ok": True, "message": "Music index rebuild started", "rebuild": dict(self.music_index_rebuild_status), "state": self.snapshot()}

    def blt_status_snapshot(self) -> dict[str, Any]:
        with self.lock:
            return {
                "ok": not bool(self.latest_blt_error),
                "status": self.latest_blt_status,
                "context": dict(self.latest_blt_context),
                "error": self.latest_blt_error,
                "sources": [dict(source) for source in self.latest_blt_sources],
                "cached": True,
                "last_poll_time": self.last_blt_poll_time,
            }

    def poll_blt(self, send_on_change: bool = True) -> dict[str, Any]:
        config = self.config()
        sources = blt_sources(config)
        if not sources:
            with self.lock:
                self.latest_blt_error = "BLT params URL is not configured."
                self.latest_blt_status = "BeatLink unavailable: BLT params URL is not configured."
                self.latest_blt_sources = []
                self.last_blt_poll_time = datetime.now().isoformat(timespec="seconds")
            return {"ok": False, "status": self.latest_blt_status, "context": self.latest_blt_context, "error": self.latest_blt_error, "sources": []}

        source_results: list[dict[str, Any]] = []
        selected: tuple[dict[str, Any], dict[str, str], str] | None = None
        results_by_index: list[tuple[dict[str, Any], dict[str, str] | None, str] | None] = [None] * len(sources)

        def read_source(index: int, source: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, str] | None, str]:
            try:
                context = self.fetch_blt_context(source)
                track_key = self.blt_track_key(context)
                return index, {
                    "id": source["id"],
                    "label": source["label"],
                    "url": source["url"],
                    "preferred": bool(source.get("preferred")),
                    "ok": True,
                    "status": "Live track loaded",
                    "track": {
                        "title": context.get("title", ""),
                        "artist": context.get("artist", ""),
                        "full_track": context.get("full_track", ""),
                        "player": context.get("player", context.get("device_name", "")),
                    },
                }, context, track_key
            except Exception as exc:
                message = str(exc)
                return index, {
                    "id": source["id"],
                    "label": source["label"],
                    "url": source["url"],
                    "preferred": bool(source.get("preferred")),
                    "ok": False,
                    "status": message,
                    "error": message,
                }, None, ""

        executor = ThreadPoolExecutor(max_workers=max(1, min(len(sources), 4)))
        futures = [executor.submit(read_source, index, source) for index, source in enumerate(sources)]
        try:
            for future in as_completed(futures, timeout=BLT_POLL_TIMEOUT_SECONDS):
                index, result, context, track_key = future.result()
                results_by_index[index] = (result, context, track_key)
        except FuturesTimeoutError:
            pass
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

        for index, source in enumerate(sources):
            item = results_by_index[index]
            if item is None:
                result = {
                    "id": source["id"],
                    "label": source["label"],
                    "url": source["url"],
                    "preferred": bool(source.get("preferred")),
                    "ok": False,
                    "status": "Timed out waiting for BeatLink source.",
                    "error": "Timed out waiting for BeatLink source.",
                }
                context = None
                track_key = ""
            else:
                result, context, track_key = item
            source_results.append(result)
            if selected is None and result.get("ok") and context is not None:
                selected = (source, context, track_key)

        waiting_count = sum(
            1
            for source in source_results
            if not source.get("ok") and "waiting for the current master deck to be playing" in text_value(source.get("status", ""))
        )
        errors = [f"{source['label']}: {source.get('error') or source.get('status')}" for source in source_results if not source.get("ok")]

        try:
            if selected is None:
                message = "; ".join(errors) or "No BeatLink source has an active master track."
                waiting_for_master = waiting_count == len(sources)
                with self.lock:
                    self.latest_blt_error = message
                    self.latest_blt_status = "BeatLink connected; waiting for an active master deck." if waiting_for_master else f"BeatLink unavailable: {message}"
                    self.latest_blt_sources = source_results
                    self.last_blt_poll_time = datetime.now().isoformat(timespec="seconds")
                    if waiting_for_master:
                        self.latest_blt_context = {}
                return {
                    "ok": False,
                    "status": self.latest_blt_status,
                    "context": self.latest_blt_context,
                    "error": message,
                    "sources": source_results,
                }

            source, context, track_key = selected
            track_key = self.blt_track_key(context)
            changed = bool(track_key and track_key != self.latest_blt_key)
            if changed and self.manual_mode == "cdj":
                context = self.update_track_artwork(context, track_key)
            source_label = text_value(source.get("label", "BeatLink")) or "BeatLink"
            bpm_changed = self.follow_now_playing_bpm(context, source_label)
            if bpm_changed:
                config["bpm_flip_bpm"] = str(self.bpm)
                save_config(config)
            with self.lock:
                self.latest_blt_context = context
                self.latest_blt_status = f"BeatLink live track loaded from {source_label}"
                self.latest_blt_error = ""
                self.latest_blt_sources = source_results
                self.last_blt_poll_time = datetime.now().isoformat(timespec="seconds")
                if changed or bpm_changed:
                    self.latest_blt_key = track_key
                    if self.manual_mode == "cdj":
                        self.set_event(f"BeatLink track from {source_label}: {context.get('full_track', 'Loaded track')}")
            sent = []
            if send_on_change and changed and self.manual_mode == "cdj":
                sent = self.send_blt_outputs(context, f"BeatLink {source_label}")
            return {
                "ok": True,
                "status": self.latest_blt_status,
                "changed": changed,
                "context": context,
                "sent": sent,
                "source": {key: source[key] for key in ("id", "label", "url") if key in source},
                "sources": source_results,
            }
        except Exception as exc:
            message = str(exc)
            with self.lock:
                self.latest_blt_error = message
                waiting_for_master = "waiting for the current master deck to be playing" in message
                self.latest_blt_status = message if waiting_for_master else f"BeatLink unavailable: {message}"
                self.latest_blt_sources = source_results
                self.last_blt_poll_time = datetime.now().isoformat(timespec="seconds")
                if waiting_for_master:
                    self.latest_blt_context = {}
            return {"ok": False, "status": self.latest_blt_status, "context": self.latest_blt_context, "error": message, "sources": source_results}

    def send_blt_outputs(self, context: dict[str, str], source: str) -> list[dict[str, Any]]:
        config = self.config()
        outputs = normalize_blt_osc_outputs(config.get("blt_osc_outputs", DEFAULT_BLT_OSC_OUTPUTS))
        sent = []
        for output in outputs:
            if not output.get("enabled", False):
                continue
            address = clean_osc_address(output.get("address", ""))
            if not address:
                continue
            field = str(output.get("field", "full_track"))
            value = context.get(field, "")
            self.send_osc_string(config, address, value)
            sent.append({"label": output.get("label", field), "address": address, "value": value})
        self.set_event(f"Sent {source} text outputs")
        return sent

    def test_blt_outputs(self) -> dict[str, Any]:
        context = {
            "title": "Test Title",
            "artist": "Test Artist",
            "album": "Test Album",
            "full_track": "Test Artist - Test Title",
            "track_info": "128 BPM | Player 1 CDJ",
            "bpm": "128",
            "player_number": "1",
            "device_name": "CDJ Test",
            "source_player": "test",
            "player": "Player 1",
            "comment": self.color_comment(),
        }
        sent = self.send_blt_outputs(context, "test")
        return {"ok": True, "message": "Sent enabled BLT text outputs", "sent": sent, "state": self.snapshot()}

    def enter_manual_mode(self, mode: str) -> dict[str, Any]:
        config = self.config()
        if mode == "vinyl":
            text = str(config.get("vinyl_track_text", DEFAULT_VINYL_TRACK_TEXT))
            source_path = portable_project_path(config.get("vinyl_logo_path", DEFAULT_VINYL_LOGO_PATH))
            status_label = "Vinyl logo"
        elif mode == "studio":
            text = str(config.get("studio_track_text", DEFAULT_STUDIO_TRACK_TEXT))
            source_path = portable_project_path(config.get("studio_artwork_path", DEFAULT_STUDIO_ARTWORK_PATH))
            status_label = "NO TALKING STUDIO"
        elif mode == "videogame":
            text = str(config.get("videogame_track_text", DEFAULT_VIDEOGAME_TRACK_TEXT))
            source_path = portable_project_path(config.get("videogame_artwork_path", DEFAULT_VIDEOGAME_ARTWORK_PATH))
            if not source_path.exists():
                fallback_path = portable_project_path(config.get("fallback_artwork_path", DEFAULT_VIDEOGAME_ARTWORK_PATH))
                if fallback_path.exists():
                    source_path = fallback_path
            status_label = "Videogames"
        else:
            raise ValueError(f"Unknown manual mode: {mode}")
        if not source_path.exists():
            raise ValueError(f"{status_label} file does not exist: {source_path}")
        self.write_placeholder_artwork(source_path, status_label, mode)
        self.maybe_auto_apply_artwork_palette(fallback_used=False, track_key=f"manual:{mode}:{source_path}", force=True)
        context = self.manual_context(text, mode)
        sent = self.send_blt_outputs(context, mode)
        with self.lock:
            self.manual_mode = mode
            self.set_event(f"{status_label} mode active")
        return {"ok": True, "message": f"{status_label} active", "sent": sent, "state": self.snapshot()}

    def resume_cdj(self) -> dict[str, Any]:
        sent: list[dict[str, Any]] = []
        with self.lock:
            self.manual_mode = "cdj"
            self.set_event("CDJ artwork mode resumed")
        if self.latest_blt_context:
            track_key = self.blt_track_key(self.latest_blt_context)
            context = self.update_track_artwork(dict(self.latest_blt_context), track_key, force=True)
            sent = self.send_blt_outputs(context, "CDJ resume")
            with self.lock:
                self.latest_blt_context = context
        return {"ok": True, "message": "CDJ artwork mode resumed", "sent": sent, "state": self.snapshot()}

    def set_bpm(self, bpm: Any | None = None, division: Any | None = None, seconds: Any | None = None) -> None:
        with self.lock:
            if seconds is not None:
                self.bpm_seconds = parse_bpm_flip_seconds(seconds)
                self.bpm_flip_mode = "seconds"
                self.bpm_follow_now_playing = False
            else:
                if bpm is not None:
                    self.bpm = parse_bpm(bpm)
                    self.bpm_flip_mode = "bars"
                if division is not None:
                    self.bpm_division = normalize_bpm_swap_rate(division)
                    self.bpm_flip_mode = "bars"
            self.bpm_interval_ms = (
                bpm_seconds_interval_ms(self.bpm_seconds)
                if self.bpm_flip_mode == "seconds"
                else bpm_flip_interval_ms(self.bpm, self.bpm_division)
            )

    def follow_now_playing_bpm(self, context: dict[str, str], source: str = "now playing") -> bool:
        bpm = text_value(context.get("bpm", ""))
        if not bpm:
            return False
        with self.lock:
            if not self.bpm_follow_now_playing:
                return False
        try:
            parsed_bpm = parse_bpm(bpm)
        except ValueError:
            return False
        changed = False
        with self.lock:
            changed = abs(self.bpm - parsed_bpm) >= 0.05
            self.bpm = parsed_bpm
            self.bpm_flip_mode = "bars"
            self.bpm_interval_ms = bpm_flip_interval_ms(self.bpm, self.bpm_division)
            if changed:
                self.set_event(f"BPM snapped to {self.bpm:g} from {source}")
        if changed and self.bpm_running:
            self.bpm_resync_event.set()
        return changed

    def start_bpm_swap(self, bpm: Any | None = None, division: Any | None = None, seconds: Any | None = None) -> dict[str, Any]:
        self.set_bpm(bpm, division, seconds)
        with self.lock:
            self.bpm_running = True
            if self.bpm_flip_mode == "seconds":
                self.set_event(f"Color rotation started every {self.bpm_seconds:g} seconds")
            else:
                self.set_event(f"BPM color rotation started at {self.bpm:g} BPM, {self.bpm_division}")
            self.bpm_stop_event.clear()
            self.bpm_resync_event.set()
            if not self.bpm_thread or not self.bpm_thread.is_alive():
                self.bpm_thread = threading.Thread(target=self.bpm_loop, name="BPMColorRotation", daemon=True)
                self.bpm_thread.start()
        return {"ok": True, "message": "BPM color rotation started", "state": self.snapshot()}

    def stop_bpm_swap(self) -> dict[str, Any]:
        with self.lock:
            self.bpm_running = False
            self.bpm_stop_event.set()
            self.bpm_resync_event.set()
            self.set_event("BPM color rotation stopped")
        return {"ok": True, "message": "BPM color rotation stopped", "state": self.snapshot()}

    def update_bpm_swap(self, bpm: Any | None = None, division: Any | None = None, seconds: Any | None = None) -> dict[str, Any]:
        self.set_bpm(bpm, division, seconds)
        with self.lock:
            config = self.config()
            if bpm is not None or seconds is not None:
                self.bpm_follow_now_playing = False
                config["bpm_follow_now_playing"] = False
            config["bpm_flip_bpm"] = str(self.bpm)
            config["bpm_flip_division"] = self.bpm_division
            config["bpm_flip_mode"] = self.bpm_flip_mode
            config["bpm_flip_seconds"] = str(self.bpm_seconds)
            save_config(config)
            running = self.bpm_running
            if self.bpm_flip_mode == "seconds":
                self.set_event(f"Color rotation set to every {self.bpm_seconds:g} seconds")
            else:
                self.set_event(f"BPM color rotation set to {self.bpm:g} BPM, {self.bpm_division}")
        if running:
            self.bpm_resync_event.set()
        return {"ok": True, "message": "BPM color rotation updated", "config": self.config_payload(), "state": self.snapshot()}

    def set_bpm_follow(self, enabled: Any) -> dict[str, Any]:
        follow_enabled = bool_from_payload(enabled)
        config = self.config()
        config["bpm_follow_now_playing"] = follow_enabled
        with self.lock:
            self.bpm_follow_now_playing = follow_enabled
            if follow_enabled:
                self.bpm_flip_mode = "bars"
                config["bpm_flip_mode"] = self.bpm_flip_mode
            self.set_event("BPM follow now playing enabled" if follow_enabled else "BPM follow now playing disabled")
        if follow_enabled and self.latest_blt_context:
            self.follow_now_playing_bpm(self.latest_blt_context, "now playing")
            config["bpm_flip_bpm"] = str(self.bpm)
        else:
            config["bpm_flip_bpm"] = str(self.bpm)
        save_config(config)
        return {
            "ok": True,
            "message": "Following now playing BPM" if follow_enabled else "Manual BPM control enabled",
            "config": self.config_payload(),
            "state": self.snapshot(),
        }

    def resync_bpm_swap(self, bpm: Any | None = None, division: Any | None = None, seconds: Any | None = None) -> dict[str, Any]:
        self.set_bpm(bpm, division, seconds)
        with self.lock:
            if not self.bpm_running:
                self.bpm_running = True
                self.bpm_stop_event.clear()
                if not self.bpm_thread or not self.bpm_thread.is_alive():
                    self.bpm_thread = threading.Thread(target=self.bpm_loop, name="BPMColorRotation", daemon=True)
                    self.bpm_thread.start()
            self.bpm_resync_event.set()
            if self.bpm_flip_mode == "seconds":
                self.set_event(f"Color rotation resynced every {self.bpm_seconds:g} seconds")
            else:
                self.set_event(f"BPM color rotation resynced at {self.bpm:g} BPM, {self.bpm_division}")
        return {"ok": True, "message": "BPM color rotation resynced", "state": self.snapshot()}

    def rotate_color_slots(self, keys: list[str]) -> None:
        attrs = {
            "color1": ("color1_name", "color1_value"),
            "color2": ("color2_name", "color2_value"),
            "strobe_color": ("strobe_color_name", "strobe_color_value"),
        }
        slots = [key for key in keys if key in attrs]
        if len(slots) < 2:
            return
        names = [getattr(self.state, attrs[key][0]) for key in slots]
        values = [getattr(self.state, attrs[key][1]) for key in slots]
        rotated_names = names[1:] + names[:1]
        rotated_values = values[1:] + values[:1]
        for key, name, value in zip(slots, rotated_names, rotated_values):
            setattr(self.state, attrs[key][0], name)
            setattr(self.state, attrs[key][1], value)
    def bpm_loop(self) -> None:
        next_flip = time.monotonic()
        config = self.config()
        while True:
            with self.lock:
                running = self.bpm_running
                delay = self.bpm_interval_ms / 1000.0
            if not running:
                return
            self.bpm_resync_event.clear()
            next_flip += delay
            wait_seconds = max(0.0, next_flip - time.monotonic())
            woke_for_resync = self.bpm_resync_event.wait(wait_seconds)
            if self.bpm_stop_event.is_set():
                return
            if woke_for_resync:
                next_flip = time.monotonic()
                continue
            try:
                config = self.config()
                rotation_keys = normalize_bpm_rotation_slots(config.get("bpm_rotation_slots", self.bpm_rotation_slots), require_multiple=True)
            except Exception as exc:
                self.log_command(f"BPM color rotation skipped: {exc}")
                continue
            with self.lock:
                if not self.bpm_running:
                    return
                self.bpm_rotation_slots = list(rotation_keys)
                self.rotate_color_slots(rotation_keys)
                self.state.source = "auto rotation"
                self.bpm_flip_count += 1
                self.bpm_last_flip_time = datetime.now().isoformat(timespec="milliseconds")
                self.bpm_last_flip_monotonic = time.monotonic()
            try:
                self.send_control_keys(rotation_keys, "auto rotation", config=config, log_event=False)
            except Exception as exc:
                self.log_command(f"BPM color rotation send failed: {exc}")
            if time.monotonic() - next_flip > delay:
                next_flip = time.monotonic()

    def set_event(self, text: str) -> None:
        self.last_event = text
        self.last_command_time = datetime.now().isoformat(timespec="seconds")
        self.log_command(text)

    def log_command(self, text: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.command_log.append(f"[{timestamp}] {text}")
        if len(self.command_log) > 250:
            self.command_log = self.command_log[-250:]

    def clear_command_log(self) -> dict[str, Any]:
        with self.lock:
            self.command_log.clear()
            self.set_event("Command log cleared")
        return {"ok": True, "message": "Command log cleared", "state": self.snapshot()}

    def presets(self) -> list[str]:
        config = self.config()
        return list(dict(config.get("performance_presets", PERFORMANCE_PRESETS)).keys())

    def control_metadata(self) -> list[dict[str, Any]]:
        config = self.config()
        controls = []
        for link, default_label, key, kind in LINK_CONTROL_SPECS:
            controls.append(
                {
                    "link": link,
                    "key": key,
                    "kind": kind,
                    "default_label": default_label,
                    "label": self.link_label(config, link),
                    "address": self.link_address(config, link),
                    "extra_addresses": self.link_extra_addresses(config, link),
                    "output_notes": self.link_output_notes(config, link),
                    "output_slots": osc_output_slots_for_link(link),
                }
            )
        return controls

    def config_payload(self) -> dict[str, Any]:
        config = self.config()
        connection = connection_payload(config)
        osc_addresses = {
            str(link): self.link_address(config, link)
            for link, _label, _key, _kind in LINK_CONTROL_SPECS
        }
        osc_extra_addresses = {
            str(link): self.link_extra_address_slots(config, link)
            for link, _label, _key, _kind in LINK_CONTROL_SPECS
        }
        osc_output_notes = {
            str(link): self.link_output_notes(config, link)
            for link, _label, _key, _kind in LINK_CONTROL_SPECS
        }
        link_labels = {
            str(link): self.link_label(config, link)
            for link, _label, _key, _kind in LINK_CONTROL_SPECS
        }
        preset_names = list(dict(config.get("performance_presets", PERFORMANCE_PRESETS)).keys())
        visual_controls = normalize_visual_controls(config.get("visual_controls", []))
        camera_controls = normalize_camera_controls(config.get("camera_controls", {}))
        generative_presets = normalize_generative_visual_presets(config.get("generative_visual_presets", {}))
        performance_banks = normalize_performance_banks(
            config.get("performance_banks", []),
            preset_names,
            visual_controls,
            camera_controls,
            generative_presets,
        )
        active_performance_bank = text_value(config.get("active_performance_bank", ""))
        if active_performance_bank not in {bank["id"] for bank in performance_banks}:
            active_performance_bank = performance_banks[0]["id"]
        panic_safe = normalize_panic_safe(
            config.get("panic_safe", {}),
            preset_names,
            visual_controls,
            camera_controls,
        )
        network_machines = normalize_network_machines(config.get("network_machines", []), config)
        network_routes = normalize_network_routes(config.get("network_routes", {}), network_machines, config)
        beatlink_sources = blt_sources(config)
        return {
            "active_connection_profile": connection["active_id"],
            "connection_profile_name": connection["active_name"],
            "connection_profiles": connection["profiles"],
            "show_machine_name": connection["show_machine_name"],
            "show_machine_lan_ip": connection["lan_ip"],
            "app_bind_host": text_value(connection["active"].get("app_bind_host", config.get("app_bind_host", ""))),
            "app_port": parse_int(connection["active"].get("app_port", config.get("app_port", 8080)), 8080, 1, 65535),
            "public_control_url": connection["public_control_url"],
            "local_control_url": connection["local_control_url"],
            "lan_control_urls": connection["lan_control_urls"],
            "beatlink_host": text_value(connection["active"].get("beatlink_host", config.get("beatlink_host", ""))),
            "beatlink_port": parse_int(connection["active"].get("beatlink_port", config.get("beatlink_port", 8088)), 8088, 1, 65535),
            "beatlink_base_url": text_value(connection["active"].get("beatlink_base_url", config.get("beatlink_base_url", ""))),
            "visualizer_url": connection["visualizer_url"],
            "blt_params_url": connection["blt_params_url"],
            "blt_sources": beatlink_sources,
            "resolume_host": connection["resolume_host"],
            "resolume_port": connection["resolume_port"],
            "osc_targets": normalize_osc_targets(config.get("osc_targets", []), config),
            "network_machines": network_machines,
            "network_routes": network_routes,
            "music_root": text_value(config.get("music_root", "")),
            "artwork_output": text_value(config.get("artwork_output", str(DEFAULT_ARTWORK_OUTPUT))),
            "fallback_artwork_path": text_value(config.get("fallback_artwork_path", "")),
            "vinyl_logo_path": text_value(config.get("vinyl_logo_path", DEFAULT_VINYL_LOGO_PATH)),
            "vinyl_track_text": text_value(config.get("vinyl_track_text", DEFAULT_VINYL_TRACK_TEXT)),
            "studio_artwork_path": text_value(config.get("studio_artwork_path", DEFAULT_STUDIO_ARTWORK_PATH)),
            "studio_track_text": text_value(config.get("studio_track_text", DEFAULT_STUDIO_TRACK_TEXT)),
            "videogame_artwork_path": text_value(config.get("videogame_artwork_path", DEFAULT_VIDEOGAME_ARTWORK_PATH)),
            "videogame_track_text": text_value(config.get("videogame_track_text", DEFAULT_VIDEOGAME_TRACK_TEXT)),
            "output_pixels": normalize_artwork_size(config.get("output_pixels", DEFAULT_OUTPUT_PIXELS)),
            "cdj_artwork_width": artwork_dimensions(config, "cdj")[0],
            "cdj_artwork_height": artwork_dimensions(config, "cdj")[1],
            "fallback_artwork_width": artwork_dimensions(config, "fallback")[0],
            "fallback_artwork_height": artwork_dimensions(config, "fallback")[1],
            "vinyl_artwork_width": artwork_dimensions(config, "vinyl")[0],
            "vinyl_artwork_height": artwork_dimensions(config, "vinyl")[1],
            "studio_artwork_width": artwork_dimensions(config, "studio")[0],
            "studio_artwork_height": artwork_dimensions(config, "studio")[1],
            "videogame_artwork_width": artwork_dimensions(config, "videogame")[0],
            "videogame_artwork_height": artwork_dimensions(config, "videogame")[1],
            "bpm_flip_bpm": text_value(config.get("bpm_flip_bpm", "125")),
            "bpm_flip_division": normalize_bpm_swap_rate(config.get("bpm_flip_division", "1/4")),
            "bpm_flip_mode": normalize_bpm_flip_mode(config.get("bpm_flip_mode", "bars")),
            "bpm_flip_seconds": text_value(config.get("bpm_flip_seconds", "8")),
            "bpm_rotation_slots": normalize_bpm_rotation_slots(config.get("bpm_rotation_slots", DEFAULT_BPM_ROTATION_SLOTS), require_multiple=True),
            "bpm_follow_now_playing": bool(config.get("bpm_follow_now_playing", False)),
            "default_fallback_template": text_value(config.get("default_fallback_template", DEFAULT_TEMPLATE)),
            "look_apply_lights": bool(config.get("look_apply_lights", True)),
            "preset_keep_current_colors": bool(config.get("preset_keep_current_colors", False)),
            "use_artwork_palette": bool(config.get("use_artwork_palette", False)),
            "neutral_artwork_color": text_value(config.get("neutral_artwork_color", "blue")),
            "neutral_artwork_primary": text_value(config.get("neutral_artwork_primary", config.get("neutral_artwork_color", "teal"))),
            "neutral_artwork_secondary": text_value(config.get("neutral_artwork_secondary", "blue")),
            "neutral_artwork_accent": text_value(config.get("neutral_artwork_accent", "magenta")),
            "artwork_palette_fallback_only": bool(config.get("artwork_palette_fallback_only", False)),
            "manual_override_default_mode": text_value(config.get("manual_override_default_mode", "Auto")),
            "osc_addresses": osc_addresses,
            "osc_extra_addresses": osc_extra_addresses,
            "osc_output_notes": osc_output_notes,
            "link_labels": link_labels,
            "blt_osc_outputs": normalize_blt_osc_outputs(config.get("blt_osc_outputs", DEFAULT_BLT_OSC_OUTPUTS)),
            "blt_field_choices": BLT_FIELD_CHOICES,
            "now_playing_opacity_address": clean_osc_address(config.get("now_playing_opacity_address", "")),
            "camera_controls": camera_controls,
            "camera_opacity_addresses": normalize_camera_opacity_addresses(config.get("camera_opacity_addresses", {})),
            "camera_opacity_labels": normalize_camera_opacity_labels(config.get("camera_opacity_labels", {})),
            "visual_controls": visual_controls,
            "visual_opacity_address": clean_osc_address(config.get("visual_opacity_address", "")),
            "visual_slider_controls": normalize_visual_slider_controls(config.get("visual_slider_controls", []), config),
            "generative_visual_presets": generative_presets,
            "current_generative_visual": normalize_generative_visual(config.get("current_generative_visual", self.active_generative_visual), self.active_generative_visual),
            "math_scene_templates": normalize_math_scene_templates(config.get("math_scene_templates", {})),
            "math_scenes": config.get("math_scenes", {}),
            "preset_links": normalize_preset_links(
                config.get("preset_links", {}),
                preset_names,
            ),
            "show_sequences": normalize_show_sequences(config.get("show_sequences", {}), preset_names),
            "performance_banks": performance_banks,
            "active_performance_bank": active_performance_bank,
            "panic_safe": panic_safe,
            "controls": self.control_metadata(),
            "colors": {"names": SORTED_COLOR_NAMES, "hex": COLOR_HEX},
            "percent_choices": PERCENT_CHOICES,
            "bpm_divisions": [name for name, _multiplier in BPM_FLIP_DIVISIONS],
            "preset_groups": self.preset_payload(),
        }

    def update_config(self, payload: dict[str, Any]) -> dict[str, Any]:
        current = self.config()
        config = dict(current)
        simple_text_keys = (
            "blt_params_url",
            "resolume_host",
            "show_machine_name",
            "show_machine_lan_ip",
            "app_bind_host",
            "public_control_url",
            "beatlink_host",
            "beatlink_base_url",
            "visualizer_url",
            "music_root",
            "artwork_output",
            "fallback_artwork_path",
            "vinyl_logo_path",
            "vinyl_track_text",
            "studio_artwork_path",
            "studio_track_text",
            "videogame_artwork_path",
            "videogame_track_text",
            "default_fallback_template",
            "neutral_artwork_color",
            "neutral_artwork_primary",
            "neutral_artwork_secondary",
            "neutral_artwork_accent",
            "manual_override_default_mode",
        )
        for key in simple_text_keys:
            if key in payload:
                config[key] = text_value(payload[key])
        if "network_machines" in payload:
            config["network_machines"] = normalize_network_machines(payload.get("network_machines"), config)
        if "network_routes" in payload:
            machines = normalize_network_machines(config.get("network_machines", []), config)
            config["network_routes"] = normalize_network_routes(payload.get("network_routes"), machines, config)
        if "connection_profiles" in payload:
            config["connection_profiles"] = normalize_connection_profiles(payload.get("connection_profiles"), config)
        if "active_connection_profile" in payload:
            active_id = text_value(payload.get("active_connection_profile")) or "pc_server_tablet"
            profiles = normalize_connection_profiles(config.get("connection_profiles", []), config)
            valid_ids = {profile["id"] for profile in profiles}
            if active_id not in valid_ids:
                active_id = "pc_server_tablet" if "pc_server_tablet" in valid_ids else profiles[0]["id"]
            config["active_connection_profile"] = active_id
        if "app_port" in payload:
            config["app_port"] = parse_int(payload["app_port"], 8080, 1, 65535)
        if "beatlink_port" in payload:
            config["beatlink_port"] = parse_int(payload["beatlink_port"], 8088, 1, 65535)
        if "resolume_port" in payload:
            config["resolume_port"] = parse_int(payload["resolume_port"], 7000, 1, 65535)
        if "osc_targets" in payload:
            config["osc_targets"] = [
                target
                for target in normalize_osc_targets(payload.get("osc_targets"), config)
                if target.get("source") != "auto"
            ]
        if "output_pixels" in payload:
            config["output_pixels"] = normalize_artwork_size(payload["output_pixels"])
        for source_key in ARTWORK_SIZE_SOURCES:
            width_key = f"{source_key}_artwork_width"
            height_key = f"{source_key}_artwork_height"
            if width_key in payload:
                config[width_key] = normalize_artwork_size(payload[width_key])
            if height_key in payload:
                config[height_key] = normalize_artwork_size(payload[height_key])
        if "bpm_flip_bpm" in payload:
            config["bpm_flip_bpm"] = str(parse_bpm(payload["bpm_flip_bpm"]))
        if "bpm_flip_division" in payload:
            config["bpm_flip_division"] = normalize_bpm_swap_rate(payload["bpm_flip_division"])
        if "bpm_flip_mode" in payload:
            config["bpm_flip_mode"] = normalize_bpm_flip_mode(payload["bpm_flip_mode"])
        if "bpm_flip_seconds" in payload:
            config["bpm_flip_seconds"] = str(parse_bpm_flip_seconds(payload["bpm_flip_seconds"]))
        if "bpm_rotation_slots" in payload:
            config["bpm_rotation_slots"] = normalize_bpm_rotation_slots(payload.get("bpm_rotation_slots"), require_multiple=True, default_on_empty=False)
        if "bpm_follow_now_playing" in payload:
            config["bpm_follow_now_playing"] = bool_from_payload(payload["bpm_follow_now_playing"])
        if "look_apply_lights" in payload:
            config["look_apply_lights"] = bool_from_payload(payload["look_apply_lights"])
        if "preset_keep_current_colors" in payload:
            config["preset_keep_current_colors"] = bool_from_payload(payload["preset_keep_current_colors"])
        if "use_artwork_palette" in payload:
            config["use_artwork_palette"] = bool_from_payload(payload["use_artwork_palette"])
        if "artwork_palette_fallback_only" in payload:
            config["artwork_palette_fallback_only"] = bool_from_payload(payload["artwork_palette_fallback_only"])

        labels = payload.get("link_labels")
        if isinstance(labels, dict):
            merged = dict(config.get("link_labels", {}))
            for link, default_label, _key, _kind in LINK_CONTROL_SPECS:
                merged[str(link)] = text_value(labels.get(str(link), labels.get(link, merged.get(str(link), default_label)))) or default_label
            config["link_labels"] = merged

        addresses = payload.get("osc_addresses")
        if isinstance(addresses, dict):
            merged = dict(config.get("osc_addresses", {}))
            for link, _label, _key, _kind in LINK_CONTROL_SPECS:
                raw = addresses.get(str(link), addresses.get(link, merged.get(str(link), DEFAULT_OSC_ADDRESSES[str(link)])))
                merged[str(link)] = clean_osc_address(raw) or DEFAULT_OSC_ADDRESSES[str(link)]
            config["osc_addresses"] = merged

        extra_addresses = payload.get("osc_extra_addresses")
        if isinstance(extra_addresses, dict):
            existing_extras = config.get("osc_extra_addresses", {})
            if not isinstance(existing_extras, dict):
                existing_extras = {}
            merged_extras: dict[str, list[str]] = {}
            for link, _label, _key, _kind in LINK_CONTROL_SPECS:
                link_key = str(link)
                raw_values = extra_addresses.get(link_key, extra_addresses.get(link))
                if raw_values is None:
                    raw_values = existing_extras.get(link_key, [])
                if not isinstance(raw_values, list):
                    raw_values = []
                slot_count = extra_osc_address_slots_for_link(link)
                cleaned = [clean_osc_address(value) for value in raw_values[:slot_count]]
                merged_extras[link_key] = [
                    *cleaned,
                    *( [""] * slot_count ),
                ][:slot_count]
            config["osc_extra_addresses"] = merged_extras

        output_notes = payload.get("osc_output_notes")
        if isinstance(output_notes, dict):
            existing_notes = config.get("osc_output_notes", {})
            if not isinstance(existing_notes, dict):
                existing_notes = {}
            merged_notes: dict[str, list[str]] = {}
            for link, _label, _key, _kind in LINK_CONTROL_SPECS:
                link_key = str(link)
                raw_values = output_notes.get(link_key, output_notes.get(link))
                if raw_values is None:
                    raw_values = existing_notes.get(link_key, [])
                if not isinstance(raw_values, list):
                    raw_values = []
                slot_count = osc_output_slots_for_link(link)
                merged_notes[link_key] = [
                    *[text_value(value) for value in raw_values[:slot_count]],
                    *( [""] * slot_count ),
                ][:slot_count]
            config["osc_output_notes"] = merged_notes

        if "blt_osc_outputs" in payload:
            config["blt_osc_outputs"] = normalize_blt_osc_outputs(payload.get("blt_osc_outputs"))
        if "now_playing_opacity_address" in payload:
            config["now_playing_opacity_address"] = clean_osc_address(payload.get("now_playing_opacity_address", ""))

        if "camera_controls" in payload:
            config["camera_controls"] = normalize_camera_controls(payload.get("camera_controls"))
        if "camera_opacity_addresses" in payload:
            config["camera_opacity_addresses"] = normalize_camera_opacity_addresses(payload.get("camera_opacity_addresses"))
        if "camera_opacity_labels" in payload:
            config["camera_opacity_labels"] = normalize_camera_opacity_labels(payload.get("camera_opacity_labels"))

        if "visual_controls" in payload:
            config["visual_controls"] = normalize_visual_controls(payload.get("visual_controls"))
        if "visual_slider_controls" in payload:
            config["visual_slider_controls"] = normalize_visual_slider_controls(payload.get("visual_slider_controls"), config)
            sliders = normalize_visual_slider_controls(config.get("visual_slider_controls", []), config)
            if sliders:
                config["visual_opacity_address"] = sliders[0]["address"]
        if "visual_opacity_address" in payload:
            config["visual_opacity_address"] = clean_osc_address(payload.get("visual_opacity_address", ""))
        if "generative_visual_presets" in payload:
            config["generative_visual_presets"] = normalize_generative_visual_presets(payload.get("generative_visual_presets"))
        if "current_generative_visual" in payload:
            config["current_generative_visual"] = normalize_generative_visual(payload.get("current_generative_visual"), self.active_generative_visual)
        if "math_scenes" in payload and isinstance(payload.get("math_scenes"), dict):
            config["math_scenes"] = payload["math_scenes"]

        connection_keys = {
            "active_connection_profile",
            "show_machine_name",
            "app_bind_host",
            "app_port",
            "public_control_url",
            "beatlink_host",
            "beatlink_port",
            "beatlink_base_url",
            "blt_params_url",
            "resolume_host",
            "resolume_port",
            "visualizer_url",
        }
        if any(key in payload for key in connection_keys):
            profiles = normalize_connection_profiles(config.get("connection_profiles", []), config)
            active_id = text_value(config.get("active_connection_profile", "pc_server_tablet")) or "pc_server_tablet"
            for profile in profiles:
                if profile["id"] != active_id:
                    continue
                for key in (
                    "app_bind_host",
                    "public_control_url",
                    "beatlink_host",
                    "beatlink_base_url",
                    "blt_params_url",
                    "resolume_host",
                    "visualizer_url",
                ):
                    if key in payload:
                        profile[key] = text_value(payload[key])
                if "app_port" in payload:
                    profile["app_port"] = parse_int(payload["app_port"], 8080, 1, 65535)
                if "beatlink_port" in payload:
                    profile["beatlink_port"] = parse_int(payload["beatlink_port"], 8088, 1, 65535)
                if "resolume_port" in payload:
                    profile["resolume_port"] = parse_int(payload["resolume_port"], 7000, 1, 65535)
            config["connection_profiles"] = profiles

        if "preset_links" in payload:
            preset_names = list(dict(config.get("performance_presets", PERFORMANCE_PRESETS)).keys())
            config["preset_links"] = normalize_preset_links(payload.get("preset_links"), preset_names)
        if "show_sequences" in payload:
            preset_names = list(dict(config.get("performance_presets", PERFORMANCE_PRESETS)).keys())
            config["show_sequences"] = normalize_show_sequences(payload.get("show_sequences"), preset_names)
        if "performance_banks" in payload or "active_performance_bank" in payload:
            preset_names = list(dict(config.get("performance_presets", PERFORMANCE_PRESETS)).keys())
            visual_controls = normalize_visual_controls(config.get("visual_controls", []))
            camera_controls = normalize_camera_controls(config.get("camera_controls", {}))
            generative_presets = normalize_generative_visual_presets(config.get("generative_visual_presets", {}))
            banks = normalize_performance_banks(
                payload.get("performance_banks", config.get("performance_banks", [])),
                preset_names,
                visual_controls,
                camera_controls,
                generative_presets,
            )
            config["performance_banks"] = banks
            requested_bank = text_value(payload.get("active_performance_bank", config.get("active_performance_bank", "")))
            config["active_performance_bank"] = requested_bank if requested_bank in {bank["id"] for bank in banks} else banks[0]["id"]
        if "panic_safe" in payload:
            preset_names = list(dict(config.get("performance_presets", PERFORMANCE_PRESETS)).keys())
            config["panic_safe"] = normalize_panic_safe(
                payload.get("panic_safe"),
                preset_names,
                normalize_visual_controls(config.get("visual_controls", [])),
                normalize_camera_controls(config.get("camera_controls", {})),
            )

        save_config(config)
        self.reload_from_config()
        message = "Settings saved"
        mode = self.manual_mode
        changed_keys = set(payload.keys())
        global_artwork_keys = {"artwork_output", "output_pixels"}
        fallback_size_keys = {"fallback_artwork_width", "fallback_artwork_height"}
        vinyl_keys = {"vinyl_track_text", "vinyl_logo_path", "vinyl_artwork_width", "vinyl_artwork_height", *global_artwork_keys}
        studio_keys = {"studio_track_text", "studio_artwork_path", "studio_artwork_width", "studio_artwork_height", *global_artwork_keys}
        videogame_keys = {"videogame_track_text", "videogame_artwork_path", "videogame_artwork_width", "videogame_artwork_height", *global_artwork_keys}
        cdj_artwork_keys = {"music_root", "fallback_artwork_path", "cdj_artwork_width", "cdj_artwork_height", *fallback_size_keys, *global_artwork_keys}
        try:
            if mode == "vinyl" and changed_keys.intersection(vinyl_keys):
                result = self.enter_manual_mode("vinyl")
                message = f"Settings saved; {result.get('message', 'Vinyl mode refreshed')}"
            elif mode == "studio" and changed_keys.intersection(studio_keys):
                result = self.enter_manual_mode("studio")
                message = f"Settings saved; {result.get('message', 'Studio mode refreshed')}"
            elif mode == "videogame" and changed_keys.intersection(videogame_keys):
                result = self.enter_manual_mode("videogame")
                message = f"Settings saved; {result.get('message', 'Videogames mode refreshed')}"
            elif mode == "cdj" and self.latest_blt_context and changed_keys.intersection(cdj_artwork_keys):
                self.resume_cdj()
                message = "Settings saved; CDJ artwork/text refreshed"
            else:
                self.set_event("Saved app settings")
        except Exception as exc:
            message = f"Settings saved; active mode refresh failed: {exc}"
            self.set_event(message)
        return {"ok": True, "message": message, "config": self.config_payload(), "state": self.snapshot()}

    def set_control(self, key: str, value: Any) -> dict[str, Any]:
        key = str(key or "").strip()
        config = self.config()
        with self.lock:
            if key == "color1":
                self.state.color1_name, self.state.color1_value = color_name_to_value(str(value), self.state.color1_name)
            elif key == "color2":
                self.state.color2_name, self.state.color2_value = color_name_to_value(str(value), self.state.color2_name)
            elif key == "strobe_color":
                self.state.strobe_color_name, self.state.strobe_color_value = color_name_to_value(str(value), self.state.strobe_color_name)
            elif key == "motion":
                self.state.motion_value = percent_to_value(motion_percent(value))
            elif key == "saturation":
                self.state.saturation_percent = parse_percent(value, self.state.saturation_percent)
                self.state.saturation_value = percent_to_value(self.state.saturation_percent)
            elif key == "brightness":
                self.state.brightness_percent = parse_percent(value, self.state.brightness_percent)
                self.state.brightness_value = percent_to_value(self.state.brightness_percent)
            elif key == "fx":
                self.state.fx_value = percent_to_value(value)
            elif key == "pulse":
                self.state.pulse_value = percent_to_value(value)
            else:
                raise ValueError(f"Unknown control: {key}")
            self.state.source = "web-control"
            link, output_value, label = self.state_control_value_label(config, key)
            addresses = self.link_addresses(config, link)
            for address in addresses:
                self.send_osc_float(config, address, output_value)
            self.set_event(f"Sent {label}")
        sent = [
            {"link": link, "label": label, "address": address, "value": output_value, "slot": index}
            for index, address in enumerate(addresses)
        ]
        if key in COLOR_SLOT_KEYS and bool(config.get("use_artwork_palette", False)):
            sent.extend(self.maybe_auto_apply_artwork_palette(fallback_used=False, track_key=f"web-control:{key}", force=True))
        return {
            "ok": True,
            "message": f"Sent {label}",
            "sent": sent,
            "state": self.snapshot(),
        }

    def set_palette_color(self, color: Any, target: Any) -> dict[str, Any]:
        color_name = str(color or "").strip()
        target_key = str(target or "").strip().casefold().replace("-", "_")
        target_map = {
            "1": ("color1",),
            "color1": ("color1",),
            "color_1": ("color1",),
            "primary": ("color1",),
            "2": ("color2",),
            "color2": ("color2",),
            "color_2": ("color2",),
            "secondary": ("color2",),
            "3": ("strobe_color",),
            "color3": ("strobe_color",),
            "color_3": ("strobe_color",),
            "tertiary": ("strobe_color",),
            "accent": ("strobe_color",),
            "primary_secondary": ("color1", "color2"),
            "primarysecondary": ("color1", "color2"),
            "color1_color2": ("color1", "color2"),
            "color2_color3": ("color2", "strobe_color"),
            "color1_color3": ("color1", "strobe_color"),
            "all": ("color1", "color2", "strobe_color"),
        }
        keys = list(target_map.get(target_key, ()))
        if not keys:
            raise ValueError("Choose Color 1, Color 2, Color 3, 1+2, 2+3, 1+3, or All.")
        clean_name, clean_value = color_name_to_value(color_name, "indigo")
        with self.lock:
            for key in keys:
                if key == "color1":
                    self.state.color1_name, self.state.color1_value = clean_name, clean_value
                elif key == "color2":
                    self.state.color2_name, self.state.color2_value = clean_name, clean_value
                elif key == "strobe_color":
                    self.state.strobe_color_name, self.state.strobe_color_value = clean_name, clean_value
            self.state.source = f"artwork:{target_key}"
        target_label = " + ".join(COLOR_SLOT_LABELS.get(key, key) for key in keys)
        sent = self.send_control_keys(keys, f"{clean_name} to {target_label}")
        return {
            "ok": True,
            "message": f"Sent {clean_name} to {target_label}",
            "sent": sent,
            "state": self.snapshot(),
        }

    def send_link(self, link: Any) -> dict[str, Any]:
        try:
            link_number = int(str(link).strip())
        except (TypeError, ValueError) as exc:
            raise ValueError("Link must be a number from 1 to 8.") from exc
        key = next((candidate for number, _label, candidate, _kind in LINK_CONTROL_SPECS if number == link_number), "")
        if not key:
            raise ValueError("Link must be a number from 1 to 8.")
        config = self.config()
        with self.lock:
            _link, output_value, label = self.state_control_value_label(config, key)
            addresses = self.link_addresses(config, link_number)
            for address in addresses:
                self.send_osc_float(config, address, output_value)
            self.set_event(f"Resent {label}")
        return {
            "ok": True,
            "message": f"Resent Link {link_number}",
            "sent": [
                {"link": link_number, "label": label, "address": address, "value": output_value, "slot": index}
                for index, address in enumerate(addresses)
            ],
            "state": self.snapshot(),
        }

    def send_all_links(self) -> dict[str, Any]:
        sent = self.send_state("all links")
        return {"ok": True, "message": "Sent all links", "sent": sent, "state": self.snapshot()}

    def send_camera_item(self, config: dict[str, Any], item: dict[str, Any]) -> dict[str, Any] | None:
        address = clean_osc_address(item.get("address", ""))
        if not address:
            return None
        label = text_value(item.get("label", item.get("name", item.get("id", ""))))
        self.send_osc_float(config, address, 1.0)
        return {"label": label, "address": address, "value": 1.0}

    def send_visual_item(self, config: dict[str, Any], item: dict[str, Any]) -> dict[str, Any] | None:
        address = clean_osc_address(item.get("address", ""))
        if not address:
            return None
        label = text_value(item.get("label", item.get("name", item.get("id", ""))))
        self.send_osc_float(config, address, 1.0)
        return {"label": label, "address": address, "value": 1.0}

    def visual_trigger(self, item_id: Any) -> dict[str, Any]:
        item_id_text = text_value(item_id)
        visual_items = normalize_visual_controls(self.config().get("visual_controls", []))
        item = next((candidate for candidate in visual_items if candidate["id"] == item_id_text), None)
        if not item:
            raise ValueError("Unknown visual button.")
        label = text_value(item.get("label", item.get("name", item_id_text)))
        config = self.config()
        sent: list[dict[str, Any]] = []
        direct = self.send_visual_item(config, item)
        if direct:
            sent.append(direct)
        with self.lock:
            self.last_visual_button = item_id_text
        if not sent:
            self.set_event(f"{label} needs an OSC address")
            return {"ok": True, "message": f"{label} needs an OSC address", "state": self.snapshot()}
        self.record_delivery("visuals", sent)
        self.set_event(f"Sent {label}")
        return {
            "ok": True,
            "message": f"Sent {label}",
            "sent": sent,
            "state": self.snapshot(),
        }

    def visual_opacity_trigger(self, value: Any) -> dict[str, Any]:
        return self.visual_slider_trigger("visual_slider_1", value)

    def now_playing_opacity_trigger(self, value: Any) -> dict[str, Any]:
        config = self.config()
        percent = parse_percent(value, self.now_playing_opacity)
        address = clean_osc_address(config.get("now_playing_opacity_address", ""))
        with self.lock:
            self.now_playing_opacity = percent
        if not address:
            self.set_event("Now Playing opacity needs an OSC address")
            return {"ok": True, "message": "Now Playing opacity needs an OSC address", "state": self.snapshot()}
        output_value = percent_to_value(percent)
        self.send_osc_float(config, address, output_value)
        self.record_delivery("visuals", [{"address": address, "value": output_value}])
        self.set_event(f"Sent Now Playing opacity {percent}%")
        return {
            "ok": True,
            "message": f"Sent Now Playing opacity {percent}%",
            "sent": [{"kind": "now_playing_opacity", "label": DEFAULT_NOW_PLAYING_OPACITY_LABEL, "address": address, "value": output_value, "display": f"{percent}%"}],
            "state": self.snapshot(),
        }

    def visual_slider_trigger(self, slider_id: Any, value: Any) -> dict[str, Any]:
        slider_id_text = text_value(slider_id) or "visual_slider_1"
        config = self.config()
        sliders = normalize_visual_slider_controls(config.get("visual_slider_controls", []), config)
        slider = next((item for item in sliders if item["id"] == slider_id_text), None)
        if not slider:
            raise ValueError("Unknown visual slider.")
        current = self.visual_slider_values.get(slider_id_text, 100)
        percent = parse_percent(value, current)
        label = text_value(slider.get("label", slider.get("name", slider_id_text))) or slider_id_text
        address = clean_osc_address(slider.get("address", ""))
        with self.lock:
            self.visual_slider_values[slider_id_text] = percent
            if slider_id_text == "visual_slider_1":
                self.visual_opacity = percent
        if not address:
            self.set_event(f"{label} needs an OSC address")
            return {"ok": True, "message": f"{label} needs an OSC address", "state": self.snapshot()}
        output_value = percent_to_value(percent)
        self.send_osc_float(config, address, output_value)
        self.record_delivery("visuals", [{"address": address, "value": output_value}])
        self.set_event(f"Sent {label} {percent}%")
        return {
            "ok": True,
            "message": f"Sent {label} {percent}%",
            "sent": [{"kind": "visual_slider", "id": slider_id_text, "label": label, "address": address, "value": output_value, "display": f"{percent}%"}],
            "state": self.snapshot(),
        }

    def update_generative_visual(self, values: Any, persist: bool = True, event_label: str = "Generative visuals updated") -> dict[str, Any]:
        config = self.config()
        with self.lock:
            next_values = normalize_generative_visual(values, self.active_generative_visual)
            self.active_generative_visual = next_values
            config["current_generative_visual"] = next_values
            if persist:
                save_config(config)
            self.set_event(event_label)
        return {"ok": True, "message": event_label, "config": self.config_payload(), "state": self.snapshot()}

    def trigger_math_scene(self, scene_id: Any, mode: str = "trigger") -> dict[str, Any]:
        scene_id_text = text_value(scene_id)
        templates = normalize_math_scene_templates(self.config().get("math_scene_templates", {}))
        template = next((item for item in templates if item["id"] == scene_id_text), None)
        if not template:
            raise ValueError(f"Unknown math scene: {scene_id_text}")
        base_values = template.get("scene", {})
        values = normalize_generative_visual(base_values, self.active_generative_visual)
        values["enabled"] = True
        values["blackout"] = False
        action = "Previewing" if text_value(mode).casefold() == "preview" else "Triggered"
        return self.update_generative_visual(values, event_label=f"{action} math scene: {template['name']}")

    def stop_generative_visual(self) -> dict[str, Any]:
        with self.lock:
            next_values = normalize_generative_visual({"blackout": True, "enabled": False}, self.active_generative_visual)
            self.active_generative_visual = next_values
            config = self.config()
            config["current_generative_visual"] = next_values
            save_config(config)
            self.set_event("Generative visual output stopped")
        return {"ok": True, "message": "Generative visual output stopped", "config": self.config_payload(), "state": self.snapshot()}

    def generative_visual_state(self) -> dict[str, Any]:
        now = time.monotonic()
        with self.lock:
            gen = dict(self.active_generative_visual)
            bpm = float(self.bpm)
            beat_seconds = max(0.001, 60.0 / max(1.0, bpm))
            beat_position = now / beat_seconds
            beat = int(beat_position)
            beat_phase = beat_position % 1.0
            beat_pulse = max(0.0, 1.0 - beat_phase * 2.4)
            colors = {
                "color1": self.state.color1_name,
                "color2": self.state.color2_name,
                "color3": self.state.strobe_color_name,
                "primary": self.state.color1_name,
                "secondary": self.state.color2_name,
                "tertiary": self.state.strobe_color_name,
                "accent": self.state.strobe_color_name,
            }
            source = self.state.source
            active_look = self.active_look_name or (source.split(":", 1)[1] if source.startswith("performance:") else source)
            visual_state = {
                "bpm": bpm,
                "beat": beat,
                "beatPhase": beat_phase,
                "bar": beat // 4,
                "phrase": beat // 32,
                "energy": parse_unit_interval(getattr(self.state, "energy", 3), 3, 1, 5) / 5.0,
                "primaryHue": COLOR_HUE_VALUES.get(colors["primary"], 0.0),
                "secondaryHue": COLOR_HUE_VALUES.get(colors["secondary"], 0.5),
                "tertiaryHue": COLOR_HUE_VALUES.get(colors["tertiary"], 0.83),
                "accentHue": COLOR_HUE_VALUES.get(colors["accent"], 0.83),
                "trackTitle": text_value(self.latest_blt_context.get("title", "")),
                "artist": text_value(self.latest_blt_context.get("artist", "")),
                "activeLook": active_look,
                "activeShowStep": self.active_show_step,
                "deck": text_value(self.latest_blt_context.get("player", self.latest_blt_context.get("device_name", ""))),
                "section": self.state.section,
                "beatPulse": beat_pulse,
                "preset": gen["preset"],
                "intensity": gen["intensity"],
                "complexity": gen["complexity"],
                "motion": gen["motion"],
                "beatResponse": gen["beat_response"],
                "scale": gen["scale"],
                "zoom": gen["zoom"],
                "rotation": gen["rotation"],
                "symmetry": gen["symmetry"],
                "warp": gen["warp"],
                "lineWidth": gen["line_width"],
                "trail": gen["trail"],
                "automationEnabled": gen["automation_enabled"],
                "automationTarget": gen["automation_target"],
                "automationMode": gen["automation_mode"],
                "automationDivision": gen["automation_division"],
                "automationShape": gen["automation_shape"],
                "automationDepth": gen["automation_depth"],
                "automationOffset": gen["automation_offset"],
                "layerEnabled": gen["layer_enabled"],
                "layerStyle": gen["layer_style"],
                "layerMix": gen["layer_mix"],
                "layerSpeed": gen["layer_speed"],
                "phraseMorph": gen["phrase_morph"],
                "colorSource": gen["color_source"],
                "enabled": gen["enabled"],
                "quality": gen["quality"],
                "opacity": gen["opacity"],
                "freeze": gen["freeze"],
                "blackout": gen["blackout"],
                "seed": gen["seed"],
                "renderer": GEN_VISUAL_PRESET_DEFS.get(gen["preset"], GEN_VISUAL_PRESET_DEFS["lissajous_orbit"])["renderer"],
            }
        return {"ok": True, "time": datetime.now().isoformat(timespec="milliseconds"), "visualState": visual_state, "generative_visual": gen}

    def linked_items_for_config(self, config: dict[str, Any], link: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
        items: list[tuple[str, dict[str, Any]]] = []
        visual_id = text_value(link.get("visual_id", ""))
        if visual_id:
            visual_item = next((item for item in normalize_visual_controls(config.get("visual_controls", [])) if item["id"] == visual_id), None)
            if visual_item:
                items.append(("visual", visual_item))

        camera_config = normalize_camera_controls(config.get("camera_controls", {}))
        for group_key in ("main_box", "pip_box", "background"):
            camera_id = text_value(link.get(f"{group_key}_id", ""))
            if not camera_id:
                continue
            camera_item = next((item for item in camera_config["groups"].get(group_key, []) if item["id"] == camera_id), None)
            if camera_item:
                items.append((group_key, camera_item))

        scene_id = text_value(link.get("scene_id", ""))
        if scene_id:
            scene_item = next((item for item in camera_config["scenes"] if item["id"] == scene_id), None)
            if scene_item:
                items.append(("scene", scene_item))
        return items

    def apply_preset_bpm_link(self, config: dict[str, Any], link: dict[str, Any], preset_name: str) -> dict[str, Any] | None:
        if not bool_from_payload(link.get("bpm_enabled", False)):
            return None
        slots = link.get("bpm_rotation_slots") or list(DEFAULT_BPM_ROTATION_SLOTS)
        running = bool_from_payload(link.get("bpm_running", False))
        with self.lock:
            self.bpm = float(link.get("bpm", self.bpm))
            self.bpm_division = text_value(link.get("bpm_division", self.bpm_division)) or self.bpm_division
            self.bpm_flip_mode = text_value(link.get("bpm_flip_mode", self.bpm_flip_mode)) or self.bpm_flip_mode
            self.bpm_seconds = float(link.get("bpm_seconds", self.bpm_seconds))
            self.bpm_follow_now_playing = bool_from_payload(link.get("bpm_follow_now_playing", self.bpm_follow_now_playing))
            self.bpm_rotation_slots = list(slots)
            self.bpm_interval_ms = (
                bpm_seconds_interval_ms(self.bpm_seconds)
                if self.bpm_flip_mode == "seconds"
                else bpm_flip_interval_ms(self.bpm, self.bpm_division)
            )
            self.bpm_running = running
            if running:
                self.bpm_stop_event.clear()
                self.bpm_resync_event.set()
                if not self.bpm_thread or not self.bpm_thread.is_alive():
                    self.bpm_thread = threading.Thread(target=self.bpm_loop, name="BPMColorRotation", daemon=True)
                    self.bpm_thread.start()
            else:
                self.bpm_stop_event.set()
                self.bpm_resync_event.set()
            self.set_event(f"{preset_name} BPM rotation recalled")
        config["bpm_flip_bpm"] = str(self.bpm)
        config["bpm_flip_division"] = self.bpm_division
        config["bpm_flip_mode"] = self.bpm_flip_mode
        config["bpm_flip_seconds"] = str(self.bpm_seconds)
        config["bpm_follow_now_playing"] = self.bpm_follow_now_playing
        config["bpm_rotation_slots"] = list(self.bpm_rotation_slots)
        save_config(config)
        return {
            "kind": "bpm",
            "label": "BPM Color Rotation",
            "value": "running" if running else "stopped",
            "display": f"{self.bpm:g} BPM {self.bpm_division}",
        }

    def send_preset_link_actions(self, config: dict[str, Any], preset_name: str, apply_lights: bool = True) -> list[dict[str, Any]]:
        links = normalize_preset_links(
            config.get("preset_links", {}),
            list(dict(config.get("performance_presets", PERFORMANCE_PRESETS)).keys()),
        )
        link = links.get(preset_name, {})
        if not link:
            return []
        sent: list[dict[str, Any]] = []
        section_name = text_value(link.get("section_preset", "")).upper()
        section_presets = dict(config.get("section_presets", {}))
        if apply_lights and section_name and section_name in section_presets:
            with self.lock:
                apply_values_to_state(self.state, section_presets[section_name], exact=False)
                self.state.section = section_name
                self.state.source = f"performance:{preset_name}+section:{section_name}"
            for item in self.send_state(f"{preset_name} section {section_name}"):
                item["kind"] = "section_preset"
                sent.append(item)
        active_visual = ""
        active_cameras: dict[str, str] = {}
        for kind, item in self.linked_items_for_config(config, link):
            if kind == "visual":
                direct = self.send_visual_item(config, item)
                active_visual = text_value(item.get("id", ""))
            else:
                direct = self.send_camera_item(config, item)
                active_cameras[kind] = text_value(item.get("id", ""))
            if direct:
                direct["kind"] = kind
                sent.append(direct)
        mode = text_value(link.get("now_playing_mode", "")).casefold()
        if mode in {"vinyl", "studio", "videogame"}:
            mode_result = self.enter_manual_mode(mode)
            for item in mode_result.get("sent", []):
                if isinstance(item, dict):
                    item["kind"] = "now_playing"
                    sent.append(item)
            sent.append({"kind": "now_playing", "label": mode, "value": mode})
        elif mode == "cdj":
            self.resume_cdj()
            sent.append({"kind": "now_playing", "label": "CDJ", "value": "cdj"})
        now_playing_opacity = link.get("now_playing_opacity", "")
        if now_playing_opacity != "":
            opacity_result = self.now_playing_opacity_trigger(now_playing_opacity)
            for item in opacity_result.get("sent", []):
                if isinstance(item, dict):
                    sent.append(item)
        if apply_lights:
            bpm_result = self.apply_preset_bpm_link(config, link, preset_name)
            if bpm_result:
                sent.append(bpm_result)
        generative_visual = link.get("generative_visual", {})
        if isinstance(generative_visual, dict) and generative_visual:
            gen_values = normalize_generative_visual(generative_visual, self.active_generative_visual)
            self.update_generative_visual(gen_values, event_label=f"{preset_name} generator look")
            sent.append({
                "kind": "generative_visual",
                "label": GEN_VISUAL_PRESET_DEFS.get(gen_values.get("preset", ""), {}).get("name", gen_values.get("preset", "Generator")),
                "value": gen_values.get("preset", ""),
            })
        with self.lock:
            if active_visual:
                self.last_visual_button = active_visual
            for group_key, item_id in active_cameras.items():
                self.last_camera_buttons[group_key] = item_id
        if active_visual:
            self.record_delivery("visuals", [item for item in sent if item.get("kind") == "visual"])
        if active_cameras:
            self.record_delivery("cameras", [item for item in sent if item.get("kind") in {*active_cameras.keys(), "scene"}])
        return sent

    def camera_trigger(self, kind: Any, item_id: Any, group: Any = "") -> dict[str, Any]:
        kind_text = text_value(kind).casefold()
        item_id_text = text_value(item_id)
        camera_config = normalize_camera_controls(self.config().get("camera_controls", {}))
        items: list[dict[str, Any]]
        if kind_text == "scene":
            items = camera_config["scenes"]
        else:
            group_key = text_value(group)
            items = camera_config["groups"].get(group_key, [])
        item = next((candidate for candidate in items if candidate["id"] == item_id_text), None)
        if not item:
            raise ValueError("Unknown camera or scene button.")
        label = text_value(item.get("label", item.get("name", item_id_text)))
        config = self.config()
        sent: list[dict[str, Any]] = []
        direct = self.send_camera_item(config, item)
        if direct:
            sent.append(direct)
        with self.lock:
            if kind_text == "scene":
                self.last_camera_buttons["scene"] = item_id_text
            else:
                self.last_camera_buttons[text_value(group)] = item_id_text
        if not sent:
            self.set_event(f"{label} needs an OSC address")
            return {"ok": True, "message": f"{label} needs an OSC address", "state": self.snapshot()}
        self.record_delivery("cameras", sent)
        self.set_event(f"Sent {label}")
        return {
            "ok": True,
            "message": f"Sent {label}",
            "sent": sent,
            "state": self.snapshot(),
        }

    def camera_opacity_trigger(self, group: Any, value: Any) -> dict[str, Any]:
        group_key = text_value(group)
        valid_groups = {key for key, _label in CAMERA_GROUP_SPECS}
        if group_key not in valid_groups:
            raise ValueError("Unknown camera opacity group.")
        percent = parse_percent(value, self.camera_opacity.get(group_key, 100))
        config = self.config()
        addresses = normalize_camera_opacity_addresses(config.get("camera_opacity_addresses", {}))
        address = addresses.get(group_key, "")
        with self.lock:
            self.camera_opacity[group_key] = percent
        group_label = dict(CAMERA_GROUP_SPECS).get(group_key, group_key)
        if not address:
            self.set_event(f"{group_label} opacity needs an OSC address")
            return {"ok": True, "message": f"{group_label} opacity needs an OSC address", "state": self.snapshot()}
        output_value = percent_to_value(percent)
        self.send_osc_float(config, address, output_value)
        self.record_delivery("cameras", [{"address": address, "value": output_value}])
        self.set_event(f"Sent {group_label} opacity {percent}%")
        return {
            "ok": True,
            "message": f"Sent {group_label} opacity {percent}%",
            "sent": [{"kind": "camera_opacity", "group": group_key, "address": address, "value": output_value, "display": f"{percent}%"}],
            "state": self.snapshot(),
        }

    def reset_control(self, key: str) -> dict[str, Any]:
        key = str(key or "").strip()
        defaults = parse_comment_tags(DEFAULT_TEMPLATE)
        default_by_control = {
            "color1": defaults.get("PRIMARY", "indigo"),
            "color2": defaults.get("SECONDARY", "magenta"),
            "strobe_color": defaults.get("STROBE", "purple"),
            "motion": defaults.get("MOTION", "50"),
            "saturation": defaults.get("SATURATION", "100"),
            "brightness": defaults.get("BRIGHTNESS", "100"),
            "fx": defaults.get("FX", "25"),
            "pulse": defaults.get("PULSE", "0"),
        }
        if key not in default_by_control:
            raise ValueError(f"Unknown control: {key}")
        return self.set_control(key, default_by_control[key])

    def safe_reset(self) -> dict[str, Any]:
        values = parse_comment_tags(
            "COLOR1=blue;COLOR2=purple;COLOR3=blue;STROBE_PERCENT=0;"
            "SATURATION=100;BRIGHTNESS=100;MOTION=20;FX=0;PULSE=0"
        )
        with self.lock:
            apply_values_to_state(self.state, values, exact=True)
            self.state.source = "safe reset"
        sent = self.send_state("safe reset")
        return {"ok": True, "message": "Safe light look sent", "sent": sent, "state": self.snapshot()}

    def panic_safe(self) -> dict[str, Any]:
        config = self.config()
        preset_names = list(dict(config.get("performance_presets", PERFORMANCE_PRESETS)).keys())
        safety = normalize_panic_safe(
            config.get("panic_safe", {}),
            preset_names,
            normalize_visual_controls(config.get("visual_controls", [])),
            normalize_camera_controls(config.get("camera_controls", {})),
        )
        sent: list[dict[str, Any]] = []
        self.stop_bpm_swap()
        if safety["stop_generator"]:
            self.stop_generative_visual()
        if safety["look"]:
            sent.extend(self.apply_preset(safety["look"], "performance", apply_lights=True).get("sent", []))
        else:
            sent.extend(self.safe_reset().get("sent", []))
        overrides = {
            "visual": safety["visual_id"],
            "main_box": safety["main_box_id"],
            "pip_box": safety["pip_box_id"],
            "background": safety["background_id"],
            "scene": safety["scene_id"],
        }
        camera_config = normalize_camera_controls(config.get("camera_controls", {}))
        visuals = normalize_visual_controls(config.get("visual_controls", []))
        for kind, item_id in overrides.items():
            if not item_id:
                continue
            items = visuals if kind == "visual" else camera_config["scenes"] if kind == "scene" else camera_config["groups"].get(kind, [])
            item = next((candidate for candidate in items if candidate["id"] == item_id), None)
            if not item:
                continue
            direct = self.send_visual_item(config, item) if kind == "visual" else self.send_camera_item(config, item)
            if direct:
                direct["kind"] = kind
                sent.append(direct)
            with self.lock:
                if kind == "visual":
                    self.last_visual_button = item_id
                elif kind == "scene":
                    self.last_camera_buttons["scene"] = item_id
                else:
                    self.last_camera_buttons[kind] = item_id
        self.record_delivery("visuals", [item for item in sent if item.get("kind") == "visual"])
        self.record_delivery("cameras", [item for item in sent if item.get("kind") in {"main_box", "pip_box", "background", "scene"}])
        with self.lock:
            self.state.source = "panic safe"
            self.set_event("PANIC SAFE recalled the configured safe state")
        return {
            "ok": True,
            "message": "Panic safe state sent: BPM stopped, generator stopped, safe cues recalled.",
            "sent": sent,
            "config": self.config_payload(),
            "state": self.snapshot(),
        }

    def save_current_colors_as_template(self) -> dict[str, Any]:
        config = self.config()
        config["default_fallback_template"] = self.color_comment()
        save_config(config)
        self.set_event("Saved current colors as default fallback template")
        return {"ok": True, "message": "Saved current colors as default template", "config": self.config_payload(), "state": self.snapshot()}

    def snapshot(self) -> dict[str, Any]:
        config = self.config()
        with self.lock:
            return {
                "manual_mode": self.manual_mode,
                "last_event": self.last_event,
                "last_command_time": self.last_command_time,
                "bpm": self.bpm,
                "bpm_follow_now_playing": self.bpm_follow_now_playing,
                "bpm_division": self.bpm_division,
                "bpm_flip_mode": self.bpm_flip_mode,
                "bpm_seconds": self.bpm_seconds,
                "bpm_rotation_slots": list(self.bpm_rotation_slots),
                "bpm_interval_ms": self.bpm_interval_ms,
                "bpm_running": self.bpm_running,
                "bpm_flip_count": self.bpm_flip_count,
                "bpm_last_flip_time": self.bpm_last_flip_time,
                "last_camera_buttons": dict(self.last_camera_buttons),
                "last_visual_button": self.last_visual_button,
                "delivery_status": {key: dict(value) for key, value in self.delivery_status.items()},
                "generative_visual": dict(self.active_generative_visual),
                "camera_opacity": dict(self.camera_opacity),
                "visual_opacity": self.visual_opacity,
                "now_playing_opacity": self.now_playing_opacity,
                "visual_sliders": dict(self.visual_slider_values),
                "active_look_name": self.active_look_name,
                "outputs": [
                    {
                        "link": link,
                        "key": key,
                        "kind": kind,
                        "label": self.link_label(config, link),
                        "value": self.state_control_value_label(config, key)[1],
                        "display": self.state_control_value_label(config, key)[2],
                        "color": (
                            self.state.color1_name
                            if key == "color1"
                            else self.state.color2_name
                            if key == "color2"
                            else self.state.strobe_color_name
                            if key == "strobe_color"
                            else ""
                        ),
                        "hex": (
                            COLOR_HEX.get(self.state.color1_name, "")
                            if key == "color1"
                            else COLOR_HEX.get(self.state.color2_name, "")
                            if key == "color2"
                            else COLOR_HEX.get(self.state.strobe_color_name, "")
                            if key == "strobe_color"
                            else ""
                        ),
                    }
                    for link, _label, key, kind in LINK_CONTROL_SPECS
                ],
                "colors": {
                    "color1": self.state.color1_name,
                    "color2": self.state.color2_name,
                    "color3": self.state.strobe_color_name,
                    "primary": self.state.color1_name,
                    "secondary": self.state.color2_name,
                    "tertiary": self.state.strobe_color_name,
                    "accent": self.state.strobe_color_name,
                },
                "color_comment": self.color_comment(),
                "source": self.state.source,
                "command_log": self.command_log[-80:],
            }

    def handle_command(self, payload: dict[str, Any]) -> dict[str, Any]:
        command = str(payload.get("command", "")).strip().casefold()
        if command == "preset":
            return self.apply_preset(str(payload.get("name", "")), str(payload.get("group", "performance")), payload.get("apply_lights"))
        if command == "save_current_look":
            return self.save_current_look(str(payload.get("name", "")))
        if command == "vinyl":
            return self.enter_manual_mode("vinyl")
        if command in {"studio", "no_talking_studio"}:
            return self.enter_manual_mode("studio")
        if command in {"videogame", "video_game", "game"}:
            return self.enter_manual_mode("videogame")
        if command == "resume":
            return self.resume_cdj()
        if command == "rebuild_music_index":
            return self.rebuild_music_index()
        if command in {"swap", "rotate", "rotate_colors"}:
            return self.rotate_selected_colors(payload.get("slots"))
        if command == "relationship":
            return self.apply_color_relationship(str(payload.get("relationship", "")))
        if command == "artwork_palette":
            return self.apply_artwork_palette()
        if command == "set_control":
            return self.set_control(str(payload.get("key", "")), payload.get("value"))
        if command == "set_palette_color":
            return self.set_palette_color(payload.get("color"), payload.get("target"))
        if command == "send_link":
            return self.send_link(payload.get("link"))
        if command == "send_all_links":
            return self.send_all_links()
        if command == "visual_trigger":
            return self.visual_trigger(payload.get("id"))
        if command == "visual_opacity":
            return self.visual_opacity_trigger(payload.get("value"))
        if command == "visual_slider":
            return self.visual_slider_trigger(payload.get("id"), payload.get("value"))
        if command == "now_playing_opacity":
            return self.now_playing_opacity_trigger(payload.get("value"))
        if command == "generative_visual":
            return self.update_generative_visual(payload.get("values", payload))
        if command == "math_scene_trigger":
            return self.trigger_math_scene(payload.get("id"), str(payload.get("mode", "trigger")))
        if command == "generative_visual_stop":
            return self.stop_generative_visual()
        if command == "linked_look":
            return self.apply_preset(str(payload.get("name", "")), "performance", payload.get("apply_lights"))
        if command == "camera_trigger":
            return self.camera_trigger(payload.get("kind"), payload.get("id"), payload.get("group"))
        if command == "camera_opacity":
            return self.camera_opacity_trigger(payload.get("group"), payload.get("value"))
        if command == "reset_control":
            return self.reset_control(str(payload.get("key", "")))
        if command == "safe_reset":
            return self.safe_reset()
        if command == "panic_safe":
            return self.panic_safe()
        if command == "use_current_colors":
            return self.save_current_colors_as_template()
        if command == "test_blt_outputs":
            return self.test_blt_outputs()
        if command == "clear_log":
            return self.clear_command_log()
        if command == "bpm_start":
            return self.start_bpm_swap(payload.get("bpm"), payload.get("division"), payload.get("seconds"))
        if command == "bpm_stop":
            return self.stop_bpm_swap()
        if command == "bpm_resync":
            return self.resync_bpm_swap(payload.get("bpm"), payload.get("division"), payload.get("seconds"))
        if command == "bpm_follow":
            return self.set_bpm_follow(payload.get("enabled"))
        if command == "bpm_update":
            return self.update_bpm_swap(payload.get("bpm"), payload.get("division"), payload.get("seconds"))
        raise ValueError(f"Unknown command: {command}")


ENGINE = ShowEngine()


def system_confidence_payload(config: dict[str, Any], blt: dict[str, Any], show: dict[str, Any]) -> list[dict[str, Any]]:
    targets = normalize_osc_targets(config.get("osc_targets", []), config)
    udp_targets = [target for target in targets if target.get("enabled") and target.get("host")]
    deliveries = show.get("delivery_status", {}) if isinstance(show, dict) else {}
    visual_controls = normalize_visual_controls(config.get("visual_controls", []))
    camera_controls = normalize_camera_controls(config.get("camera_controls", {}))

    def udp_system(key: str, label: str, configured: bool) -> dict[str, Any]:
        delivery = deliveries.get(key, {}) if isinstance(deliveries, dict) else {}
        last_sent = text_value(delivery.get("last_sent", "")) if isinstance(delivery, dict) else ""
        if not udp_targets:
            return {"key": key, "label": label, "state": "offline", "summary": "No UDP target", "detail": "No enabled OSC target is configured."}
        if not configured:
            return {"key": key, "label": label, "state": "unconfigured", "summary": "Needs mapping", "detail": "An OSC target exists, but this output has no configured cue address."}
        if last_sent:
            return {"key": key, "label": label, "state": "sent", "summary": "Sent", "detail": f"UDP packet dispatched {last_sent}. UDP has no acknowledgement.", "last_sent": last_sent}
        return {"key": key, "label": label, "state": "ready", "summary": "Ready (UDP)", "detail": "Configured to dispatch UDP. Delivery cannot be confirmed by OSC alone."}

    blt_ok = bool(blt.get("ok")) if isinstance(blt, dict) else False
    blt_detail = text_value(blt.get("status", "")) if isinstance(blt, dict) else ""
    systems = [{
        "key": "beatlink",
        "label": "BeatLink",
        "state": "connected" if blt_ok else "offline",
        "summary": "Connected" if blt_ok else "Waiting",
        "detail": blt_detail or ("HTTP source responded." if blt_ok else "No live BeatLink response yet."),
    }]
    systems.append(udp_system("lights", "Lights", any(clean_osc_address(address) for address in config.get("osc_addresses", {}).values()) if isinstance(config.get("osc_addresses", {}), dict) else False))
    systems.append(udp_system("visuals", "Visuals", any(clean_osc_address(item.get("address", "")) for item in visual_controls)))
    camera_items = [*camera_controls.get("scenes", [])]
    for group_items in camera_controls.get("groups", {}).values():
        camera_items.extend(group_items)
    systems.append(udp_system("cameras", "Cameras", any(clean_osc_address(item.get("address", "")) for item in camera_items)))
    return systems


def preflight_check(
    key: str,
    label: str,
    ok: bool,
    summary: str,
    detail: str = "",
    severity: str | None = None,
    category: str = "System",
) -> dict[str, Any]:
    return {
        "key": key,
        "label": label,
        "ok": bool(ok),
        "summary": summary,
        "detail": detail,
        "severity": severity or ("ok" if ok else "warning"),
        "category": category,
    }


def git_preflight_payload() -> dict[str, Any]:
    git_dir = PROJECT_ROOT / ".git"

    def read_text(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8", errors="ignore").strip()
        except Exception:
            return ""

    def read_commit(ref_name: str) -> str:
        ref_path = git_dir / ref_name
        commit = read_text(ref_path)
        if commit:
            return commit[:7]
        packed = read_text(git_dir / "packed-refs")
        for line in packed.splitlines():
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) == 2 and parts[1] == ref_name:
                return parts[0][:7]
        return ""

    head = read_text(git_dir / "HEAD")
    branch = ""
    commit = ""
    if head.startswith("ref: "):
        ref = head[5:].strip()
        branch = ref.rsplit("/", 1)[-1]
        commit = read_commit(ref)
    elif head:
        commit = head[:7]

    remote = ""
    config_text = read_text(git_dir / "config")
    in_origin = False
    for raw_line in config_text.splitlines():
        line = raw_line.strip()
        if line.startswith("["):
            in_origin = line == '[remote "origin"]'
            continue
        if in_origin and line.startswith("url") and "=" in line:
            remote = line.split("=", 1)[1].strip()
            break

    dirty = ""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=0.35,
            check=False,
        )
        if result.returncode == 0:
            dirty = result.stdout.strip()
    except Exception:
        dirty = ""

    return {
        "branch": branch,
        "commit": commit,
        "remote": remote,
        "dirty": bool(dirty),
        "dirty_count": len([line for line in dirty.splitlines() if line.strip()]),
    }

def check_http_json(url: str, timeout: float = 0.35) -> tuple[bool, str]:
    if not url:
        return False, "No URL configured."
    try:
        with urlopen(url, timeout=timeout) as response:
            response.read(4096)
            return 200 <= response.status < 400, f"HTTP {response.status} from {url}"
    except Exception as exc:
        return False, f"{url} did not respond: {exc}"


def make_preflight_payload(host: str, port: int) -> dict[str, Any]:
    config = load_config()
    connection = connection_payload(config, port)
    git_info = git_preflight_payload()
    checks: list[dict[str, Any]] = []

    checks.append(preflight_check("server", "App server", True, "Running", f"Serving on {connection['local_control_url']}", category="Server"))
    checks.append(
        preflight_check(
            "config",
            "Local config",
            CONFIG_PATH.exists(),
            "Config file present" if CONFIG_PATH.exists() else "Using defaults",
            str(CONFIG_PATH),
            severity="ok" if CONFIG_PATH.exists() else "warning",
            category="Server",
        )
    )

    music_root_raw = text_value(config.get("music_root", ""))
    music_root = portable_project_path(music_root_raw) if music_root_raw else Path("")
    checks.append(
        preflight_check(
            "music_root",
            "Music root",
            bool(music_root_raw and music_root.exists() and music_root.is_dir()),
            "Ready" if music_root_raw and music_root.exists() and music_root.is_dir() else "Not available",
            str(music_root) if music_root_raw else "Set Music Root if album-art matching is needed.",
            severity="warning",
            category="Media",
        )
    )

    artwork_path = artwork_output_path(config)
    checks.append(
        preflight_check(
            "artwork_output",
            "Current artwork",
            artwork_path.exists(),
            "Artwork generated" if artwork_path.exists() else "No current artwork yet",
            str(artwork_path),
            severity="ok" if artwork_path.exists() else "warning",
            category="Media",
        )
    )
    checks.append(
        preflight_check(
            "artwork_folder",
            "Artwork folder",
            artwork_path.parent.exists(),
            "Folder exists" if artwork_path.parent.exists() else "Folder missing",
            str(artwork_path.parent),
            severity="error" if not artwork_path.parent.exists() else "ok",
            category="Media",
        )
    )

    sources = blt_sources(config)
    if sources:
        any_blt_ok = False
        details: list[str] = []
        for source in sources[:1]:
            ok, detail = check_http_json(source.get("url", ""))
            any_blt_ok = any_blt_ok or ok
            details.append(f"{source.get('label', 'BLT')}: {detail}")
        if len(sources) > 1:
            details.append(f"Skipped {len(sources) - 1} additional BLT source(s) to keep preflight fast.")
        checks.append(
            preflight_check(
                "beatlink",
                "Beat Link Trigger",
                any_blt_ok,
                "Reachable" if any_blt_ok else "Waiting for BLT",
                "\n".join(details),
                severity="warning" if not any_blt_ok else "ok",
                category="Network",
            )
        )
    else:
        checks.append(preflight_check("beatlink", "Beat Link Trigger", False, "No BLT source configured", "Set BLT URL or network routes in Settings.", severity="warning", category="Network"))

    targets = normalize_osc_targets(config.get("osc_targets", []), config)
    enabled_targets = [target for target in targets if target.get("enabled") and target.get("host")]
    checks.append(
        preflight_check(
            "osc_targets",
            "OSC output targets",
            bool(enabled_targets),
            f"{len(enabled_targets)} enabled target(s)" if enabled_targets else "No enabled OSC targets",
            ", ".join(f"{target['label']} {target['host']}:{target['port']}" for target in enabled_targets) or "Configure Resolume/stream OSC targets before show time.",
            severity="error" if not enabled_targets else "ok",
            category="Network",
        )
    )

    resolume_host = connection.get("resolume_host", "")
    checks.append(
        preflight_check(
            "active_resolume",
            "Active Resolume route",
            bool(resolume_host),
            f"{resolume_host}:{connection.get('resolume_port', '')}" if resolume_host else "No active Resolume host",
            "UDP OSC cannot confirm delivery, but the route must be configured.",
            severity="warning" if not resolume_host else "ok",
            category="Network",
        )
    )

    checks.append(
        preflight_check(
            "git",
            "Git version",
            bool(git_info.get("commit")),
            f"{git_info.get('branch') or 'unknown'} @ {git_info.get('commit') or 'unknown'}",
            git_info.get("remote", "No remote configured"),
            severity="warning" if not git_info.get("commit") else "ok",
            category="Code",
        )
    )
    checks.append(
        preflight_check(
            "git_clean",
            "Local code changes",
            not git_info.get("dirty"),
            "Clean" if not git_info.get("dirty") else f"{git_info.get('dirty_count')} local change(s)",
            "Push or discard local code changes before updating the performance PC." if git_info.get("dirty") else "Working tree has no local code edits.",
            severity="warning" if git_info.get("dirty") else "ok",
            category="Code",
        )
    )

    errors = [check for check in checks if not check["ok"] and check["severity"] == "error"]
    warnings = [check for check in checks if not check["ok"] and check["severity"] == "warning"]
    return {
        "ok": not errors,
        "status": "ready" if not errors and not warnings else "warnings" if not errors else "blocked",
        "time": datetime.now().isoformat(timespec="seconds"),
        "uptime_seconds": round(time.time() - SERVER_START_TIME, 1),
        "app": {"name": "NT Performance Hub"},
        "server": {
            "bind_host": host,
            "port": port,
            "local_url": connection["local_control_url"],
            "lan_urls": connection["lan_control_urls"],
            "preflight_url": f"http://127.0.0.1:{port}/preflight",
        },
        "git": git_info,
        "checks": checks,
        "summary": {"errors": len(errors), "warnings": len(warnings), "total": len(checks)},
    }
def make_status_payload(host: str, port: int, include_settings: bool = True, poll_blt: bool = True) -> dict[str, Any]:
    config = load_config()
    connection = connection_payload(config, port)
    artwork_path = artwork_output_path(config)
    ips = local_ipv4_addresses()
    remote_urls = [f"http://{ip}:{port}/" for ip in ips]
    blt = ENGINE.poll_blt(send_on_change=True) if poll_blt else ENGINE.blt_status_snapshot()
    show = ENGINE.snapshot()
    payload = {
        "app": "NT Performance Hub",
        "version": APP_VERSION,
        "time": datetime.now().isoformat(timespec="seconds"),
        "server": {
            "bind_host": host,
            "port": port,
            "remote_urls": remote_urls,
            "local_url": connection["local_control_url"],
            "lan_urls": connection["lan_control_urls"],
            "public_control_url": connection["public_control_url"],
        },
        "config": {
            "path": str(CONFIG_PATH),
            "exists": CONFIG_PATH.exists(),
            "revision": config_revision(),
            "profile": connection["active_name"],
            "profile_id": connection["active_id"],
            "show_machine_name": connection["show_machine_name"],
            "resolume_ip": connection["resolume_host"],
            "resolume_port": connection["resolume_port"],
            "osc_targets": normalize_osc_targets(config.get("osc_targets", []), config),
            "blt_params_url": connection["blt_params_url"],
            "blt_params_urls": [source["url"] for source in blt_sources(config)],
        },
        "artwork": {
            "path": str(artwork_path),
            "exists": artwork_path.exists(),
            "url": "/api/artwork/current",
            "matched_file": ENGINE.latest_matched_file,
            "match_score": ENGINE.latest_match_score,
            "status": ENGINE.latest_artwork_status,
            "updated": (
                datetime.fromtimestamp(artwork_path.stat().st_mtime).isoformat(timespec="seconds")
                if artwork_path.exists()
                else ""
            ),
            "index_rebuild": dict(ENGINE.music_index_rebuild_status),
        },
        "show": show,
        "confidence": system_confidence_payload(config, blt, show),
        "blt": blt,
        "notes": [
            "This app can send performance commands from a browser.",
            "BeatLink live track watching is polling the configured BLT source URLs.",
        ],
    }
    if include_settings:
        payload["presets"] = ENGINE.presets()
        payload["settings"] = ENGINE.config_payload()
    else:
        payload["presets"] = []
    return payload


class AppRequestHandler(SimpleHTTPRequestHandler):
    server_version = "NTPerformanceHub"
    quiet_access_log_paths = {
        "/api/artwork/current",
        "/api/generative/state",
        "/api/identity",
        "/api/preflight",
        "/api/status",
        "/health",
    }

    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def end_headers(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/") or parsed.path == "/health":
            self.send_header("Cache-Control", "no-store")
        else:
            self.send_header("Cache-Control", f"private, max-age={STATIC_ASSET_CACHE_SECONDS}, must-revalidate")
        super().end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/identity":
            self.send_json({"ok": True, "app": {"name": "NT Performance Hub"}})
            return
        if parsed.path == "/api/preflight":
            self.send_json(make_preflight_payload(self.server.bind_host, self.server.server_port))
            return
        if parsed.path == "/api/status":
            query = parse_qs(parsed.query)
            include_settings = text_value(query.get("settings", ["1"])[0]).casefold() not in {"0", "false", "no"}
            poll_blt = text_value(query.get("blt", ["1"])[0]).casefold() not in {"0", "false", "no"}
            self.send_json(make_status_payload(self.server.bind_host, self.server.server_port, include_settings=include_settings, poll_blt=poll_blt))
            return
        if parsed.path == "/api/config":
            self.send_json({"ok": True, "config": ENGINE.config_payload(), "state": ENGINE.snapshot()})
            return
        if parsed.path == "/api/generative/state":
            self.send_json(ENGINE.generative_visual_state())
            return
        if parsed.path == "/preflight":
            self.path = "/preflight.html"
            return super().do_GET()
        if parsed.path == "/visuals/generative":
            self.path = "/generative.html"
            return super().do_GET()
        if parsed.path == "/api/presets":
            self.send_json({"ok": True, "presets": ENGINE.preset_payload(), "state": ENGINE.snapshot()})
            return
        if parsed.path == "/api/artwork/palette":
            self.send_json({"ok": True, "palette": ENGINE.extract_artwork_palette(), "state": ENGINE.snapshot()})
            return
        if parsed.path == "/api/artwork/current":
            self.send_current_artwork()
            return
        if parsed.path == "/health":
            self.send_json({"ok": True, "time": datetime.now().isoformat(timespec="seconds")})
            return
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/command":
            try:
                payload = self.read_json_body()
                self.send_json(ENGINE.handle_command(payload))
            except ValueError as exc:
                self.send_json({"ok": False, "message": str(exc), "state": ENGINE.snapshot()}, status=HTTPStatus.BAD_REQUEST)
            except Exception as exc:
                self.send_json({"ok": False, "message": f"Command failed: {exc}", "state": ENGINE.snapshot()}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if parsed.path == "/api/config":
            try:
                payload = self.read_json_body()
                self.send_json(ENGINE.update_config(payload))
            except ValueError as exc:
                self.send_json({"ok": False, "message": str(exc), "config": ENGINE.config_payload(), "state": ENGINE.snapshot()}, status=HTTPStatus.BAD_REQUEST)
            except Exception as exc:
                self.send_json({"ok": False, "message": f"Settings save failed: {exc}", "config": ENGINE.config_payload(), "state": ENGINE.snapshot()}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if parsed.path == "/api/presets":
            try:
                payload = self.read_json_body()
                self.send_json(ENGINE.save_preset_group(str(payload.get("group", "")), payload.get("presets", {})))
            except ValueError as exc:
                self.send_json({"ok": False, "message": str(exc), "presets": ENGINE.preset_payload(), "state": ENGINE.snapshot()}, status=HTTPStatus.BAD_REQUEST)
            except Exception as exc:
                self.send_json({"ok": False, "message": f"Preset save failed: {exc}", "presets": ENGINE.preset_payload(), "state": ENGINE.snapshot()}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON body: {exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object.")
        return payload

    def send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_current_artwork(self) -> None:
        path = artwork_output_path(load_config())
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Current artwork file not found")
            return

        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        try:
            data = path.read_bytes()
        except OSError as exc:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Could not read artwork: {exc}")
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: Any) -> None:
        if self.is_routine_access_log(args):
            return
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} {format % args}")

    def is_routine_access_log(self, args: tuple[Any, ...]) -> bool:
        if len(args) < 2:
            return False
        request_line = str(args[0])
        status_code = int(args[1]) if str(args[1]).isdigit() else 0
        if status_code >= 400:
            return False
        parts = request_line.split()
        if len(parts) < 2 or parts[0] != "GET":
            return False
        return urlparse(parts[1]).path in self.quiet_access_log_paths


class AppServer(ThreadingHTTPServer):
    bind_host: str


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the remote control web server.")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host. Use 0.0.0.0 for remote devices.")
    parser.add_argument("--port", type=int, default=8080, help="HTTP port.")
    args = parser.parse_args()

    WEB_ROOT.mkdir(exist_ok=True)
    server = AppServer((args.host, args.port), AppRequestHandler)
    server.bind_host = args.host

    print("NT Performance Hub - remote control server")
    print(f"Local:  http://localhost:{args.port}/")
    print(f"Preflight: http://localhost:{args.port}/preflight")
    for url in local_ipv4_addresses():
        print(f"Remote: http://{url}:{args.port}/")
    print("Routine polling logs hidden; errors and commands still print.")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping app server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()


