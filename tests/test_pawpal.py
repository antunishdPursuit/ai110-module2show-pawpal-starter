from datetime import date
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task, Schedule, ScheduleType


def test_mark_complete_sets_last_completed_date():
    """mark_complete() should set last_completed_date to today."""
    task = Task(
        title="Feed",
        description="Morning kibble",
        assigned_pet_id=1,
        schedule=Schedule(ScheduleType.DAILY, start_date=date.today())
    )
    assert task.last_completed_date is None
    task.mark_complete()
    assert task.last_completed_date == date.today()


def test_add_task_increases_pet_task_count():
    """Adding a task to a pet should increase its task count by 1."""
    pet = Pet(name="Buddy", species="Dog", age=3)
    task = Task(
        title="Walk",
        description="Evening walk",
        assigned_pet_id=pet.pet_id,
        schedule=Schedule(ScheduleType.DAILY, start_date=date.today())
    )
    before = len(pet.get_tasks())
    pet.add_task(task)
    assert len(pet.get_tasks()) == before + 1
