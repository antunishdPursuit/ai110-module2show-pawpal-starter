import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule, ScheduleType, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Persist Owner across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Section 1: Owner Setup ─────────────────────────────────────────────────
st.subheader("Owner")
owner_name = st.text_input("Your name", value="Jordan")

if st.button("Set Owner"):
    st.session_state.owner = Owner(owner_name)
    st.success(f"Owner set: {owner_name}")

if st.session_state.owner is None:
    st.info("Set an owner above to get started.")
    st.stop()

owner = st.session_state.owner

# ── Section 2: Add a Pet ───────────────────────────────────────────────────
st.divider()
st.subheader("Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, age=age)
    try:
        owner.add_pet(new_pet)
        st.success(f"Added {pet_name} the {species}!")
    except ValueError as e:
        st.error(str(e))

if owner.pets:
    st.markdown("**Registered pets:**")
    for p in owner.pets:
        st.write(f"- [{p.pet_id}] {p.name} ({p.species}, age {p.age})")
else:
    st.info("No pets yet. Add one above.")

# ── Section 3: Add a Task ──────────────────────────────────────────────────
st.divider()
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_options = {f"{p.name} (ID {p.pet_id})": p for p in owner.pets}
    selected_label = st.selectbox("Assign to pet", list(pet_options.keys()))
    selected_pet = pet_options[selected_label]

    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        task_desc = st.text_input("Description", value="20 min walk")
    with col2:
        schedule_type = st.selectbox("Schedule", ["DAILY", "WEEKLY", "CUSTOM"])
        interval = st.number_input("Interval (days, CUSTOM only)", min_value=1, max_value=365, value=3)

    if st.button("Add Task"):
        stype = ScheduleType[schedule_type]
        schedule = Schedule(stype, start_date=date.today(), interval=interval)
        new_task = Task(
            title=task_title,
            description=task_desc,
            assigned_pet_id=selected_pet.pet_id,
            schedule=schedule
        )
        try:
            selected_pet.add_task(new_task)
            st.success(f"Task '{task_title}' added to {selected_pet.name}!")
        except ValueError as e:
            st.error(str(e))

# ── Section 4: Today's Schedule ───────────────────────────────────────────
st.divider()
st.subheader("Today's Schedule")

all_due = []
for pet in owner.pets:
    all_due.extend(pet.get_due_tasks_today())

if not all_due:
    st.info("No tasks due today.")
else:
    conflicts = Scheduler.detect_conflicts(all_due, pets=owner.pets)
    for warning in conflicts:
        st.warning(f"⚠️ {warning}")

    # ── Filters ──
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_status = st.selectbox("Filter by status", ["all", "pending", "done", "overdue"])
    with col_f2:
        pet_names = ["all"] + [p.name for p in owner.pets]
        filter_pet = st.selectbox("Filter by pet", pet_names)

    filtered = Scheduler.filter_tasks(
        all_due,
        status=None if filter_status == "all" else filter_status,
        pet_name=None if filter_pet == "all" else filter_pet,
        pets=owner.pets
    )

    if not filtered:
        st.info("No tasks match the selected filters.")

    pet_lookup = {p.pet_id: p for p in owner.pets}
    for task in Scheduler.sort_by_time(filtered):
        pet = pet_lookup.get(task.assigned_pet_id)
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{task.title}** — {task.description}  `{task.status}`")
            st.caption(f"{pet.name if pet else ''} · {task.time_of_day.strftime('%I:%M %p') if task.time_of_day else 'Anytime'}")
        with col2:
            if task.status != "done":
                if st.button("Done", key=f"done_{task.task_id}", use_container_width=True):
                    new_task = Scheduler.complete_and_reschedule(task, pet)
                    if new_task:
                        st.toast(f"Next '{task.title}' on {new_task.schedule.next_due_date} 📅")
                    else:
                        st.toast(f"'{task.title}' complete! ✅")
                    st.rerun()
