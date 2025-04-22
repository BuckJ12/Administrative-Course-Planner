import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ClickableTable from '@/Shared/components/ClickableTable';
import courseService from '@/Services/courseService';
import { courses } from '@/types/courseTypes';
import { toast } from 'react-toastify';
import CreateButton from '@/Shared/components/CreateButton';

function CourseDash() {
  const [courses, setCourses] = useState<courses[]>([]);
  const navigate = useNavigate();

  const columns = [
    { title: 'Name', field: 'name' },
    { title: 'Credits', field: 'credit_hours' },
    { title: 'Days', field: 'meeting_days' },
    { title: 'Sections', field: 'number_of_sections' },
    { title: 'Max Students', field: 'max_students' },
    { title: 'Time Slots Needed', field: 'slots_needed' },
    {
      title: 'Professors',
      field: 'professors',
      render: (rowData: any) =>
        Array.isArray(rowData.professors)
          ? rowData.professors.join(', ')
          : rowData.professors,
    },
  ];

  useEffect(() => {
    const fetchData = async () => {
      const data = await courseService.getAll();
      setCourses(data);
    };
    fetchData();
  }, []);

  const handleRowClick = (row: courses) => {
    navigate(`/course/${row.id}`);
  };

  const deleteCourse = async (id: number) => {
    await courseService.delete(id);
  };

  const handleDeleteClick = async (c: courses) => {
    const originalCourses = [...courses];
    try {
      setCourses(courses.filter((course) => course.id !== c.id));
      await deleteCourse(c.id);
      toast.success('Course deleted successfully');
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      setCourses(originalCourses);
      toast.error('Error deleting course, please try again');
    }
  };

  return (
    <>
      <h1 className='flex justify-center align-items-center'>
        Courses
        <CreateButton
          handleClick={() => navigate('/courses/add')}
        ></CreateButton>
      </h1>
      <ClickableTable
        columns={columns}
        data={courses}
        onRowClick={handleRowClick}
        onRowDelete={handleDeleteClick}
        deleteModalRenderer={undefined}
      />
    </>
  );
}
export default CourseDash;
