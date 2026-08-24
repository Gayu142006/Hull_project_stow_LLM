from langgraph.graph import StateGraph, START, END
from .state import StowState
from .nodes import (
    validate_item, 
    get_locations, 
    run_optimization, 
    generate_recommendation_explanation
)

def build_graph():
    workflow = StateGraph(StowState)

    # Add nodes
    workflow.add_node("validate_item", validate_item)
    workflow.add_node("get_locations", get_locations)
    workflow.add_node("run_optimization", run_optimization)
    workflow.add_node("generate_recommendation_explanation", generate_recommendation_explanation)

    # Add edges
    workflow.add_edge(START, "validate_item")
    workflow.add_edge("validate_item", "get_locations")
    workflow.add_edge("get_locations", "run_optimization")
    workflow.add_edge("run_optimization", "generate_recommendation_explanation")
    workflow.add_edge("generate_recommendation_explanation", END)

    # Compile the graph
    app = workflow.compile()
    
    return app

# Expose a compiled instance
agent_app = build_graph()
