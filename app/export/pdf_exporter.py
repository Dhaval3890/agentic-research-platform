from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from datetime import datetime


def export_proposal_to_pdf(
    proposal_text: str,
    output_path: str,
    client_name: str
):
    """
    Converts proposal text into a professional PDF.
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        name="HeadingStyle",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        name="BodyStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        spaceAfter=10
    )

    elements = []

    # 🟣 COVER PAGE
    elements.append(Spacer(1, 2 * inch))
    elements.append(Paragraph("Market Research Proposal", title_style))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"<b>Client:</b> {client_name}", body_style))
    elements.append(Paragraph(
        f"<b>Date:</b> {datetime.today().strftime('%d %B %Y')}",
        body_style
    ))
    elements.append(PageBreak())

    # 🟣 CONTENT PAGES
    lines = proposal_text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            elements.append(Spacer(1, 8))
            continue

        if line.startswith("# "):
            elements.append(
                Paragraph(line.replace("# ", ""), heading_style)
            )
        elif line.startswith("## "):
            elements.append(
                Paragraph(line.replace("## ", ""), heading_style)
            )
        else:
            elements.append(Paragraph(line, body_style))

    doc.build(elements)

    return output_path
