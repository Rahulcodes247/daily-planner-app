from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import enum

class StatusEnum(str, enum.Enum):
    start = "start"
    inprogress = "inprogress"
    completed = "completed"


class ActivityItem(BaseModel):
    name: str
    hours: float


class ReflectionCreate(BaseModel):
    user_id: Optional[int] = None
    activities: Optional[List[ActivityItem]] = None
    start_date: Optional[date]
    end_date: Optional[date]
    best_experience: Optional[str]
    worst_experience: Optional[str]
    lesson_learned: Optional[str]
    happy_level: Optional[int]
    status: Optional[StatusEnum] = StatusEnum.start
