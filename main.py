from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule, ScheduleType


# --- Setup Owner ---
owner = Owner("Jordan")

# --- Create Pets ---
dog = Pet(name="Rex", species="Dog", age=4)
cat = Pet(name="Luna", species="Cat", age=2)
owner.add_pet(dog)
owner.add_pet(cat)

# --- Create Tasks for Rex (Dog) ---
morning_feed = Task(
    title="Morning Feed",
    description="1 cup of dry food at 7am",
    assigned_pet_id=dog.pet_id,
    schedule=Schedule(ScheduleType.DAILY, start_date=date.today())
)
walk = Task(
    title="Walk",
    description="Evening walk, 20 minutes at 6pm",
    assigned_pet_id=dog.pet_id,
    schedule=Schedule(ScheduleType.CUSTOM, start_date=date.today(), interval=2)
)

# --- Create Tasks for Luna (Cat) ---
feed_cat = Task(
    title="Morning Feed",
    description="Half can of wet food at 8am",
    assigned_pet_id=cat.pet_id,
    schedule=Schedule(ScheduleType.DAILY, start_date=date.today())
)
grooming = Task(
    title="Grooming",
    description="Brush coat for 5 minutes",
    assigned_pet_id=cat.pet_id,
    schedule=Schedule(ScheduleType.WEEKLY, start_date=date.today())
)

# --- Assign Tasks ---
dog.add_task(morning_feed)
dog.add_task(walk)
cat.add_task(feed_cat)
cat.add_task(grooming)

# --- Print Today's Schedule ---
print("=" * 40)
print(f"  TODAY'S SCHEDULE — {date.today()}")
print(f"  Owner: {owner.name}")
print("=" * 40)

for pet in owner.pets:
    due_tasks = pet.get_due_tasks_today()
    print(f"\n{pet.name} ({pet.species}, age {pet.age})")
    print("-" * 30)
    if not due_tasks:
        print("  No tasks due today.")
    else:
        for task in due_tasks:
            print(f"  [ ] {task.title}")
            print(f"      {task.description}")
            print(f"      Next due: {task.schedule.next_due_date}")

print("\n" + "=" * 40)
