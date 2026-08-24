from pydantic import BaseModel, Field

class ItemInput(BaseModel):
    item_id: str
    length_cm: float = Field(..., gt=0)
    width_cm: float = Field(..., gt=0)
    height_cm: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    category: str
