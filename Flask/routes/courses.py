from flask import Blueprint, jsonify, request
from models import Course, Professor, CourseProfessor, db

courses_blueprint = Blueprint('courses', __name__)

@courses_blueprint.route('/courses', methods=['GET'])
def get_courses():
    """
    Returns all the professors
    Output Json
    {
        "course_id": 1,
        "course_name": Mr Smith,
        "credit_hours": 1,
        "meeting_days": 'MWF' 
    }
    """
    courses = Course.query.all()
    data = [{
        'course_id': course.course_id,
        'course_name': course.course_name,
        'credit_hours': course.credit_hours,
        'meeting_days': course.meeting_days
    } for course in courses]
    return jsonify(data)

@courses_blueprint.route('/courses', methods=['POST'])
def add_course():
    """
        Adds a new Course
        Expected Json
        {
            "course_name": Mr Smith,
            "credit_hours": 1,
            "meeting_days": 'MWF'
        }
    """
    data = request.json
    new_course = Course(
        course_name=data.get('course_name'),
        credit_hours=data.get('credit_hours'),
        meeting_days=data.get('meeting_days')
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Course added successfully'}), 201

@courses_blueprint.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course_by_id(course_id):
    """
        Deletes Course by ID.
        Id is stored in HTTP string
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
        Name is stored in HTTP string
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