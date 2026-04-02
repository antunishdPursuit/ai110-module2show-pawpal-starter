from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from typing import Optional


class ScheduleType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"


@dataclass
class Schedule:
    schedule_type: ScheduleType     # renamed from "type" to avoid shadowing built-in
    interval: int                   # e.g., every 2 days
    start_date: date
    next_due_date: date

    def calculate_next_due_date(self) -> date:
        self.next_due_date = self.next_due_date + timedelta(days=self.interval)
        return self.next_due_date

    def is_due_today(self) -> bool:
        return self.next_due_date <= date.today()   # <= catches missed/overdue tasks


@dataclass
class Task:
    task_id: int
    title: str                          # e.g., "Feed", "Walk"
    description: str
    assigned_pet_id: int                # stores pet_id to avoid circular reference
    schedule: Optional[Schedule] = None
    last_completed_date: Optional[date] = None

    def mark_complete(self):
        self.last_completed_date = date.today()
        if self.schedule:
            self.schedule.calculate_next_due_date()

    def update_task(self, title: str = None, description: str = None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description


@dataclass
class Pet:
    pet_id: int
    name: str
    species: str                        # "dog", "cat", etc.
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task_id: int):
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_tasks(self) -> list[Task]:
        return self.tasks

    def get_due_tasks_today(self) -> list[Task]:
        return [t for t in self.tasks if t.schedule and t.schedule.is_due_today()]


class Owner:
    def __init__(self, owner_id: int, name: str):
        self.owner_id = owner_id
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def remove_pet(self, pet_id: int):
        self.pets = [p for p in self.pets if p.pet_id != pet_id]

    def find_pet(self, pet_id: int) -> Optional[Pet]:
        return next((p for p in self.pets if p.pet_id == pet_id), None)

    def view_daily_plan(self) -> dict[str, list[Task]]:
        return {pet.name: pet.get_due_tasks_today() for pet in self.pets}
