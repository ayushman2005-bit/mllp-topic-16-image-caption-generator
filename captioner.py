"""BLIP image captioning inference code shared by the web app and CLI."""

from __future__ import annotations

import threading
from dataclasses import dataclass

import torch
from PIL import Image
from transformers import AutoModelForMultimodalLM, AutoProcessor

DEFAULT_MODEL_ID = "Salesforce/blip-image-captioning-base"
DEFAULT_MAX_NEW_TOKENS = 32
DEFAULT_NUM_BEAMS = 3

_GENERATION_LOCK = threading.Lock()


@dataclass(frozen=True)
class CaptionModel:
    processor: object
    model: object
    device: torch.device
    model_id: str


def load_caption_model(model_id: str = DEFAULT_MODEL_ID) -> CaptionModel:
    """Download (on first use), load, and prepare the pretrained BLIP model."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForMultimodalLM.from_pretrained(model_id)
    model.to(device)
    model.eval()
    return CaptionModel(processor, model, device, model_id)


def caption_image(
    image: Image.Image,
    bundle: CaptionModel,
    *,
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
    num_beams: int = DEFAULT_NUM_BEAMS,
) -> str:
    """Generate one caption from a PIL image using deterministic beam search."""
    if not 1 <= max_new_tokens <= 64:
        raise ValueError("max_new_tokens must be between 1 and 64.")
    if not 1 <= num_beams <= 8:
        raise ValueError("num_beams must be between 1 and 8.")

    rgb_image = image.convert("RGB")
    inputs = bundle.processor(images=rgb_image, return_tensors="pt")
    inputs = {key: value.to(bundle.device) for key, value in inputs.items()}

    # Serialize generation to avoid concurrent requests competing for CPU/GPU memory.
    with _GENERATION_LOCK, torch.inference_mode():
        output_ids = bundle.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            num_beams=num_beams,
        )

    caption = bundle.processor.batch_decode(output_ids, skip_special_tokens=True)[0]
    caption = " ".join(caption.strip().split())
    if not caption:
        raise RuntimeError("The model returned an empty caption.")
    return caption
