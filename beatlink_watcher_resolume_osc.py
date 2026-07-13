"""
Watch Beat Link Trigger for the active CDJ track and update Resolume artwork.

Install requirements:
    pip install mutagen Pillow

Optional, if you use the Python launcher on Windows:
    py -m pip install mutagen Pillow
"""

from __future__ import annotations

import builtins
import argparse
import json
import re
import socket
import struct
import sys
import threading
import time
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.error import URLError
from urllib.request import urlopen

from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen import File as MutagenFile

from extract_album_artwork import DEFAULT_OUTPUT_PIXELS, process_mp3


def print(*args: Any, **kwargs: Any) -> None:
    """Print watcher logs immediately, including when running inside the GUI."""
    kwargs.setdefault("flush", True)
    safe_args = []
    output_encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    for arg in args:
        text = str(arg)
        safe_args.append(text.encode(output_encoding, errors="replace").decode(output_encoding, errors="replace"))
    builtins.print(*safe_args, **kwargs)

BLT_PARAMS_URL = "http://192.168.1.9:17081/params.json"
RESOLUME_OSC_HOST = "192.168.1.9"
RESOLUME_OSC_PORT = 7000
RESOLUME_OSC_ENABLED = True
RESOLUME_OSC_DELAY_SECONDS = 0.0
OSC_TITLE_ADDRESS = "/blt/title"
OSC_ARTIST_ADDRESS = "/blt/artist"
OSC_TRACK_ADDRESS = "/blt/track"
OSC_TRACK_INFO_ADDRESS = "/blt/track-info"
RESOLUME_LINK_OSC_ADDRESSES = {
    link_number: f"/composition/layers/1/clips/2/dashboard/link{link_number}"
    for link_number in range(1, 9)
}
VISUAL_LINK_CONTROLS = (
    {
        "key": "PRIMARY",
        "link": 1,
        "label": "Color 1",
        "tag": "PRIMARY",
        "value_type": "color",
    },
    {
        "key": "SECONDARY",
        "link": 2,
        "label": "Color 2",
        "tag": "SECONDARY",
        "value_type": "color",
    },
    {
        "key": "STROBE_PERCENT",
        "link": 3,
        "label": "Strobe Frequency",
        "tag": "STROBE_PERCENT",
        "value_type": "strobe_percent",
    },
    {
        "key": "STROBE",
        "link": 4,
        "label": "Strobe Color",
        "tag": "STROBE",
        "value_type": "strobe_color",
    },
    {
        "key": "SATURATION",
        "link": 5,
        "label": "Saturation",
        "tag": "SATURATION",
        "value_type": "saturation",
    },
    {
        "key": "BRIGHTNESS",
        "link": 6,
        "label": "Brightness",
        "tag": "BRIGHTNESS",
        "value_type": "brightness",
    },
)
VISUAL_OSC_ADDRESSES = {
    control["key"]: RESOLUME_LINK_OSC_ADDRESSES[control["link"]]
    for control in VISUAL_LINK_CONTROLS
}
RESOLUME_TRACK_TEXT_ADDRESS = "/composition/layers/28/clips/2/video/source/blocktextgenerator/text/params/lines"
RESOLUME_TRACK_INFO_TEXT_ADDRESS = "/composition/layers/27/clips/2/video/source/blocktextgenerator/text/params/lines"
MUSIC_ROOT = Path(r"F:\Music Collection")
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
INDEX_PATH = DATA_DIR / "music_library_index.json"
VISUAL_DEFAULTS_CONFIG_PATH = CONFIG_DIR / "visual_defaults.json"
POLL_SECONDS = 2.0
MATCH_THRESHOLD = 0.72
COLOR_HUE_VALUES = {
    "red": 0.000,
    "orange": 0.083,
    "amber": 0.100,
    "yellow": 0.166,
    "lime": 0.250,
    "green": 0.333,
    "teal": 0.458,
    "cyan": 0.500,
    "blue": 0.666,
    "indigo": 0.708,
    "purple": 0.750,
    "violet": 0.764,
    "uv": 0.780,
    "magenta": 0.833,
    "pink": 0.900,
}
STROBE_COLOR_NAMES = (
    *(
        name
        for name, _value in sorted(COLOR_HUE_VALUES.items(), key=lambda item: (item[1], item[0]))
    ),
)
STROBE_COLOR_VALUES = {
    name: COLOR_HUE_VALUES[name]
    for name in STROBE_COLOR_NAMES
}
STROBE_PERCENT_VALUES = {
    "0": 0.0,
    "0%": 0.0,
    "off": 0.0,
    "10": 0.1,
    "10%": 0.1,
    "25": 0.25,
    "25%": 0.25,
    "low": 0.25,
    "50": 0.5,
    "50%": 0.5,
    "medium": 0.5,
    "75": 0.75,
    "75%": 0.75,
    "high": 0.75,
    "90": 0.9,
    "90%": 0.9,
    "95": 0.95,
    "95%": 0.95,
    "100": 0.95,
    "100%": 0.95,
    "full": 0.95,
}
SATURATION_VALUES = {
    "0": 0.0,
    "0%": 0.0,
    "off": 0.0,
    "10": 0.1,
    "10%": 0.1,
    "25": 0.25,
    "25%": 0.25,
    "low": 0.25,
    "50": 0.5,
    "50%": 0.5,
    "medium": 0.5,
    "75": 0.75,
    "75%": 0.75,
    "high": 0.75,
    "90": 0.9,
    "90%": 0.9,
    "95": 0.95,
    "95%": 0.95,
    "100": 1.0,
    "100%": 1.0,
    "full": 1.0,
}
BRIGHTNESS_VALUES = dict(SATURATION_VALUES)
DEFAULT_VISUAL_TAGS = {
    "PRIMARY": "blue",
    "SECONDARY": "purple",
    "STROBE_PERCENT": "0",
    "STROBE": "red",
    "SATURATION": "100",
    "BRIGHTNESS": "100",
}
ACTIVE_VISUAL_DEFAULTS = dict(DEFAULT_VISUAL_TAGS)
COLOR_VISUAL_KEYS = tuple(control["key"] for control in VISUAL_LINK_CONTROLS if control["value_type"] == "color")
VISUAL_CONTROL_KEYS = tuple(control["key"] for control in VISUAL_LINK_CONTROLS)
last_visual_defaults_config_mtime = 0.0


