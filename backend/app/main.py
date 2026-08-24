# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Depends, HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from .database import engine, get_db, init_db
from .models.item import ItemInput
from .models.location import LocationResponse, StowLocation
from .optimization.best_fit import calculate_best_fit
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Stow Space Optimization API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Stow Space Agent API is running"}

@app.get("/api/items/{item_id}", response_model=ItemInput)
def get_item(item_id: str):
    # Mock item for Phase 6 frontend integration
    return {
        "item_id": item_id,
        "length_cm": 20.0,
        "width_cm": 15.0,
        "height_cm": 10.0,
        "weight_kg": 2.5,
        "category": "general"
    }

@app.get("/api/locations", response_model=list[LocationResponse])
def get_locations(db: Session = Depends(get_db)):
    locations = db.query(StowLocation).all()
    return locations

@app.post("/api/stow/recommend")
def recommend_stow_location(item: ItemInput, db: Session = Depends(get_db)):
    from .agent.graph import agent_app
    
    locations = db.query(StowLocation).filter(StowLocation.status == "AVAILABLE").all()
    
    loc_dicts = [
        {
            "location_id": loc.location_id,
            "available_length_cm": loc.available_length_cm,
            "available_width_cm": loc.available_width_cm,
            "available_height_cm": loc.available_height_cm,
            "weight_capacity_kg": loc.weight_capacity_kg,
            "status": loc.status
        }
        for loc in locations
    ]
    
    item_dict = item.model_dump()
    
    initial_state = {
        "item": item_dict,
        "available_locations": loc_dicts
    }
    
    # Run the langgraph workflow
    final_state = agent_app.invoke(initial_state)
    
    # Extract the results
    result = final_state.get("optimization_result", {})
    explanation = final_state.get("explanation", "No explanation available.")
    
    # Merge explanation into result
    result["llm_explanation"] = explanation
    
    return result

@app.post("/api/stow/confirm")
def confirm_stow(location_id: str, db: Session = Depends(get_db)):
    # This is a stub for future phases
    location = db.query(StowLocation).filter(StowLocation.location_id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # In a real app we'd update occupied_volume and maybe change status
    # location.status = "OCCUPIED" 
    # db.commit()
    
    return {"status": "CONFIRMED", "location_id": location_id}
