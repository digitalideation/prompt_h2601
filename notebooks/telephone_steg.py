"""Small RGB least-significant-bit envelope. Concealment, not encryption."""
import hashlib
import io
import json
import struct

from PIL import Image

MAGIC = b"H26TEL01"
HEADER = 44  # magic (8), length (4), SHA-256 (32)
MAX_PAYLOAD = 65536


def validate(record):
    from telephone_helpers import route
    if not isinstance(record, dict) or record.get("schema") != 1:
        raise ValueError("Unknown Telephone record format.")
    expected = route(record.get("group"), record.get("seat"), record.get("round"))
    if any(record.get(key) != value for key, value in expected.items()):
        raise ValueError("Inconsistent route in hidden record.")
    if record.get("mode") not in ("live", "practice"):
        raise ValueError("Unknown mode in hidden record.")
    if not isinstance(record.get("prompt"), str) or not record["prompt"].strip():
        raise ValueError("Missing prompt in hidden record.")
    if not isinstance(record.get("session"), str) or not record["session"]:
        raise ValueError("Missing session in hidden record.")
    return record


def encode(image_bytes, record):
    from telephone_helpers import clean_png
    # Explicit allowlist excludes local paths, tokens and widget state.
    keys = ("group", "seat", "round", "folder", "incoming", "outgoing", "send_to",
            "prompt", "model", "model_version", "settings", "mode", "session",
            "prediction_id", "recorded_at_utc", "observation", "source_filename")
    safe = {key: record.get(key) for key in keys}
    safe["session"] = safe["session"] or "legacy"
    safe["schema"] = 1
    validate(safe)
    payload = json.dumps(safe, ensure_ascii=False, sort_keys=True).encode("utf-8")
    if len(payload) > MAX_PAYLOAD:
        raise ValueError("Prompt record too large to hide. Shorten it before generating.")
    envelope = MAGIC + struct.pack(">I", len(payload)) + hashlib.sha256(payload).digest() + payload
    with Image.open(io.BytesIO(clean_png(image_bytes))) as image:
        pixels = bytearray(image.tobytes())
        if len(envelope) * 8 > len(pixels):
            raise ValueError("Image too small to hold this prompt record.")
        for i, byte in enumerate(envelope):
            for bit in range(8):
                index = i * 8 + bit
                pixels[index] = (pixels[index] & 254) | ((byte >> (7 - bit)) & 1)
        result = Image.frombytes("RGB", image.size, bytes(pixels))
        output = io.BytesIO()
        result.save(output, format="PNG")
        return output.getvalue()


def decode(data):
    if len(data) > 20 * 1024 * 1024:
        raise ValueError("Image exceeds 20 MB.")
    with Image.open(io.BytesIO(data)) as image:
        if image.format != "PNG" or image.mode != "RGB" or image.width * image.height > 16_000_000:
            raise ValueError("Use the original RGB PNG exported by Telephone.")
        pixels = image.tobytes()
    def read_bytes(count):
        if count * 8 > len(pixels):
            raise ValueError("Truncated hidden record.")
        return bytes(sum((pixels[i * 8 + bit] & 1) << (7 - bit) for bit in range(8))
                     for i in range(count))
    header = read_bytes(HEADER)
    if header[:8] != MAGIC:
        raise ValueError("No Telephone record found. Use the original exported PNG.")
    length = struct.unpack(">I", header[8:12])[0]
    if not 0 < length <= MAX_PAYLOAD:
        raise ValueError("Invalid hidden record length.")
    payload = read_bytes(HEADER + length)[HEADER:]
    if hashlib.sha256(payload).digest() != header[12:]:
        raise ValueError("Hidden record damaged, possibly by image editing.")
    return validate(json.loads(payload.decode("utf-8")))
