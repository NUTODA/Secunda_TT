from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Building, Activity, Organization, OrganizationPhone

engine = create_engine("sqlite:///./test.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_data():
    db = SessionLocal()

    try:
        buildings = [
            Building(
                address="г. Москва, ул. Ленина 1, офис 3",
                latitude=55.7558,
                longitude=37.6173,
            ),
            Building(
                address="г. Москва, ул. Блюхера 32/1",
                latitude=55.7600,
                longitude=37.6200,
            ),
            Building(
                address="г. Санкт-Петербург, Невский пр. 10",
                latitude=59.9343,
                longitude=30.3351,
            ),
        ]

        for building in buildings:
            db.add(building)
        db.commit()

        activities = [
            Activity(name="Еда", level=1),
            Activity(name="Автомобили", level=1),
            Activity(name="Одежда", level=1),
            Activity(name="Мясная продукция", level=2, parent_id=1),
            Activity(name="Молочная продукция", level=2, parent_id=1),
            Activity(name="Овощи и фрукты", level=2, parent_id=1),
            Activity(name="Грузовые", level=2, parent_id=2),
            Activity(name="Легковые", level=2, parent_id=2),
            Activity(name="Запчасти", level=3, parent_id=8),
            Activity(name="Аксессуары", level=3, parent_id=8),
        ]

        for activity in activities:
            db.add(activity)
        db.commit()

        organizations = [
            Organization(name='ООО "Рога и Копыта"', building_id=1),
            Organization(name='АО "Мясной двор"', building_id=2),
            Organization(name='ИП "Молочные реки"', building_id=1),
            Organization(name='ООО "Автозапчасти"', building_id=3),
        ]

        for org in organizations:
            db.add(org)
        db.commit()

        phones = [
            OrganizationPhone(organization_id=1, phone_number="2-222-222"),
            OrganizationPhone(organization_id=1, phone_number="3-333-333"),
            OrganizationPhone(organization_id=2, phone_number="8-923-666-13-13"),
            OrganizationPhone(organization_id=3, phone_number="4-444-444"),
            OrganizationPhone(organization_id=4, phone_number="5-555-555"),
        ]

        for phone in phones:
            db.add(phone)
        db.commit()

        org1 = db.query(Organization).filter(Organization.id == 1).first()
        activity1 = db.query(Activity).filter(Activity.id == 4).first()
        activity2 = db.query(Activity).filter(Activity.id == 5).first()
        org1.activities.extend([activity1, activity2])

        org2 = db.query(Organization).filter(Organization.id == 2).first()
        org2.activities.append(activity1)

        org3 = db.query(Organization).filter(Organization.id == 3).first()
        org3.activities.append(activity2)

        org4 = db.query(Organization).filter(Organization.id == 4).first()
        activity9 = db.query(Activity).filter(Activity.id == 9).first()
        org4.activities.append(activity9)

        db.commit()
        print("Тестовые данные успешно добавлены!")

    except Exception as e:
        db.rollback()
        print(f"Ошибка при добавлении данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
