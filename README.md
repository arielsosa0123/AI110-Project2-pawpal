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

## ✨ Features

- **Priority-based daily plan** — orders a pet's tasks by priority (high → low), breaking ties by earliest time, and skips anything already completed (`Schedule.build_plan()`).
- **Sorting by time** — returns tasks in chronological order using their `"HH:MM"` time (`Scheduler.sort_by_time()`).
- **Filtering** — show one pet's tasks (`Scheduler.filter_by_pet()`) or only pending/completed tasks (`Scheduler.filter_by_status()`).
- **Conflict warnings** — flags when two tasks (same pet or different pets) are booked for the same time and returns a plain warning instead of crashing (`Scheduler.detect_conflicts()`).
- **Daily & weekly recurrence** — completing a recurring task automatically creates its next occurrence, with the due date advanced by 1 or 7 days (`Task.next_occurrence()`, `Scheduler.complete_task()`).
- **Automatic walk** — each pet's daily walk is included in the plan without adding it as a separate task (`Pet.walk_task()`).
- **Plan explanation** — a readable summary of what happens when and total care time (`Schedule.explain()`).

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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Total care time: 70 min across 4 task(s).

Daily plan for Luna (cat) on 2026-07-08:
  07:30 — Walk Luna (10 min) [priority: high]
  08:15 — Feeding (10 min) [priority: high]
  12:00 — Litter cleaning (10 min) [priority: medium]
  19:00 — Play with feather toy (15 min) [priority: low]
Total care time: 45 min across 4 task(s).

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

Take 1:
=================================================================================== test session starts ===================================================================================
platform win32 -- Python 3.13.12, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\ariel\OneDrive\Documents\CodePath\AI110\Project2-PawPal\AI110-Project2-pawpal
plugins: anyio-4.14.1
collected 2 items                                                                                                                                                                          

tests\test_pawpal.py ..                                                                                                                                                              [100%]

==================================================================================== 2 passed in 0.07s ====================================================================================

Take 2:
=================================================================================== test session starts ===================================================================================
platform win32 -- Python 3.13.12, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\ariel\OneDrive\Documents\CodePath\AI110\Project2-PawPal\AI110-Project2-pawpal
plugins: anyio-4.14.1
collected 14 items                                                                                                                                                                         

tests\test_pawpal.py ..............                                                                                                                                                  [100%]

=================================================================================== 14 passed in 0.09s ====================================================================================

## 📐 Smarter Scheduling

The `Scheduler` class in `pawpal_system.py` adds algorithms on top of the core
domain model. Each feature and the method that implements it:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks by their `"HH:MM"` time using `sorted()` with a lambda key; zero-padded 24h strings sort correctly as text. `Schedule.build_plan()` additionally orders by priority, then time. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Return one pet's tasks by name, or only completed/pending tasks. |
| Conflict handling | `Scheduler.detect_conflicts()` | Lightweight check that returns warning strings (never raises) when two pending tasks — for the same or different pets — share the exact same start time. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.complete_task()` | Completing a `daily`/`weekly` task auto-creates its next instance; the new due date is computed with `timedelta` (today + 1 or + 7 days). |

## 📸 Demo Walkthrough

1. Type the owner's name in the Owner field.
2. Fill out the Add a Pet form (name, species, walk time, walk duration) and click Add pet. You can add more than one pet.
3. Pick which pet you're planning for from the dropdown.
4. Add some tasks with the Add a Task form (title, time, duration, priority). They show up in the tasks table, and the pet's daily walk is added for you.
5. Click Generate schedule to see the day's plan ordered by priority and time, plus a "Why this plan?" section that explains it.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
