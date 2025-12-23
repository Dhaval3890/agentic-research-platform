from fpdf import FPDF
import streamlit as st


def clean_for_pdf(text: str) -> str:
    """
    Cleans text so FPDF (latin-1) never crashes.
    """
    if not text:
        return ""

    return (
        text
        .replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
        .replace("…", "...")
        .encode("latin-1", "ignore")
        .decode("latin-1")
    )


def generate_proposal_pdf(
    recommendation: str,
    proposal: str,
    filename: str = "research_proposal.pdf"
):
    """
    Generates a PDF and exposes a Streamlit download button.
    """

    rec_text = clean_for_pdf(recommendation)
    prop_text = clean_for_pdf(proposal)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    pdf.multi_cell(
        0,
        8,
        f"""RECOMMENDED RESEARCH APPROACH

{rec_text}

--------------------------------------------------

DRAFT PROPOSAL

{prop_text}
"""
    )

    pdf_bytes = pdf.output(dest="S")

    st.download_button(
        label="📄 Download Proposal PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
    )
