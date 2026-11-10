"""Streamlit interface for the MLLP image captioning assignment."""

from __future__ import annotations

import io
import time

import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

from captioner import DEFAULT_MODEL_ID, caption_image, load_caption_model

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 25_000_000
ALLOWED_TYPES = ["jpg", "jpeg", "png", "webp"]


@st.cache_resource(show_spinner="Loading the BLIP model (first load downloads about 1 GB)...")
def get_model(model_id: str = DEFAULT_MODEL_ID):
    return load_caption_model(model_id)


def prepare_image(data: bytes) -> Image.Image:
    """Validate an uploaded image and return an EXIF-corrected RGB copy."""
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValueError("The image exceeds the 10 MB upload limit.")

    try:
        with Image.open(io.BytesIO(data)) as source:
            width, height = source.size
            if width <= 0 or height <= 0 or width * height > MAX_IMAGE_PIXELS:
                raise ValueError("The image is too large. Maximum dimensions are 25 megapixels.")
            source.verify()
        with Image.open(io.BytesIO(data)) as source:
            return ImageOps.exif_transpose(source).convert("RGB")
    except UnidentifiedImageError as exc:
        raise ValueError("This file is not a supported image. Try JPG, PNG, or WebP.") from exc
    except OSError as exc:
        raise ValueError("The image could not be decoded. Please try another file.") from exc


def main() -> None:
    st.set_page_config(
        page_title="Image Caption Generator | MLLP Topic 16",
        page_icon="🖼️",
        layout="centered",
    )
    st.title("Image Caption Generator")
    st.caption("MLLP experiential learning project · Topic 16 · BLIP")
    st.write(
        "Upload a photo to generate a short English description. The image is processed in memory; "
        "the app does not save uploaded images."
    )

    uploaded = st.file_uploader(
        "Choose an image",
        type=ALLOWED_TYPES,
        max_upload_size=10,
        help="JPG, PNG, or WebP. Maximum size: 10 MB.",
    )

    if uploaded is None:
        st.info("Choose an image, then select **Generate caption**.")
        with st.expander("How it works"):
            st.write(
                "BLIP converts the image into visual features, then generates an English caption. "
                "The pretrained model is downloaded from Hugging Face the first time the app runs."
            )
        return

    try:
        image = prepare_image(uploaded.getvalue())
    except ValueError as exc:
        st.error(str(exc))
        return

    st.image(image, caption=f"Uploaded image: {uploaded.name}", use_container_width=True)
    if st.button("Generate caption", type="primary", use_container_width=True):
        try:
            with st.spinner("Generating a caption..."):
                bundle = get_model(DEFAULT_MODEL_ID)
                started = time.perf_counter()
                result = caption_image(image, bundle)
                elapsed = time.perf_counter() - started
            st.subheader("Generated description")
            st.success(result)
            st.caption(
                f"Model: `{DEFAULT_MODEL_ID}` · Device: `{bundle.device}` · "
                f"Generation time: {elapsed:.2f} seconds"
            )
            st.download_button(
                "Download caption as text",
                data=result + "\n",
                file_name="image_caption.txt",
                mime="text/plain",
            )
            st.caption(
                "Captions can omit details or describe them incorrectly. Review the result before relying on it."
            )
        except Exception as exc:  # show a useful setup error without exposing a traceback in the UI
            st.error(
                "Caption generation failed. Check the installation and internet connection for the first "
                "model download, then see README.md for troubleshooting."
            )
            st.caption(f"Details: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
