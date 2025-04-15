from ortools.sat.python import cp_model
from models import Course, Professor, CourseProfessor, Room, RoomRestriction, TimeSlot, Section, ScheduleModel

def generate_schedule(db_session):
    """Generate the schedule using OR-Tools allowing multi-slot courses and return the results as a dictionary."""
    # Load data from the database
    courses = Course.query.all()
    professors = Professor.query.all()
    course_professors = CourseProfessor.query.all()
    rooms = Room.query.all()
    room_restrictions = RoomRestriction.query.all()
    time_slots = TimeSlot.query.all()
    sections = Section.query.all()

    # Build convenient mappings (by id)
    courses_dict = {c.id: c for c in courses}
    professors_dict = {p.id: p for p in professors}
    rooms_dict = {r.id: r for r in rooms}
    
    # Map course_id to list of professor_ids who can teach that course.
    course_to_professors = {}
    for cp in course_professors:
        course_to_professors.setdefault(cp.course_id, []).append(cp.professor_id)
    
    # Map course_id to allowed rooms (if a restriction exists)
    room_restrictions_map = {}
    for rr in room_restrictions:
        room_restrictions_map.setdefault(rr.course_id, []).append(rr.room_id)
    
    # Map meeting_days (MWF, TTh) to list of time slots and sort them.
    time_slots_by_day = {}
    for ts in time_slots:
        time_slots_by_day.setdefault(ts.meeting_days, []).append(ts)
    for day in time_slots_by_day:
        time_slots_by_day[day] = sorted(time_slots_by_day[day], key=lambda x: x.id)
    
    # Map course_id to list of sections
    sections_by_course = {}
    for sec in sections:
        sections_by_course.setdefault(sec.course_id, []).append(sec)
    
    # Build a mapping from time slot ID to time string.
    time_str_by_id = {ts.id: ts.time for ts in time_slots}
    
    # Build the CP model
    model = cp_model.CpModel()
    schedule_vars = {}

    print("Model Started")
    
    # Modified variable creation: choose a starting time slot block.
    for course in courses:
        allowed_day = course.meeting_days
        ts_list = time_slots_by_day.get(allowed_day, [])
        course_secs = sections_by_course.get(course.id, [])
        available_profs = course_to_professors.get(course.id, [])
        duration = course.slots_needed  # number of consecutive slots this course requires
        
        # Only consider valid blocks within the day.
        num_slots = len(ts_list)
        for sec in course_secs:
            for prof_id in available_profs:
                # iterate over possible starting indices where a block fits
                for start_index in range(num_slots - duration + 1):
                    block = ts_list[start_index: start_index + duration]
                    block_slot_ids = tuple(ts.id for ts in block)
                    # Loop over all rooms and check room capacity restrictions
                    for room in rooms:
                        if course.max_students > room.capacity:
                            continue
                        if course.id in room_restrictions_map and room.id not in room_restrictions_map[course.id]:
                            continue

                        key = (sec.id, course.id, prof_id, allowed_day, block_slot_ids, room.id)
                        schedule_vars[key] = model.NewBoolVar(
                            f"sec_{sec.id}_course_{course.id}_prof_{prof_id}_day_{allowed_day}_slots_{block_slot_ids}_room_{room.id}"
                        )

    # Constraint: Each section must be assigned exactly one block.
    for course in courses:
        for sec in sections_by_course.get(course.id, []):
            relevant_vars = [var for key, var in schedule_vars.items() if key[0] == sec.id]
            model.Add(sum(relevant_vars) == 1)
    
    # Constraint: A room cannot be used by more than one class in any time slot.
    for day in ['MWF', 'TTh']:
        for ts in time_slots_by_day.get(day, []):
            vars_in_slot = []
            for key, var in schedule_vars.items():
                # key[3] is the day; key[4] is a tuple of time slot ids for the block
                if key[3] == day and ts.id in key[4]:
                    vars_in_slot.append(var)
            model.Add(sum(vars_in_slot) <= 1)
    
    # Constraint: A professor cannot be in more than one place during any time slot.
    for prof in professors:
        for day in time_slots_by_day:
            for ts in time_slots_by_day.get(day, []):
                prof_time_vars = [
                    var for key, var in schedule_vars.items()
                    if key[2] == prof.id and key[3] == day and ts.id in key[4]
                ]
                model.Add(sum(prof_time_vars) <= 1)
    
    # Constraint: Enforce professor time restrictions.
    for prof in professors:
        for restricted_ts in prof.time_restrictions:
            day = restricted_ts.meeting_days
            ts_id = restricted_ts.id
            prof_vars = [
                var for key, var in schedule_vars.items()
                if key[2] == prof.id and key[3] == day and ts_id in key[4]
            ]
            model.Add(sum(prof_vars) == 0)

        # ----- START PROFESSOR WORKLOAD CONSTRAINTS -----

    # Create a variable for each professor representing their total teaching load (weighted by credit hours)
    prof_load = {}
    for prof in professors:
        # Gather all schedule variables (each is 0 or 1) associated with this professor.
        # Multiply each by the corresponding course's credit hours.
        relevant_assignments = [
            courses_dict[key[1]].credit_hours * var 
            for key, var in schedule_vars.items() 
            if key[2] == prof.id
        ]
        # The upper bound can be the sum of credit hours for all courses that can possibly be taught by this professor.
        max_possible_load = sum(courses_dict[key[1]].credit_hours for key in schedule_vars if key[2] == prof.id)
        
        # Create an integer variable representing the total load.
        prof_load[prof.id] = model.NewIntVar(0, max_possible_load, f"load_{prof.id}")
        
        # Enforce that the professor's load equals the weighted sum of assignments.
        model.Add(prof_load[prof.id] == sum(relevant_assignments))
        
        # Hard constraint: Ensure the load does not exceed the professor's maximum allowed credit hours.
        model.Add(prof_load[prof.id] <= prof.max_credit_hours)

    # Optionally, if you want to balance workloads across professors, you can add an optimization objective.
    # For instance, you can minimize the difference between the highest and lowest loads.
    max_load = model.NewIntVar(0, max(max_possible_load for _ in professors), "max_load")
    min_load = model.NewIntVar(0, max(max_possible_load for _ in professors), "min_load")
    model.AddMaxEquality(max_load, [prof_load[prof.id] for prof in professors])
    model.AddMinEquality(min_load, [prof_load[prof.id] for prof in professors])
    load_difference = model.NewIntVar(0, max(max_possible_load for _ in professors), "load_difference")
    model.Add(load_difference == max_load - min_load)

    # Set the solver to minimize the difference in load, thereby encouraging a balanced assignment.
    model.Minimize(load_difference)

    # ----- END PROFESSOR WORKLOAD CONSTRAINTS -----

    
    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return {"status": "No feasible schedule found."}
    
    result_schedule = []
    for key, var in schedule_vars.items():
        if solver.Value(var) == 1:
            section_id, course_id, prof_id, day, block_slot_ids, room_id = key
            # Here we display the starting time of the block.
            # Optionally, you could also output the entire list of time strings.
            start_time = time_str_by_id.get(block_slot_ids[0], "Unknown")
            result_schedule.append({
                "course_name": courses_dict[course_id].name,
                "section_id": section_id,
                "professor": professors_dict[prof_id].name,
                "start_time": start_time,
                "time_slots": [time_str_by_id.get(tsid, "Unknown") for tsid in block_slot_ids],
                "room": rooms_dict[room_id].name,
                "days": day
            })

            result_schedule.sort(key=lambda x: (x["days"], x["start_time"]))
    
    return {
        "status": "Schedule generated successfully.",
        "schedule": result_schedule,
    }
