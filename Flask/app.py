# app.py
from flask import Flask
from config import Config
from models import db
from routes.courses import courses_blueprint
from routes.professors import professors_blueprint
from routes.rooms import rooms_blueprint
from routes.time_slots import time_slots_blueprint
from routes.scheduler import scheduler_blueprint
#from routes.auth import auth_blueprint
from flask_cors import CORS
import pymysql
pymysql.install_as_MySQLdb()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    # Create the database tables if they don't exist.
    with app.app_context():
        db.create_all()

    # Register our blueprint
    app.register_blueprint(courses_blueprint)
    app.register_blueprint(professors_blueprint)
    app.register_blueprint(rooms_blueprint)
    app.register_blueprint(time_slots_blueprint)
    app.register_blueprint(scheduler_blueprint)
    # app.register_blueprint(auth_blueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
