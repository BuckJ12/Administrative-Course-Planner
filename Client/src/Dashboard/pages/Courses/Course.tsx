import ClickableTable from '@/Shared/components/ClickableTable';
import CourseService from '@/Services/courseService';
import { toast } from 'react-toastify';
import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { courseFullDTO } from '@/types/courseTypes';
import BackButton from '@/Shared/components/BackButton';
import UpdateButton from '@/Shared/components/UpdateButton';
import { professor } from '@/types/professorTypes';
import { room } from '@/types/roomTypes';
import Loading from '@/Shared/components/Loading';
import CourseCard from './CourseCard';

function Course() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [course, setCourse] = useState<courseFullDTO | null>(null);
  const { id } = useParams();

  // Convert id to a number
  const numericId = Number(id);

  useEffect(() => {
    // Check if numericId is a valid number
    if (isNaN(numericId)) {
      toast.error('Invalid course id');
      navigate('/courses');
      return;
    }

    const fetchCourse = async () => {
      try {
        const data = await CourseService.getById(numericId);
        setCourse(data);
        setIsLoading(false);
      } catch (error) {
        toast.error('Failed to fetch course details');
        console.error('Error fetching course details:', error);
      }
    };

    fetchCourse();
  }, []);

  const professorColumns = [
    { title: 'Name', field: 'name' },
    { title: 'Max Hours', field: 'max_credit_hours' },
  ];
  const roomColumns = [
    { title: 'Name', field: 'name' },
    { title: 'Capacity', field: 'capacity' },
  ];
  const handleProfRowClick = (row: professor) =>
    navigate(`/professor/${row.id}`);
  const handleRoomRowClick = (row: room) => navigate(`/room/${row.id}`);

  const goToUpdate = () => toast('Feature Not Yet Implemented'); //navigate(`/course/${course?.course_id}/edit`); //Todo Fix edit to work
  const goBack = () => navigate('/courses');

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div>
      <div className='relative w-full mb-4'>
        <BackButton handleClick={goBack}>Courses</BackButton>
        <div className='flex justify-center items-center h-full'>
          <h1 className='flex items-center justify-center mb-0'>
            {`${course?.name}`}
            <UpdateButton handleClick={goToUpdate} />
          </h1>
        </div>
      </div>

      <CourseCard
        name={course!.name}
        creditHours={course!.credit_hours}
        meeting_Days={course!.meeting_days}
        numberOfSections={course!.number_of_sections}
        max_students={course!.max_students}
      />
      <div className='flex gap-4'>
        <div className='mb-4 flex-auto'>
          <h4 className='mb-2'>Professors</h4>
          <ClickableTable
            columns={professorColumns}
            data={course?.professors || []}
            onRowClick={handleProfRowClick}
            onRowDelete={undefined}
            deleteModalRenderer={undefined}
          />
        </div>

        <div className='mb-4 flex-auto'>
          <h4 className='mb-2'>Allowed Rooms</h4>
          <ClickableTable
            columns={roomColumns}
            data={course?.rooms || []}
            onRowClick={handleRoomRowClick}
            onRowDelete={undefined}
            deleteModalRenderer={undefined}
          />
        </div>
      </div>
    </div>
  );
}

export default Course;
