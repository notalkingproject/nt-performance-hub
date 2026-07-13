"""
Extract embedded album artwork from an MP3 file and save it as a JPEG.

Install requirements:
    pip install mutagen Pillow

Optional, if you use the Python launcher on Windows:
    py -m pip install mutagen Pillow
"""

from __future__ import annotations

import sys
import hashlib
import os
import tempfile
import time
from pathlib import Path
from typing import Optional, Tuple

from mutagen.id3 import APIC, ID3, ID3NoHeaderError
from PIL import Image, ImageOps, UnidentifiedImageError
import io


OUTPUT_IMAGE = Path(r"C:\Users\ryant\Videos\Resolume Visuals\Album Artwork\current_artwork.jpg")
FALLBACK_ARTWORK_IMAGE = Path(r"F:\Branding\Resolume Visuals - Branding\NO_TALKING_DOUGHNUT_LOGO_2.png")
DEFAULT_OUTPUT_PIXELS = 1024
SUPPORTED_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png"}
QUIT_COMMANDS = {"q", "quit", "exit"}


def normalize_mp3_path(raw_path: str) -> Optional[Path]:
    """Normalize a user-provided Windows path and confirm it points to an MP3."""
    raw_path = raw_path.strip()
    if not raw_path:
        print("ERROR: No MP3 path was entered.")
        return None

    if raw_path.lower() in QUIT_COMMANDS:
        return Path("__QUIT__")

    # Windows "Copy as path" often includes surrounding quotes.
    cleaned_path = raw_path.strip('"').strip("'").strip()
    mp3_path = Path(cleaned_path)

    if mp3_path.suffix.lower() != ".mp3":
        print(f"ERROR: The selected file does not look like an MP3: {mp3_path}")
        return None

    return mp3_path


def prompt_for_mp3_path() -> Optional[Path]:
    """Ask the user for an MP3 path and normalize pasted Windows path formats."""
    return normalize_mp3_path(input("Paste an MP3 path, or type q to quit: "))


def find_embedded_artwork(mp3_path: Path) -> Optional[Tuple[bytes, str]]:
    """Return the first embedded album-art image bytes and MIME type from an MP3 file."""
    try:
        tags = ID3(mp3_path)
    except FileNotFoundError:
        print(f"ERROR: MP3 file was not found: {mp3_path}")
        return None
    except ID3NoHeaderError:
        print(f"ERROR: MP3 file has no ID3 tag header: {mp3_path}")
        return None
    except Exception as exc:
        print(f"ERROR: Could not read ID3 tags from MP3: {exc}")
        return None

    artwork_frames = tags.getall("APIC")
    if not artwork_frames:
        print("ERROR: No embedded album artwork was found in the MP3 ID3 tags.")
        return None

    # Prefer front-cover artwork when it is present. APIC type 3 means front cover.
    front_cover = next((frame for frame in artwork_frames if isinstance(frame, APIC) and frame.type == 3), None)
    selected_frame = front_cover or artwork_frames[0]

    mime_type = (selected_frame.mime or "").lower().strip()
    if mime_type not in SUPPORTED_MIME_TYPES:
        print(f"ERROR: Embedded artwork uses an unsupported image type: {mime_type or 'unknown'}")
        return None

    return selected_frame.data, mime_type


def load_fallback_artwork() -> Optional[Tuple[bytes, str]]:
    """Load the configured fallback artwork image when an MP3 has no embedded art."""
    try:
        return FALLBACK_ARTWORK_IMAGE.read_bytes(), fallback_artwork_mime_type(FALLBACK_ARTWORK_IMAGE)
    except FileNotFoundError:
        print(f"ERROR: Fallback artwork image was not found: {FALLBACK_ARTWORK_IMAGE}")
    except PermissionError:
        print(f"ERROR: Permission denied while reading fallback artwork: {FALLBACK_ARTWORK_IMAGE}")
    except Exception as exc:
        print(f"ERROR: Could not read fallback artwork image: {exc}")

    return None


def fallback_artwork_mime_type(path: Path) -> str:
    """Return the image MIME type to report for a configured fallback file."""
    suffix = path.suffix.casefold()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    return "image/png"


def parse_output_pixels(raw_pixels: str) -> Optional[int]:
    """Parse a requested square output size in pixels."""
    raw_pixels = raw_pixels.strip()
    if not raw_pixels:
        return DEFAULT_OUTPUT_PIXELS

    try:
        pixels = int(raw_pixels)
    except ValueError:
        print(f"ERROR: Output size must be a whole number, not: {raw_pixels}")
        return None

    if pixels < 1:
        print("ERROR: Output size must be at least 1 pixel.")
        return None

    return pixels


