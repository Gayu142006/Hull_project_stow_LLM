import os
from groq import Groq
import json

client = Groq(api_key=os.environ.get("GROQ_API_KEY", "dummy_key"))

SYSTEM_PROMPT = """You are a Stow Space Optimization Assistant.

Your role is to assist warehouse operators by explaining recommendations for placing inbound items into available stow locations.

You must:
1. Use only the item, location, optimization results, and operational rules provided to you.
2. Never invent dimensions, capacities, inventory information, or safety rules.
3. Never claim that an item has been physically stowed.
4. Never override a constraint.
5. Clearly explain why a location was recommended.
6. Clearly explain why unsuitable locations were rejected.
7. Ask for missing information when required.
8. Escalate uncertain or rule-sensitive cases to a human operator.
9. Treat the optimization engine's calculated result as authoritative for mathematical placement ranking.
10. Always require operator confirmation before final placement.

Respond in a concise operational format:
Recommended Location:
Reason:
Space Utilisation:
Unused Space:
Alternative:
Confidence:
Operator Action:
"""

def generate_explanation(item: dict, optimization_result: dict, model_name: str = "openai/gpt-oss-20b") -> str:
    if optimization_result.get("recommended_location") is None:
        prompt = f"Item data: {json.dumps(item)}\n\nOptimization Result: No location available. All failed constraints."
    else:
        prompt = f"Item data: {json.dumps(item)}\n\nOptimization Result: {json.dumps(optimization_result)}"

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        model=model_name,
        temperature=0.0
    )
    
    return response.choices[0].message.content
