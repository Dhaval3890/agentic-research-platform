from app.langgraph.state import ResearchState
from app.langgraph.graph import proposal_graph

state = ResearchState(
    organization="Tesla",
    industry="Automotive",
    geography=["India"],
    primary_objective="Evaluate market opportunity / growth potential",
    methodology="Quantitative",
    timeline="2–4 weeks"
)

final = proposal_graph.invoke(state)

print("\n--- RECOMMENDATION ---\n")
print(final["recommendation"])

print("\n--- PROPOSAL ---\n")
print(final["proposal"])
