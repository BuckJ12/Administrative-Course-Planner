from flask import Blueprint, jsonify, request
from models import Course, Professor, Section, Room, db

courses_blueprint = Blueprint('courses', __name__)

@courses_blueprint.route('/courses', methods=['GET'])
def get_courses():
    """
    Returns all courses with their number of sections and associated professors.
    Output JSON:
    [
        {
            "id": 1,
            "name": "Science",
            "credit_hours": 1,
            "meeting_days": "MWF",
            "number_of_sections": 3,
            "max_students": 10,
            "slots_needed": 1,
            "professors": [
                "Dr. Smith",
            ]
        },
        ...
    ]
    """
    courses = Course.query.all()
    data = []
    for course in courses:
        course_data = {
            'id': course.id,
            'name': course.name,
            'credit_hours': course.credit_hours,
            'meeting_days': course.meeting_days,
            'number_of_sections': len(course.sections),
            'max_students': course.max_students,
            'slots_needed': course.slots_needed,
            'professors': [prof.name for prof in course.professors]
        }
        data.append(course_data)
    return jsonify(data)

@courses_blueprint.route('/courses/<int:course_id>', methods=['GET'])
def get_courses_by_ID(course_id):
    """
    Returns all courses with their number of sections and associated professors.
    Output JSON:
    [
        {
            "id": 1,
            "name": "Science",
            "credit_hours": 1,
            "meeting_days": "MWF",
            "max_students": 10,
            "slots_needed": 1,
            "number_of_sections": 3,
            "professors": [
                {
                    "max_credit_hours": 1,
                    "name": "Dr. Smith",
                    "professor_id": 1
                },
            ]
            "rooms": [
                {
                    "id": 1,
                    "name": "Room A"
                    "capacity": 1,
                }
            ]
        },
        ...
    ]
    """
    course = Course.query.get(course_id)
    course_data = {
            'id': course.id,
            'name': course.name,
            'credit_hours': course.credit_hours,
            'meeting_days': course.meeting_days,
            'max_students': course.max_students,
            'slots_needed': course.slots_needed,
            'number_of_sections': len(course.sections),
            'professors': [prof.to_dict() for prof in course.professors],
            'rooms': [room.to_dict() for room in course.rooms],
        }
    return jsonify(course_data)


@courses_blueprint.route('/courses', methods=['POST'])
def add_course():
    data = request.json
    print(data)
    if not data.get('max_students'):
        return jsonify({'error': 'Missing required fields'}), 400
    new_course = Course(
        name=data.get('name'),
        credit_hours=data.get('credit_hours'),
        meeting_days=data.get('meeting_Days'),
        max_students=data.get('max_students'),
        slots_needed=data.get('slots_needed', 1),
    )
    db.session.add(new_course)
    db.session.commit()

    # Optionally create sections if provided
    num_sections = data.get('numberOfSections')
    if num_sections:
        num_sections = int(num_sections)  # Convert string to int
        for sec_num in range(1, num_sections + 1):
            new_section = Section(course_id=new_course.id, section_number=sec_num)
            db.session.add(new_section)

    
    # Optionally assign professors if provided
    professors = data.get('professors')
    if professors:
        for prof in professors:
            professor = Professor.query.get(prof)
            if professor:
                new_course.professors.append(professor)
            else:
                pass

    rooms = data.get('rooms')
    if rooms:
        for room in rooms:
            room_obj = Room.query.get(room)
            if room_obj:
                new_course.rooms.append(room_obj)
            else:
                pass

    db.session.commit()
    return jsonify({'message': 'Course added successfully'}), 201


@courses_blueprint.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course_by_id(course_id):
    """
    Deletes Course by ID.
    The course_id is provided in the URL.
    """
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'})

@courses_blueprint.route('/courses/<int:course_id>', methods=['PUT'])
def update_course_by_id(course_id):
    """
    Updates Course by ID.
    The course_id is provided in the URL.
    """
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    data = request.json
    course.name = data.get('name', course.name)
    course.credit_hours = data.get('credit_hours', course.credit_hours)
    course.meeting_days = data.get('meeting_days', course.meeting_days)
    course.max_students = data.get('max_students', course.max_students)
    course.slots_needed = data.get('slots_needed', course.slots_needed)

    # Optionally create and delete sections if needed
    num_sections = data.get('numberOfSections')
    if num_sections:
        num_sections = int(num_sections)
        if len(course.sections) > num_sections:
            for sec in course.sections[num_sections:]:
                db.session.delete(sec)
        else:
            for sec_num in range(len(course.sections) + 1, num_sections + 1):
                new_section = Section(course_id=course.id, section_number=sec_num)
                db.session.add(new_section)
    
    # Optionally assign or delete professors if needed
    professors = data.get('professors')
    if professors:
        for prof in professors:
            professor = Professor.query.get(prof)
            if professor:
                if professor not in course.professors:
                    course.professors.append(professor)
            else:
                pass
        for prof in course.professors:
            if prof.id not in professors:
                course.professors.remove(prof)
    
    rooms = data.get('rooms')
    if rooms:
        for room in rooms:
            room_obj = Room.query.get(room)
            if room_obj:
                if room_obj not in course.rooms:
                    course.rooms.append(room_obj)
            else:
                pass
        for room in course.rooms:
            if room.id not in rooms:
                course.rooms.remove(room)
                
    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'Course updated successfully'})