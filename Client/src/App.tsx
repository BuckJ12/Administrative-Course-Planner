import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styles from './App.module.css';
import CourseDash from './Dashboard/pages/Courses/CourseDash';
import AddCourse from './Dashboard/pages/Courses/AddCourse';
import Course from './Dashboard/pages/Courses/Course';
import ProfDash from './Dashboard/pages/Professors/ProfDash';
import Professor from './Dashboard/pages/Professors/Professor';
import AddProfessor from './Dashboard/pages/Professors/AddProfessor';
import RoomDash from './Dashboard/pages/Rooms/RoomDash';
import AddRoom from './Dashboard/pages/Rooms/AddRoom';
import Room from './Dashboard/pages/Rooms/Room';
import Sidebar from './Shared/components/Sidebar';

function App() {
  return (
    <div className={styles.content}>
      <Router>
        <ToastContainer />
        <Sidebar />
        <Routes>
          {/* Define your routes here */}
          {/* Root route example */}
          {/* Course routes */}
          <Route path='/courses' element={<CourseDash />} />
          <Route path='/courses/add' element={<AddCourse />} />
          <Route path='/course/:id' element={<Course />} />
          {/* Professors route */}
          <Route path='/professors' element={<ProfDash />} />
          <Route path='/professors/add' element={<AddProfessor />} />
          <Route path='/professor/:id' element={<Professor />} />
          {/* Room routes */}
          <Route path='/rooms' element={<RoomDash />} />
          <Route path='/rooms/add' element={<AddRoom />} />
          <Route path='/room/:id' element={<Room />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
