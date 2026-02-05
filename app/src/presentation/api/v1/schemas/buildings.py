from pydantic import BaseModel


class BuildingResponse(BaseModel):
    id: int
    address: str
    location: tuple[float, float]
