import ClickableTable from '@/Shared/components/ClickableTable';
import ProfService from '@/Services/profService';
import { toast } from 'react-toastify';
import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import BackButton from '@/Shared/components/BackButton';
import UpdateButton from '@/Shared/components/UpdateButton';
import Loading from '@/Shared/components/Loading';
import ProfCard from './ProfCard';
import { profFullDTO } from '@/types/professorTypes';
import { courses } from '@/types/courseTypes';

function Professor() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [prof, setProf] = useState<profFullDTO | null>(null);
  const { id } = useParams();

  // Convert id to a number
  const numericId = Number(id);

  useEffect(() => {
    // Check if numericId is a valid number
    if (isNaN(numericId)) {
      toast.error('Invalid course id');
      navigate('/professors');
      return;
    }

    const fetchCourse = async () => {
      try {
        const data = await ProfService.getById(numericId);
        setProf(data);
        setIsLoading(false);
      } catch (error) {
        toast.error('Failed to fetch course details');
        console.error('Error fetching course details:', error);
      }
    };

    fetchCourse();
  }, []);

  const courseColumns = [
    { title: 'Name', field: 'name' },
    { title: 'Credits Hours', field: 'credit_hours' },
    { title: 'Days', field: 'meeting_days' },
    {
      title: 'Sections',
      field: 'sections',
      render: (rowData: any) => rowData.sections.length,
    },
  ];
  const handleCourseRowClick = (row: courses) => navigate(`/course/${row.id}`);

  const goToUpdate = () => toast('Feature Not Yet Implemented'); //navigate(`/course/${course?.course_id}/edit`); //Todo Fix edit to work
  const goBack = () => navigate('/professors');

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div>
      <div className='relative w-full mb-4'>
        <BackButton handleClick={goBack}>Professors</BackButton>
        <div className='flex justify-center items-center h-full'>
          <h1 className='flex items-center justify-center mb-0'>
            {`${prof?.name}`}
            <UpdateButton handleClick={goToUpdate} />
          </h1>
        </div>
      </div>

      <ProfCard name={prof!.name} maxCreditHours={prof!.max_credit_hours} />

      <div className='gap-4'>
        <div className='mb-4'>
          <h4 className='mb-2'>Courses</h4>
          <ClickableTable
            columns={courseColumns}
            data={prof?.courses || []}
            onRowClick={handleCourseRowClick}
            onRowDelete={undefined}
            deleteModalRenderer={undefined}
          />
        </div>
      </div>
    </div>
  );
}

export default Professor;
