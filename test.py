import pandas as pd
from ortools.sat.python import cp_model

def consecutive_penalty(n):
    return (n * (n + 1)) // 2  # 1, 3, 6, 10, ...


# Define the model
model = cp_model.CpModel()

# Example data
courses = ["Math 101", "CS 101", "CS 201", "Physics 102", "History 105"]
sections_per_course = {"Math 101": 2, "CS 101": 2, "CS 201": 1, "Physics 102": 2, "History 105": 1}
meeting_days = {"Math 101": "MWF", "CS 101": "MWF", "CS 201": "MWF", "Physics 102": "MWF", "History 105": "TTh"}

# Restrict courses to specific days
course_allowed_days = {
    "Math 101": ["MWF"],
    "CS 101": ["MWF"],
    "CS 201": ["MWF"],
    "Physics 102": ["MWF"],
    "History 105": ["TTh"],  # This course can only be held on Tuesday and Thursday
}

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

time_slot_penalty = {
    "8AM": 4, "9:30AM": 1, "11AM": 0, "12:30PM": 0, "2PM": 1, "3:30PM": 3
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
            for allowed_day in course_allowed_days[course]:  # Restrict by allowed days
                for t in range(len(time_slots[allowed_day])):  # Iterate over available times for allowed days
                    for r, room in enumerate(rooms):
                        if course in room_restrictions and room not in room_restrictions[course]:
                            continue  # Skip rooms that this course cannot be in

                        schedule[(course, sec, prof, allowed_day, t, r)] = model.NewBoolVar(
                            f"{course}_S{sec}_P{prof}_D{allowed_day}_T{t}_R{room}"
                        )

# Prevent Room Conflicts: No two classes in the same room at the same time
for allowed_day in ["MWF", "TTh"]:
    for t in range(len(time_slots[allowed_day])):
        for r, room in enumerate(rooms):
            model.Add(
                sum(schedule[(course, sec, prof, allowed_day, t, r)]
                    for course, num_sections in sections_per_course.items()
                    for sec in range(num_sections)
                    for prof in professors[course]
                    if (course, sec, prof, allowed_day, t, r) in schedule) <= 1
            )

# Constraint: Each section must be assigned exactly one professor, time slot, and room
for course, num_sections in sections_per_course.items():
    for sec in range(num_sections):
        model.Add(sum(schedule[(course, sec, prof, allowed_day, t, r)]
                      for prof in professors[course]
                      for allowed_day in course_allowed_days[course]
                      for t in range(len(time_slots[allowed_day]))
                      for r, room in enumerate(rooms)
                      if (course, sec, prof, allowed_day, t, r) in schedule) == 1)
        
#Constraint: Time penalty
total_time_penalty = model.NewIntVar(0, sum([max(time_slot_penalty.values())] * len(schedule)), "total_time_penalty")
model.Add(total_time_penalty == sum(
    schedule[(course, sec, prof, allowed_day, t, r)] * time_slot_penalty[time_slots[allowed_day][t]]
    for course, num_sections in sections_per_course.items()
    for sec in range(num_sections)
    for prof in professors[course]
    for allowed_day in course_allowed_days[course]
    for t in range(len(time_slots[allowed_day]))
    for r, room in enumerate(rooms)
    if (course, sec, prof, allowed_day, t, r) in schedule
))


# Ensure Room Capacity is Not Exceeded
for course, num_sections in sections_per_course.items():
    for sec in range(num_sections):
        for prof in professors[course]:
            for allowed_day in course_allowed_days[course]:
                for t in range(len(time_slots[allowed_day])):
                    for r, room in enumerate(rooms):
                        if (course, sec, prof, allowed_day, t, r) in schedule:
                            model.Add(schedule[(course, sec, prof, allowed_day, t, r)] * course_max_students[course] <= room_capacity[room])

# Track Professor Workload and Balance It
for prof in max_credits.keys():
    model.Add(prof_workload[prof] == sum(schedule[(course, sec, prof, allowed_day, t, r)] * credit_hours[course]
                                         for course, num_sections in sections_per_course.items()
                                         for sec in range(num_sections)
                                         for allowed_day in course_allowed_days[course]
                                         for t in range(len(time_slots[allowed_day]))
                                         for r, room in enumerate(rooms)
                                         if (course, sec, prof, allowed_day, t, r) in schedule))

# Create decision variables for tracking consecutive classes per professor
consecutive_classes = {prof: [] for prof in max_credits.keys()}

for prof in max_credits.keys():
    for allowed_day in ["MWF", "TTh"]:
        for t in range(len(time_slots[allowed_day]) - 1):  # Check adjacent time slots
            consecutive_var = model.NewBoolVar(f"consecutive_{prof}_{allowed_day}_T{t}")
            consecutive_classes[prof].append(consecutive_var)

            # Ensure this variable is 1 if the professor teaches in both consecutive slots
            model.Add(consecutive_var >= sum(
                schedule[(course, sec, prof, allowed_day, t, r)] +
                schedule[(course, sec, prof, allowed_day, t + 1, r)]
                for course, num_sections in sections_per_course.items()
                for sec in range(num_sections)
                for r, room in enumerate(rooms)
                if (course, sec, prof, allowed_day, t, r) in schedule and (course, sec, prof, allowed_day, t + 1, r) in schedule
            ) - 1)

# Total consecutive class penalty variable
total_consecutive_penalty = model.NewIntVar(0, sum([consecutive_penalty(5)] * len(max_credits.keys())), "total_consecutive_penalty")

# Sum up penalties for consecutive classes
model.Add(total_consecutive_penalty == sum(
    consecutive_penalty(len(consecutive_classes[prof])) * consecutive_var
    for prof in max_credits.keys()
    for consecutive_var in consecutive_classes[prof]
))


# Fair Workload Distribution
max_workload = model.NewIntVar(0, max(max_credits.values()), "max_workload")
min_workload = model.NewIntVar(0, max(max_credits.values()), "min_workload")

model.AddMaxEquality(max_workload, [prof_workload[prof] for prof in max_credits.keys()])
model.AddMinEquality(min_workload, [prof_workload[prof] for prof in max_credits.keys()])
workload_balance = model.NewIntVar(0, max(max_credits.values()), "workload_balance")
model.Add(workload_balance == max_workload - min_workload)

# Minimize workload imbalance, class times and consecutive classes
model.Minimize(workload_balance + total_time_penalty + total_consecutive_penalty)

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
                for allowed_day in course_allowed_days[course]:
                    for t in range(len(time_slots[allowed_day])):
                        for r, room in enumerate(rooms):
                            if (course, sec, prof, allowed_day, t, r) in schedule and solver.Value(schedule[(course, sec, prof, allowed_day, t, r)]) == 1:
                                time = time_slots[allowed_day][t]
                                course_schedule.append([course, sec + 1, prof, time, room, allowed_day])

                                if prof not in prof_schedule:
                                    prof_schedule[prof] = []
                                prof_schedule[prof].append(f"{course} (Sec {sec+1}) at {time} in {room} ({allowed_day})")

    df_courses = pd.DataFrame(course_schedule, columns=["Course", "Section", "Professor", "Time", "Room", "Days"])
    print("\nCourse Schedule:")
    # Sort the DataFrame by the "Professor" column
    df_courses = df_courses.sort_values(by=["Professor","Time"])

    # Print the sorted DataFrame
    print("\nSorted Course Schedule by Professor:")
    print(df_courses.to_string(index=False))
    print(total_consecutive_penalty)

else:
    print("No feasible schedule found.")
    print("\nSolver Status:", status)
    print("\nSolver Response Stats:\n", solver.ResponseStats())
