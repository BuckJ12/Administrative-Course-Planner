from flask import Blueprint, jsonify, request
from models import Section, db

sections_blueprint = Blueprint('sections', __name__)

@sections_blueprint.route('/sections', methods=['GET'])
def get_sections():
    """
    Returns all the Section Slots
    Output Json
    {
        "section_id": 1,
        "course_id": 1,
        "section_number": 1
    }
    """
    sections = Section.query.all()
    data = [{
        'section_id': sec.section_id,
        'course_id': sec.course_id,
        'section_number': sec.section_number
    } for sec in sections]
    return jsonify(data)

@sections_blueprint.route('/sections', methods=['POST'])
def add_section():
    """
        Adds a new Section Slot
        Expected Json
        {
            "course_id": 1,
            "section_number": 1
        }
    """
    data = request.json
    new_section = Section(
        course_id=data.get('course_id'),
        section_number=data.get('section_number')
    )
    db.session.add(new_section)
    db.session.commit()
    return jsonify({'message': 'Section added successfully'}), 201

@sections_blueprint.route('/sections/<int:section_id>', methods=['DELETE'])
def delete_section_by_id(section_id):
    """
        Deletes Section by ID.
        Id is stored in HTTP string
    """
    sec = Section.query.get(section_id)
    if not sec:
        return jsonify({'error': 'Section not found'}), 404
    db.session.delete(sec)
    db.session.commit()
    return jsonify({'message': 'Section deleted successfully'})
