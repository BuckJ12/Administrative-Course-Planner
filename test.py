import pandas as pd
from ortools.sat.python import cp_model

# Define the model
model = cp_model.CpModel()

# Example data
courses = ["Math 101", "CS 101", "CS 201", "Physics 102", "History 105"]
sections_per_course = {"Math 101": 2, "CS 101": 2, "CS 201": 1, "Physics 102": 2, "History 105": 1}
meeting_days = {"Math 101": "MWF", "CS 101": "MWF", "CS 201": "MWF", "Physics 102": "MWF", "History 105": "TTh"}

# Professors available for each course
professors = {
    "Math 101": ["Dr. Smith", "Dr. Johnson"],
    "CS 101": ["Dr. Brown", "Dr. Green"],
    "CS 201": ["Dr. Brown"],
    "Physics 102": ["Dr. Green", "Dr. Miller"],
    "History 105": ["Dr. White"]
}

# Define max credit hours each professor can teach
max_credits = {"Dr. Smith": 16, "Dr. Johnson": 16, "Dr. Brown": 18, "Dr. Green": 16, "Dr. Miller": 16, "Dr. White": 14}
credit_hours = {"Math 101": 3, "CS 101": 3, "CS 201": 4, "Physics 102": 3, "History 105": 2}

# Time slots
time_slots = {
    "MWF": ["8AM", "9:30AM", "11AM", "12:30PM", "2PM", "3:30PM"],
    "TTh": ["8AM", "9:30AM", "11AM", "12:30PM", "2PM", "3:30PM"]
}

# Room capacities
rooms = ["Room A", "Room B", "Lab Room C"]
room_capacity = {"Room A": 30, "Room B": 50, "Lab Room C": 40}

# Some courses can only be held in specific rooms
room_restrictions = {
    "CS 201": ["Lab Room C"],  # CS 201 can only be held in the Lab
    "Physics 102": ["Room A", "Room B"],  # Physics can be held in standard classrooms
}

# Course enrollment limits
course_max_students = {"Math 101": 25, "CS 101": 40, "CS 201": 30, "Physics 102": 35, "History 105": 20}

# Create decision variables
schedule = {}
prof_workload = {prof: model.NewIntVar(0, max_credits[prof], f"workload_{prof}") for prof in max_credits.keys()}

for course, num_sections in sections_per_course.items():
    for sec in range(num_sections):
        for prof in professors[course]:
            for t in range(len(time_slots[meeting_days[course]])):  # Restrict to valid meeting days
                for r, room in enumerate(rooms):
                    if course in room_restrictions and room not in room_restrictions[course]:
                        continue  # Skip rooms that this course cannot be in

                    schedule[(course, sec, prof, t, r)] = model.NewBoolVar(f"{course}_S{sec}_P{prof}_T{t}_R{room}")

# **Prevent Room Conflicts: No two classes in the same room at the same time**
for t in range(max(len(time_slots["MWF"]), len(time_slots["TTh"]))):
    for r, room in enumerate(rooms):
        model.Add(
            sum(schedule[(course, sec, prof, t, r)]
                for course, num_sections in sections_per_course.items()
                for sec in range(num_sections)
                for prof in professors[course]
                if (course, sec, prof, t, r) in schedule) <= 1
        )

# Constraint: Each section must be assigned exactly one professor, time slot, and room
for course, num_sections in sections_per_course.items():
    for sec in range(num_sections):
        model.Add(sum(schedule[(course, sec, prof, t, r)]
                      for prof in professors[course]
                      for t in range(len(time_slots[meeting_days[course]]))
                      for r, room in enumerate(rooms)
                      if (course, sec, prof, t, r) in schedule) == 1)

# **Ensure Room Capacity is Not Exceeded**
for course, num_sections in sections_per_course.items():
    for sec in range(num_sections):
        for prof in professors[course]:
            for t in range(len(time_slots[meeting_days[course]])):
                for r, room in enumerate(rooms):
                    if (course, sec, prof, t, r) in schedule:
                        model.Add(schedule[(course, sec, prof, t, r)] * course_max_students[course] <= room_capacity[room])

# **Track Professor Workload and Balance It**
for prof in max_credits.keys():
    model.Add(prof_workload[prof] == sum(schedule[(course, sec, prof, t, r)] * credit_hours[course]
                                         for course, num_sections in sections_per_course.items()
                                         for sec in range(num_sections)
                                         for t in range(len(time_slots[meeting_days[course]]))
                                         for r, room in enumerate(rooms)
                                         if (course, sec, prof, t, r) in schedule))

# **Fair Workload Distribution**
max_workload = model.NewIntVar(0, max(max_credits.values()), "max_workload")
min_workload = model.NewIntVar(0, max(max_credits.values()), "min_workload")

model.AddMaxEquality(max_workload, [prof_workload[prof] for prof in max_credits.keys()])
model.AddMinEquality(min_workload, [prof_workload[prof] for prof in max_credits.keys()])
workload_balance = model.NewIntVar(0, max(max_credits.values()), "workload_balance")
model.Add(workload_balance == max_workload - min_workload)

# **Minimize workload imbalance**
model.Minimize(workload_balance)

# Solve the problem
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    print("\n===========================")
    print("      FINAL SCHEDULE       ")
    print("===========================")

    # Store schedules in a list for display
    course_schedule = []
    prof_schedule = {}

    for course, num_sections in sections_per_course.items():
        for sec in range(num_sections):
            for prof in professors[course]:
                for t in range(len(time_slots[meeting_days[course]])):
                    for r, room in enumerate(rooms):
                        if (course, sec, prof, t, r) in schedule and solver.Value(schedule[(course, sec, prof, t, r)]) == 1:
                            time = time_slots[meeting_days[course]][t]
                            course_schedule.append([course, sec + 1, prof, time, room, meeting_days[course]])

                            # Add to professor's schedule
                            if prof not in prof_schedule:
                                prof_schedule[prof] = []
                            prof_schedule[prof].append(f"{course} (Sec {sec+1}) at {time} in {room} ({meeting_days[course]})")

    df_courses = pd.DataFrame(course_schedule, columns=["Course", "Section", "Professor", "Time", "Room", "Days"])
    print("\nCourse Schedule:")
    print(df_courses.to_string(index=False))

else:
    print("No feasible schedule found.")
    print("\nSolver Status:", status)
    print("\nSolver Response Stats:\n", solver.ResponseStats())
