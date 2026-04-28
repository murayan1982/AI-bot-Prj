from pydantic import BaseModel


class SleepSummary(BaseModel):
    date: str
    total_sleep_minutes: int
    efficiency: int | None = None
    deep_sleep_minutes: int | None = None
    rem_sleep_minutes: int | None = None
    awake_minutes: int | None = None