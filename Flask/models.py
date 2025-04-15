# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'Courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)
    meeting_days = db.Column(db.Enum('MWF', 'TTh'), nullable=False)
    sections = db.relationship('Section', backref='course', cascade="all, delete", lazy=True)
    slots_needed = db.Column(db.Integer, default=1, nullable=False) 
    max_students = db.Column(db.Integer, nullable=False)
    professors = db.relationship('Professor', secondary='Course_Professors',
                                backref=db.backref('courses', lazy=True))
    rooms = db.relationship('Room', secondary='Room_Restrictions',
                                backref=db.backref('courses', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'credit_hours': self.credit_hours,
            'meeting_days': self.meeting_days,
            'sections': [section.section_number for section in self.sections],
            'professors': [professor.name for professor in self.professors],
        }
class Professor(db.Model):
    __tablename__ = 'Professors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    max_credit_hours = db.Column(db.Integer, nullable=False)
    time_restrictions = db.relationship('TimeSlot', secondary='Time_Restrictions',
                                backref=db.backref('professors', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'max_credit_hours': self.max_credit_hours,
        }

class CourseProfessor(db.Model):
    __tablename__ = 'Course_Professors'
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id', ondelete='CASCADE'), primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('Professors.id', ondelete='CASCADE'), primary_key=True)

class Room(db.Model):
    __tablename__ = 'Rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'capacity': self.capacity,
        }

class RoomRestriction(db.Model):
    __tablename__ = 'Room_Restrictions'
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id', ondelete='CASCADE'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id', ondelete='CASCADE'), primary_key=True)

class TimeSlot(db.Model):
    __tablename__ = 'Time_Slots'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), nullable=False)
    meeting_days = db.Column(db.Enum('MWF', 'TTh'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time,
            'meeting_days': self.meeting_days,
        }

class Section(db.Model):
    __tablename__ = 'Sections'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id', ondelete='CASCADE'), nullable=False)
    section_number = db.Column(db.Integer, nullable=False)

class ScheduleModel(db.Model):
    __tablename__ = 'Schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('Sections.id', ondelete='CASCADE'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('Professors.id', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id', ondelete='CASCADE'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('Time_Slots.id', ondelete='CASCADE'), nullable=False)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    permission = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, permission):
        self.username = username
        self.password = generate_password_hash(password)
        self.permission = permission

class TimeRestrictions(db.Model):
    __tablename__ = 'Time_Restrictions'
    professor_id = db.Column(db.Integer, db.ForeignKey('Professors.id', ondelete='CASCADE'), primary_key=True)
    timeslot_id = db.Column(db.Integer, db.ForeignKey('Time_Slots.id', ondelete='CASCADE'), primary_key=True)

