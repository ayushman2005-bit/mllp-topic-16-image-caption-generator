"""Command-line entry point for generating a caption from one image."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps

from captioner import DEFAULT_MODEL_ID, caption_image, load_caption_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an English caption for an image with BLIP.")
    parser.add_argument("image", type=Path, help="Path to a JPG, PNG, or WebP image")
    parser.add_argument("--model", default=DEFAULT_MODEL_ID, help="Hugging Face model ID")
    parser.add_argument("--beams", type=int, default=3, help="Beam-search width (1 to 8)")
    args = parser.parse_args()

    if not args.image.is_file():
        parser.error(f"Image file not found: {args.image}")

    with Image.open(args.image) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")

    bundle = load_caption_model(args.model)
    print(caption_image(image, bundle, num_beams=args.beams))


if __name__ == "__main__":
    main()
