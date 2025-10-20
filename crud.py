from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from models import Organization, Building, Activity, OrganizationPhone
from typing import List, Optional
import math


# Вспомогательные функции для работы с координатами
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in kilometers using Haversine formula"""
    R = 6371  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# CRUD операции
def get_organizations_in_building(db: Session, building_id: int) -> List[Organization]:
    return db.query(Organization).filter(Organization.building_id == building_id).all()


def get_organizations_by_activity(db: Session, activity_id: int) -> List[Organization]:
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return []

    return activity.organizations


def get_organizations_in_radius(
    db: Session, lat: float, lon: float, radius_km: float
) -> List[Organization]:
    all_organizations = db.query(Organization).all()
    organizations_in_radius = []

    for org in all_organizations:
        distance = calculate_distance(
            lat, lon, org.building.latitude, org.building.longitude
        )
        if distance <= radius_km:
            organizations_in_radius.append(org)

    return organizations_in_radius


def get_organizations_in_rectangle(
    db: Session, min_lat: float, max_lat: float, min_lon: float, max_lon: float
) -> List[Organization]:
    return (
        db.query(Organization)
        .join(Building)
        .filter(
            and_(
                Building.latitude >= min_lat,
                Building.latitude <= max_lat,
                Building.longitude >= min_lon,
                Building.longitude <= max_lon,
            )
        )
        .all()
    )


def get_all_buildings(db: Session) -> List[Building]:
    return db.query(Building).all()


def get_organization_by_id(db: Session, org_id: int) -> Optional[Organization]:
    return db.query(Organization).filter(Organization.id == org_id).first()


def get_organizations_by_activity_tree(
    db: Session, activity_id: int
) -> List[Organization]:
    """Найти организации по всему дереву деятельности"""

    # Получаем все дочерние активности (включая саму активность)
    def get_all_child_activities(activity_id: int) -> List[int]:
        activity_ids = [activity_id]
        children = db.query(Activity).filter(Activity.parent_id == activity_id).all()
        for child in children:
            activity_ids.extend(get_all_child_activities(child.id))
        return activity_ids

    all_activity_ids = get_all_child_activities(activity_id)

    # Находим организации, связанные с любой из этих активностей
    organizations = (
        db.query(Organization)
        .filter(Organization.activities.any(Activity.id.in_(all_activity_ids)))
        .all()
    )

    return organizations


def search_organizations_by_name(db: Session, name: str) -> List[Organization]:
    return db.query(Organization).filter(Organization.name.ilike(f"%{name}%")).all()


def get_activity_by_id(db: Session, activity_id: int) -> Optional[Activity]:
    return db.query(Activity).filter(Activity.id == activity_id).first()
