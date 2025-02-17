# scheduler.py
from ortools.sat.python import cp_model
from models import Course, Professor, CourseProfessor, Room, RoomRestriction, TimeSlot, Section, CourseEnrollmentLimit

def consecutive_penalty(n):
    return (n * (n + 1)) // 2

def generate_schedule(db_session):
    """Generate the schedule using OR-Tools and return the results as a dictionary."""
    # ----------------------------------
    # 1. Load data from the database
    # ----------------------------------
    courses = Course.query.all()
    professors = Professor.query.all()
    course_professors = CourseProfessor.query.all()
    rooms = Room.query.all()
    room_restrictions = RoomRestriction.query.all()
    time_slots = TimeSlot.query.all()
    sections = Section.query.all()
    enrollment_limits = CourseEnrollmentLimit.query.all()

    # Build convenient mappings (by id)
    courses_dict = {c.course_id: c for c in courses}
    professors_dict = {p.professor_id: p for p in professors}
    rooms_dict = {r.room_id: r for r in rooms}

    # Map course_id to list of professor_ids who can teach that course.
    course_to_professors = {}
    for cp in course_professors:
        course_to_professors.setdefault(cp.course_id, []).append(cp.professor_id)

    # Map course_id to allowed rooms (if a restriction exists)
    room_restrictions_map = {}
    for rr in room_restrictions:
        room_restrictions_map.setdefault(rr.course_id, []).append(rr.room_id)

    # Map course_id to max number of students
    enrollment_limits_map = {cel.course_id: cel.max_students for cel in enrollment_limits}

    # Map meeting_days (MWF, TTh) to list of time slots
    time_slots_by_day = {}
    for ts in time_slots:
        time_slots_by_day.setdefault(ts.meeting_days, []).append(ts)
    for day in time_slots_by_day:
        # Sort by time_slot_id or another field if you have one to indicate order.
        time_slots_by_day[day] = sorted(time_slots_by_day[day], key=lambda x: x.time_slot_id)

    # Map course_id to list of sections
    sections_by_course = {}
    for sec in sections:
        sections_by_course.setdefault(sec.course_id, []).append(sec)

    # Define a static mapping of time string to penalty.
    time_slot_penalty = {"8AM": 4, "9:30AM": 1, "11AM": 0, "12:30PM": 0, "2PM": 1, "3:30PM": 3}
    # Build mapping from time_slot_id to its time string.
    time_str_by_id = {ts.time_slot_id: ts.time for ts in time_slots}

    # ----------------------------------
    # 2. Build the CP model
    # ----------------------------------
    model = cp_model.CpModel()

    schedule_vars = {}

    for course in courses:
        course_id = course.course_id
        allowed_day = course.meeting_days  # e.g., "MWF" or "TTh"
        ts_list = time_slots_by_day.get(allowed_day, [])
        course_secs = sections_by_course.get(course_id, [])
        available_profs = course_to_professors.get(course_id, [])
        for sec in course_secs:
            for prof_id in available_profs:
                for ts in ts_list:
                    for room in rooms:
                        # Enforce room restrictions if they exist
                        if course_id in room_restrictions_map and room.room_id not in room_restrictions_map[course_id]:
                            continue
                        key = (sec.section_id, course_id, prof_id, allowed_day, ts.time_slot_id, room.room_id)
                        schedule_vars[key] = model.NewBoolVar(
                            f"sec_{sec.section_id}_course_{course_id}_prof_{prof_id}_day_{allowed_day}_ts_{ts.time_slot_id}_room_{room.room_id}"
                        )

    # ----------------------------------
    # Add your constraints here.
    # For example, ensure each section is assigned exactly once:
    # ----------------------------------
    for course in courses:
        course_id = course.course_id
        for sec in sections_by_course.get(course_id, []):
            relevant_vars = [var for key, var in schedule_vars.items() if key[0] == sec.section_id]
            model.Add(sum(relevant_vars) == 1)

    # No room conflicts at the same time:
    for day in ['MWF', 'TTh']:
        ts_list = time_slots_by_day.get(day, [])
        for ts in ts_list:
            for room in rooms:
                vars_in_slot = [
                    var for key, var in schedule_vars.items()
                    if key[3] == day and key[4] == ts.time_slot_id and key[5] == room.room_id
                ]
                model.Add(sum(vars_in_slot) <= 1)

    # Room capacity constraint:
    for key, var in schedule_vars.items():
        course_id = key[1]
        max_students = enrollment_limits_map.get(course_id, 0)
        room_cap = rooms_dict[key[5]].capacity
        model.Add(var * max_students <= room_cap)

    # Track professor workload
    prof_workload = {}
    for prof in professors:
        workload_var = model.NewIntVar(0, prof.max_credit_hours, f"workload_prof_{prof.professor_id}")
        prof_workload[prof.professor_id] = workload_var
        assigned_vars = []
        for key, var in schedule_vars.items():
            if key[2] == prof.professor_id:
                course_id = key[1]
                assigned_vars.append(var * courses_dict[course_id].credit_hours)
        if assigned_vars:
            model.Add(workload_var == sum(assigned_vars))
        else:
            model.Add(workload_var == 0)

    # Time penalty constraint:
    total_time_penalty = model.NewIntVar(0, 10000, "total_time_penalty")
    model.Add(total_time_penalty == sum(
        var * time_slot_penalty.get(time_str_by_id.get(key[4], "11AM"), 0)
        for key, var in schedule_vars.items()
    ))

    # Penalty for consecutive classes:
    consecutive_penalty_terms = []
    for prof in professors:
        for day in ['MWF', 'TTh']:
            ts_list = time_slots_by_day.get(day, [])
            for i in range(len(ts_list) - 1):
                ts1 = ts_list[i]
                ts2 = ts_list[i + 1]
                vars_ts1 = [
                    var for key, var in schedule_vars.items()
                    if key[2] == prof.professor_id and key[3] == day and key[4] == ts1.time_slot_id
                ]
                vars_ts2 = [
                    var for key, var in schedule_vars.items()
                    if key[2] == prof.professor_id and key[3] == day and key[4] == ts2.time_slot_id
                ]
                if vars_ts1 and vars_ts2:
                    cons_var = model.NewBoolVar(
                        f"consecutive_prof_{prof.professor_id}_{day}_{ts1.time_slot_id}_{ts2.time_slot_id}"
                    )
                    model.Add(cons_var >= sum(vars_ts1) + sum(vars_ts2) - 1)
                    consecutive_penalty_terms.append(cons_var)

    total_consecutive_penalty = model.NewIntVar(0, 10000, "total_consecutive_penalty")
    if consecutive_penalty_terms:
        model.Add(total_consecutive_penalty == sum(consecutive_penalty_terms))
    else:
        model.Add(total_consecutive_penalty == 0)

    # Workload balance among professors:
    max_workload = model.NewIntVar(0, max([prof.max_credit_hours for prof in professors]), "max_workload")
    min_workload = model.NewIntVar(0, max([prof.max_credit_hours for prof in professors]), "min_workload")
    model.AddMaxEquality(max_workload, list(prof_workload.values()))
    model.AddMinEquality(min_workload, list(prof_workload.values()))
    workload_balance = model.NewIntVar(0, max([prof.max_credit_hours for prof in professors]), "workload_balance")
    model.Add(workload_balance == max_workload - min_workload)

    # Define the objective:
    model.Minimize(workload_balance + total_time_penalty + total_consecutive_penalty)

    # ----------------------------------
    # 3. Solve the model
    # ----------------------------------
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return {"status": "No feasible schedule found."}

    # ----------------------------------
    # 4. Build the result schedule
    # ----------------------------------
    result_schedule = []
    for key, var in schedule_vars.items():
        if solver.Value(var) == 1:
            section_id, course_id, prof_id, day, ts_id, room_id = key
            # You can query the section from the database if you need additional details.
            result_schedule.append({
                "course_name": courses_dict[course_id].course_name,
                "section_id": section_id,
                "professor": professors_dict[prof_id].name,
                "time": time_str_by_id.get(ts_id, "Unknown"),
                "room": rooms_dict[room_id].room_name,
                "days": day
            })

    # Optionally, you can return additional information like penalty details.
    return {
        "status": "Schedule generated successfully.",
        "schedule": result_schedule,
        "workload_balance": solver.Value(workload_balance),
        "total_time_penalty": solver.Value(total_time_penalty),
        "total_consecutive_penalty": solver.Value(total_consecutive_penalty)
    }
