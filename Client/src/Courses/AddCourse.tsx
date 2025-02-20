import React, { useState, FormEvent } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const AddCourse: React.FC = () => {
  const [courseName, setCourseName] = useState<string>("");
  const [creditHours, setCreditHours] = useState<number>(0);
  const [meetingDays, setMeetingDays] = useState<string>("");
  const [error, setError] = useState<string>("");
  const navigate = useNavigate();

  // Get the JWT token from localStorage
  const token = localStorage.getItem("token");

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    const newCourse = {
      course_name: courseName,
      credit_hours: creditHours,
      meeting_days: meetingDays,
    };

    // Configure the request with the Authorization header
    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };

    try {
      await axios.post("http://localhost:5000/courses", newCourse, config);
      // Navigate back to the dashboard after successful addition
      navigate("/dashboard");
    } catch (err) {
      console.error("Error adding course:", err);
      setError("Error adding course. Please try again.");
    }
  };

  return (
    <div className="add-course">
      <h1>Add New Course</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="courseName">Course Name:</label>
          <input
            type="text"
            id="courseName"
            value={courseName}
            onChange={(e) => setCourseName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="creditHours">Credit Hours:</label>
          <input
            type="number"
            id="creditHours"
            value={creditHours}
            onChange={(e) => setCreditHours(parseInt(e.target.value, 10) || 0)}
            required
          />
        </div>
        <div>
          <label htmlFor="meetingDays">Meeting Days:</label>
          <input
            type="text"
            id="meetingDays"
            value={meetingDays}
            onChange={(e) => setMeetingDays(e.target.value)}
            required
          />
        </div>
        <button type="submit">Add Course</button>
      </form>
    </div>
  );
};

export default AddCourse;
