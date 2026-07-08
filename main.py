"""PawPal+ demo script.

Builds a small owner/pet/task setup and prints today's schedule for each pet.
Run with:  python main.py
"""

from datetime import date

from pawpal_system import Owner, Pet, Schedule, Task


def main() -> None:
    # 1. Create an owner.
    owner = Owner("Jordan")

    # 2. Create at least two pets and attach them to the owner.
    mochi = Pet(name="Mochi", species="dog", walk_time="08:00", walk_duration=30)
    luna = Pet(name="Luna", species="cat", walk_time="07:30", walk_duration=10)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # 3. Add at least three tasks with different times to the pets.
    mochi.add_task(Task("Breakfast", time="09:00", duration_minutes=10, priority="high"))
    mochi.add_task(Task("Meds", time="07:30", duration_minutes=5, priority="high"))
    mochi.add_task(Task("Fetch in the park", time="16:30", duration_minutes=25, priority="low"))

    luna.add_task(Task("Feeding", time="08:15", duration_minutes=10, priority="high"))
    luna.add_task(Task("Litter cleaning", time="12:00", duration_minutes=10, priority="medium"))
    luna.add_task(Task("Play with feather toy", time="19:00", duration_minutes=15, priority="low"))

    # 4. Print today's schedule for each of the owner's pets.
    today = date.today()
    print(f"===== Today's Schedule for {owner.name}'s pets =====\n")
    for pet in owner.get_pets():
        schedule = Schedule(day=today, pet=pet)
        print(schedule.explain())
        print()


if __name__ == "__main__":
    main()
