# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


### Testing PawPal+

```bash
python -m pytest
```

| Test | What it checks |
|---|---|
| `test_mark_complete_sets_last_completed_date` | `mark_complete()` sets `last_completed_date` to today |
| `test_add_task_increases_pet_task_count` | Adding a task to a pet increases its task count by 1 |
| `test_sort_by_time_returns_chronological_order` | Tasks sort earliest-first; tasks with no time sort last |
| `test_complete_and_reschedule_creates_next_day_task` | Completing a daily task marks it done and adds a new task due tomorrow |
| `test_detect_conflicts_flags_same_time_tasks` | Two tasks at the same time produce a `CONFLICT` warning with the correct time |
| `test_detect_conflicts_no_warnings_for_different_times` | Tasks at different times produce no warnings |
