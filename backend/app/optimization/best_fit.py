from typing import List, Dict, Any
from itertools import permutations

def fits_in_location(item_dims: tuple, location_dims: tuple) -> bool:
    """Checks if item fits in location in any orientation."""
    for orientation in set(permutations(item_dims)):
        if (orientation[0] <= location_dims[0] and 
            orientation[1] <= location_dims[1] and 
            orientation[2] <= location_dims[2]):
            return True
    return False

def calculate_best_fit(item: Dict[str, Any], locations: List[Dict[str, Any]]) -> Dict[str, Any]:
    valid_locations = []
    
    item_vol = item["length_cm"] * item["width_cm"] * item["height_cm"]
    item_dims = (item["length_cm"], item["width_cm"], item["height_cm"])
    
    for loc in locations:
        if loc["status"] != "AVAILABLE":
            continue
            
        if item["weight_kg"] > loc["weight_capacity_kg"]:
            continue
            
        loc_dims = (loc["available_length_cm"], loc["available_width_cm"], loc["available_height_cm"])
        if not fits_in_location(item_dims, loc_dims):
            continue
            
        available_vol = loc["available_length_cm"] * loc["available_width_cm"] * loc["available_height_cm"]
        unused_vol = available_vol - item_vol
        space_util = (item_vol / available_vol) * 100 if available_vol > 0 else 0
        
        valid_locations.append({
            "location_id": loc["location_id"],
            "space_utilisation_percent": round(space_util, 1),
            "unused_volume_cm3": round(unused_vol, 1)
        })
        
    if not valid_locations:
        return {
            "recommended_location": None,
            "reason": "No available locations can accommodate this item.",
            "space_utilisation_percent": None,
            "unused_volume_cm3": None,
            "confidence": "NONE",
            "alternative_locations": [],
            "requires_operator_confirmation": True
        }
        
    # Sort by highest space utilisation (lowest unused volume)
    valid_locations.sort(key=lambda x: x["space_utilisation_percent"], reverse=True)
    
    best_loc = valid_locations[0]
    alternatives = valid_locations[1:]
    
    return {
        "recommended_location": best_loc["location_id"],
        "reason": f"{best_loc['location_id']} is the best available dimensional fit and provides high space utilisation.",
        "space_utilisation_percent": best_loc["space_utilisation_percent"],
        "unused_volume_cm3": best_loc["unused_volume_cm3"],
        "confidence": "HIGH" if best_loc["space_utilisation_percent"] > 50 else "MEDIUM",
        "alternative_locations": alternatives,
        "requires_operator_confirmation": True
    }
