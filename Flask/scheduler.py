from ortools.sat.python import cp_model
from models import Course, Professor, CourseProfessor, Room, RoomRestriction, TimeSlot, Section, ScheduleModel

def generate_schedule(db_session):
    """Generate the schedule using OR-Tools and return the results as a dictionary."""
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
    
    # Map meeting_days (MWF, TTh) to list of time slots
    time_slots_by_day = {}
    for ts in time_slots:
        time_slots_by_day.setdefault(ts.meeting_days, []).append(ts)
    for day in time_slots_by_day:
        time_slots_by_day[day] = sorted(time_slots_by_day[day], key=lambda x: x.id)
    
    # Map course_id to list of sections
    sections_by_course = {}
    for sec in sections:
        sections_by_course.setdefault(sec.course_id, []).append(sec)
    
    # Define a static mapping of time string to penalty.
    time_slot_penalty = {"8:00": 4, "9:30": 1, "11:00": 0, "12:30": 0, "2:00": 1, "3:30": 3}
    time_str_by_id = {ts.id: ts.time for ts in time_slots}
    
    # Build the CP model
    model = cp_model.CpModel()
    schedule_vars = {}

    print("Model Started")
    
    for course in courses:
        allowed_day = course.meeting_days
        ts_list = time_slots_by_day.get(allowed_day, [])
        course_secs = sections_by_course.get(course.id, [])
        available_profs = course_to_professors.get(course.id, [])
        
        for sec in course_secs:
            for prof_id in available_profs:
                for ts in ts_list:
                    for room in rooms:
                        if course.max_students > room.capacity:
                            continue
                        if course.id in room_restrictions_map and room.id not in room_restrictions_map[course.id]:
                            continue
                        
                        key = (sec.id, course.id, prof_id, allowed_day, ts.id, room.id)
                        schedule_vars[key] = model.NewBoolVar(f"sec_{sec.id}_course_{course.id}_prof_{prof_id}_day_{allowed_day}_ts_{ts.id}_room_{room.id}")


    # Constraints
    for course in courses:
        for sec in sections_by_course.get(course.id, []):
            relevant_vars = [var for key, var in schedule_vars.items() if key[0] == sec.id]
            model.Add(sum(relevant_vars) == 1)
    
    for day in ['MWF', 'TTh']:
        ts_list = time_slots_by_day.get(day, [])
        for ts in ts_list:
            for room in rooms:
                vars_in_slot = [var for key, var in schedule_vars.items() if key[3] == day and key[4] == ts.id and key[5] == room.id]
                model.Add(sum(vars_in_slot) <= 1)
    
    for course in courses:
        for sec in sections_by_course.get(course.id, []):
            relevant_vars = [var for key, var in schedule_vars.items() if key[0] == sec.id]
            for prof_id in course_to_professors.get(course.id, []):
                prof_vars = [var for key, var in schedule_vars.items() if key[2] == prof_id]
                model.Add(sum(relevant_vars) <= sum(prof_vars))

    # Constraint: A professor cannot teach more than one class at the same time on the same day.
    for prof in professors:
        for day, ts_list in time_slots_by_day.items():
            for ts in ts_list:
                prof_time_vars = [
                    var for key, var in schedule_vars.items()
                    if key[2] == prof.id and key[3] == day and key[4] == ts.id
                ]
                model.Add(sum(prof_time_vars) <= 1)
    
    total_time_penalty = model.NewIntVar(0, 10000, "total_time_penalty")
    model.Add(total_time_penalty == sum(var * time_slot_penalty.get(time_str_by_id.get(key[4], "11:00"), 0) for key, var in schedule_vars.items()))
    

    # Solve the model
    solver = cp_model.CpSolver()
    #solver.parameters.cp_model_presolve = False  # Disables presolve to see raw constraint interactions
    #solver.parameters.log_search_progress = True
    
    
    status = solver.Solve(model)
    
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return {"status": "No feasible schedule found."}
    
    if status == cp_model.INFEASIBLE:
        print("Infeasible constraints detected.")
        print(f"Number of conflicts encountered: {solver.NumConflicts()}")
        solver.parameters.enumerate_all_solutions = True

    
    result_schedule = []
    for key, var in schedule_vars.items():
        if solver.Value(var) == 1:
            section_id, course_id, prof_id, day, ts_id, room_id = key
            result_schedule.append({
                "course_name": courses_dict[course_id].name,
                "section_id": section_id,
                "professor": professors_dict[prof_id].name,
                "time": time_str_by_id.get(ts_id, "Unknown"),
                "room": rooms_dict[room_id].name,
                "days": day
            })
    
    return {
        "status": "Schedule generated successfully.",
        "schedule": result_schedule,
        "total_time_penalty": solver.Value(total_time_penalty)
    }