TrackIndexEntry = Dict[str, str]
latest_osc_generation = 0


def canonical_strobe_percent(value: str) -> str:
    """Normalize strobe comment values to the number-only template format."""
    cleaned = str(value).strip().casefold().removesuffix("%")
    aliases = {
        "off": "0",
        "low": "25",
        "medium": "50",
        "high": "75",
        "full": "95",
        "100": "95",
    }
    return aliases.get(cleaned, cleaned)


def canonical_saturation(value: str) -> str:
    """Normalize saturation comment values to the number-only template format."""
    cleaned = str(value).strip().casefold().removesuffix("%")
    aliases = {
        "off": "0",
        "low": "25",
        "medium": "50",
        "high": "75",
        "full": "100",
    }
    return aliases.get(cleaned, cleaned)


def canonical_brightness(value: str) -> str:
    """Normalize brightness comment values to the number-only template format."""
    return canonical_saturation(value)


def osc_pad(value: bytes) -> bytes:
    """Pad an OSC byte string to a 4-byte boundary."""
    padding = (4 - (len(value) % 4)) % 4
    return value + (b"\x00" * padding)


def osc_string(value: str) -> bytes:
    """Encode an OSC string with a null terminator and 4-byte padding."""
    return osc_pad(value.encode("utf-8") + b"\x00")


def send_osc_string(address: str, value: str) -> None:
    """Send one OSC string message to Resolume."""
    if not RESOLUME_OSC_ENABLED:
        return

    packet = osc_string(address) + osc_string(",s") + osc_string(value)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(packet, (RESOLUME_OSC_HOST, RESOLUME_OSC_PORT))


def send_osc_float(address: str, value: float) -> None:
    """Send one OSC float message to Resolume."""
    if not RESOLUME_OSC_ENABLED:
        return

    packet = osc_string(address) + osc_string(",f") + struct.pack(">f", float(value))
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(packet, (RESOLUME_OSC_HOST, RESOLUME_OSC_PORT))


def send_track_osc(track: Dict[str, str]) -> None:
    """Send title, artist, and combined track text to Resolume over OSC."""
    title = track.get("title") or ""
    artist = track.get("artist") or ""
    full_track = describe_track(track)

    try:
        send_osc_string(OSC_TITLE_ADDRESS, title)
        send_osc_string(OSC_ARTIST_ADDRESS, artist)
        send_osc_string(OSC_TRACK_ADDRESS, full_track)
        send_osc_string(RESOLUME_TRACK_TEXT_ADDRESS, full_track)
        print(f"Sent OSC title: {OSC_TITLE_ADDRESS} = {title}")
        print(f"Sent OSC artist: {OSC_ARTIST_ADDRESS} = {artist}")
        print(f"Sent OSC track: {OSC_TRACK_ADDRESS} = {full_track}")
        print(f"Sent OSC track text: {RESOLUME_TRACK_TEXT_ADDRESS} = {full_track}")
    except OSError as exc:
        print(f"ERROR: Could not send OSC text to Resolume: {exc}")


