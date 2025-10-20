from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import crud
import schemas
import models
from database import get_db, engine
from dependencies import verify_api_key
from utils import build_activity_tree
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Organization Directory API",
    description="REST API для справочника организаций, зданий и видов деятельности",
    version="1.0.0",
)


# 1. Список всех организаций в конкретном здании
@app.get(
    "/buildings/{building_id}/organizations",
    response_model=List[schemas.OrganizationResponse],
    summary="Организации в здании",
)
def get_organizations_in_building(
    building_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """Получить список всех организаций в указанном здании"""
    organizations = crud.get_organizations_in_building(db, building_id)
    if not organizations:
        raise HTTPException(
            status_code=404, detail="No organizations found in this building"
        )
    return organizations


# 2. Список организаций по виду деятельности
@app.get(
    "/activities/{activity_id}/organizations",
    response_model=List[schemas.OrganizationResponse],
    summary="Организации по виду деятельности",
)
def get_organizations_by_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """Получить организации, занимающиеся указанным видом деятельности"""
    organizations = crud.get_organizations_by_activity(db, activity_id)
    if not organizations:
        raise HTTPException(
            status_code=404, detail="No organizations found for this activity"
        )
    return organizations


# 3. Организации рядом на карте (радиус)
@app.post(
    "/organizations/nearby/radius",
    response_model=List[schemas.OrganizationResponse],
    summary="Организации в радиусе",
)
def get_organizations_in_radius(
    request: schemas.RadiusSearchRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """Найти организации в заданном радиусе от указанной точки"""
    organizations = crud.get_organizations_in_radius(
        db, request.latitude, request.longitude, request.radius_km
    )
    return organizations


# 4. Организации рядом на карте (прямоугольник)
@app.post(
    "/organizations/nearby/rectangle",
    response_model=List[schemas.OrganizationResponse],
    summary="Организации в прямоугольной области",
)
def get_organizations_in_rectangle(
    request: schemas.RectangleSearchRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """Найти организации в прямоугольной области на карте"""
    organizations = crud.get_organizations_in_rectangle(
        db, request.min_lat, request.max_lat, request.min_lon, request.max_lon
    )
    return organizations


# 5. Список всех зданий
@app.get(
    "/buildings",
    response_model=List[schemas.BuildingResponse],
    summary="Список всех зданий",
)
def get_all_buildings(
    db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)
):
    """Получить перечень всех зданий в справочнике"""
    return crud.get_all_buildings(db)


# 6. Информация об организации по ID
@app.get(
    "/organizations/{organization_id}",
    response_model=schemas.OrganizationResponse,
    summary="Информация об организации",
)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """Получить полную информацию об организации по её ID"""
    organization = crud.get_organization_by_id(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


# 7. Поиск по дереву деятельности
@app.get(
    "/activities/{activity_id}/tree/organizations",
    response_model=List[schemas.OrganizationResponse],
    summary="Организации по дереву деятельности",
)
def get_organizations_by_activity_tree(
    activity_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """Найти все организации, чья деятельность входит в указанную ветку дерева"""
    organizations = crud.get_organizations_by_activity_tree(db, activity_id)
    if not organizations:
        raise HTTPException(
            status_code=404, detail="No organizations found in this activity tree"
        )
    return organizations


# 8. Поиск организации по названию
@app.get(
    "/organizations/search/name",
    response_model=List[schemas.OrganizationResponse],
    summary="Поиск организации по названию",
)
def search_organizations_by_name(
    name: str = Query(..., description="Название организации или его часть"),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """Найти организации по названию (или части названия)"""
    organizations = crud.search_organizations_by_name(db, name)
    return organizations


# Получить дерево активностей
@app.get("/activities/tree", summary="Дерево видов деятельности")
def get_activities_tree(
    db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)
):
    """Получить полное дерево видов деятельности"""
    activities = db.query(models.Activity).all()
    tree = build_activity_tree(activities)
    return tree


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
