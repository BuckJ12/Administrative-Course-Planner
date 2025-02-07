-- Create the database
drop database CourseScheduling;
CREATE DATABASE IF NOT EXISTS CourseScheduling;

USE CourseScheduling;

-- Table for storing courses
CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) UNIQUE NOT NULL,
    credit_hours INT NOT NULL,
    meeting_days ENUM('MWF', 'TTh') NOT NULL
);

-- Table for storing professors
CREATE TABLE Professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    max_credit_hours INT NOT NULL
);

-- Table to store which professors can teach which courses (Many-to-Many)
CREATE TABLE Course_Professors (
    course_id INT,
    professor_id INT,
    PRIMARY KEY (course_id, professor_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (professor_id) REFERENCES Professors(professor_id) ON DELETE CASCADE
);

-- Table for rooms
CREATE TABLE Rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(50) UNIQUE NOT NULL,
    capacity INT NOT NULL
);

-- Table for room restrictions (some courses can only be in specific rooms)
CREATE TABLE Room_Restrictions (
    course_id INT,
    room_id INT,
    PRIMARY KEY (course_id, room_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE CASCADE
);

-- Table for available time slots
CREATE TABLE Time_Slots (
    time_slot_id INT AUTO_INCREMENT PRIMARY KEY,
    time VARCHAR(20) NOT NULL,
    meeting_days ENUM('MWF', 'TTh') NOT NULL
);

-- Table for course sections
CREATE TABLE Sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    section_number INT NOT NULL,
    UNIQUE (course_id, section_number),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

-- Table for scheduling sections with professors, rooms, and time slots
CREATE TABLE Schedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    professor_id INT NOT NULL,
    room_id INT NOT NULL,
    time_slot_id INT NOT NULL,
    FOREIGN KEY (section_id) REFERENCES Sections(section_id) ON DELETE CASCADE,
    FOREIGN KEY (professor_id) REFERENCES Professors(professor_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE CASCADE,
    FOREIGN KEY (time_slot_id) REFERENCES Time_Slots(time_slot_id) ON DELETE CASCADE
);

-- Table for tracking course enrollment limits
CREATE TABLE Course_Enrollment_Limits (
    course_id INT PRIMARY KEY,
    max_students INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);
