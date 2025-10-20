from sqlalchemy.orm import Session
from models import Organization, Building, Activity


def build_activity_tree(activities: list, parent_id: int = None) -> list:
    """Строит древовидную структуру активностей"""
    tree = []
    for activity in activities:
        if activity.parent_id == parent_id:
            children = build_activity_tree(activities, activity.id)
            activity_dict = {
                "id": activity.id,
                "name": activity.name,
                "level": activity.level,
                "parent_id": activity.parent_id,
                "children": children,
            }
            tree.append(activity_dict)
    return tree
