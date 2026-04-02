# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
we should be able to upload the pet's details, assign tasks associated with the pet, and then create a daily plan to do it.
1. Pet
Attributes:
petId
name
species (dog, cat, etc.)
age

Methods:
addTask(task)
removeTask(task)
getTasks()

2. Task
Attributes:
taskId
title (e.g., “Feed”, “Walk”)
description
frequency
assignedPet

Methods:
markComplete()
updateTask()

3. Schedule
Attributes:
type (daily, weekly, custom)
interval (e.g., every 2 days)
startDate
nextDueDate

Methods:
calculateNextDueDate()
isDueToday()

4. Owner 
Attributes:
userId
name

Methods:
addPet()
viewDailyPlan()

- What classes did you include, and what responsibilities did you assign to each?
    the classess we needed are pets, tasks, and frequency.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
These are the changes made. 
Schedule
    Change	Reason
type → schedule_type + ScheduleType Enum	Avoids shadowing the Python built-in; Enum prevents invalid string values like "biweekly"
calculate_next_due_date() implemented	Advances next_due_date by interval days and updates self.next_due_date in place — resolves the ambiguous return-vs-mutate issue
is_due_today() uses <= instead of ==	Catches overdue/missed tasks — a task due yesterday still needs to show up today
Task

Change	Reason
mark_complete() implemented	Now sets last_completed_date and calls schedule.calculate_next_due_date() only if a schedule exists
update_task() given parameters	Added title and description as optional kwargs — previously had no way to actually update anything
Pet

Change	Reason
All stubs implemented	add_task, remove_task, get_tasks all filled in
remove_task matches by task_id	Avoids silent failures from object reference mismatches
get_due_tasks_today() has null guard	Skips tasks where schedule is None — prevents the AttributeError crash
Owner

Change	Reason
add_pet() implemented	Appends to self.pets
remove_pet(pet_id) added	Symmetric with add_pet; matches by pet_id
find_pet(pet_id) added	Resolves the Task → Pet navigation gap — given a task.assigned_pet_id, you can now look up the pet
view_daily_plan() implemented	Returns a dict of {pet_name: [due_tasks]} — structured and easy to display or iterate
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
