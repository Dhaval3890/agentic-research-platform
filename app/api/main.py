from fastapi import FastAPI, Response
from pydantic import BaseModel
from app.agents.proposal_writer import generate_proposal
from app.utils.pdf_export import generate_proposal_pdf

app = FastAPI()


class ProposalInput(BaseModel):
    client_name: str
    email: str
    product: str
    objective: str
    methodology: str
    target_group: str
    location: str
    budget: str


@app.post("/run-proposal")
def run_proposal(data: ProposalInput):
    proposal_text = generate_proposal(data.dict())
    return {"proposal": proposal_text}


@app.post("/export/pdf")
def export_pdf(data: ProposalInput):
    proposal_text = generate_proposal(data.dict())
    pdf_bytes = generate_proposal_pdf(proposal_text)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=research_proposal.pdf"
        },
    )
