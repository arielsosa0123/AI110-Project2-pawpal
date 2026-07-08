"""PawPal+ system classes.

Skeleton generated from diagrams/uml_draft.mmd.
Method bodies are stubs -- implement the scheduling logic next.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    """A single pet-care task (e.g. a walk, a feeding)."""

    title: str
    time: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    completed: bool = False

    def mark_done(self) -> None:
        """Mark this task as completed."""
        raise NotImplementedError

    def reschedule(self, time: str) -> None:
        """Move this task to a new time."""
        raise NotImplementedError


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
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        raise NotImplementedError

    def get_tasks(self) -> list[Task]:
        """Return this pet's care tasks."""
        raise NotImplementedError


class Owner:
    """A pet owner who can own many pets."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner (and set the back-reference)."""
        raise NotImplementedError

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        raise NotImplementedError

    def get_pets(self) -> list[Pet]:
        """Return this owner's pets."""
        raise NotImplementedError


class Schedule:
    """A day's plan of tasks for a single pet."""

    def __init__(self, day: date, pet: Pet) -> None:
        self.day = day
        self.pet = pet
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to this schedule."""
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        """Remove a task from this schedule."""
        raise NotImplementedError

    def todays_tasks(self) -> list[Task]:
        """Return the tasks scheduled for today."""
        raise NotImplementedError

    def build_plan(self) -> list[Task]:
        """Choose and order tasks based on priority, time, and constraints."""
        raise NotImplementedError

    def explain(self) -> str:
        """Explain why each task was chosen and when it happens."""
        raise NotImplementedError
