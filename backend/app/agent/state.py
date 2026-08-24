from typing import TypedDict, List, Dict, Any, Optional

class StowState(TypedDict):
    item: Dict[str, Any]
    available_locations: List[Dict[str, Any]]
    optimization_result: Dict[str, Any]
    explanation: str
    requires_operator_confirmation: bool
