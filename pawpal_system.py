"""PawPal+ system classes.

Domain model for the PawPal+ pet-care planner. Mirrors diagrams/uml.mmd:
Owner -> Pet -> Task, with Schedule building an ordered daily plan and Priority
ranking tasks.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import IntEnum

# How often a task repeats. "once" tasks never regenerate; "daily"/"weekly"
# tasks spawn their next occurrence when completed.
FREQUENCIES = ("once", "daily", "weekly")


class Priority(IntEnum):
    """How important a task is. Higher value == scheduled earlier."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @classmethod
    def from_value(cls, value: "Priority | str | int") -> "Priority":
        """Coerce a Priority, a name ("high"), or a rank (3) into a Priority."""
        if isinstance(value, Priority):
            return value
        if isinstance(value, int):
            return cls(value)
        return cls[value.strip().upper()]

    def __str__(self) -> str:
        return self.name.lower()


@dataclass
class Task:
    """A single pet-care task (e.g. a walk, a feeding)."""

    title: str
    time: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    frequency: str = "once"  # "once" | "daily" | "weekly"
    due_date: date | None = None

    def __post_init__(self) -> None:
        # Accept "high"/3/Priority.HIGH from callers (e.g. the Streamlit UI).
        self.priority = Priority.from_value(self.priority)
        self.frequency = self.frequency.strip().lower()
        if self.frequency not in FREQUENCIES:
            raise ValueError(
                f"frequency must be one of {FREQUENCIES}, got {self.frequency!r}"
            )

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reschedule(self, time: str) -> None:
        """Move this task to a new time."""
        self.time = time

    def is_recurring(self) -> bool:
        """True if this task repeats (daily or weekly)."""
        return self.frequency in ("daily", "weekly")

    def next_occurrence(self) -> "Task | None":
        """Return the next instance of a recurring task, or None if one-off.

        The new task keeps the same time/duration/priority/frequency but is
        not completed, and its due_date advances by one day (daily) or seven
        days (weekly) from this task's due_date (or today if unset).
        """
        if not self.is_recurring():
            return None
        step = timedelta(days=1) if self.frequency == "daily" else timedelta(days=7)
        base = self.due_date or date.today()
        return Task(
            title=self.title,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            completed=False,
            frequency=self.frequency,
            due_date=base + step,
        )


@dataclass
class Pet:
    """A pet that care tasks are planned for."""

    name: str
    species: str
    walk_time: str
    walk_duration: int
    owner: "Owner | None" = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's care tasks."""
        return list(self.tasks)

    def walk_task(self) -> Task:
        """Represent the pet's daily walk as a high-priority Task."""
        return Task(
            title=f"Walk {self.name}",
            time=self.walk_time,
            duration_minutes=self.walk_duration,
            priority=Priority.HIGH,
        )


class Owner:
    """A pet owner who can own many pets."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner (and set the back-reference)."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        if pet in self.pets:
            self.pets.remove(pet)
            if pet.owner is self:
                pet.owner = None

    def get_pets(self) -> list[Pet]:
        """Return this owner's pets."""
        return list(self.pets)


class Schedule:
    """A day's plan of tasks for a single pet."""

    def __init__(self, day: date, pet: Pet) -> None:
        self.day = day
        self.pet = pet
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to this schedule."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this schedule."""
        if task in self.tasks:
            self.tasks.remove(task)

    def todays_tasks(self) -> list[Task]:
        """Return the tasks scheduled for today (the pet's walk + its tasks)."""
        return [self.pet.walk_task(), *self.pet.get_tasks(), *self.tasks]

    def build_plan(self) -> list[Task]:
        """Choose and order tasks based on priority, then time.

        Completed tasks are dropped. Remaining tasks are ordered highest
        priority first, breaking ties by earliest scheduled time.
        """
        pending = [task for task in self.todays_tasks() if not task.completed]
        return sorted(
            pending,
            key=lambda task: (-int(task.priority), task.time),
        )

    def explain(self) -> str:
        """Explain why each task was chosen and when it happens."""
        plan = self.build_plan()
        header = f"Daily plan for {self.pet.name} ({self.pet.species}) on {self.day}:"
        if not plan:
            return f"{header}\n  Nothing to do today \N{PARTY POPPER}"

        lines = [header]
        for task in plan:
            lines.append(
                f"  {task.time} \N{EM DASH} {task.title} "
                f"({task.duration_minutes} min) [priority: {task.priority}]"
            )
        total = sum(task.duration_minutes for task in plan)
        lines.append(f"Total care time: {total} min across {len(plan)} task(s).")
        return "\n".join(lines)


class Scheduler:
    """Algorithms over an owner's tasks: sorting, filtering, recurrence, and
    conflict detection.

    Built around an :class:`Owner` so it can see every pet's tasks at once,
    which is what makes cross-pet conflict detection and per-pet filtering
    possible. The sorting/filtering helpers are static so they can also be
    used on any loose list of tasks.
    """

    def __init__(self, owner: Owner | None = None) -> None:
        self.owner = owner

    # -- sorting -----------------------------------------------------------
    @staticmethod
    def sort_by_time(tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by their "HH:MM" time, earliest first.

        Zero-padded 24-hour strings sort correctly as plain text, so the
        lambda key just returns ``task.time`` -- no time parsing needed.
        """
        return sorted(tasks, key=lambda task: task.time)

    # -- filtering ---------------------------------------------------------
    @staticmethod
    def filter_by_status(tasks: list[Task], completed: bool = False) -> list[Task]:
        """Return only tasks whose completed flag matches ``completed``."""
        return [task for task in tasks if task.completed == completed]

    def all_tasks(self) -> list[Task]:
        """Return every task across all of the owner's pets."""
        tasks: list[Task] = []
        if self.owner is not None:
            for pet in self.owner.get_pets():
                tasks.extend(pet.get_tasks())
        return tasks

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return the tasks belonging to the pet with the given name."""
        if self.owner is None:
            return []
        for pet in self.owner.get_pets():
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    # -- recurring tasks ---------------------------------------------------
    def complete_task(self, task: Task, pet: Pet) -> Task | None:
        """Mark a task complete and auto-create its next occurrence.

        Returns the newly created follow-up task (added to ``pet``) for a
        recurring task, or None for a one-off task.
        """
        task.mark_done()
        follow_up = task.next_occurrence()
        if follow_up is not None:
            pet.add_task(follow_up)
        return follow_up

    # -- conflict detection ------------------------------------------------
    def detect_conflicts(self) -> list[str]:
        """Return warning strings for pending tasks sharing the same time slot.

        Lightweight: it only compares exact start times (not overlapping
        durations) and never raises -- an empty list means "no conflicts".
        Tasks are compared across every pet, so a dog walk and a cat feeding
        booked for the same minute are flagged.
        """
        by_time: dict[str, list[str]] = defaultdict(list)
        if self.owner is not None:
            for pet in self.owner.get_pets():
                for task in pet.get_tasks():
                    if not task.completed:
                        by_time[task.time].append(f"{task.title} ({pet.name})")

        warnings: list[str] = []
        for slot, labels in sorted(by_time.items()):
            if len(labels) > 1:
                warnings.append(
                    f"\N{WARNING SIGN} Conflict at {slot}: " + ", ".join(labels)
                )
        return warnings
