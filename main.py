from datetime import date, time
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
    description="1 cup of dry food",
    assigned_pet_id=dog.pet_id,
    schedule=Schedule(ScheduleType.DAILY, start_date=date.today()),
    time_of_day=time(7, 0)
)
walk = Task(
    title="Walk",
    description="Evening walk, 20 minutes",
    assigned_pet_id=dog.pet_id,
    schedule=Schedule(ScheduleType.CUSTOM, start_date=date.today(), interval=2),
    time_of_day=time(18, 0)
)

# --- Create Tasks for Luna (Cat) ---
feed_cat = Task(
    title="Morning Feed",
    description="Half can of wet food",
    assigned_pet_id=cat.pet_id,
    schedule=Schedule(ScheduleType.DAILY, start_date=date.today()),
    time_of_day=time(8, 0)
)
grooming = Task(
    title="Grooming",
    description="Brush coat for 5 minutes",
    assigned_pet_id=cat.pet_id,
    schedule=Schedule(ScheduleType.WEEKLY, start_date=date.today()),
    time_of_day=time(10, 0)
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
            d = task.to_display_dict()
            print(f"  [ ] {d['time_of_day']}  {d['title']}")
            print(f"      {d['description']}")
            print(f"      Next due: {d['next_due']}")

print("\n" + "=" * 40)

# --- Demo: filter by status ---
print("\n--- Marking Rex's Morning Feed as complete ---")
morning_feed.mark_complete()

print("\n--- Rex's pending tasks ---")
for t in dog.get_tasks_by_status("pending"):
    print(f"  {t.title} ({t.status})")

print("\n--- Rex's done tasks ---")
for t in dog.get_tasks_by_status("done"):
    print(f"  {t.title} ({t.status})")

# --- Demo: filter by pet via owner ---
print("\n--- All tasks for Luna (via owner) ---")
for t in owner.get_tasks_for_pet(cat.pet_id):
    print(f"  {t.title} [{t.status}]")

print("\n--- Luna's pending tasks only ---")
for t in owner.get_tasks_for_pet(cat.pet_id, status="pending"):
    print(f"  {t.title} [{t.status}]")
