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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
