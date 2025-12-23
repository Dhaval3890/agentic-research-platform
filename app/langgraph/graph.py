from langgraph.graph import StateGraph
from app.langgraph.state import ResearchState
from app.langgraph.nodes import combined_node

builder = StateGraph(ResearchState)
builder.add_node("combined", combined_node)
builder.set_entry_point("combined")

proposal_graph = builder.compile()
