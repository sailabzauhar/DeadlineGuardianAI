from pydantic import BaseModel


class Task(BaseModel):
    day: int
    title: str
    description: str
    estimated_hours: float


class Plan(BaseModel):
    goal: str
    estimated_days: int
    risk_level: str
    recommended_daily_hours: float
    buffer_days: int
    strategy: str
    tasks: list[Task]