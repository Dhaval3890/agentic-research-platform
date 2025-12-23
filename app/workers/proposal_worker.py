import threading
from app.llm.local_llm import llm_long

def generate_proposal_async(state: dict, callback=None):
    def task():
        prompt = f"""
Create a detailed, client-ready market research proposal.

Client:
- Organization: {state['organization']}
- Industry: {state['industry']}
- Geography: {state['geography']}
- Objective: {state['primary_objective']}
- Methodology: {state['methodology']}
- Timeline: {state['timeline']}
- Budget: {state['budget']}

Include:
- Executive Summary
- Objectives
- Methodology
- Sample Design
- Timeline
- Deliverables
- Expected Outcomes

Do NOT ask questions.
Do NOT mention AI.
"""

        proposal = llm_long(prompt)

        if callback:
            callback(proposal)

    threading.Thread(target=task, daemon=True).start()
