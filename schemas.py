from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Базовые схемы
class ActivityBase(BaseModel):
    name: str
    level: int


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class OrganizationBase(BaseModel):
    name: str
    building_id: int


# Схемы для ответов
class PhoneResponse(BaseModel):
    phone_number: str


class ActivityResponse(ActivityBase):
    id: int
    parent_id: Optional[int] = None
    children: List["ActivityResponse"] = []

    class Config:
        from_attributes = True


class BuildingResponse(BuildingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OrganizationResponse(OrganizationBase):
    id: int
    building: BuildingResponse
    activities: List[ActivityResponse]
    phones: List[PhoneResponse]
    created_at: datetime

    class Config:
        from_attributes = True


class BuildingWithOrganizationsResponse(BuildingResponse):
    organizations: List[OrganizationResponse]


# Схемы для запросов
class RadiusSearchRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: float


class RectangleSearchRequest(BaseModel):
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float


ActivityResponse.model_rebuild()
