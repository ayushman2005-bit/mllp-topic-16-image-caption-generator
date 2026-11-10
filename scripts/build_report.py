"""Generate the MLLP Topic 16 project report as a polished A4 PDF."""

from __future__ import annotations

from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "MLLP_Topic16_Project_Report.pdf"
PAGE_W, PAGE_H = A4
MARGIN_X = 0.68 * inch
MARGIN_BOTTOM = 0.58 * inch
BODY_TOP = PAGE_H - 0.73 * inch
BODY_HEIGHT = BODY_TOP - MARGIN_BOTTOM
CONTENT_W = PAGE_W - 2 * MARGIN_X

NAVY = colors.HexColor("#11263D")
BLUE = colors.HexColor("#1C5B7A")
TEAL = colors.HexColor("#0F766E")
PALE = colors.HexColor("#EDF5F6")
PALE_BLUE = colors.HexColor("#EEF3F8")
INK = colors.HexColor("#1D2935")
MUTED = colors.HexColor("#536271")
RULE = colors.HexColor("#D8E1E8")
WHITE = colors.white


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover_kicker": ParagraphStyle(
            "cover_kicker", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9,
            leading=12, textColor=colors.HexColor("#9AE6D0"), spaceAfter=12,
        ),
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=29,
            leading=34, textColor=WHITE, alignment=TA_LEFT, spaceAfter=7,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle", parent=base["Normal"], fontName="Helvetica", fontSize=13,
            leading=18, textColor=colors.HexColor("#DCE8F2"), spaceAfter=6,
        ),
        "title": ParagraphStyle(
            "title", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=21,
            leading=25, textColor=NAVY, spaceBefore=5, spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=15,
            leading=19, textColor=NAVY, spaceBefore=9, spaceAfter=6, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11,
            leading=14, textColor=BLUE, spaceBefore=7, spaceAfter=4, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2,
            leading=13.4, textColor=INK, spaceAfter=6,
        ),
        "body_small": ParagraphStyle(
            "body_small", parent=base["BodyText"], fontName="Helvetica", fontSize=8.1,
            leading=10.7, textColor=INK, spaceAfter=3,
        ),
        "table_head": ParagraphStyle(
            "table_head", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8.3,
            leading=10.2, textColor=WHITE,
        ),
        "table_cell": ParagraphStyle(
            "table_cell", parent=base["Normal"], fontName="Helvetica", fontSize=8.2,
            leading=10.8, textColor=INK,
        ),
        "callout": ParagraphStyle(
            "callout", parent=base["BodyText"], fontName="Helvetica", fontSize=9,
            leading=13, textColor=NAVY, spaceAfter=0,
        ),
        "caption": ParagraphStyle(
            "caption", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=7.8,
            leading=10, textColor=MUTED, alignment=TA_CENTER,
        ),
        "reference": ParagraphStyle(
            "reference", parent=base["BodyText"], fontName="Helvetica", fontSize=8.1,
            leading=11.5, textColor=INK, leftIndent=15, firstLineIndent=-15, spaceAfter=5,
        ),
    }


class Pipeline(Spacer):
    """Editable-in-report vector pipeline diagram."""

    def __init__(self, width: float, height: float = 82):
        super().__init__(width, height)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        labels = [
            "Image\nupload",
            "File checks\n+ RGB",
            "BLIP image\nprocessor",
            "Vision\nencoder",
            "Text\ndecoder",
            "Caption\n+ download",
        ]
        n = len(labels)
        gap = 12
        box_w = (self.width - (n - 1) * gap) / n
        box_h = 43
        y = 21
        for i, label in enumerate(labels):
            x = i * (box_w + gap)
            c.setFillColor(PALE if i < n - 1 else colors.HexColor("#DDF2EA"))
            c.setStrokeColor(RULE)
            c.roundRect(x, y, box_w, box_h, 5, fill=1, stroke=1)
            c.setFillColor(NAVY if i < n - 1 else TEAL)
            c.setFont("Helvetica-Bold", 7.5)
            rows = label.split("\n")
            row_h = 10
            start_y = y + (box_h + (len(rows) - 1) * row_h) / 2 - 2.5
            for j, row in enumerate(rows):
                c.drawCentredString(x + box_w / 2, start_y - j * row_h, row)
            if i < n - 1:
                mid_y = y + box_h / 2
                x1 = x + box_w + 2
                x2 = x + box_w + gap - 2
                c.setStrokeColor(TEAL)
                c.setLineWidth(1.3)
                c.line(x1, mid_y, x2, mid_y)
                c.line(x2 - 4, mid_y + 3, x2, mid_y)
                c.line(x2 - 4, mid_y - 3, x2, mid_y)


