import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ClickableTable from '@/Shared/components/ClickableTable';
import courseService from '@/Services/courseService';
import { courses } from '@/types/courseTypes';

function CourseDash() {
  const [courses, setCourses] = useState<courses[]>([]);
  const navigate = useNavigate();

  const columns = [
    { title: 'Name', field: 'name' },
    { title: 'Credits', field: 'credit_hours' },
    { title: 'Days', field: 'meeting_days' },
    { title: 'Sections', field: 'number_of_sections' },
    { title: 'Max Students', field: 'max_students' },
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

  const handleDeleteClick = () => {
    // TODO: implement click functionality
  };

  return (
    <>
      <h1>Courses</h1>
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