def send_track_info_osc(track_info: str) -> None:
    """Send track BPM/source-player info to Resolume."""
    if not track_info:
        return

    try:
        send_osc_string(OSC_TRACK_INFO_ADDRESS, track_info)
        send_osc_string(RESOLUME_TRACK_INFO_TEXT_ADDRESS, track_info)
        print(f"Sent OSC track info: {RESOLUME_TRACK_INFO_TEXT_ADDRESS} = {track_info}")
    except OSError as exc:
        print(f"ERROR: Could not send OSC track info to Resolume: {exc}")


def parse_visual_comment_tags(comment: str) -> Dict[str, str]:
    """Parse supported visual control tags from a free-form comment field."""
    parsed: Dict[str, str] = {}
    supported_keys = set(ACTIVE_VISUAL_DEFAULTS)

    for part in re.split(r"\s*;\s*", comment or ""):
        if "=" not in part:
            continue

        key, value = part.split("=", 1)
        normalized_key = key.strip().upper()
        if normalized_key in {"ACCENT", "STROBE_COLOR", "STROBECOLOUR"}:
            normalized_key = "STROBE"
        if normalized_key in {"ENERGY", "STROBE%", "STROBE_PERCENT", "STROBEPERCENT", "STROBE_RATE"}:
            normalized_key = "STROBE_PERCENT"
        if normalized_key in {"SAT", "SATURATION", "SATURATION_PERCENT", "SATURATION%", "SATURATIONPERCENT"}:
            normalized_key = "SATURATION"
        if normalized_key in {"BRIGHTNESS", "BRIGHTNESS_PERCENT", "BRIGHTNESS%", "BRIGHTNESSPERCENT", "DIMMER"}:
            normalized_key = "BRIGHTNESS"
        if normalized_key not in supported_keys:
            continue

        parsed_value = value.strip().casefold()
        if normalized_key == "STROBE_PERCENT":
            parsed_value = canonical_strobe_percent(parsed_value)
        elif normalized_key == "SATURATION":
            parsed_value = canonical_saturation(parsed_value)
        elif normalized_key == "BRIGHTNESS":
            parsed_value = canonical_brightness(parsed_value)

        parsed[normalized_key] = parsed_value

    return parsed


def resolve_visual_controls(comment: str) -> Dict[str, float]:
    """Resolve comment tags to normalized Resolume dashboard float values."""
    tags = parse_visual_comment_tags(comment)
    resolved: Dict[str, float] = {}

    for key in COLOR_VISUAL_KEYS:
        color = tags.get(key, ACTIVE_VISUAL_DEFAULTS[key]).casefold()
        if color not in COLOR_HUE_VALUES:
            fallback = ACTIVE_VISUAL_DEFAULTS[key]
            print(
                f"WARNING: Unknown {key} color '{color}' in Comment tag. "
                f"Using default '{fallback}'."
            )
            color = fallback
        resolved[key] = COLOR_HUE_VALUES[color]

    strobe_color = tags.get("STROBE", ACTIVE_VISUAL_DEFAULTS["STROBE"]).casefold()
    if strobe_color not in STROBE_COLOR_VALUES:
        fallback = ACTIVE_VISUAL_DEFAULTS["STROBE"]
        print(
            f"WARNING: Unknown STROBE color '{strobe_color}' in Comment tag. "
            f"Using default '{fallback}'."
        )
        strobe_color = fallback
    resolved["STROBE"] = STROBE_COLOR_VALUES[strobe_color]

    strobe_percent = canonical_strobe_percent(tags.get("STROBE_PERCENT", ACTIVE_VISUAL_DEFAULTS["STROBE_PERCENT"]))
    if strobe_percent not in STROBE_PERCENT_VALUES:
        fallback = ACTIVE_VISUAL_DEFAULTS["STROBE_PERCENT"]
        print(
            f"WARNING: Unknown STROBE_PERCENT value '{strobe_percent}' in Comment tag. "
            f"Using default '{fallback}'."
        )
        strobe_percent = fallback
    resolved["STROBE_PERCENT"] = STROBE_PERCENT_VALUES[strobe_percent]

    saturation = canonical_saturation(tags.get("SATURATION", ACTIVE_VISUAL_DEFAULTS["SATURATION"]))
    if saturation not in SATURATION_VALUES:
        fallback = ACTIVE_VISUAL_DEFAULTS["SATURATION"]
        print(
            f"WARNING: Unknown SATURATION value '{saturation}' in Comment tag. "
            f"Using default '{fallback}'."
        )
        saturation = fallback
    resolved["SATURATION"] = SATURATION_VALUES[saturation]

    brightness = canonical_brightness(tags.get("BRIGHTNESS", ACTIVE_VISUAL_DEFAULTS["BRIGHTNESS"]))
    if brightness not in BRIGHTNESS_VALUES:
        fallback = ACTIVE_VISUAL_DEFAULTS["BRIGHTNESS"]
        print(
            f"WARNING: Unknown BRIGHTNESS value '{brightness}' in Comment tag. "
            f"Using default '{fallback}'."
        )
        brightness = fallback
    resolved["BRIGHTNESS"] = BRIGHTNESS_VALUES[brightness]

    return resolved


