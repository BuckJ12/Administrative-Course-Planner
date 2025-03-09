from flask import Blueprint, jsonify, request
from models import Course, Professor, CourseProfessor, Section, db

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
        max_students=data.get('max_students')
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

@courses_blueprint.route('/courses/delete_by_name/<string:course_name>', methods=['DELETE'])
def delete_course_by_name(course_name):
    """
    Deletes Course by Name.
    The course name is provided in the URL.
    """
    course = Course.query.filter_by(course_name=course_name).first()
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'})

@courses_blueprint.route('/courses/add_professors', methods=['POST'])
def add_professors_to_course():
    """
    Assigns multiple professors to a course.
    Expected JSON:
    {
        "course_id": 101,
        "professor_ids": [1, 2, 3]
    }
    """
    data = request.json
    course_id = data.get('course_id')
    professor_ids = data.get('professor_ids')

    if not course_id or not professor_ids:
        return jsonify({'error': 'Missing course_id or professor_ids'}), 400

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    successful_additions = []
    already_assigned = []

    for professor_id in professor_ids:
        professor = Professor.query.get(professor_id)
        if not professor:
            continue  # Skip invalid professors

        # Check if the professor is already assigned to this course
        existing_assignment = CourseProfessor.query.filter_by(professor_id=professor_id, course_id=course_id).first()
        if existing_assignment:
            already_assigned.append(professor_id)
            continue

        # Assign professor to the course
        new_assignment = CourseProfessor(professor_id=professor_id, course_id=course_id)
        db.session.add(new_assignment)
        successful_additions.append(professor_id)

    db.session.commit()

    return jsonify({
        'message': 'Professors assigned to course successfully',
        'added_professors': successful_additions,
        'already_assigned': already_assigned
    }), 201

@courses_blueprint.route('/courses/remove_professors', methods=['DELETE'])
def remove_professors_from_course():
    """
    Removes multiple professors from a course.
    Expected JSON:
    {
        "course_id": 101,
        "professor_ids": [1, 2, 3]
    }
    """
    data = request.json
    course_id = data.get('course_id')
    professor_ids = data.get('professor_ids')

    if not course_id or not professor_ids:
        return jsonify({'error': 'Missing course_id or professor_ids'}), 400

    assignments_deleted = []
    not_found = []

    for professor_id in professor_ids:
        assignment = CourseProfessor.query.filter_by(professor_id=professor_id, course_id=course_id).first()
        if assignment:
            db.session.delete(assignment)
            assignments_deleted.append(professor_id)
        else:
            not_found.append(professor_id)

    db.session.commit()

    return jsonify({
        'message': 'Professors removed from course successfully',
        'removed_professors': assignments_deleted,
        'not_found_professors': not_found
    }), 200
