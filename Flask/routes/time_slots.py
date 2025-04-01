from flask import Blueprint, jsonify, request
from models import TimeSlot, db

time_slots_blueprint = Blueprint('time_slots', __name__)

@time_slots_blueprint.route('/time_slots', methods=['GET'])
def get_time_slots():
    """
    Returns all the Time Slots
    Output Json
    {
        "id": 1,
        "time": 2:30,
        "meeting_days": MWF
    }
    """
    ts = TimeSlot.query.all()
    data = [{
        'id': slot.id,
        'time': slot.time,
        'meeting_days': slot.meeting_days
    } for slot in ts]
    return jsonify(data)

@time_slots_blueprint.route('/time_slots', methods=['POST'])
def add_time_slot():
    """
        Adds a new Time Slot
        Expected Json
        {
            "time": Mr Smith,
            "meeting_days": MWF
        }
    """
    data = request.json
    new_slot = TimeSlot(
        time=data.get('time'),
        meeting_days=data.get('meeting_days')
    )
    db.session.add(new_slot)
    db.session.commit()
    return jsonify({'message': 'Time slot added successfully'}), 201

@time_slots_blueprint.route('/time_slots/<int:time_slot_id>', methods=['DELETE'])
def delete_time_slot_by_id(time_slot_id):
    """
        Deletes Time Slot by ID.
        Id is stored in HTTP string
    """
    slot = TimeSlot.query.get(time_slot_id)
    if not slot:
        return jsonify({'error': 'Time slot not found'}), 404
    db.session.delete
