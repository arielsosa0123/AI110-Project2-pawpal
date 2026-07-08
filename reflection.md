# PawPal+ Project Reflection

## 1. System Design

Brainstorm Ideas
- Pet
    - Add a pet
    - Remove a pet
    - Name
    - Time for walk and duration
- Owner
    - Add an Owner
    - Remove an Owner
    - Name
    - Pet
    - Time for walk and duration
- Task
    - New Task
    - Remove
    - Time
    - Duration
- Schedule
    - Toaday's Tasks
    - Add a Task
    - Remove a task

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    I think the initial UML design is pretty solid, having the main relationships between the classes is what is most important. I did not spot any immediate issues.

    We have plenty of attributes for each class that allow for Owners and pets to have a direct relationship. Owner just has its name and list of pets or pet. we are allowed to add, remove, and get pets(). For Pets, we have plenty of attributes such as name, species, its owner, a list of tasks, Walking time and duration. Task extends the pets class, by allowing each pet to have any additional care tasks, holding attributes like title, time, duration_minutes, most importantly priority, and a completed attribute. Schedule extends both pet and task, by allowing to build scheudle based on pets walks, and any additional tasks provided for each pet. Attributes especially important is date, time, and list of tasks. Having additional methods to explain the schedule, build_plan, today's tasks, and etc.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    Yes, I added a has_tasks() attribute to the pet. Which makes it easier for the sceduler to navigate a pet based soley on walking schedule or having to check for additional tasks to schedule. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

    The scheduler mostly looks at two things, time and priority. Priority is the big one since that decides what gets done first when the day fills up. High priority stuff like meds and feeding gets pushed to the top and then everything else falls in after that. Time is the tiebreaker so if two tasks are both high priority the earlier one just goes first. I picked those two because they match how a real owner actually thinks about their day. You care most about the important stuff getting done and after that you just go in order of the clock. Duration is tracked too so the plan can show total care time but it does not really drive the ordering.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

    One tradeoff is that my conflict detection only catches tasks that start at the exact same time. So if a walk starts at 08:00 and runs 30 minutes and a feeding is set for 08:15 it will not warn me even though those actually overlap in real life. I went with the simpler version on purpose. Checking for exact matches is easy to read and it never crashes, it just groups tasks by their time and warns when a slot has more than one thing in it. Doing full overlap checking would mean turning every time into minutes and comparing ranges which is more code and more edge cases for something that is really just a daily helper. For a busy pet owner catching the obvious double books covers the common case and I left the overlap thing as a future improvement.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

    I used AI a good amount through this whole thing. Early on it helped me brainstorm the classes and talk through how Owner, Pet, Task and Schedule should relate to each other. Later it was more about the actual implementation, stuff like how to sort my tasks by time with a lambda key and how to use timedelta so recurring tasks land on the right day. It also helped me think through edge cases for my tests. The prompts that worked best were the specific ones where I already knew what I wanted and just needed the how. The vague questions gave me pretty generic answers but when I asked something like how do I sort HH:MM strings correctly I got exactly what I needed.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

    There was a moment where the AI wanted to fold the recurring task logic straight into mark_done so finishing a task would spawn the next one automatically. I did not go with that because I already had a test that just checked mark_done flips the completed flag and I did not want that method doing two jobs at once. Instead I kept mark_done simple and put the recurrence in complete_task on the scheduler. To verify things I mostly leaned on running main.py and my tests. If the AI gave me something I would run it and actually look at the output to make sure the dates and ordering were right instead of just trusting that it looked correct.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

    I tested the main behaviors of the scheduler. Sorting to make sure tasks come back in time order, recurrence to confirm that finishing a daily task creates a new one for the next day, and conflict detection to check it flags two tasks at the same time. I also added smaller ones like an empty list not blowing up, a one off task not creating a follow up, and a bad frequency getting rejected. These felt important because they are the parts a user would actually notice if they broke. If my sorting was off or a recurring task did not come back the whole plan would feel broken.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

    I feel pretty confident the scheduler does what it is supposed to for normal use since all my tests pass and the demo runs clean. The stuff I am less sure about is the messier real world cases. If I had more time I would test times that are not zero padded since my sorting kind of assumes HH:MM, and I would test tasks whose durations overlap instead of just matching start times. Those are the spots where I know the current logic is making an assumption.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    I am most satisfied with how the scheduling logic came together. Getting the plan to sort by priority and then time and actually explain itself in plain english felt good. The recurring task piece was also satisfying because once it worked it just handled itself.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    If I did another pass I would make the conflict detection smarter so it looks at whether tasks actually overlap instead of just sharing a start time. I would also probably clean up how the walk gets added since right now it lives kind of separately from the normal tasks and that makes a couple things a little awkward.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    The biggest thing I learned is that designing the classes first actually pays off. Having the UML and knowing how Owner, Pet, Task and Schedule fit together meant that when I went to build the logic I was not fighting my own structure. And with AI the takeaway was that it is way more useful when I come in with a clear idea of what I want and use it to move faster instead of asking it to figure everything out for me.
