
from flask import Blueprint, jsonify, request
from models import Professor, Course, CourseProfessor, db

professors_blueprint = Blueprint('professors', __name__)

@professors_blueprint.route('/professors', methods=['GET'])
def get_professors():
    """
    Returns all the professors
    Output Json
    {
        "professor_id": 1,
        "name": Mr Smith,
        "max_credit_hours": 1
    }
    """
    profs = Professor.query.all()
    data = [{
        'professor_id': prof.professor_id,
        'name': prof.name,
        'max_credit_hours': prof.max_credit_hours
    } for prof in profs]
    return jsonify(data)

@professors_blueprint.route('/professors', methods=['POST'])
def add_professor():
    """
        Adds a new Professor
        Expected Json
        {
            "name": Mr Smith,
            "max_credit_hours": 1
        }
    """
    data = request.json
    new_prof = Professor(
        name=data.get('name'),
        max_credit_hours=data.get('max_credit_hours')
    )
    db.session.add(new_prof)
    db.session.commit()
    return jsonify({'message': 'Professor added successfully'}), 201

@professors_blueprint.route('/professors/<int:professor_id>', methods=['DELETE'])
def delete_professor_by_id(professor_id):
    """
        Deletes Professor by ID.
        Id is stored in HTTP string
    """
    prof = Professor.query.get(professor_id)
    if not prof:
        return jsonify({'error': 'Professor not found'}), 404
    db.session.delete(prof)
    db.session.commit()
    return jsonify({'message': 'Professor deleted successfully'})

@professors_blueprint.route('/professors/delete_by_name/<string:name>', methods=['DELETE'])
def delete_professor_by_name(name):
    """
        Deletes Professor by Name.
        Name is stored in HTTP string
    """
    prof = Professor.query.filter_by(name=name).first()
    if not prof:
        return jsonify({'error': 'Professor not found'}), 404
    db.session.delete(prof)
    db.session.commit()
    return jsonify({'message': 'Professor deleted successfully'})

@professors_blueprint.route('/professors/add_to_courses', methods=['POST'])
def add_professor_to_courses():
    """
    Assigns a professor to multiple courses.
    Expected JSON:
    {
        "professor_id": 1,
        "course_ids": [101, 102, 103]
    }
    """
    data = request.json
    professor_id = data.get('professor_id')
    course_ids = data.get('course_ids')

    if not professor_id or not course_ids:
        return jsonify({'error': 'Missing professor_id or course_ids'}), 400

    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({'error': 'Professor not found'}), 404

    successful_additions = []
    already_assigned = []

    for course_id in course_ids:
        course = Course.query.get(course_id)
        if not course:
            continue  # Skip invalid courses

        # Check if the professor is already assigned to this course
        existing_assignment = CourseProfessor.query.filter_by(professor_id=professor_id, course_id=course_id).first()
        if existing_assignment:
            already_assigned.append(course_id)
            continue

        # Assign professor to the course
        new_assignment = CourseProfessor(professor_id=professor_id, course_id=course_id)
        db.session.add(new_assignment)
        successful_additions.append(course_id)

    db.session.commit()

    return jsonify({
        'message': 'Professor assigned to courses successfully',
        'added_courses': successful_additions,
        'already_assigned': already_assigned
    }), 201

@professors_blueprint.route('/professors/remove_from_courses', methods=['DELETE'])
def remove_professor_from_courses():
    """
    Removes a professor from multiple courses.
    Expected JSON:
    {
        "professor_id": 1,
        "course_ids": [101, 102, 103]
    }
    """
    data = request.json
    professor_id = data.get('professor_id')
    course_ids = data.get('course_ids')

    if not professor_id or not course_ids:
        return jsonify({'error': 'Missing professor_id or course_ids'}), 400

    assignments_deleted = []
    not_found = []

    for course_id in course_ids:
        assignment = CourseProfessor.query.filter_by(professor_id=professor_id, course_id=course_id).first()
        if assignment:
            db.session.delete(assignment)
            assignments_deleted.append(course_id)
        else:
            not_found.append(course_id)

    db.session.commit()

    return jsonify({
        'message': 'Professor removed from courses successfully',
        'removed_courses': assignments_deleted,
        'not_found_courses': not_found
    }), 200
