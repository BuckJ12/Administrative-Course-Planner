import { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import styles from './Sidebar.module.css';

function Sidebar() {
  const location = useLocation();
  const [isExpanded, setIsExpanded] = useState({
    course: false,
    prof: false,
    room: false,
  });

  useEffect(() => {
    if (location.pathname.startsWith('/courses')) {
      setIsExpanded({ course: true, prof: false, room: false });
    } else if (location.pathname.startsWith('/professors')) {
      setIsExpanded({ course: false, prof: true, room: false });
    } else if (location.pathname.startsWith('/rooms')) {
      setIsExpanded({ course: false, prof: false, room: true });
    } else {
      setIsExpanded({ course: false, prof: false, room: false });
    }
  }, [location]);
  const handleExpandClick = (section: 'course' | 'prof' | 'room') => {
    setIsExpanded({ ...isExpanded, [section]: !isExpanded[section] });
  };

  return (
    <div className={`${styles.sidebar} flex flex-col`}>
      <li className={styles.nav}>
        <div onClick={() => null}>
          <NavLink to='/'>
            <img
              src='/ChronoSync.png'
              alt='Logo'
              className={styles.logoImage}
            />
          </NavLink>
        </div>
      </li>
      <ul className={styles.nav}>
        <li className={styles.navItem}>
          <div onClick={() => handleExpandClick('course')}>
            <NavLink
              to='/courses'
              className={({ isActive }) =>
                isActive ? `${styles.activeNavLink}` : ''
              }
            >
              Courses
            </NavLink>
            <span
              className={isExpanded.course ? styles.arrowUp : styles.arrowDown}
            />
          </div>
          {isExpanded.course && (
            <>
              <ul className={styles.subNav}>
                <li className={styles.subNavItem}>
                  <NavLink
                    to='/courses/add'
                    className={({ isActive }) =>
                      isActive ? `${styles.activeNavLink}` : ''
                    }
                  >
                    - Create
                  </NavLink>
                </li>
              </ul>
            </>
          )}
        </li>
        <li className={styles.navItem}>
          <div onClick={() => handleExpandClick('prof')}>
            <NavLink
              to='/professors'
              className={({ isActive }) =>
                isActive ? `${styles.activeNavLink}` : ''
              }
            >
              Professors
            </NavLink>
            <span
              className={isExpanded.prof ? styles.arrowUp : styles.arrowDown}
            />
          </div>
          {isExpanded.prof && (
            <ul className={styles.subNav}>
              <li className={styles.subNavItem}>
                <NavLink
                  to='/professors/add'
                  className={({ isActive }) =>
                    isActive ? `${styles.activeNavLink}` : ''
                  }
                >
                  - Create
                </NavLink>
              </li>
            </ul>
          )}
        </li>
        <li className={styles.navItem}>
          <div onClick={() => handleExpandClick('room')}>
            <NavLink
              to='/rooms'
              className={({ isActive }) =>
                isActive ? `${styles.activeNavLink}` : ''
              }
            >
              Rooms
            </NavLink>
            <span
              className={isExpanded.room ? styles.arrowUp : styles.arrowDown}
            />
          </div>
          {isExpanded.room && (
            <ul className={styles.subNav}>
              <li className={styles.subNavItem}>
                <NavLink
                  to='/rooms/add'
                  className={({ isActive }) =>
                    isActive ? `${styles.activeNavLink}` : ''
                  }
                >
                  - Create
                </NavLink>
              </li>
            </ul>
          )}
        </li>
      </ul>
    </div>
  );
}

export default Sidebar;
