from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Schedule:
    type: str           # "daily", "weekly", "custom"
    interval: int       # e.g., every 2 days
    start_date: date
    next_due_date: date

    def calculate_next_due_date(self):
        pass

    def is_due_today(self) -> bool:
        pass


@dataclass
class Task:
    task_id: int
    title: str          # e.g., "Feed", "Walk"
    description: str
    frequency: str
    assigned_pet: Optional["Pet"] = None
    schedule: Optional[Schedule] = None
    completed: bool = False

    def mark_complete(self):
        pass

    def update_task(self):
        pass


@dataclass
class Pet:
    pet_id: int
    name: str
    species: str        # "dog", "cat", etc.
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, owner_id: int, name: str):
        self.owner_id = owner_id
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def view_daily_plan(self):
        pass
