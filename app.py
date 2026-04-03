import streamlit as st
from datetime import date, time
from pawpal_system import Owner, Pet, Task, Schedule, ScheduleType, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 720px;
    }

    h1 { font-size: 1.8rem !important; font-weight: 700 !important; letter-spacing: -0.5px; }
    h2 { font-size: 1.1rem !important; font-weight: 600 !important; color: #555 !important; text-transform: uppercase; letter-spacing: 1px; }
    h3 { font-size: 1rem !important; font-weight: 600 !important; }

    .card {
        background: #ffffff;
        border: 1px solid #f0f0f0;
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }

    .card-left { display: flex; flex-direction: column; gap: 2px; }
    .card-time  { font-size: 0.72rem; font-weight: 600; color: #999; text-transform: uppercase; letter-spacing: 0.5px; }
    .card-title { font-size: 1rem; font-weight: 600; color: #1a1a1a; }
    .card-desc  { font-size: 0.82rem; color: #888; }
    .card-pet   { font-size: 0.75rem; color: #bbb; margin-top: 2px; }

    .badge {
        font-size: 0.7rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }
    .badge-pending { background: #f0f4ff; color: #4a6cf7; }
    .badge-done    { background: #edfaf3; color: #2dba74; }
    .badge-overdue { background: #fff0f0; color: #e04040; }

    .conflict-box {
        background: #fff8ec;
        border-left: 4px solid #f5a623;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
        color: #7a5200;
    }

    .pet-card {
        background: #f9f9f9;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
    }
    .pet-card-icon  { font-size: 2rem; }
    .pet-card-name  { font-weight: 700; font-size: 1rem; color: #1a1a1a; margin-top: 4px; }
    .pet-card-sub   { color: #aaa; font-size: 0.8rem; }
    .pet-card-id    { color: #ccc; font-size: 0.7rem; margin-top: 4px; }

    .section-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #aaa;
        margin-bottom: 0.4rem;
    }

    div[data-testid="stButton"] button {
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    hr { border-color: #f0f0f0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("# 🐾 PawPal+")
st.markdown("<p style='color:#999;margin-top:-12px;font-size:0.9rem'>Your daily pet care companion</p>", unsafe_allow_html=True)

# ── Owner Setup ────────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None

if st.session_state.owner is None:
    st.markdown("---")
    st.markdown("### Get started")
    col1, col2 = st.columns([3, 1])
    with col1:
        owner_name = st.text_input("Your name", placeholder="e.g. Alex", label_visibility="collapsed")
    with col2:
        if st.button("Let's go →", use_container_width=True):
            if owner_name.strip():
                st.session_state.owner = Owner(owner_name.strip())
                st.rerun()
            else:
                st.error("Please enter your name.")
    st.stop()

owner = st.session_state.owner

# ── Nav tabs ───────────────────────────────────────────────────────────────
tab_today, tab_pets, tab_tasks = st.tabs(["📅  Today", "🐶  My Pets", "✅  Add Task"])

# ══════════════════════════════════════════════════════════════════════════
# TAB 1 — TODAY'S SCHEDULE
# ══════════════════════════════════════════════════════════════════════════
with tab_today:
    st.markdown(f"<p style='color:#999;font-size:0.85rem;margin-bottom:1rem'>{date.today().strftime('%A, %B %d')}</p>", unsafe_allow_html=True)

    all_due = []
    for pet in owner.pets:
        all_due.extend(pet.get_due_tasks_today())

    if not owner.pets:
        st.info("Add your pets first in the **My Pets** tab.")
    elif not all_due:
        st.success("All clear — nothing due today! 🎉")
    else:
        # conflict warnings
        conflicts = Scheduler.detect_conflicts(all_due, pets=owner.pets)
        for warning in conflicts:
            st.markdown(f'<div class="conflict-box">⚠️ {warning}</div>', unsafe_allow_html=True)

        pet_lookup = {p.pet_id: p for p in owner.pets}
        species_icon = {"dog": "🐶", "cat": "🐱", "other": "🐾"}

        sorted_tasks = Scheduler.sort_by_time(all_due)
        for task in sorted_tasks:
            pet = pet_lookup.get(task.assigned_pet_id)
            icon = species_icon.get(pet.species.lower(), "🐾") if pet else "🐾"
            time_label = task.time_of_day.strftime("%I:%M %p").lstrip("0") if task.time_of_day else "Anytime"
            badge_class = f"badge-{task.status}"

            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div class="card">
                  <div class="card-left">
                    <span class="card-time">{time_label}</span>
                    <span class="card-title">{task.title}</span>
                    <span class="card-desc">{task.description}</span>
                    <span class="card-pet">{icon} {pet.name if pet else ''}</span>
                  </div>
                  <span class="badge {badge_class}">{task.status}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if task.status != "done":
                    if st.button("Done", key=f"done_{task.task_id}", use_container_width=True):
                        new_task = Scheduler.complete_and_reschedule(task, pet)
                        if new_task:
                            st.toast(f"Next '{task.title}' on {new_task.schedule.next_due_date} 📅")
                        else:
                            st.toast(f"'{task.title}' complete! ✅")
                        st.rerun()

# ══════════════════════════════════════════════════════════════════════════
# TAB 2 — MY PETS
# ══════════════════════════════════════════════════════════════════════════
with tab_pets:
    # registered pets
    if owner.pets:
        st.markdown('<p class="section-label">Registered</p>', unsafe_allow_html=True)
        species_icon = {"dog": "🐶", "cat": "🐱", "other": "🐾"}
        cols = st.columns(len(owner.pets))
        for i, p in enumerate(owner.pets):
            icon = species_icon.get(p.species.lower(), "🐾")
            with cols[i]:
                st.markdown(f"""
                <div class="pet-card">
                  <div class="pet-card-icon">{icon}</div>
                  <div class="pet-card-name">{p.name}</div>
                  <div class="pet-card-sub">{p.species} · {p.age}y</div>
                  <div class="pet-card-id">ID {p.pet_id}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("")

    # add new pet form
    st.markdown('<p class="section-label">Add a pet</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        new_pet_name = st.text_input("Name", placeholder="Mochi", label_visibility="collapsed")
    with col2:
        new_species = st.selectbox("Species", ["dog", "cat", "other"], label_visibility="collapsed")
    with col3:
        new_age = st.number_input("Age", min_value=0, max_value=30, value=2, label_visibility="collapsed")

    if st.button("Add Pet", use_container_width=False):
        if new_pet_name.strip():
            try:
                owner.add_pet(Pet(name=new_pet_name.strip(), species=new_species, age=new_age))
                st.toast(f"{new_pet_name} added! 🐾")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
        else:
            st.error("Pet needs a name.")

# ══════════════════════════════════════════════════════════════════════════
# TAB 3 — ADD TASK
# ══════════════════════════════════════════════════════════════════════════
with tab_tasks:
    if not owner.pets:
        st.info("Add your pets first in the **My Pets** tab.")
    else:
        pet_options = {f"{p.name}": p for p in owner.pets}
        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task", placeholder="Morning walk")
            task_desc = st.text_input("Details", placeholder="20 min around the block")
            selected_pet_name = st.selectbox("For", list(pet_options.keys()))
        with col2:
            task_time = st.time_input("Time", value=time(8, 0))
            schedule_type = st.selectbox("Repeats", ["DAILY", "WEEKLY", "CUSTOM"])
            interval = st.number_input("Every N days (Custom only)", min_value=1, max_value=365, value=3)

        if st.button("Add Task →", use_container_width=False):
            if task_title.strip():
                selected_pet = pet_options[selected_pet_name]
                stype = ScheduleType[schedule_type]
                schedule = Schedule(stype, start_date=date.today(), interval=interval)
                new_task = Task(
                    title=task_title.strip(),
                    description=task_desc.strip(),
                    assigned_pet_id=selected_pet.pet_id,
                    schedule=schedule,
                    time_of_day=task_time
                )
                try:
                    selected_pet.add_task(new_task)
                    st.toast(f"'{task_title}' added for {selected_pet_name} at {task_time.strftime('%I:%M %p')} ✅")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
            else:
                st.error("Task needs a title.")

        # show existing tasks per pet
        if any(p.tasks for p in owner.pets):
            st.markdown("---")
            st.markdown('<p class="section-label">All tasks</p>', unsafe_allow_html=True)
            for pet in owner.pets:
                if pet.tasks:
                    st.markdown(f"**{pet.name}**")
                    for t in Scheduler.sort_by_time(pet.get_tasks()):
                        time_label = t.time_of_day.strftime("%I:%M %p").lstrip("0") if t.time_of_day else "Anytime"
                        badge_class = f"badge-{t.status}"
                        st.markdown(f"""
                        <div class="card">
                          <div class="card-left">
                            <span class="card-time">{time_label}</span>
                            <span class="card-title">{t.title}</span>
                            <span class="card-desc">{t.description}</span>
                          </div>
                          <span class="badge {badge_class}">{t.status}</span>
                        </div>
                        """, unsafe_allow_html=True)
