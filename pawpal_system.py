from dataclasses import dataclass, field
from datetime import date, time, timedelta
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
        """Advance next_due_date by interval days and return the new date."""
        self.next_due_date = self.next_due_date + timedelta(days=self.interval)
        return self.next_due_date

    def is_due_today(self) -> bool:
        """Return True if the task is due today or is overdue."""
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
    time_of_day: Optional[time] = None          # e.g. time(7, 0) for 7:00am
    task_id: int = field(default_factory=_task_ids.next)
    last_completed_date: Optional[date] = None

    @property
    def status(self) -> str:
        """Derive task status from completion and schedule: done, overdue, or pending."""
        today = date.today()
        if self.last_completed_date == today:
            return "done"
        if self.schedule and self.schedule.next_due_date < today:
            return "overdue"
        return "pending"

    def mark_complete(self):
        """Mark the task complete for today and advance its schedule."""
        today = date.today()
        if self.last_completed_date == today:
            print(f"Task '{self.title}' already marked complete today — skipping.")
            return
        self.last_completed_date = today
        if self.schedule:
            self.schedule.calculate_next_due_date()

    def update_task(self, title: str = None, description: str = None, schedule: Schedule = None):
        """Update one or more task fields; raises ValueError if title is empty."""
        if title is not None:
            if title.strip() == "":
                raise ValueError("title cannot be empty")
            self.title = title
        if description is not None:
            self.description = description
        if schedule is not None:
            self.schedule = schedule

    def to_display_dict(self) -> dict:
        """Return a plain dict of task fields formatted for terminal display."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "time_of_day": self.time_of_day.strftime("%I:%M %p") if self.time_of_day else "no time set",
            "status": self.status,
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
        """Add a task to this pet; raises ValueError on mismatched pet or duplicate task."""
        if task.assigned_pet_id != self.pet_id:
            raise ValueError(f"Task is assigned to pet_id {task.assigned_pet_id}, not {self.pet_id}")
        if any(t.task_id == task.task_id for t in self.tasks):
            raise ValueError(f"Task {task.task_id} already exists for this pet")
        self.tasks.append(task)

    def remove_task(self, task_id: int):
        """Remove a task by ID; raises ValueError if not found."""
        original_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        if len(self.tasks) == original_len:
            raise ValueError(f"Task {task_id} not found")

    def get_tasks(self) -> list[Task]:
        """Return a shallow copy of all tasks for this pet."""
        return list(self.tasks)     # shallow copy to prevent external mutation

    def get_tasks_by_status(self, status: str) -> list[Task]:
        """Return all tasks matching the given status: 'pending', 'done', or 'overdue'."""
        return [t for t in self.tasks if t.status == status]

    def get_due_tasks_today(self) -> list[Task]:
        """Return tasks due today sorted by time_of_day; tasks with no time sort last."""
        due = [t for t in self.tasks if t.schedule and t.schedule.is_due_today()]
        return sorted(due, key=lambda t: (t.time_of_day is None, t.time_of_day))


class Owner:
    def __init__(self, name: str):
        self.owner_id: int = _owner_ids.next()
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Register a pet to this owner; raises ValueError on duplicate pet_id."""
        if any(p.pet_id == pet.pet_id for p in self.pets):
            raise ValueError(f"Pet {pet.pet_id} already registered")
        self.pets.append(pet)

    def remove_pet(self, pet_id: int):
        """Remove a pet by ID; raises ValueError if not found."""
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

    def get_tasks_for_pet(self, pet_id: int, status: str = None) -> list[Task]:
        """Return tasks for a specific pet, optionally filtered by status."""
        pet = self.get_pet(pet_id)
        if status:
            return pet.get_tasks_by_status(status)
        return pet.get_tasks()

    def view_daily_plan(self):
        """Print a formatted daily schedule for all pets owned by this owner."""
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
                    print(f"  [{d['status'].upper()}] {d['time_of_day']}  {d['title']} — {d['description']}")
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
