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
    schedule_type: ScheduleType
    start_date: date
    interval: int = 1               # set automatically for DAILY/WEEKLY; required for CUSTOM

    def __post_init__(self):
        if self.schedule_type == ScheduleType.DAILY:
            self.interval = 1
        elif self.schedule_type == ScheduleType.WEEKLY:
            self.interval = 7
        elif self.schedule_type == ScheduleType.CUSTOM:
            if self.interval <= 0:
                raise ValueError("CUSTOM schedule requires interval > 0")
        self.next_due_date: date = self.start_date

    def calculate_next_due_date(self) -> date:
        self.next_due_date = self.next_due_date + timedelta(days=self.interval)
        return self.next_due_date

    def is_due_today(self) -> bool:
        # <= intentionally catches overdue/missed tasks
        return self.next_due_date <= date.today()


class _IDCounter:
    """Simple auto-incrementing ID generator shared across entity types."""
    def __init__(self):
        self._count = 0

    def next(self) -> int:
        self._count += 1
        return self._count


_pet_ids = _IDCounter()
_task_ids = _IDCounter()
_owner_ids = _IDCounter()


@dataclass
class Task:
    title: str
    description: str
    assigned_pet_id: int
    schedule: Optional[Schedule] = None
    task_id: int = field(default_factory=_task_ids.next)
    last_completed_date: Optional[date] = None

    def mark_complete(self):
        today = date.today()
        if self.last_completed_date == today:
            print(f"Task '{self.title}' already marked complete today — skipping.")
            return
        self.last_completed_date = today
        if self.schedule:
            self.schedule.calculate_next_due_date()

    def update_task(self, title: str = None, description: str = None, schedule: Schedule = None):
        if title is not None:
            if title.strip() == "":
                raise ValueError("title cannot be empty")
            self.title = title
        if description is not None:
            self.description = description
        if schedule is not None:
            self.schedule = schedule

    def to_display_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_today": self.schedule.is_due_today() if self.schedule else "no schedule",
            "next_due": str(self.schedule.next_due_date) if self.schedule else "N/A",
            "last_completed": str(self.last_completed_date) if self.last_completed_date else "never",
        }


@dataclass
class Pet:
    name: str
    species: str
    age: int
    pet_id: int = field(default_factory=_pet_ids.next)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        if task.assigned_pet_id != self.pet_id:
            raise ValueError(f"Task is assigned to pet_id {task.assigned_pet_id}, not {self.pet_id}")
        if any(t.task_id == task.task_id for t in self.tasks):
            raise ValueError(f"Task {task.task_id} already exists for this pet")
        self.tasks.append(task)

    def remove_task(self, task_id: int):
        original_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        if len(self.tasks) == original_len:
            raise ValueError(f"Task {task_id} not found")

    def get_tasks(self) -> list[Task]:
        return list(self.tasks)     # shallow copy to prevent external mutation

    def get_due_tasks_today(self) -> list[Task]:
        return [t for t in self.tasks if t.schedule and t.schedule.is_due_today()]


class Owner:
    def __init__(self, name: str):
        self.owner_id: int = _owner_ids.next()
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        if any(p.pet_id == pet.pet_id for p in self.pets):
            raise ValueError(f"Pet {pet.pet_id} already registered")
        self.pets.append(pet)

    def remove_pet(self, pet_id: int):
        original_len = len(self.pets)
        self.pets = [p for p in self.pets if p.pet_id != pet_id]
        if len(self.pets) == original_len:
            raise ValueError(f"Pet {pet_id} not found")

    def find_pet(self, pet_id: int) -> Optional[Pet]:
        """Returns None if not found — use when existence is uncertain."""
        return next((p for p in self.pets if p.pet_id == pet_id), None)

    def get_pet(self, pet_id: int) -> Pet:
        """Raises ValueError if not found — use when pet is expected to exist."""
        pet = self.find_pet(pet_id)
        if pet is None:
            raise ValueError(f"Pet {pet_id} not found")
        return pet

    def view_daily_plan(self):
        print(f"\n=== Daily Plan for {self.name} ===")
        if not self.pets:
            print("No pets registered.")
            return
        for pet in self.pets:
            due = pet.get_due_tasks_today()
            print(f"\n{pet.name} ({pet.species}, age {pet.age}):")
            if not due:
                print("  No tasks due today.")
            else:
                for task in due:
                    d = task.to_display_dict()
                    print(f"  [{d['task_id']}] {d['title']} — {d['description']}")
                    print(f"       Next due: {d['next_due']} | Last completed: {d['last_completed']}")


# --- Quick terminal test ---
if __name__ == "__main__":
    owner = Owner("Alex")

    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Whiskers", species="Cat", age=5)
    owner.add_pet(dog)
    owner.add_pet(cat)

    feed_dog = Task(
        title="Feed",
        description="Morning kibble",
        assigned_pet_id=dog.pet_id,
        schedule=Schedule(ScheduleType.DAILY, start_date=date.today())
    )
    walk_dog = Task(
        title="Walk",
        description="30 min walk around the block",
        assigned_pet_id=dog.pet_id,
        schedule=Schedule(ScheduleType.CUSTOM, start_date=date.today(), interval=2)
    )
    feed_cat = Task(
        title="Feed",
        description="Wet food twice daily",
        assigned_pet_id=cat.pet_id,
        schedule=Schedule(ScheduleType.DAILY, start_date=date.today())
    )

    dog.add_task(feed_dog)
    dog.add_task(walk_dog)
    cat.add_task(feed_cat)

    owner.view_daily_plan()

    print("\n--- Marking Buddy's feed as complete ---")
    feed_dog.mark_complete()
    print(f"Next feed due: {feed_dog.schedule.next_due_date}")

    print("\n--- Attempting to mark complete again today ---")
    feed_dog.mark_complete()

    owner.view_daily_plan()