def prompt_for_output_pixels() -> int:
    """Ask for an optional square output size, defaulting when Enter is pressed."""
    while True:
        pixels = parse_output_pixels(input(f"Square size in pixels, or Enter for {DEFAULT_OUTPUT_PIXELS}: "))
        if pixels is not None:
            return pixels


def fit_image_to_square(image: Image.Image, output_pixels: int) -> Image.Image:
    """Return an exact square RGB image by center-cropping to fill the canvas."""
    output_size = (output_pixels, output_pixels)
    return ImageOps.fit(
        image,
        output_size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )


def save_artwork_as_jpeg(image_data: bytes, mime_type: str, output_path: Path, output_pixels: int) -> bool:
    """Open embedded artwork, resize it, and save it as a simple JPEG file."""
    output_size = (output_pixels, output_pixels)
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
        with Image.open(io.BytesIO(image_data)) as source_image:
            source_image.load()
            image_format = source_image.format or "unknown"
            print(f"Detected embedded artwork type: {mime_type} ({image_format})")

            # Make a plain 8-bit RGB image. JPEG avoids PNG alpha/palette/chunk
            # variants that some live visual tools can misread during reload.
            image = ImageOps.exif_transpose(source_image).convert("RGB")

            square_image = fit_image_to_square(image, output_pixels)
            square_image.save(
                temp_output_path,
                format="JPEG",
                quality=95,
                optimize=False,
                progressive=False,
                subsampling=0,
            )

        last_error: PermissionError | None = None
        for attempt in range(6):
            try:
                temp_output_path.replace(output_path)
                last_error = None
                break
            except PermissionError as exc:
                last_error = exc
                time.sleep(0.12 * (attempt + 1))
        if last_error is not None:
            raise last_error
        os.utime(output_path, None)
        with Image.open(output_path) as saved_image:
            saved_size = saved_image.size
            saved_mode = saved_image.mode
        if saved_size != output_size:
            print(f"WARNING: Saved image is {saved_size[0]}x{saved_size[1]}, expected {output_pixels}x{output_pixels}.")
        file_hash = hash_file(output_path)
        file_size = output_path.stat().st_size
        print(f"SUCCESS: Album artwork saved to: {output_path}")
        print(f"SUCCESS: Final image is {saved_size[0]}x{saved_size[1]} pixels, {saved_mode} mode.")
        print(f"SUCCESS: Wrote {file_size:,} bytes. SHA256: {file_hash[:12]}")
        return True
    except UnidentifiedImageError:
        print("ERROR: Embedded artwork data could not be opened as an image.")
    except PermissionError:
        print(f"ERROR: Permission denied while writing output file: {output_path}")
    except Exception as exc:
        print(f"ERROR: Could not save artwork as JPEG: {exc}")
    finally:
        try:
            if temp_output_path.exists():
                temp_output_path.unlink()
        except OSError:
            pass

    return False


def hash_file(path: Path) -> str:
    """Return a SHA256 hash for the saved artwork file."""
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def process_mp3(mp3_path: Path, output_pixels: int = DEFAULT_OUTPUT_PIXELS) -> bool:
    """Extract artwork from one MP3 and write it to the configured image path."""
    print(f"Reading MP3: {mp3_path}")
    print(f"Output square size: {output_pixels}x{output_pixels}")
    artwork = find_embedded_artwork(mp3_path)
    if artwork is None:
        print(f"Using fallback artwork: {FALLBACK_ARTWORK_IMAGE}")
        artwork = load_fallback_artwork()
        if artwork is None:
            return False

    image_data, mime_type = artwork
    return save_artwork_as_jpeg(image_data, mime_type, OUTPUT_IMAGE, output_pixels)


def main() -> int:
    """Update artwork from one command-line path or keep prompting interactively."""
    print("Album Artwork Extractor")
    print(f"Output file: {OUTPUT_IMAGE}")
    print()

    if len(sys.argv) > 1:
        mp3_path = normalize_mp3_path(sys.argv[1])
        if mp3_path is None or mp3_path == Path("__QUIT__"):
            return 1
        output_pixels = DEFAULT_OUTPUT_PIXELS
        if len(sys.argv) > 2:
            output_pixels = parse_output_pixels(sys.argv[2])
            if output_pixels is None:
                return 1
        return 0 if process_mp3(mp3_path, output_pixels) else 1

    print("Paste a new MP3 path whenever you want to update the current artwork.")
    print()

    while True:
        mp3_path = prompt_for_mp3_path()
        if mp3_path == Path("__QUIT__"):
            print("Goodbye.")
            return 0
        if mp3_path is None:
            print()
            continue

        output_pixels = prompt_for_output_pixels()
        process_mp3(mp3_path, output_pixels)
        print()


if __name__ == "__main__":
    sys.exit(main())
