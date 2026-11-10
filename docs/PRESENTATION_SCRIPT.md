# Presentation and demo recording script

Target length: 4 to 5 minutes. Replace the group-detail prompts with the students' own information before recording. Each member should describe their actual contribution in their own words.

## 1. Opening (20 seconds)

"We are Shourya Basu, Manit Kumar Sahu, Ayushman Mahapatra, and Shrutik Sinha. Our MLLP Topic 16 project generates a short English description for an uploaded image."

## 2. Problem and objective (35 seconds)

"Images are useful, but a text description makes visual content easier to search, review, and access. We built a small application that accepts an image and returns a caption using a pretrained vision-language model. The output is a draft description, so a person should review it before using it in a high-stakes setting."

## 3. Method and pipeline (50 seconds)

"The app checks the file, corrects its orientation, and converts it to RGB. The BLIP processor prepares the image for the model. BLIP encodes the image and generates caption tokens, which the app decodes and displays. The app can use a CUDA GPU when available and otherwise uses CPU. The first launch downloads model weights, then caches them for later runs."

## 4. Live demonstration (90 seconds)

1. Start the app with `streamlit run app.py`.
2. Upload one of the sample images from `data/sample_images/`.
3. Select **Generate caption** and wait for the first model download if the cache is empty.
4. Read the generated caption, device, and inference time aloud.
5. Download the caption text and show the output file.
6. Repeat with a second image that has different objects or activity.

## 5. Results and limitations (45 seconds)

"We reviewed the model's outputs on representative images. It usually gives a short sentence about the main objects and activity, but can miss small details, confuse similar objects, or add an unsupported detail. Our evaluation is qualitative, so we do not claim a measured benchmark score."

## 6. Contributions and close (30 seconds)

Each member: state the actual work completed and point to the relevant files or demo step. Close with: "The prototype runs locally, uses an open pretrained model, and can be extended with a larger evaluation set, multilingual captions, or user-reviewed accessibility descriptions."