def describe_visual_controls(comment: str, values: Dict[str, float]) -> None:
    """Print a clear visual metadata summary for the console."""
    tags = parse_visual_comment_tags(comment)

    print("Visual metadata from Comment:")
    for key in VISUAL_CONTROL_KEYS:
        word = tags.get(key, ACTIVE_VISUAL_DEFAULTS[key]).casefold()
        default_note = " default" if key not in tags else ""
        print(f"  {key:<9} {word:<8} -> {values[key]:.3f}{default_note}")


def send_visual_control_osc(values: Dict[str, float]) -> None:
    """Send parsed visual metadata values to Resolume dashboard controls."""
    try:
        print("Sending visual OSC controls:")
        for key, address in VISUAL_OSC_ADDRESSES.items():
            send_osc_float(address, values[key])
            print(f"  {address} = {values[key]:.3f} ({key})")
    except OSError as exc:
        print(f"ERROR: Could not send visual OSC controls to Resolume: {exc}")


def validate_visual_defaults(defaults: Dict[str, str]) -> Dict[str, str]:
    """Validate default visual tags and fall back when needed."""
    validated = dict(DEFAULT_VISUAL_TAGS)

    for key in COLOR_VISUAL_KEYS:
        value = str(defaults.get(key, validated[key])).strip().casefold()
        if value in COLOR_HUE_VALUES:
            validated[key] = value
        else:
            print(f"WARNING: Unknown default {key} color '{value}'. Keeping '{validated[key]}'.")

    strobe_color = str(defaults.get("STROBE", validated["STROBE"])).strip().casefold()
    if strobe_color in STROBE_COLOR_VALUES:
        validated["STROBE"] = strobe_color
    else:
        print(f"WARNING: Unknown default STROBE color '{strobe_color}'. Keeping '{validated['STROBE']}'.")

    strobe_percent = canonical_strobe_percent(str(defaults.get("STROBE_PERCENT", validated["STROBE_PERCENT"])))
    if strobe_percent in STROBE_PERCENT_VALUES:
        validated["STROBE_PERCENT"] = strobe_percent
    else:
        print(f"WARNING: Unknown default STROBE_PERCENT '{strobe_percent}'. Keeping '{validated['STROBE_PERCENT']}'.")

    saturation = canonical_saturation(str(defaults.get("SATURATION", validated["SATURATION"])))
    if saturation in SATURATION_VALUES:
        validated["SATURATION"] = saturation
    else:
        print(f"WARNING: Unknown default SATURATION '{saturation}'. Keeping '{validated['SATURATION']}'.")

    brightness = canonical_brightness(str(defaults.get("BRIGHTNESS", validated["BRIGHTNESS"])))
    if brightness in BRIGHTNESS_VALUES:
        validated["BRIGHTNESS"] = brightness
    else:
        print(f"WARNING: Unknown default BRIGHTNESS '{brightness}'. Keeping '{validated['BRIGHTNESS']}'.")

    return validated


def load_visual_defaults_config(force: bool = False) -> None:
    """Load live-editable visual defaults written by the GUI."""
    global last_visual_defaults_config_mtime

    if not VISUAL_DEFAULTS_CONFIG_PATH.exists():
        return

    try:
        mtime = VISUAL_DEFAULTS_CONFIG_PATH.stat().st_mtime
    except OSError:
        return

    if not force and mtime == last_visual_defaults_config_mtime:
        return

    try:
        raw_defaults = json.loads(VISUAL_DEFAULTS_CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"WARNING: Could not read visual defaults config: {exc}")
        return

    if not isinstance(raw_defaults, dict):
        print("WARNING: Visual defaults config is not a JSON object.")
        return

    ACTIVE_VISUAL_DEFAULTS.update(validate_visual_defaults(raw_defaults))
    last_visual_defaults_config_mtime = mtime
    print(
        "Loaded live visual defaults: "
        + ", ".join(f"{key}={value}" for key, value in ACTIVE_VISUAL_DEFAULTS.items())
    )


