"""Basic tests for the PawPal+ domain classes."""

from pawpal_system import Pet, Task


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
