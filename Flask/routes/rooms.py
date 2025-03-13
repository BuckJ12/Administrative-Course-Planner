from flask import Blueprint, jsonify, request
from models import Room, db

rooms_blueprint = Blueprint('rooms', __name__)

@rooms_blueprint.route('/rooms', methods=['GET'])
def get_rooms():
    """
    Returns all the Rooms
    Output Json
    {
        "id": 1,
        "name": Mr Smith,
        "capacity": 1
    }
    """
    rooms = Room.query.all()
    data = [{
        'id': room.id,
        'name': room.name,
        'capacity': room.capacity
    } for room in rooms]
    return jsonify(data)

@rooms_blueprint.route('/rooms/<int:room_id>', methods=['GET'])
def get_room_by_id(room_id):
    """
    Returns a Room by ID
    Output Json
    {
        "id": 1,
        "name": Mr Smith,
        "capacity": 1
    }
    """
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    return jsonify({
        'id': room.id,
        'name': room.name,
        'capacity': room.capacity
    })

@rooms_blueprint.route('/rooms', methods=['POST'])
def add_room():
    """
        Adds a new Room
        Expected Json
        {
            "name": Lab 103,
            "capacity": 1
        }
    """
    data = request.json
    new_room = Room(
        name=data.get('name'),
        capacity=data.get('capacity')
    )
    db.session.add(new_room)
    db.session.commit()
    return jsonify({'message': 'Room added successfully'}), 201

@rooms_blueprint.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room_by_id(room_id):
    """
        Deletes Room by ID.
        Id is stored in HTTP string
    """
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted successfully'})