def send_scheduled_track_osc(track: Dict[str, str], generation: int) -> None:
    """Send delayed OSC only if no newer track has been scheduled."""
    if generation != latest_osc_generation:
        return
    send_track_osc(track)


def schedule_track_osc(track: Dict[str, str]) -> None:
    """Send track text to Resolume after the configured delay."""
    global latest_osc_generation

    if RESOLUME_OSC_DELAY_SECONDS <= 0:
        send_track_osc(track)
        return

    latest_osc_generation += 1
    generation = latest_osc_generation
    delayed_track = dict(track)
    timer = threading.Timer(
        RESOLUME_OSC_DELAY_SECONDS,
        send_scheduled_track_osc,
        args=(delayed_track, generation),
    )
    timer.daemon = True
    timer.start()
    print(f"Scheduled OSC text update in {RESOLUME_OSC_DELAY_SECONDS:g} seconds.")


def normalize_text(value: Any) -> str:
    """Normalize metadata and filenames for loose matching."""
    text = str(value or "").casefold()
    text = re.sub(r"\([^)]*\)|\[[^]]*\]", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"\b(feat|ft|featuring|with|original mix|extended mix|radio edit)\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def make_match_key(artist: str, title: str) -> str:
    """Create a fuzzy-match key from artist and title."""
    return normalize_text(f"{artist} {title}")


def get_first_tag_value(tags: Any, names: Iterable[str]) -> str:
    """Return the first populated metadata value from a Mutagen tag object."""
    if not tags:
        return ""

    for name in names:
        value = tags.get(name)
        if not value:
            continue
        if isinstance(value, list):
            return str(value[0]) if value else ""
        return str(value)

    return ""


def read_mp3_index_entry(mp3_path: Path) -> Optional[TrackIndexEntry]:
    """Read enough metadata from an MP3 to support matching against BLT."""
    try:
        audio = MutagenFile(mp3_path, easy=True)
    except Exception:
        return None

    tags = audio.tags if audio else None
    title = get_first_tag_value(tags, ("title",))
    artist = get_first_tag_value(tags, ("artist", "albumartist", "performer"))
    album = get_first_tag_value(tags, ("album",))
    comment = get_first_tag_value(tags, ("comment", "description"))

    fallback_key = normalize_text(mp3_path.stem)
    match_key = make_match_key(artist, title) or fallback_key

    return {
        "path": str(mp3_path),
        "title": title,
        "artist": artist,
        "album": album,
        "comment": comment,
        "filename": mp3_path.stem,
        "match_key": match_key,
        "fallback_key": fallback_key,
    }


def read_mp3_comment(mp3_path: Path) -> Tuple[str, str]:
    """Read the current Comment metadata from a matched MP3 file."""
    try:
        audio = MutagenFile(mp3_path, easy=True)
    except Exception as exc:
        print(f"WARNING: Could not refresh Comment metadata for {mp3_path}: {exc}")
        audio = None

    tags = audio.tags if audio else None
    easy_comment = get_first_tag_value(tags, ("comment", "description"))
    if easy_comment:
        return easy_comment, "easy comment"

    try:
        id3_tags = ID3(mp3_path)
    except ID3NoHeaderError:
        return "", "no ID3 tag"
    except Exception as exc:
        print(f"WARNING: Could not inspect ID3 comment frames for {mp3_path}: {exc}")
        return "", "ID3 read error"

    comment_frames = id3_tags.getall("COMM")
    for frame in comment_frames:
        text = " ".join(str(part) for part in frame.text if str(part).strip()).strip()
        if text:
            description = frame.desc or "COMM"
            language = frame.lang or "und"
            return text, f"ID3 COMM desc='{description}' lang='{language}'"

    for key, frame in id3_tags.items():
        if key.startswith("COMM"):
            text_values = getattr(frame, "text", [])
            text = " ".join(str(part) for part in text_values if str(part).strip()).strip()
            if text:
                return text, f"ID3 {key}"

    return "", "no comment frame"


def build_music_index() -> List[TrackIndexEntry]:
    """Scan the music library and build a searchable MP3 metadata index."""
    print(f"Building music index from: {MUSIC_ROOT}")
    entries: List[TrackIndexEntry] = []

    for mp3_path in MUSIC_ROOT.rglob("*.mp3"):
        entry = read_mp3_index_entry(mp3_path)
        if entry:
            entries.append(entry)
            if len(entries) % 500 == 0:
                print(f"Indexed {len(entries):,} MP3 files...")

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Indexed {len(entries):,} MP3 files.")
    print(f"Saved index: {INDEX_PATH}")
    return entries


def load_music_index(rebuild: bool = False) -> List[TrackIndexEntry]:
    """Load the cached music index, rebuilding it when needed."""
    if rebuild or not INDEX_PATH.exists():
        return build_music_index()

    try:
        entries = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        if entries and "comment" not in entries[0]:
            print("Music index does not include Comment metadata yet, rebuilding it.")
            return build_music_index()
        return entries
    except Exception as exc:
        print(f"Could not read index cache, rebuilding it: {exc}")
        return build_music_index()


def fetch_blt_params() -> Optional[Dict[str, Any]]:
    """Fetch current player state from Beat Link Trigger's OBS overlay server."""
    try:
        with urlopen(BLT_PARAMS_URL, timeout=3) as response:
            return json.loads(response.read().decode("utf-8"))
    except URLError as exc:
        print(f"Waiting for Beat Link Trigger overlay server: {exc}")
    except Exception as exc:
        print(f"Could not read Beat Link Trigger params: {exc}")

    return None


def is_truthy(value: Any) -> bool:
    """Interpret BLT JSON booleans and boolean-like strings."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().casefold() in {"true", "yes", "1", "on", "playing"}
    return False


def is_player_playing(player: Dict[str, Any]) -> bool:
    """Return True only when BLT indicates the player is actively playing."""
    if is_truthy(player.get("is-paused")):
        return False
    if is_truthy(player.get("is-cued")) or is_truthy(player.get("is-cueing")):
        return False

    explicit_playing = get_first_present_value(
        player,
        (
            "is-playing",
            "is_playing",
            "playing",
            "is-running",
            "is_running",
            "play-state",
            "play_state",
            "state",
            "status",
        ),
    )
    if explicit_playing not in (None, ""):
        return is_truthy(explicit_playing)

    return bool(player.get("track")) and not is_truthy(player.get("is-paused"))


def find_matching_player(master: Dict[str, Any], players: Any) -> Dict[str, Any]:
    """Merge master track data with its full player object when possible."""
    if not isinstance(players, dict):
        return master

    master_number = str(master.get("number") or master.get("player") or "").strip()
    if not master_number:
        return master

    for player in players.values():
        if not isinstance(player, dict):
            continue
        player_number = str(player.get("number") or player.get("player") or "").strip()
        if player_number == master_number:
            merged = dict(player)
            merged.update({key: value for key, value in master.items() if value not in (None, "")})
            return merged

    return master


def get_display_time(value: Any) -> str:
    """Extract a display-ready time string from a BLT time object or scalar."""
    if isinstance(value, dict):
        for key in ("display", "text", "formatted", "value"):
            if value.get(key):
                return str(value[key])
        return ""

    if value is None:
        return ""

    return str(value)


def get_first_present_value(source: Dict[str, Any], keys: Iterable[str]) -> Any:
    """Return the first non-empty value from a dictionary."""
    for key in keys:
        value = source.get(key)
        if value not in (None, ""):
            return value
    return ""


def format_bpm(value: Any) -> str:
    """Format a BLT BPM value for display."""
    if isinstance(value, dict):
        value = get_first_present_value(value, ("display", "text", "effective", "value", "bpm"))

    if value in (None, ""):
        return ""

    try:
        bpm = float(value)
    except (TypeError, ValueError):
        return str(value)

    if bpm > 1000:
        bpm = bpm / 100.0

    if bpm.is_integer():
        return str(int(bpm))

    return f"{bpm:.1f}"


def format_source_player(value: Any) -> str:
    """Format source player text for display."""
    if isinstance(value, dict):
        value = get_first_present_value(value, ("display", "text", "name", "number", "value", "player"))

    if value in (None, ""):
        return ""

    text = str(value).strip()
    if text.casefold().startswith("player"):
        return text
    if text.isdigit():
        return f"Player {text}"
    return text


def format_player_number(value: Any) -> str:
    """Format a player number for display."""
    if isinstance(value, dict):
        value = get_first_present_value(value, ("display", "text", "number", "value", "player"))

    if value in (None, ""):
        return ""

    text = str(value).strip()
    if text.casefold().startswith("player"):
        return text
    if text.isdigit():
        return f"Player {text}"
    return text


def format_device_name(value: Any) -> str:
    """Format a CDJ/XDJ device name for display."""
    if isinstance(value, dict):
        value = get_first_present_value(value, ("display", "text", "name", "model", "value"))

    if value in (None, ""):
        return ""

    return str(value).strip()


def build_track_info(track: Dict[str, str]) -> str:
    """Build the layer 27 text from BPM, player number, and device name."""
    parts = []
    bpm = track.get("bpm", "")
    player_number = track.get("player_number", "")
    device_name = track.get("device_name", "")

    if bpm:
        parts.append(f"{bpm} BPM")

    player_parts = [part for part in (player_number, device_name) if part]
    if player_parts:
        parts.append(" ".join(player_parts))

    return " | ".join(parts)


def select_active_track(params: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """Pick the master track only when the master player is actively playing."""
    master = params.get("master")
    if not isinstance(master, dict):
        return None

    players = params.get("players")
    player = find_matching_player(master, players)

    if not is_player_playing(player):
        return None

    track = player.get("track")
    if not isinstance(track, dict):
        return None

    title = str(track.get("title") or "").strip()
    artist = str(track.get("artist") or "").strip()
    album = str(track.get("album") or "").strip()
    player_number = format_player_number(
        get_first_present_value(player, ("number", "player", "player-number", "player_number"))
    )
    bpm = format_bpm(
        get_first_present_value(track, ("bpm", "tempo"))
        or get_first_present_value(player, ("bpm", "tempo", "effective-tempo", "effective_tempo"))
    )
    device_name = format_device_name(
        get_first_present_value(
            player,
            (
                "device-name",
                "device_name",
                "device",
                "name",
                "model",
                "product",
                "type",
            ),
        )
    )
    source_player = format_source_player(
        get_first_present_value(
            player,
            (
                "track-source-player",
                "track_source_player",
                "source-player",
                "source_player",
                "source",
                "number",
                "player",
            ),
        )
    )

    if title or artist:
        return {
            "title": title,
            "artist": artist,
            "album": album,
            "player": player_number,
            "bpm": bpm,
            "player_number": player_number,
            "device_name": device_name,
            "source_player": source_player,
        }

    return None


def score_match(track: Dict[str, str], entry: TrackIndexEntry) -> float:
    """Score how likely a library entry is to be the BLT track."""
    query_key = make_match_key(track.get("artist", ""), track.get("title", ""))
    if not query_key:
        query_key = normalize_text(track.get("title", ""))

    metadata_score = SequenceMatcher(None, query_key, entry.get("match_key", "")).ratio()
    filename_score = SequenceMatcher(None, query_key, entry.get("fallback_key", "")).ratio()
    title_score = SequenceMatcher(
        None,
        normalize_text(track.get("title", "")),
        normalize_text(entry.get("title", "") or entry.get("filename", "")),
    ).ratio()

    return max(metadata_score, filename_score * 0.96, title_score * 0.88)


def find_best_match(track: Dict[str, str], index: List[TrackIndexEntry]) -> Optional[Tuple[TrackIndexEntry, float]]:
    """Find the best local MP3 match for a BLT track."""
    best_entry: Optional[TrackIndexEntry] = None
    best_score = 0.0

    for entry in index:
        score = score_match(track, entry)
        if score > best_score:
            best_entry = entry
            best_score = score

    if best_entry and best_score >= MATCH_THRESHOLD:
        return best_entry, best_score

    return None


def describe_track(track: Dict[str, str]) -> str:
    """Format a track for console output."""
    artist = track.get("artist") or "Unknown Artist"
    title = track.get("title") or "Unknown Title"
    return f"{artist} - {title}"


def print_visual_comment_help() -> None:
    """Print accepted visual metadata tags and values."""
    print("Visual Comment tag format:")
    print("  PRIMARY=blue;SECONDARY=purple;STROBE_PERCENT=50;STROBE=red;SATURATION=100;BRIGHTNESS=100")
    print("  Legacy ACCENT=color is also accepted as the strobe color.")
    print("Resolume dashboard link order:")
    for control in VISUAL_LINK_CONTROLS:
        print(f"  Link {control['link']}: {control['label']} ({control['tag']})")
    print("  Links 7-8: reserved / unmapped")
    print(
        "Active fallback defaults: "
        + ", ".join(f"{key}={value}" for key, value in ACTIVE_VISUAL_DEFAULTS.items())
    )
    print("Supported keys:")
    print("  PRIMARY, SECONDARY, STROBE_PERCENT, STROBE, SATURATION, BRIGHTNESS")
    print("Accepted strobe frequency values:")
    print("  0, 10, 25, 50, 75, 90, 95")
    print("Accepted saturation values:")
    print("  0, 10, 25, 50, 75, 90, 100")
    print("Accepted brightness values:")
    print("  0, 10, 25, 50, 75, 90, 100")
    print("Accepted hue values:")

    color_items = sorted(COLOR_HUE_VALUES.items(), key=lambda item: (item[1], item[0]))
    for start in range(0, len(color_items), 6):
        line = ", ".join(f"{name}={value:.3f}" for name, value in color_items[start : start + 6])
        print(f"  {line}")


def watch(rebuild_index: bool = False, output_pixels: int = DEFAULT_OUTPUT_PIXELS) -> int:
    """Continuously watch BLT and update artwork when the active track changes."""
    index = load_music_index(rebuild=rebuild_index)
    last_track_key = ""
    last_track_info = ""
    last_visual_values_key = ""
    last_waiting_message_time = 0.0

    print()
    print("NT Performance Hub")
    print(f"BLT params: {BLT_PARAMS_URL}")
    print(f"Music root: {MUSIC_ROOT}")
    print(f"Output size: {output_pixels}x{output_pixels}")
    print("Press Ctrl+C to stop.")
    print()
    print_visual_comment_help()
    print()

    while True:
        params = fetch_blt_params()
        if not params:
            time.sleep(POLL_SECONDS)
            continue

        track = select_active_track(params)
        if not track:
            now = time.time()
            if now - last_waiting_message_time >= 10:
                print("Waiting for a Beat Link master player that is actively playing...")
                last_waiting_message_time = now
            time.sleep(POLL_SECONDS)
            continue

        track_info = build_track_info(track)
        if track_info and track_info != last_track_info:
            last_track_info = track_info
            send_track_info_osc(track_info)

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
        if track_key == last_track_key:
            time.sleep(POLL_SECONDS)
            continue

        last_track_key = track_key
        print(f"Active track: {describe_track(track)}")
        schedule_track_osc(track)

        match = find_best_match(track, index)
        if not match:
            print("ERROR: Could not confidently match this track to a local MP3.")
            print("       Rebuild the index if the file was recently added.")
            print()
            time.sleep(POLL_SECONDS)
            continue

        entry, score = match
        print(f"Matched local file ({score:.0%}): {entry['path']}")

        current_comment, comment_source = read_mp3_comment(Path(entry["path"]))
        if current_comment:
            print(f"Current Comment metadata ({comment_source}): {current_comment}")
        else:
            print(f"Current Comment metadata: none found ({comment_source}), using visual defaults.")

        load_visual_defaults_config()
        visual_values = resolve_visual_controls(current_comment)
        visual_values_key = json.dumps(visual_values, sort_keys=True)
        if visual_values_key != last_visual_values_key:
            last_visual_values_key = visual_values_key
            describe_visual_controls(current_comment, visual_values)
            send_visual_control_osc(visual_values)

        process_mp3(Path(entry["path"]), output_pixels)
        print()
        time.sleep(POLL_SECONDS)


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Watch Beat Link Trigger and update Resolume artwork/OSC.")
    parser.add_argument("output_pixels", nargs="?", type=int, default=DEFAULT_OUTPUT_PIXELS)
    parser.add_argument("--rebuild-index", action="store_true")
    parser.add_argument("--rebuild-only", action="store_true")
    parser.add_argument("--default-primary", default=DEFAULT_VISUAL_TAGS["PRIMARY"])
    parser.add_argument("--default-secondary", default=DEFAULT_VISUAL_TAGS["SECONDARY"])
    parser.add_argument("--default-strobe", default=DEFAULT_VISUAL_TAGS["STROBE"])
    parser.add_argument("--default-accent", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--default-strobe-percent", default=DEFAULT_VISUAL_TAGS["STROBE_PERCENT"])
    parser.add_argument("--default-energy", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--default-saturation", default=DEFAULT_VISUAL_TAGS["SATURATION"])
    parser.add_argument("--default-brightness", default=DEFAULT_VISUAL_TAGS["BRIGHTNESS"])
    args = parser.parse_args()

    requested_defaults = {
        "PRIMARY": args.default_primary.casefold(),
        "SECONDARY": args.default_secondary.casefold(),
        "STROBE": (args.default_accent or args.default_strobe).casefold(),
        "STROBE_PERCENT": (args.default_energy or args.default_strobe_percent).casefold(),
        "SATURATION": args.default_saturation.casefold(),
        "BRIGHTNESS": args.default_brightness.casefold(),
    }

    ACTIVE_VISUAL_DEFAULTS.update(validate_visual_defaults(requested_defaults))
    load_visual_defaults_config(force=True)

    if args.rebuild_only:
        build_music_index()
        return 0

    try:
        return watch(rebuild_index=args.rebuild_index, output_pixels=args.output_pixels)
    except KeyboardInterrupt:
        print()
        print("Watcher stopped.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
