import re
from db_service import SessionLocal
from models import User, Reflection, Plan
from model_schema import ReflectionCreate, PlanCreate, PlanUpdate


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


def save_reflection_output(reflection: ReflectionCreate):
    db_reflection = Reflection(**reflection.dict())
    with SessionLocal() as db:
        db.add(db_reflection)
        db.commit()
        db.refresh(db_reflection)
        return db_reflection


def create_plan(plan: PlanCreate) -> Plan:
    db_plan = Plan(**plan.dict())
    with SessionLocal() as db:
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        return db_plan


def parse_chat_output_to_dict(chat_output: str) -> list[dict]:
    # Step 1: Extract rows
    lines = chat_output.strip().split('\n')
    lines = lines[3:]  # Skip headers and separator

    # Step 2: Parse each row
    parsed = []
    for line in lines:
        print(f"DEBUG: {line = }")
        match = re.match(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', line)
        if match:
            print(f"DEBUG: {match = }")
            time_slot, activity = match.groups()
            if '-' in time_slot:
                time_start, time_end = time_slot.split('-')
            else:
                time_start = time_slot.strip()
                time_end = None
            parsed.append({
                'time_start': time_start.strip(),
                'time_end': time_end,
                'name': activity.strip(),
            })
    return parsed


def prepare_plan_insert_data(user_input: dict) -> PlanCreate:
    data: dict = {
        "wakeup_time": user_input.get("wake_up_time"),
        "sleep_time": user_input.get("sleep_time"),
        "preferred_office_start_time": user_input.get("office_start_time"),
        "preferred_office_end_time": user_input.get("office_end_time"),
        "preferred_breakfast_time": user_input.get("breakfast_time"),
        "preferred_lunch_time": user_input.get("lunch_time"),
        "preferred_dinner_time": user_input.get("dinner_time"),
        "constraints_or_preference": user_input.get("preferences"),
    }
    optional_activities = user_input.get("activity_hours")
    if optional_activities:
        data["optional_activities"] = [{"name": key, "hours": value} for key, value in optional_activities.items()]
    else:
        data["optional_activities"] = []
    return PlanCreate(**data)


def update_plan(plan_id: int, plan_output: PlanUpdate):
    with SessionLocal() as db:
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise Exception(f"Plan with id {plan_id} not found")

        plan.output = plan_output.model_dump()
        db.commit()
        db.refresh(plan)
        return plan
