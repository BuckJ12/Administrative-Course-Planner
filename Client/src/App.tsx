// src/App.tsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./Dashboard";
import AddCourse from "./Courses/AddCourse";
import Courses from "./Courses/courses";
import Unauthorized from "./unauthorized";
import Home from "./home";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Public Route */}
        <Route path="/login" element={<Home />} />
        <Route path="/unauthorized" element={<Unauthorized />} />

        {/* Need to be Later Protected Routes */}
        <Route path="/home" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/add-course" element={<AddCourse />} />
        <Route path="/courses/:id" element={<Courses />} />

        {/* Catch-All Route */}
        <Route path="*" element={<Home />} />
      </Routes>
    </Router>
  );
};

export default App;
