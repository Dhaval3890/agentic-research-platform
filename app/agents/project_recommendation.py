from app.langgraph.state import ResearchState
from app.llm.local_llm import llm_quick


def project_recommendation_agent(state: ResearchState) -> ResearchState:
    prompt = f"""
You are a senior market research consultant.

Client:
Organization: {state.organization}
Industry: {state.industry}
Geography: {', '.join(state.geography)}
Objective: {state.primary_objective}

Return a PROFESSIONAL recommendation in plain English.
DO NOT return JSON.
DO NOT use bullet points.
"""

    recommendation_text = llm_quick(prompt)
    state.recommendation = str(recommendation_text)

    return state
