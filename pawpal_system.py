"""PawPal+ system classes.

Domain model for the PawPal+ pet-care planner. Mirrors diagrams/uml.mmd:
Owner -> Pet -> Task, with Schedule building an ordered daily plan and Priority
ranking tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import IntEnum


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

    def __post_init__(self) -> None:
        # Accept "high"/3/Priority.HIGH from callers (e.g. the Streamlit UI).
        self.priority = Priority.from_value(self.priority)

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reschedule(self, time: str) -> None:
        """Move this task to a new time."""
        self.time = time


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
