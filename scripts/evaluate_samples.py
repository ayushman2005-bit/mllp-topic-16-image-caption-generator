"""Run BLIP on the project's credited sample images and save observed results."""

from __future__ import annotations

import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
import transformers
from PIL import Image, ImageOps
import streamlit

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "data" / "sample_images"
OUTPUT = ROOT / "output" / "sample_results.json"
IMAGE_NAMES = ["dog_park.jpg", "cat_portrait.jpg", "bicycle_in_grass.jpg"]
sys.path.insert(0, str(ROOT))


def main() -> None:
    from captioner import DEFAULT_MODEL_ID, DEFAULT_MAX_NEW_TOKENS, DEFAULT_NUM_BEAMS
    from captioner import caption_image, load_caption_model

    bundle = load_caption_model(DEFAULT_MODEL_ID)
    results = []
    for name in IMAGE_NAMES:
        path = SAMPLES / name
        with Image.open(path) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
        started = time.perf_counter()
        caption = caption_image(image, bundle)
        elapsed = time.perf_counter() - started
        results.append(
            {
                "image": name,
                "caption": caption,
                "generation_seconds": round(elapsed, 3),
                "image_dimensions": list(image.size),
            }
        )

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": DEFAULT_MODEL_ID,
        "max_new_tokens": DEFAULT_MAX_NEW_TOKENS,
        "num_beams": DEFAULT_NUM_BEAMS,
        "device": str(bundle.device),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "streamlit": streamlit.__version__,
        "results": results,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
