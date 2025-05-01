from pydantic import BaseModel, condecimal, RootModel, validator
from typing import List, Optional
from datetime import date, time, datetime
import enum

from sqlalchemy.sql.base import Options

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


class ActivityPercentage(BaseModel):
    activity: str
    percent: condecimal(ge=0, le=100)  # Ensures percent is between 0 and 100


class ReflectionOutputSchema(RootModel[List[ActivityPercentage]]):
    pass


# class Plan(BaseModel):
#     user_id: Optional[int] = None
#     activities: Optional[List[ActivityItem]] = None
#     start_date: Optional[date]
#     end_date: Optional[date]
#     best_experience: Optional[str]
#     worst_experience: Optional[str]
#     lesson_learned: Optional[str]
#     happy_level: Optional[int]
#     status: Optional[StatusEnum] = StatusEnum.start

class PlanStatusEnum(str, enum.Enum):
    start = "start"
    inprogress = "inprogress"
    completed = "completed"


class OptionalActivity(BaseModel):
    name: str
    hours: float

class OutputActivity(BaseModel):
    name: str
    time_start: str
    time_end: Optional[str] = None

    # @validator('time_start', 'time_end', pre=True)
    # def parse_time(cls, value):
    #     if value is None:
    #         return value
    #     if isinstance(value, time):
    #         return value
    #     try:
    #         return datetime.strptime(value, "%I:%M %p").time()  # parses '10:00 PM'
    #     except ValueError:
    #         return None
    #         # raise ValueError(f"Invalid time format: {value}")

class PlanBase(BaseModel):
    user_id: Optional[int] = None

    wakeup_time: time
    sleep_time: time

    preferred_office_start_time: time
    preferred_office_end_time: time

    preferred_breakfast_time: time
    preferred_lunch_time: time
    preferred_dinner_time: time

    constraints_or_preference: Optional[str] = None

    optional_activities: Optional[List[OptionalActivity]] = None

    status: PlanStatusEnum = PlanStatusEnum.start

    # output: Optional[List[OutputActivity]] = None


class PlanCreate(PlanBase):
    pass


class PlanUpdate(RootModel[List[OutputActivity]]):
    pass
