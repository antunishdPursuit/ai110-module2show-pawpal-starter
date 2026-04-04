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
it shows the time, frequency, and we can decided which pet is it for
- How did you decide which constraints mattered most?
I wanted something easy to implement so it can easier to update the UI
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
sort_by_time — dropped strftime("%H:%M"), now uses native time object comparison via tuple sort
detect_conflicts — renamed t → slot to remove the shadow on the time import; flattened the inner loop into a list comprehension
filter_tasks — single-pass comprehension, dict only built when pet_name is actually provided
complete_and_reschedule — removed the print() so no terminal noise bleeds through when called from the UI
- Why is that tradeoff reasonable for this scenario?
so it can make more sense in the UI. It has to be easier for users to use 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
The way i used AI was to let it guide me to solutions and think about how they work in the context of this project. I wanted to know why it thought certain choices were better than others and how I would explain it to people I just met. 
- What kinds of prompts or questions were most helpful?
The mermaid diagram was the most helpful becuase it made me think how each compenont of my app works. I also wanted to see what data I needed to store and what data needed to added. It gave a great visual of what was needed and not needed.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One suggesstion I didn't agree was with the implemntation of the classes. It wanted to connect the owner to the tasks but I made sure to change it so that owner had many pets and that 1 pet can have many tasks
- How did you evaluate or verify what the AI suggested?
I just tested what was given to me. I found it was better to see if it worked then just revert back to a previous implemtation of the code in case anything broke. I also read the code to see if it was easily fixable or not
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I thought each test would fail and I would have to work on it for a longer time than expected but it was easily done. I was able to get the tests done after a few implemnations of prompts and code changes
- Why were these tests important?
Any codebase should have tests in place to check if something is working without having to turn on the server. Also, its a great way to check if something is working or not
**b. Confidence**

- How confident are you that your scheduler works correctly?
I'm pretty confident it works as intended but I made a few more changes so that the UI can work more intuitively. 
- What edge cases would you test next if you had more time?
I would test for multuple pets with multiple tasks, two pets having the same task, and duplicate owners and pets. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm most satisifed seeing how AI was able to help with creating, debugging, and understanding the code. It was a seamless experience and I hope to contunie using AI for the forseeable future. I alos like that the UI was improved after a few suggestions. Of course I want to do more but I like the way it looks now compared to the beginning.
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I want to make the UI look even better. I was looking up more desgins online but I wanted something less complicated for a simple app. I want to get better at prompting and context so that the next project can look amazing. 
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
AI is not going to do everything for me. I still need to prompt and nudge it to work more smoothly and I'm hoping to improve this skill for the next project. Also, AI can already do a lot of things I haven't thought of before so I'm interested in doing more and also exploring more the capabilities of AI. 