def image_flowable(path: Path, max_width: float, max_height: float) -> Image:
    thumb_dir = ROOT / "tmp" / "pdfs" / "report_thumbnails"
    thumb_dir.mkdir(parents=True, exist_ok=True)
    thumb_path = thumb_dir / f"{path.stem}_thumb.jpg"
    with PILImage.open(path) as source:
        image = source.convert("RGB")
        image.thumbnail((900, 700), PILImage.Resampling.LANCZOS)
        image.save(thumb_path, format="JPEG", quality=88, optimize=True)
        image_w, image_h = image.size
    factor = min(max_width / image_w, max_height / image_h)
    return Image(str(thumb_path), width=image_w * factor, height=image_h * factor)


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 2.2 * inch, PAGE_W, 2.2 * inch, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 2.27 * inch, PAGE_W, 0.07 * inch, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN_X, 0.35 * inch, "MLLP GROUP ASSIGNMENT  |  TOPIC 16  |  SUBMISSION DEADLINE: 12 NOVEMBER 2026")
    canvas.restoreState()


def draw_body(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN_X, PAGE_H - 0.53 * inch, PAGE_W - MARGIN_X, PAGE_H - 0.53 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica-Bold", 7.4)
    canvas.drawString(MARGIN_X, PAGE_H - 0.42 * inch, "MLLP  |  IMAGE-TO-TEXT DESCRIPTION GENERATION")
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARGIN_X, 0.34 * inch, "Project report  |  Topic 16")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.34 * inch, f"Page {doc.page}")
    canvas.restoreState()


