from typing import Dict, Any
from .state import StowState
from ..optimization.best_fit import calculate_best_fit
from ..services.groq_service import generate_explanation

def validate_item(state: StowState) -> StowState:
    # Here we would normally ensure all required fields exist
    # For now, we assume the FastAPI Pydantic model handles basic validation
    # We could add business logic validation here.
    return state

def get_locations(state: StowState) -> StowState:
    # In a full LangGraph, this node might actually query the DB.
    # For this prototype, the FastAPI endpoint passes the locations into the initial state.
    return state

def run_optimization(state: StowState) -> StowState:
    item = state.get("item", {})
    locations = state.get("available_locations", [])
    
    result = calculate_best_fit(item, locations)
    
    return {"optimization_result": result, "requires_operator_confirmation": True}

def generate_recommendation_explanation(state: StowState) -> StowState:
    item = state.get("item", {})
    opt_result = state.get("optimization_result", {})
    
    # We only call LLM if there's actually an optimization result
    if opt_result:
        explanation = generate_explanation(item, opt_result)
        return {"explanation": explanation}
        
    return {"explanation": "No optimization result provided."}
