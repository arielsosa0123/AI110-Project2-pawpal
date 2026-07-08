"""Tests for the PawPal+ domain classes and Scheduler algorithms."""

from datetime import date

import pytest

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


# ---------------------------------------------------------------------------
# Basics
# ---------------------------------------------------------------------------
def test_mark_done_changes_task_status():
    """Task completion: mark_done() flips completed from False to True."""
    task = Task("Morning walk", time="08:00", duration_minutes=20, priority="high")
    assert task.completed is False

    task.mark_done()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Task addition: adding a task to a Pet increases its task count."""
    pet = Pet(name="Mochi", species="dog", walk_time="08:00", walk_duration=30)
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Feeding", time="09:00", duration_minutes=10, priority="high"))

    assert len(pet.get_tasks()) == 1


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------
def test_sort_by_time_returns_chronological_order():
    """Sorting: tasks come back in chronological (earliest-first) order."""
    tasks = [
        Task("Fetch", "16:30", 25),
        Task("Breakfast", "09:00", 10),
        Task("Meds", "07:30", 5),
    ]

    ordered = Scheduler.sort_by_time(tasks)

    assert [t.time for t in ordered] == ["07:30", "09:00", "16:30"]


def test_sort_by_time_empty_list():
    """Sorting an empty list returns an empty list, not an error."""
    assert Scheduler.sort_by_time([]) == []


def test_build_plan_priority_ties_broken_by_time():
    """Two high-priority tasks: the earlier time is scheduled first."""
    pet = Pet(name="Mochi", species="dog", walk_time="08:00", walk_duration=30)
    pet.add_task(Task("Breakfast", "09:00", 10, priority="high"))
    pet.add_task(Task("Meds", "07:30", 5, priority="high"))

    plan = Schedule_of(pet).build_plan()
    times = [t.time for t in plan if t.priority == Priority.HIGH]

    # 07:30 walk, 07:30 meds, 09:00 breakfast are all high; earliest first.
    assert times == sorted(times)


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------
def test_completing_daily_task_creates_next_day_task():
    """Recurrence: completing a daily task creates a new task for the next day."""
    owner, pet = owner_with_pet()
    meds = Task("Meds", "07:30", 5, priority="high", frequency="daily",
                due_date=date(2026, 7, 8))
    pet.add_task(meds)

    follow_up = Scheduler(owner).complete_task(meds, pet)

    assert meds.completed is True
    assert follow_up is not None
    assert follow_up.due_date == date(2026, 7, 9)   # today + 1 day
    assert follow_up.completed is False
    assert follow_up in pet.get_tasks()


def test_weekly_recurrence_crosses_month_boundary():
    """timedelta handles month/year rollover: weekly task +7 days."""
    task = Task("Grooming", "10:00", 45, frequency="weekly",
                due_date=date(2026, 12, 28))

    follow_up = task.next_occurrence()

    assert follow_up.due_date == date(2027, 1, 4)


def test_completing_once_task_creates_no_followup():
    """A one-off task produces no follow-up and doesn't grow the pet's list."""
    owner, pet = owner_with_pet()
    task = Task("Vet visit", "14:00", 60)  # frequency defaults to "once"
    pet.add_task(task)
    before = len(pet.get_tasks())

    follow_up = Scheduler(owner).complete_task(task, pet)

    assert follow_up is None
    assert len(pet.get_tasks()) == before


def test_next_occurrence_preserves_fields_and_resets_completed():
    """The next instance keeps time/priority/frequency but is not completed."""
    task = Task("Meds", "07:30", 5, priority="high", frequency="daily",
                due_date=date(2026, 7, 8), completed=True)

    follow_up = task.next_occurrence()

    assert follow_up.title == "Meds"
    assert follow_up.time == "07:30"
    assert follow_up.priority == Priority.HIGH
    assert follow_up.frequency == "daily"
    assert follow_up.completed is False


def test_invalid_frequency_raises():
    """An unsupported frequency is rejected at construction time."""
    with pytest.raises(ValueError):
        Task("Bad", "10:00", 5, frequency="hourly")


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------
def test_detect_conflicts_flags_duplicate_times():
    """Conflict detection: two tasks at the same time are flagged."""
    owner, pet = owner_with_pet()
    pet.add_task(Task("Vet call", "12:00", 15))
    pet.add_task(Task("Brushing", "12:00", 10))

    conflicts = Scheduler(owner).detect_conflicts()

    assert len(conflicts) == 1
    assert "12:00" in conflicts[0]


def test_detect_conflicts_across_different_pets():
    """A shared time slot across two different pets is also flagged."""
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog", "08:00", 30)
    cat = Pet("Luna", "cat", "07:30", 10)
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task("Walk-in vet", "12:00", 15))
    cat.add_task(Task("Nail trim", "12:00", 10))

    conflicts = Scheduler(owner).detect_conflicts()

    assert len(conflicts) == 1
    assert "Mochi" in conflicts[0] and "Luna" in conflicts[0]


def test_detect_conflicts_ignores_completed_tasks():
    """A completed task does not conflict with a pending one at the same time."""
    owner, pet = owner_with_pet()
    done = Task("Old appt", "12:00", 15)
    done.mark_done()
    pet.add_task(done)
    pet.add_task(Task("New appt", "12:00", 15))

    assert Scheduler(owner).detect_conflicts() == []


def test_detect_conflicts_ignores_overlapping_durations():
    """Documented tradeoff: only exact time matches conflict, not overlaps.

    An 08:00 (30 min) task and an 08:15 task overlap in real time but are NOT
    flagged, because detect_conflicts compares start times only.
    """
    owner, pet = owner_with_pet()
    pet.add_task(Task("Walk", "08:00", 30))
    pet.add_task(Task("Feeding", "08:15", 10))

    assert Scheduler(owner).detect_conflicts() == []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def owner_with_pet():
    """Return an (owner, pet) pair with the pet already attached."""
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog", walk_time="08:00", walk_duration=30)
    owner.add_pet(pet)
    return owner, pet


def Schedule_of(pet):
    """Build a Schedule for the given pet on a fixed day."""
    from pawpal_system import Schedule
    return Schedule(day=date(2026, 7, 8), pet=pet)
