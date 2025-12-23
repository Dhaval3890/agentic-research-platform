from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ResearchState:
    # Section 0
    organization: str
    industry: str
    geography: List[str]

    # Section 1
    primary_objective: str

    # Section 2 (dynamic answers captured as dict)
    section2: Dict[str, List[str]]

    # Section 3
    methodology: str
    timeline: str
    budget: str
    outputs: List[str]

    # AI outputs
    recommendation: str = ""
    proposal: str = ""
