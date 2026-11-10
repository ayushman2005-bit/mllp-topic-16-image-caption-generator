# Image Caption Generator (MLLP Topic 16)

A local Streamlit app that accepts a JPG, PNG, or WebP image and generates a short English caption with Salesforce BLIP. The app runs on CPU or CUDA-capable GPUs and does not require an API key.

## Project team

| Member | Roll number | Contribution |
|---|---|---|
| Shourya Basu | 2330400-Basu | To be added by the group |
| Manit Kumar Sahu | 2430605-Manit | To be added by the group |
| Ayushman Mahapatra | 2330020-Ayushman | To be added by the group |
| Shrutik Sinha | 2330404-Shrutik | To be added by the group |

**Before submitting:** fill in each member's actual contribution in this table and in `docs/GROUP_DETAILS.md`.

## Run the application

The first launch downloads the model weights (about 1 GB) from Hugging Face. Keep an internet connection for that first launch. Later launches use the local Transformers cache.

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks virtual-environment activation, call Streamlit directly:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local address printed in the terminal, upload an image, and select **Generate caption**. The model cache and uploaded image are not stored in this repository. The app keeps the upload in memory during the current session.

## Command-line use

```powershell
python caption_image.py data/sample_images/dog_park.jpg
```

Use `--beams 1` for faster output or a larger value (up to 8) for a wider deterministic beam search. The default is 3.

## Processing pipeline

```mermaid
flowchart LR
    A[Upload image] --> B[Validate file, size, and dimensions]
    B --> C[Correct orientation and convert to RGB]
    C --> D[BLIP image processor]
    D --> E[Vision encoder]
    E --> F[Text decoder and beam search]
    F --> G[Caption, device, time, and TXT download]
```

The app accepts files up to 10 MB and 25 megapixels. It does not write uploaded images to disk. BLIP downloads the pretrained model on first use and reuses the cached weights later.

## Files

- `app.py` — Streamlit interface and upload validation
- `captioner.py` — shared BLIP loading and inference code
- `caption_image.py` — command-line entry point
- `docs/` — methodology, group details, results, and presentation script
- `data/sample_images/` — sample inputs and their source credits
- `output/pdf/MLLP_Topic16_Project_Report.pdf` — project report
- `output/presentation/` — editable presentation slides and recording script
- `output/video/` — presentation demonstration recording

The project report, presentation, and private GitHub repository are prepared. Before submission, the group still needs to add actual contribution statements, give the instructor access to the private repository, and record the video.

## Model and tools

- **Captioning model:** [`Salesforce/blip-image-captioning-base`](https://huggingface.co/Salesforce/blip-image-captioning-base)
- **Framework:** PyTorch and Hugging Face Transformers
- **UI:** Streamlit
- **Image handling:** Pillow

The model card describes this checkpoint as a BLIP base model pretrained for image captioning on COCO. The app runs inference only and does not fine-tune model weights. Review the model card and license before using the checkpoint outside this classroom project.

## Results and evaluation

The report and [`docs/RESULTS.md`](docs/RESULTS.md) list the generated captions and inference times for the included sample images. To reproduce the local sample run, execute `python scripts/evaluate_samples.py`. Evaluation is a small qualitative review of whether the caption identifies the main subject and scene. It is not a benchmark score and should not be treated as statistical validation.

## Limitations

- Captions are English and are usually one short sentence.
- The model can miss small objects or relations, confuse similar objects, or add details that are not visible.
- First-run model download needs internet and substantial disk space. CPU inference can take longer than GPU inference.
- The app is a prototype. Review captions before using them for accessibility, safety, or other consequential purposes.

## References

1. J. Li, D. Li, C. Xiong, and S. Hoi. “BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation.” 2022. [arXiv:2201.12086](https://arxiv.org/abs/2201.12086).
2. Salesforce AI Research. [BLIP image-captioning model card](https://huggingface.co/Salesforce/blip-image-captioning-base).
3. Hugging Face. [Transformers image-captioning task guide](https://huggingface.co/docs/transformers/main/tasks/image_captioning).
4. Streamlit. [File uploader](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader) and [resource caching](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource) documentation.
5. Sample-image credits are listed in [`data/sample_images/README.md`](data/sample_images/README.md).

## Repository URL

Private repository: [ayushman2005-bit/mllp-topic-16-image-caption-generator](https://github.com/ayushman2005-bit/mllp-topic-16-image-caption-generator)
