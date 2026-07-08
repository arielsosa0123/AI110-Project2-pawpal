"""PawPal+ Streamlit front end: add an owner and pets, give each pet care
tasks, then generate and explain a daily schedule."""

from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Schedule, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, a pet-care planning assistant. Add an owner and pets,
give each pet care tasks with times and priorities, then generate a daily plan
that orders the tasks and explains the reasoning.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** helps a pet owner plan care tasks for their pet(s) based on
constraints like time and priority. The scheduling logic lives in
`pawpal_system.py`; this Streamlit app is the interactive front end.
"""
    )

st.divider()

# ---------------------------------------------------------------------------
# Owner: create once in the session "vault", then keep its name in sync.
# ---------------------------------------------------------------------------
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
owner = st.session_state.owner
owner.name = owner_name

st.divider()

# ---------------------------------------------------------------------------
# Add a Pet: a form whose submit calls Owner.add_pet(...).
# ---------------------------------------------------------------------------
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col_b:
        walk_time = st.time_input("Daily walk time", value=time(8, 0))
    with col_c:
        walk_duration = st.number_input(
            "Walk duration (min)", min_value=1, max_value=240, value=30
        )
    submitted = st.form_submit_button("Add pet")

if submitted and pet_name.strip():
    # Build the Pet from the form, then let the Owner own it (sets back-ref).
    new_pet = Pet(
        name=pet_name.strip(),
        species=species,
        walk_time=walk_time.strftime("%H:%M"),
        walk_duration=int(walk_duration),
    )
    owner.add_pet(new_pet)
    st.success(f"Added {new_pet.name} the {new_pet.species}.")

pets = owner.get_pets()
if not pets:
    st.info("No pets yet. Add one above to start planning.")
    st.stop()

# Scheduler runs the algorithms (sorting, filtering, conflicts) over the owner.
scheduler = Scheduler(owner)

st.divider()

# ---------------------------------------------------------------------------
# Pick the active pet. Tasks and the schedule apply to this pet.
# ---------------------------------------------------------------------------
st.subheader("Tasks")
pet_labels = [f"{p.name} ({p.species})" for p in pets]
selected = st.selectbox("Pet", range(len(pets)), format_func=lambda i: pet_labels[i])
pet = pets[selected]

st.caption(f"Add care tasks for {pet.name}. Each one feeds into the scheduler.")

with st.form("add_task_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Feeding")
    with col2:
        task_time = st.time_input("Time", value=time(9, 0))
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    task_submitted = st.form_submit_button("Add task")

if task_submitted and task_title.strip():
    pet.add_task(
        Task(
            title=task_title.strip(),
            time=task_time.strftime("%H:%M"),
            duration_minutes=int(duration),
            priority=priority,
        )
    )

tasks = pet.get_tasks()
if tasks:
    pending_only = st.checkbox("Show pending tasks only", value=False)

    # Scheduler.filter_by_status + Scheduler.sort_by_time drive the table.
    shown = scheduler.filter_by_status(tasks, completed=False) if pending_only else tasks
    shown = scheduler.sort_by_time(shown)

    st.write(f"Current tasks for {pet.name} (sorted by time):")
    st.table(
        [
            {
                "time": t.time,
                "title": t.title,
                "duration": f"{t.duration_minutes} min",
                "priority": str(t.priority),
                "status": "done" if t.completed else "pending",
            }
            for t in shown
        ]
    )
else:
    st.info("No tasks yet. Add one above (the daily walk is included automatically).")

# Conflict check across all of the owner's pets.
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        st.warning(warning)
else:
    st.success("No scheduling conflicts.")

st.divider()

# ---------------------------------------------------------------------------
# Build & explain the daily schedule for the selected pet.
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    schedule = Schedule(day=date.today(), pet=pet)
    plan = schedule.build_plan()
    if not plan:
        st.info("Nothing to schedule yet — add a task above.")
    else:
        st.success(f"Planned {len(plan)} task(s) for {pet.name}.")
        st.markdown(f"### Today's Schedule for {pet.name} ({pet.species})")
        st.table(
            [
                {
                    "time": t.time,
                    "task": t.title,
                    "duration": f"{t.duration_minutes} min",
                    "priority": str(t.priority),
                }
                for t in plan
            ]
        )
        with st.expander("Why this plan?", expanded=True):
            st.text(schedule.explain())
