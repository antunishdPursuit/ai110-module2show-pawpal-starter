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

Sorting:
Passes tasks in wrong order (noon, no-time, morning) to prove the sort is actually doing work, not just returning input order.
Checks all three positions so a partial sort can't accidentally pass.

Recurrence:
test_complete_and_reschedule_creates_next_day_task
Verifies three things at once: the original task is marked done, the pet now has 2 tasks, and the new task's next_due_date is exactly tomorrow.

Conflict Detection:
The positive case (test_detect_conflicts_flags_same_time_tasks) checks that a warning exists and that the string contains "08:00 AM" — so it's not just checking for any warning, but the right one.
The negative case (test_detect_conflicts_no_warnings_for_different_times) ensures the function doesn't fire false positives.

### "Confidence Level" 
3/5 Stars

---

## Features

### Owner & Pet Management

- Create a named owner and register multiple pets (name, species, age)
- Pets are stored in session state so they persist across Streamlit reruns

### Task Scheduling

- Add care tasks (walks, feeding, meds, grooming, etc.) to any registered pet
- Choose a **schedule type**: Daily (every day), Weekly (every 7 days), or Custom (any interval in days)
- Optionally set a **time of day** for each task so the daily view can order them chronologically

### Sorting by Time (`Scheduler.sort_by_time`)

- Tasks are sorted ascending by `time_of_day` before display
- Tasks with no time set sort to the bottom ("Anytime") so timed tasks always appear first

### Conflict Detection (`Scheduler.detect_conflicts`)

- Scans all tasks due today for overlapping `time_of_day` values
- Any two tasks sharing the exact same time slot trigger a named warning: which tasks conflict and at what time
- Conflicts are surfaced as a prominent error banner in the UI with a drill-down expander listing each conflict

### Status Filtering (`Scheduler.filter_tasks`)

- Filter today's tasks by status (`pending`, `done`, `overdue`) and/or by pet name in a single pass
- Combines both filters together so results match both criteria simultaneously

### Daily Recurrence (`Scheduler.complete_and_reschedule`)

- Marking a task done calls `mark_complete()`, which records today's date and advances `schedule.next_due_date` by the task's interval
- For Daily and Weekly tasks, a new `Task` instance is automatically created for the next occurrence and added to the pet
- Custom-interval tasks are advanced but do not auto-create a new instance

### Status Derivation (`Task.status` property)

- Status is computed at read time — no stored state to go stale
- `done` if `last_completed_date` is today; `overdue` if `next_due_date` is in the past; `pending` otherwise

### UI Summary Metrics

- Displays a live count of **Pending / Overdue / Done** tasks at the top of the daily schedule
- Overdue count is highlighted in red using Streamlit's `delta_color="inverse"` to prompt action
