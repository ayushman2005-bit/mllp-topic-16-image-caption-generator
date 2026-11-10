# Sample results

Results are generated locally by `caption_image.py` with model `Salesforce/blip-image-captioning-base`, `num_beams=3`, and `max_new_tokens=32`. Inference time is measured around generation only, after the model has loaded. Times depend on the computer and are not comparable across devices.

| Input image | Generated caption | Generation time (CPU) | Qualitative observation |
|---|---|---:|---|
| `dog_park.jpg` | “a gate with a cat sitting on top of it” | 2.222 s | It noticed the entrance and a sculpture but called the animal sculpture a cat and missed that it is a dog park. |
| `cat_portrait.jpg` | “a small white cat standing in a pile of wood” | 2.367 s | It identified the main subject and described the surrounding wood. |
| `bicycle_in_grass.jpg` | “a bike is laying in the middle of a garden” | 2.472 s | It identified the bicycle and greenery, but omitted that the bicycle is partly hidden. |

These times were measured on a Windows CPU run using Python 3.11.9, PyTorch 2.14.0+cpu, and Transformers 5.22.2. Timing covers the processor and generation call, after model loading, and excludes initial download and model loading. This is a three-image qualitative review, not a statistically representative test set. We do not claim BLEU, CIDEr, or another benchmark metric because this project does not compare outputs with a sufficiently large set of human reference captions.
