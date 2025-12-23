import sys
import os
import streamlit as st
import requests
from fpdf import FPDF

# --------------------------------------------------
# PATH FIX
# --------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_TIMEOUT = 120

st.set_page_config(page_title="AI Research Interview", layout="centered")
st.title("🧠 AI Research Interview")
st.caption("Answer the questions below to generate a research recommendation and proposal.")

# --------------------------------------------------
# UTILS
# --------------------------------------------------
def clean_for_pdf(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
        .encode("latin-1", "ignore")
        .decode("latin-1")
    )

def ollama_call(prompt: str) -> dict:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 600
        }
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
        r.raise_for_status()
        response = r.json().get("response", "")
        return {"recommendation": response, "proposal": response}
    except Exception:
        return {
            "recommendation": "⚠ Model timed out. Please try again.",
            "proposal": "⚠ Model timed out. Please try again."
        }

# --------------------------------------------------
# SECTION 0 – BASIC CONTEXT
# --------------------------------------------------
st.subheader("SECTION 0: Basic Context")

org_name = st.text_input("Organisation Name")

industry = st.selectbox(
    "Industry",
    ["FMCG", "Retail", "BFSI", "Healthcare", "Technology", "Automotive", "Other"]
)

geography = st.multiselect(
    "Geography in scope",
    ["India", "Asia", "Europe", "North America", "Global"]
)

# --------------------------------------------------
# SECTION 1 – PRIMARY OBJECTIVE
# --------------------------------------------------
st.subheader("SECTION 1: Business Objective")

primary_objective = st.radio(
    "Main objective",
    [
        "Market opportunity",
        "Customer understanding",
        "Product / Innovation",
        "Brand performance",
        "Communication testing",
        "Pricing strategy",
        "Competitive benchmarking",
        "Sales / Channel improvement"
    ]
)

# --------------------------------------------------
# SECTION 2 – OBJECTIVE-BASED (RADIO + CHECKBOX)
# --------------------------------------------------
st.subheader("SECTION 2: Detailed Inputs")

section2_points = []

if primary_objective == "Market opportunity":
    market_type = st.radio(
        "What are you evaluating?",
        ["New market", "New category", "Business expansion", "Investment decision"]
    )
    info_needed = st.multiselect(
        "What do you need to know?",
        ["Market size", "Growth potential", "Competitive intensity", "Entry risks"]
    )
    section2_points += [market_type] + info_needed

elif primary_objective == "Customer understanding":
    audience = st.radio(
        "Target audience",
        ["Consumers", "Business customers", "Channel partners"]
    )
    objectives = st.multiselect(
        "What do you want to understand?",
        ["Needs & motivations", "Usage behavior", "Customer journey", "Satisfaction / loyalty"]
    )
    section2_points += [audience] + objectives

elif primary_objective == "Product / Innovation":
    stage = st.radio(
        "Product stage",
        ["Idea", "Prototype", "Ready for launch", "Already launched"]
    )
    decisions = st.multiselect(
        "Decisions required",
        ["Go / No-Go", "Feature prioritization", "UX improvement", "Post-launch optimization"]
    )
    section2_points += [stage] + decisions

elif primary_objective == "Brand performance":
    brand_goal = st.radio(
        "Brand challenge",
        ["Measure brand health", "Track brand performance", "Reposition brand"]
    )
    metrics = st.multiselect(
        "Key metrics",
        ["Awareness", "Consideration", "Preference", "Brand equity"]
    )
    section2_points += [brand_goal] + metrics

elif primary_objective == "Communication testing":
    campaign_stage = st.radio(
        "Campaign stage",
        ["Pre-launch", "Post-launch", "Overall strategy"]
    )
    evaluation = st.multiselect(
        "Evaluate",
        ["Ad concepts", "Messaging", "Media effectiveness"]
    )
    section2_points += [campaign_stage] + evaluation

elif primary_objective == "Pricing strategy":
    pricing_decision = st.radio(
        "Pricing decision",
        ["New price", "Price revision", "Discount testing", "Bundling"]
    )
    methods = st.multiselect(
        "Preferred approach",
        ["PSM", "Conjoint", "Willingness-to-pay"]
    )
    section2_points += [pricing_decision] + methods

elif primary_objective == "Competitive benchmarking":
    comparison = st.multiselect(
        "Compare on",
        ["Brand perception", "Product features", "Pricing", "Distribution"]
    )
    section2_points += comparison

elif primary_objective == "Sales / Channel improvement":
    focus = st.radio(
        "Focus area",
        ["Distribution", "Retail execution", "Shopper behavior", "Channel performance"]
    )
    section2_points.append(focus)

section2_details = ", ".join(section2_points)

# --------------------------------------------------
# SECTION 3 – CONSTRAINTS
# --------------------------------------------------
st.subheader("SECTION 3: Practical Constraints")

methodology = st.radio(
    "Preferred methodology",
    ["Qualitative", "Quantitative", "Hybrid", "Open to recommendation"]
)

timeline = st.radio(
    "Expected timeline",
    ["< 2 weeks", "2–4 weeks", "1–3 months", "Flexible"]
)

budget = st.radio(
    "Budget clarity",
    ["Budget available", "Need guidance"]
)

outputs = st.multiselect(
    "Expected outputs",
    ["PPT", "Dashboard", "Raw data", "PDF report"]
)

# --------------------------------------------------
# AI EXECUTION
# --------------------------------------------------
st.divider()

if st.button("Proceed to AI Recommendation →"):
    with st.spinner("Generating recommendation and proposal..."):

        prompt = f"""
You are a senior market research consultant.

Organisation: {org_name}
Industry: {industry}
Geography: {", ".join(geography)}
Objective: {primary_objective}

Detailed inputs:
{section2_details}

Methodology: {methodology}
Timeline: {timeline}
Budget: {budget}
Outputs: {", ".join(outputs)}

TASK:
1. Recommend best research approach
2. Draft a professional proposal with objectives, methodology, sample, timeline, deliverables
"""

        final = ollama_call(prompt)

    st.success("AI output generated")

    st.subheader("📌 Recommended Research Approach")
    st.write(final["recommendation"])

    st.subheader("📄 Draft Proposal")
    st.write(final["proposal"])

    # --------------------------------------------------
    # PDF EXPORT (FIXED)
    # --------------------------------------------------
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    pdf.multi_cell(
        0, 8,
        f"RECOMMENDED APPROACH\n\n{clean_for_pdf(final['recommendation'])}\n\n"
        f"DRAFT PROPOSAL\n\n{clean_for_pdf(final['proposal'])}"
    )

    pdf_bytes = pdf.output(dest="S").encode("latin-1")

    st.download_button(
        "📄 Download Proposal PDF",
        data=pdf_bytes,
        file_name="research_proposal.pdf",
        mime="application/pdf"
    )
