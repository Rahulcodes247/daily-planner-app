from db_service import SessionLocal
from models import User, Reflection
from model_schema import ReflectionCreate


def add_user():
    with SessionLocal() as db:
        new_user = User(name="Alice", email="alice@example.com")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # optional: to load generated ID or updated fields

        print(f"Inserted user with ID: {new_user.id}")


def create_reflection(reflection: ReflectionCreate):
    db_reflection = Reflection(**reflection.dict())
    with SessionLocal() as db:
        db.add(db_reflection)
        db.commit()
        db.refresh(db_reflection)
        return db_reflection