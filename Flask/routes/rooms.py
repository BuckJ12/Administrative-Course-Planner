from flask import Blueprint, jsonify, request
from models import Room, db

rooms_blueprint = Blueprint('rooms', __name__)

@rooms_blueprint.route('/rooms', methods=['GET'])
def get_rooms():
    """
    Returns all the Rooms
    Output Json
    {
        "room_id": 1,
        "room_name": Mr Smith,
        "capacity": 1
    }
    """
    rooms = Room.query.all()
    data = [{
        'room_id': room.room_id,
        'room_name': room.room_name,
        'capacity': room.capacity
    } for room in rooms]
    return jsonify(data)

@rooms_blueprint.route('/rooms', methods=['POST'])
def add_room():
    """
        Adds a new Room
        Expected Json
        {
            "room_name": Mr Smith,
            "capacity": 1
        }
    """
    data = request.json
    new_room = Room(
        room_name=data.get('room_name'),
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

@rooms_blueprint.route('/rooms/delete_by_name/<string:room_name>', methods=['DELETE'])
def delete_room_by_name(room_name):
    """
        Deletes Room by Name.
        Name is stored in HTTP string
    """
    room = Room.query.filter_by(room_name=room_name).first()
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted successfully'})