def make_story(s: dict[str, ParagraphStyle]):
    story = []

    story += [
        Paragraph("MLLP EXPERIENTIAL LEARNING GROUP ASSIGNMENT", s["cover_kicker"]),
        Paragraph("Image Caption Generator", s["cover_title"]),
        Paragraph("Image-to-text description generation using BLIP", s["cover_subtitle"]),
        Paragraph("Project Report  |  Topic 16", s["cover_subtitle"]),
        Spacer(1, 0.68 * inch),
    ]

    group_rows = [
        [Paragraph("GROUP MEMBER", s["table_head"]), Paragraph("ROLL NUMBER", s["table_head"]), Paragraph("CONTRIBUTION", s["table_head"])],
        [Paragraph("Shourya Basu", s["table_cell"]), Paragraph("2330400-Basu", s["table_cell"]), Paragraph("To be added by the group", s["table_cell"])],
        [Paragraph("Manit Kumar Sahu", s["table_cell"]), Paragraph("2430605-Manit", s["table_cell"]), Paragraph("To be added by the group", s["table_cell"])],
        [Paragraph("Ayushman Mahapatra", s["table_cell"]), Paragraph("2330020-Ayushman", s["table_cell"]), Paragraph("To be added by the group", s["table_cell"])],
        [Paragraph("Shrutik Sinha", s["table_cell"]), Paragraph("2330404-Shrutik", s["table_cell"]), Paragraph("To be added by the group", s["table_cell"])],
    ]
    group_table = Table(group_rows, colWidths=[1.55 * inch, 1.52 * inch, CONTENT_W - 3.07 * inch], repeatRows=1)
    group_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story += [
        Paragraph("Group details", s["h2"]), group_table, Spacer(1, 10),
        Paragraph("Submission date: 10 November 2026", s["body"]),
        Paragraph("The group supplied the member names and roll numbers. Each member's actual contribution is left for the group to complete.", s["body_small"]),
        NextPageTemplate("Body"), PageBreak(),
    ]

    story += [
        Paragraph("Project overview", s["title"]),
        Paragraph(
            "This project implements a local application that accepts an image and generates a short English description with the pretrained BLIP image-captioning model. The Streamlit interface validates the upload, prepares the image, runs inference, displays the generated caption, and lets the user download it as text. The prototype uses the model as released and does not fine-tune it.",
            s["body"],
        ),
        Paragraph(
            "The included sample run shows both useful summaries and a clear model error. BLIP described the cat and bicycle images in broad terms, while it misidentified a dog sculpture at a park entrance as a cat. This illustrates why a generated caption needs human review.",
            s["body"],
        ),
        Paragraph("1. Problem statement and objectives", s["h1"]),
        Paragraph(
            "Images communicate visual information, but people and applications often need a short text description for access, search, or cataloguing. The project task is to map one image to one natural-language caption using an image-captioning model.",
            s["body"],
        ),
        Paragraph("Objectives", s["h2"]),
        Paragraph(
            "- Accept common image formats through a simple interface.<br/>"
            "- Check file type, size, dimensions, and image decoding before inference.<br/>"
            "- Convert the image to the format expected by BLIP and generate a caption.<br/>"
            "- Display the caption and offer a text download.<br/>"
            "- Record representative outputs and describe limitations honestly.",
            s["body"],
        ),
        Paragraph("Expected outcome", s["h2"]),
        Paragraph(
            "A working local prototype that gives a concise description of the main visible subject or scene. The caption is an aid to review, not a guaranteed factual record of every image detail.",
            s["body"],
        ),
        Paragraph("2. Proposed methodology and processing pipeline", s["h1"]),
        Paragraph(
            "The app keeps the uploaded image in memory. It applies EXIF orientation correction, converts pixels to RGB, and passes the image to the Hugging Face BLIP processor. The processor prepares pixel values for the visual encoder. The decoder generates token IDs with beam search. The app decodes those tokens into a caption and shows the result.",
            s["body"],
        ),
        Pipeline(CONTENT_W),
        Paragraph("Figure 1. Processing pipeline from upload to caption output.", s["caption"]),
        Spacer(1, 6),
        Paragraph(
            "Configuration: `Salesforce/blip-image-captioning-base`, `num_beams=3`, and `max_new_tokens=32`. The model is loaded once and cached by Streamlit. The app uses CUDA when PyTorch detects a CUDA device; this sample evaluation ran on CPU.",
            s["body"],
        ),
        Paragraph("3. Models and tools used", s["h1"]),
    ]

    model_rows = [
        [Paragraph("Component", s["table_head"]), Paragraph("Use in the project", s["table_head"])],
        [Paragraph("BLIP base image captioning model", s["table_cell"]), Paragraph("Pretrained vision-language checkpoint generates captions from images. Model ID: Salesforce/blip-image-captioning-base [1, 2].", s["table_cell"])],
        [Paragraph("Hugging Face Transformers", s["table_cell"]), Paragraph("Loads the processor and model from the Hugging Face Hub and runs text generation [3].", s["table_cell"])],
        [Paragraph("PyTorch", s["table_cell"]), Paragraph("Tensor operations, model inference, and CPU/GPU device selection.", s["table_cell"])],
        [Paragraph("Streamlit", s["table_cell"]), Paragraph("Browser-based upload interface and cached model resource [4].", s["table_cell"])],
        [Paragraph("Pillow", s["table_cell"]), Paragraph("Image decoding, EXIF orientation, and RGB conversion.", s["table_cell"])],
    ]
    model_table = Table(model_rows, colWidths=[1.75 * inch, CONTENT_W - 1.75 * inch], repeatRows=1)
    model_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [
        model_table,
        Spacer(1, 6),
        Paragraph(
            "The model card describes this checkpoint as a BLIP base model for image captioning, pretrained on COCO, and identifies a BSD-3-Clause license. This project performs inference only and does not train on COCO or another dataset [2].",
            s["body"],
        ),
        Paragraph("4. Implementation and usability", s["h1"]),
        Paragraph(
            "The project is implemented in Python 3.11 with a Streamlit interface. Uploaded files are limited to JPG, PNG, and WebP, 10 MB, and 25 megapixels. Invalid or oversized images are rejected. The app does not write the upload to disk. On first use, Transformers downloads the model from Hugging Face; subsequent runs reuse the local model cache.",
            s["body"],
        ),
        Paragraph("Run instructions", s["h2"]),
        Paragraph(
            "1. Create and activate a Python virtual environment.<br/>"
            "2. Install dependencies with `python -m pip install -r requirements.txt`.<br/>"
            "3. Start the app with `streamlit run app.py`.<br/>"
            "4. Open the local address shown in the terminal, upload an image, and select `Generate caption`.<br/>"
            "5. Use `python caption_image.py path/to/image.jpg` for the command-line interface.",
            s["body"],
        ),
        Paragraph("Practical uses", s["h2"]),
        Paragraph(
            "The prototype can assist with draft alt text, photo organization, and searchable image collections. A person should review each caption, especially when accuracy matters.",
            s["body"],
        ),
    ]

    story += [
        PageBreak(),
        Paragraph("5. Results and sample outputs", s["h1"]),
        Paragraph(
            "The model was run on three CC0 sample images included in the repository. The output below is verbatim from the local CPU run. Inference time includes processor and generation work after model loading; it excludes model loading and the initial download.",
            s["body"],
        ),
    ]

    outputs = [
        ("dog_park.jpg", "a gate with a cat sitting on top of it", "The model noticed the entrance but called an animal sculpture a cat and missed that it is a dog park."),
        ("cat_portrait.jpg", "a small white cat standing in a pile of wood", "The model identified the main subject and described the surrounding wood."),
        ("bicycle_in_grass.jpg", "a bike is laying in the middle of a garden", "The model identified the bicycle and greenery but did not mention that the bicycle is partly hidden."),
    ]
    result_rows = []
    for filename, caption, observation in outputs:
        image_path = ROOT / "data" / "sample_images" / filename
        thumb = image_flowable(image_path, 1.62 * inch, 1.10 * inch)
        result_cell = [
            Paragraph(f"<b>{filename}</b>", s["body_small"]),
            Paragraph(f"<b>Caption:</b> {caption}", s["body_small"]),
            Paragraph(f"<b>Observation:</b> {observation}", s["body_small"]),
        ]
        result_rows.append([thumb, result_cell])
    results_table = Table(result_rows, colWidths=[1.85 * inch, CONTENT_W - 1.85 * inch])
    results_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, PALE_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [
        KeepTogether([results_table]),
        Spacer(1, 5),
        Paragraph(
            "Evaluation protocol: inspect whether each caption identifies the main subject and scene. This is a qualitative review of three images, not a statistically representative test set. No BLEU, CIDEr, or other benchmark score is claimed.",
            s["body_small"],
        ),
        Paragraph("Evaluation environment", s["h2"]),
    ]

    env_rows = [
        [Paragraph("Setting", s["table_head"]), Paragraph("Observed value", s["table_head"])],
        [Paragraph("Python / PyTorch", s["table_cell"]), Paragraph("3.11.9 / 2.14.0+cpu", s["table_cell"])],
        [Paragraph("Transformers / Streamlit", s["table_cell"]), Paragraph("5.22.2 / 1.67.0", s["table_cell"])],
        [Paragraph("Device", s["table_cell"]), Paragraph("CPU, no CUDA GPU detected", s["table_cell"])],
        [Paragraph("Generation times", s["table_cell"]), Paragraph("Dog park 2.222 s; cat 2.367 s; bicycle 2.472 s", s["table_cell"])],
    ]
    env_table = Table(env_rows, colWidths=[1.65 * inch, CONTENT_W - 1.65 * inch], repeatRows=1)
    env_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [
        env_table,
        PageBreak(),
        Paragraph("6. Limitations", s["h1"]),
        Paragraph(
            "- The checkpoint generates English captions and may miss small or obscured objects.<br/>"
            "- It can confuse similar objects or describe a sculpture as a real animal, as the dog-park example shows.<br/>"
            "- It can omit relations or add details that are not visible. The model provides no calibrated confidence score in this interface.<br/>"
            "- The first run needs an internet connection and about 1 GB of model weights. CPU generation is slower than GPU generation on many computers.<br/>"
            "- Three manually reviewed images cannot establish broad accuracy or fairness across scenes and people.",
            s["body"],
        ),
        Paragraph("7. Conclusion and future scope", s["h1"]),
        Paragraph(
            "The prototype completes the image-to-caption pipeline with a pretrained BLIP model, upload validation, CPU/GPU selection, caption display, and text download. The examples show that the model can summarize a clear subject while still making an object-level error in a complex scene.",
            s["body"],
        ),
        Paragraph(
            "Future work could evaluate a larger image set with human reference captions, report standard captioning metrics, add multilingual output, improve review controls, and collect user feedback. These extensions need their own data and evaluation plan.",
            s["body"],
        ),
        Paragraph("Presentation and repository handoff", s["h2"]),
        Paragraph(
            "The editable slides and a 4 to 5 minute recording script are included in the project folder. The group still needs to record the presentation, state each member's actual contribution, and add the video or an accessible video link to the repository.",
            s["body"],
        ),
        Paragraph("8. References and repository link", s["h1"]),
        Paragraph("[1] J. Li, D. Li, C. Xiong, and S. Hoi, &quot;BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation,&quot; 2022. <link href=\"https://arxiv.org/abs/2201.12086\" color=\"#1C5B7A\">arXiv:2201.12086</link>.", s["reference"]),
        Paragraph("[2] Salesforce AI Research, <link href=\"https://huggingface.co/Salesforce/blip-image-captioning-base\" color=\"#1C5B7A\">BLIP image-captioning model card</link>, accessed 10 November 2026.", s["reference"]),
        Paragraph("[3] Hugging Face, <link href=\"https://huggingface.co/docs/transformers/main/tasks/image_captioning\" color=\"#1C5B7A\">Transformers image-captioning task guide</link>, accessed 10 November 2026.", s["reference"]),
        Paragraph("[4] Streamlit, <link href=\"https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader\" color=\"#1C5B7A\">file uploader</link> and <link href=\"https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource\" color=\"#1C5B7A\">resource caching</link> documentation, accessed 10 November 2026.", s["reference"]),
        Paragraph("[5] Sample images are from Wikimedia Commons. Each contributor released the corresponding image under <link href=\"https://creativecommons.org/publicdomain/zero/1.0/\" color=\"#1C5B7A\">CC0 1.0</link>. File pages: <link href=\"https://commons.wikimedia.org/wiki/File:Dog_park.jpg\" color=\"#1C5B7A\">dog park</link>, <link href=\"https://commons.wikimedia.org/wiki/File:Gato_dom%C3%A9stico_(Felis_silvestris_catus).jpg\" color=\"#1C5B7A\">cat</link>, and <link href=\"https://commons.wikimedia.org/wiki/File:A_shared_bicycle_in_the_grass.jpg\" color=\"#1C5B7A\">bicycle</link>. Contributor names are listed in the sample-image credits.", s["reference"]),
        Spacer(1, 4),
        Paragraph("GitHub repository URL: To be added after the group publishes the repository.", s["body_small"]),
    ]
    return story


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles_map = styles()
    cover_frame = Frame(MARGIN_X, MARGIN_BOTTOM, CONTENT_W, PAGE_H - MARGIN_BOTTOM - 0.35 * inch, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    body_frame = Frame(MARGIN_X, MARGIN_BOTTOM, CONTENT_W, BODY_HEIGHT, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, title="Image Caption Generator - MLLP Topic 16 Project Report",
        author="MLLP Topic 16 group", leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=0.78 * inch, bottomMargin=MARGIN_BOTTOM,
    )
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_cover),
        PageTemplate(id="Body", frames=[body_frame], onPage=draw_body),
    ])
    doc.build(make_story(styles_map))
    print(OUTPUT)


if __name__ == "__main__":
    main()
