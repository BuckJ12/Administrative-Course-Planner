# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'Courses'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), unique=True, nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)
    meeting_days = db.Column(db.Enum('MWF', 'TTh'), nullable=False)

class Professor(db.Model):
    __tablename__ = 'Professors'
    professor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    max_credit_hours = db.Column(db.Integer, nullable=False)

class CourseProfessor(db.Model):
    __tablename__ = 'Course_Professors'
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.course_id', ondelete='CASCADE'), primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('Professors.professor_id', ondelete='CASCADE'), primary_key=True)

class Room(db.Model):
    __tablename__ = 'Rooms'
    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class RoomRestriction(db.Model):
    __tablename__ = 'Room_Restrictions'
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.course_id', ondelete='CASCADE'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.room_id', ondelete='CASCADE'), primary_key=True)

class TimeSlot(db.Model):
    __tablename__ = 'Time_Slots'
    time_slot_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), nullable=False)
    meeting_days = db.Column(db.Enum('MWF', 'TTh'), nullable=False)

class Section(db.Model):
    __tablename__ = 'Sections'
    section_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.course_id', ondelete='CASCADE'), nullable=False)
    section_number = db.Column(db.Integer, nullable=False)

class ScheduleModel(db.Model):
    __tablename__ = 'Schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('Sections.section_id', ondelete='CASCADE'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('Professors.professor_id', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.room_id', ondelete='CASCADE'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('Time_Slots.time_slot_id', ondelete='CASCADE'), nullable=False)

class CourseEnrollmentLimit(db.Model):
    __tablename__ = 'Course_Enrollment_Limits'
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.course_id', ondelete='CASCADE'), primary_key=True)
    max_students = db.Column(db.Integer, nullable=False)
