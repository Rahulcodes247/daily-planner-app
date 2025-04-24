from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey, func, Boolean, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
import enum

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)


class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    name = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

class StatusEnum(enum.Enum):
    start = "start"
    inprogress = "inprogress"
    completed = "completed"


class PlanStatusEnum(enum.Enum):
    start = "start"
    inprogress = "inprogress"
    completed = "completed"


class Reflection(Base):
    __tablename__ = 'reflection'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    activities = Column(JSON, nullable=True)  # List of dicts: [{'name': ..., 'hours': ...}]
    start_date = Column(Date)
    end_date = Column(Date)
    best_experience = Column(Text, nullable=True)
    worst_experience = Column(Text, nullable=True)
    lesson_learned = Column(Text, nullable=True)
    happy_level = Column(Integer)  # 1 to 10
    status = Column(Enum(StatusEnum), default=StatusEnum.start)
    created_at = Column(DateTime, server_default=func.now())


class Plan(Base):
    __tablename__ = 'plan'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    activities = Column(ARRAY(String))

    wakeup_time = Column(Time)
    sleep_time = Column(Time)

    preferred_office_start_time = Column(Time)
    preferred_office_end_time = Column(Time)

    preferred_breakfast_time = Column(Time)
    preferred_lunch_time = Column(Time)
    preferred_dinner_time = Column(Time)

    constraints_or_preference = Column(Text, nullable=True)

    status = Column(Enum(PlanStatusEnum), default=PlanStatusEnum.start)
    created_at = Column(DateTime, server_default=func.now())