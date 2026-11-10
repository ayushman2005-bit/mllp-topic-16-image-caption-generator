# Processing pipeline

```mermaid
flowchart LR
    A[User selects JPG, PNG, or WebP] --> B[Validate size and decode]
    B --> C[Apply EXIF orientation and convert to RGB]
    C --> D[BLIP processor resizes and normalizes image]
    D --> E[Pretrained BLIP vision encoder]
    E --> F[Text decoder generates caption]
    F --> G[Show caption and offer text download]
```

The app keeps the uploaded image in memory and does not write it to disk. On the first run, the pretrained model files download from Hugging Face and are cached by the Transformers library for later runs.
