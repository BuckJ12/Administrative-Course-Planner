
from flask import Blueprint, jsonify, request
from models import Professor, Course, CourseProfessor, db

professors_blueprint = Blueprint('professors', __name__)

@professors_blueprint.route('/professors', methods=['GET'])
def get_professors():
    """
    Returns all the professors
    Output Json
    {
        "id": 1,
        "name": Mr Smith,
        "max_credit_hours": 1
        "courses": [
            {
                "id": 101,
                "name": "Math 101",
                "credit_hours": 3
                "MeetingDays": MWF

            },
    }
    """
    profs = Professor.query.all()
    data = [{
        'id': prof.id,
        'name': prof.name,
        'max_credit_hours': prof.max_credit_hours,
        'courses': [course.to_dict() for course in prof.courses]
    } for prof in profs]
    return jsonify(data)

@professors_blueprint.route('/professors/<int:professor_id>', methods=['GET'])
def get_professor_by_id(professor_id):
    """
    Returns a professor by ID
    Output Json
    {
        "id": 1,
        "name": Mr Smith,
        "max_credit_hours": 1
        "courses": [
            {
                "id": 101,
                "name": "Math 101",
                "credit_hours": 3
                "MeetingDays": MWF
            },
    }
    """
    prof = Professor.query.get(professor_id)
    if not prof:
        return jsonify({'error': 'Professor not found'}), 404
    data = {
        'id': prof.id,
        'name': prof.name,
        'max_credit_hours': prof.max_credit_hours,
        'courses': [course.to_dict() for course in prof.courses]
    }
    return jsonify(data)

@professors_blueprint.route('/professors', methods=['POST'])
def add_professor():
    """
        Adds a new Professor
        Expected Json
        {
            "name": Mr Smith,
            "max_credit_hours": 1
            "courses": [101, 102, 103] IDs
        }
    """
    data = request.json
    new_prof = Professor(
        name=data.get('name'),
        max_credit_hours=data.get('max_credit_hours')
    )
    course_ids = data.get('courses')
    if course_ids:
        for course_id in course_ids:
            course = Course.query.get(course_id)
            if course:
                new_prof.courses.append(course)
                

    db.session.add(new_prof)
    db.session.commit()
    return jsonify({'message': 'Professor added successfully'}), 201

@professors_blueprint.route('/professors/<int:professor_id>', methods=['PUT'])
def update_professor_by_id(professor_id):
    """
        Updates Professor by ID.
        Id is stored in HTTP string
    """
    prof = Professor.query.get(professor_id)
    if not prof:
        return jsonify({'error': 'Professor not found'}), 404
    data = request.json
    prof.name = data.get('name', prof.name)
    prof.max_credit_hours = data.get('max_credit_hours', prof.max_credit_hours)

    # Optionally assign and delete courses if provided
    courses = data.get('courses')
    if courses:
        for cour in courses:
            course = Course.query.get(cour)
            if course:
                if course not in prof.courses:
                    prof.courses.append(course)
            else:
                pass
        for course in prof.courses:
            if course.id not in courses:
                prof.courses.remove(course)

                
    db.session.commit()
    return jsonify({'message': 'Professor updated successfully'})


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