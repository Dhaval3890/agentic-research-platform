from typing import Dict, Any
from app.llm.local_llm import llm_long


def proposal_generator_agent(
    intake: Dict[str, Any],
    recommendation: Dict[str, Any]
) -> str:
    """
    Generates a detailed, client-ready market research proposal.
    Assumes:
    - intake is a dict from LangGraph state
    - recommendation is a structured dict (NOT string)
    """

    # -----------------------------
    # 1. Extract Intake Fields
    # -----------------------------
    organization = intake.get("organization", "Client")
    industry = intake.get("industry", "")
    geography = ", ".join(intake.get("geography", []))
    primary_objective = intake.get("primary_objective", "")
    methodology_pref = intake.get("methodology", "")
    timeline = intake.get("timeline", "")
    budget = intake.get("budget", "")

    # -----------------------------
    # 2. Extract Recommendation (STRUCTURED)
    # -----------------------------
    recommended_projects = recommendation.get("recommended_projects", [])
    suggested_methodology = recommendation.get("suggested_methodology", "")
    target_audience = recommendation.get("target_audience", "")

    recommended_projects_text = ", ".join(recommended_projects)

    # -----------------------------
    # 3. Build PROFESSIONAL PROMPT
    # -----------------------------
    prompt = f"""
You are a senior market research consultant writing a formal, client-ready research proposal.

STRICT RULES:
- Do NOT ask questions
- Do NOT show JSON, bullet dumps, or raw data structures
- Do NOT mention AI, LLMs, or automation
- Use polished consulting language
- Write in full paragraphs
- Be detailed but professional

==============================
CLIENT CONTEXT
==============================
Organization: {organization}
Industry: {industry}
Geography: {geography}
Primary Business Objective: {primary_objective}
Preferred Methodology: {methodology_pref}
Timeline Expectation: {timeline}
Budget Guidance: {budget}

==============================
RECOMMENDED RESEARCH DIRECTION
==============================
Proposed Study Types: {recommended_projects_text}
Suggested Methodology: {suggested_methodology}
Target Audience: {target_audience}

==============================
PROPOSAL STRUCTURE (MANDATORY)
==============================

1. Cover Page
2. Executive Summary
3. Background & Business Context
4. Research Objectives
5. Recommended Research Approach
6. Research Methodology
7. Target Audience Definition
8. Geographic Scope
9. Project Timeline
10. Budget Overview (indicative, non-numeric if budget unclear)
11. Deliverables
12. Expected Outcomes & Business Impact
13. Conclusion & Next Steps

==============================
WRITING INSTRUCTIONS
==============================
- Make this proposal suitable to send directly to a CXO or client
- Assume this is an India-focused professional market research firm
- Ensure logical flow and strong business reasoning
- Length: Detailed (minimum 900–1200 words)

Now generate the complete proposal.
"""

    # -----------------------------
    # 4. Call LLM (LONG FORM)
    # -----------------------------
    proposal_text = llm_long(
        prompt=prompt,
        model="mistral"  # can switch to llama3 / mixtral later
    )

    return proposal_text
