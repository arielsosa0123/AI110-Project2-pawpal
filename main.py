"""PawPal+ demo script.

Builds a small owner/pet/task setup and exercises the Scheduler algorithms:
sorting by time, filtering by pet/status, recurring tasks, and conflict
detection. Run with:  python main.py
"""

from datetime import date

from pawpal_system import Owner, Pet, Schedule, Scheduler, Task


def hr(title: str) -> None:
    """Print a labeled section divider."""
    print(f"\n{'=' * 55}\n{title}\n{'=' * 55}")


def main() -> None:
    # 1. Create an owner.
    owner = Owner("Jordan")

    # 2. Create at least two pets and attach them to the owner.
    mochi = Pet(name="Mochi", species="dog", walk_time="08:00", walk_duration=30)
    luna = Pet(name="Luna", species="cat", walk_time="07:30", walk_duration=10)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # 3. Add tasks OUT OF ORDER so sorting has something to do.
    mochi.add_task(Task("Fetch in the park", "16:30", 25, priority="low"))
    mochi.add_task(Task("Breakfast", "09:00", 10, priority="high"))
    mochi.add_task(Task("Meds", "07:30", 5, priority="high", frequency="daily"))
    luna.add_task(Task("Play with feather toy", "19:00", 15, priority="low"))
    luna.add_task(Task("Feeding", "08:15", 10, priority="high", frequency="daily"))

    scheduler = Scheduler(owner)

    # --- Today's schedule (per pet) --------------------------------------
    hr(f"Today's Schedule for {owner.name}'s pets")
    for pet in owner.get_pets():
        print(Schedule(day=date.today(), pet=pet).explain())
        print()

    # --- Sorting by time -------------------------------------------------
    hr("Mochi's tasks sorted by time (Scheduler.sort_by_time)")
    for task in scheduler.sort_by_time(mochi.get_tasks()):
        print(f"  {task.time} -- {task.title}")

    # --- Filtering -------------------------------------------------------
    hr("Filtering (filter_by_pet / filter_by_status)")
    print("Luna's tasks:")
    for task in scheduler.filter_by_pet("Luna"):
        print(f"  {task.time} -- {task.title}")

    mochi.get_tasks()[0].mark_done()  # complete one task to show the filter
    pending = scheduler.filter_by_status(mochi.get_tasks(), completed=False)
    print(f"\nMochi's PENDING tasks ({len(pending)}):")
    for task in pending:
        print(f"  {task.time} -- {task.title}")

    # --- Recurring tasks -------------------------------------------------
    hr("Recurring tasks (complete_task auto-creates next occurrence)")
    daily_meds = next(t for t in mochi.get_tasks() if t.title == "Meds")
    daily_meds.due_date = date.today()
    print(f"Before: Mochi has {len(mochi.get_tasks())} tasks.")
    follow_up = scheduler.complete_task(daily_meds, mochi)
    print(f"Completed '{daily_meds.title}' -> next occurrence due {follow_up.due_date}.")
    print(f"After:  Mochi has {len(mochi.get_tasks())} tasks.")

    # --- Conflict detection ----------------------------------------------
    hr("Conflict detection (two tasks at the same time)")
    mochi.add_task(Task("Vet call", "12:00", 15, priority="medium"))
    luna.add_task(Task("Brushing", "12:00", 10, priority="medium"))
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts found.")


if __name__ == "__main__":
    main()
