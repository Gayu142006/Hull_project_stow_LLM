import os
import json
from dotenv import load_dotenv
load_dotenv() # Load before importing app modules

from app.agent.graph import agent_app

def run_test():
    load_dotenv()
    if not os.environ.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY") == "your_groq_api_key_here":
        print("Error: GROQ_API_KEY is missing or invalid in .env")
        print("Please set your real Groq API key before testing this integration.")
        return

    item = {
        "item_id": "TEST_ITEM_123",
        "length_cm": 15,
        "width_cm": 15,
        "height_cm": 10,
        "weight_kg": 2.0,
        "category": "electronics"
    }

    locations = [
        {
            "location_id": "BIN-A",
            "available_length_cm": 20,
            "available_width_cm": 20,
            "available_height_cm": 15,
            "weight_capacity_kg": 10,
            "status": "AVAILABLE"
        },
        {
            "location_id": "BIN-B",
            "available_length_cm": 10,
            "available_width_cm": 10,
            "available_height_cm": 10,
            "weight_capacity_kg": 5,
            "status": "AVAILABLE"
        }
    ]

    print("Running LangGraph workflow...")
    
    initial_state = {
        "item": item,
        "available_locations": locations
    }
    
    final_state = agent_app.invoke(initial_state)
    
    print("\n--- OPTIMIZATION ENGINE RESULT ---")
    print(json.dumps(final_state.get("optimization_result", {}), indent=2))
    
    print("\n--- GROQ LLM EXPLANATION ---")
    print(final_state.get("explanation", ""))

if __name__ == "__main__":
    run_test()
