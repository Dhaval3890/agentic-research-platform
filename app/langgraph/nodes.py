from app.langgraph.state import ResearchState
from app.llm.local_llm import ollama_call

def combined_node(state: ResearchState) -> ResearchState:
    prompt = f"""
You are a senior market research consultant.

CLIENT DETAILS:
Organisation: {state.organization}
Industry: {state.industry}
Geography: {", ".join(state.geography)}

PRIMARY OBJECTIVE:
{state.primary_objective}

SECTION 2 DETAILS:
{state.section2}

CONSTRAINTS:
Methodology: {state.methodology}
Timeline: {state.timeline}
Budget: {state.budget}
Outputs: {", ".join(state.outputs)}

TASK:
1. Recommend the best research approach
2. Write a professional research proposal with:
   - Background
   - Objectives
   - Methodology
   - Sample
   - Deliverables
   - Timeline

Respond in this format:

RECOMMENDATION:
<text>

PROPOSAL:
<text>
"""

    response = ollama_call(prompt)

    if "PROPOSAL:" in response:
        rec, prop = response.split("PROPOSAL:", 1)
        state.recommendation = rec.replace("RECOMMENDATION:", "").strip()
        state.proposal = prop.strip()
    else:
        state.recommendation = response
        state.proposal = "Proposal generation failed."

    return state
