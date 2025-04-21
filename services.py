from db_service import SessionLocal
from models import User


def add_user():
    with SessionLocal() as db:
        new_user = User(name="Alice", email="alice@example.com")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # optional: to load generated ID or updated fields

        print(f"Inserted user with ID: {new_user.id}")

