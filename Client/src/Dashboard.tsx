import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import ClickableTable from "./Components/ClickableTable";

// Define interfaces for your data types
interface Course {
  course_id: number;
  course_name: string;
  credit_hours: number;
  meeting_days: string;
}

interface Professor {
  id: number;
  name: string;
  department: string;
  // Add additional fields as needed
}

interface Room {
  id: number;
  room_name: string;
  capacity: number;
  // Add additional fields as needed
}

const Dashboard: React.FC = () => {
  // Local state for the different data items
  const [courses, setCourses] = useState<Course[]>([]);
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [error, setError] = useState<string>("");

  // Get the JWT token from localStorage (or your auth context)
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  useEffect(() => {
    // Define a common config with authorization header
    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };

    // Fetch courses
    axios
      .get<Course[]>("http://localhost:5000/courses", config)
      .then((res) => setCourses(res.data))
      .catch((err) => {
        console.error("Error fetching courses:", err);
        setError("Error fetching courses");
      });

    // Fetch professors
    axios
      .get<Professor[]>("http://localhost:5000/professors", config)
      .then((res) => setProfessors(res.data))
      .catch((err) => {
        console.error("Error fetching professors:", err);
        setError("Error fetching professors");
      });

    // Fetch rooms
    axios
      .get<Room[]>("http://localhost:5000/rooms", config)
      .then((res) => setRooms(res.data))
      .catch((err) => {
        console.error("Error fetching rooms:", err);
        setError("Error fetching rooms");
      });
  }, [token]);

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <section>
        <h2>
          <a onClick={() => navigate("/addCourse")}>Courses</a>
        </h2>
        <ClickableTable<Course>
          data={courses}
          columns={[
            { header: "ID", accessor: "course_id" },
            { header: "Name", accessor: "course_name" },
            { header: "Credit Hours", accessor: "credit_hours" },
            { header: "Meeting Days", accessor: "meeting_days" },
          ]}
          onRowClick={(course) => navigate(`/courses/${course.course_id}`)}
        />
      </section>

      <section>
        <h2>Professors</h2>
        <ul>
          {professors.map((prof) => (
            <li key={prof.id}>
              <strong>{prof.name}</strong> — {prof.department}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Rooms</h2>
        <ul>
          {rooms.map((room) => (
            <li key={room.id}>
              <strong>{room.room_name}</strong> — Capacity: {room.capacity}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default Dashboard;
