from flask import Blueprint, jsonify
from models import db
from scheduler import generate_schedule

scheduler_blueprint = Blueprint('scheduler', __name__)

@scheduler_blueprint.route('/schedules/generate', methods=['GET'])
def generate_schedule_route():
    result = generate_schedule(db.session)
    if result.get("status") != "Schedule generated successfully.":
        return jsonify(result), 400
    return jsonify(result)
