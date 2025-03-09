import { toast } from 'react-toastify';
import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import BackButton from '@/Shared/components/BackButton';
import UpdateButton from '@/Shared/components/UpdateButton';
import Loading from '@/Shared/components/Loading';
import { room } from '@/types/roomTypes';
import RoomService from '@/Services/roomService';
import RoomCard from './RoomCard';

function Room() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [room, setRoom] = useState<room | null>(null);
  const { id } = useParams();

  // Convert id to a number
  const numericId = Number(id);

  useEffect(() => {
    // Check if numericId is a valid number
    if (isNaN(numericId)) {
      toast.error('Invalid course id');
      navigate('/rooms');
      return;
    }

    const fetchCourse = async () => {
      try {
        const data = await RoomService.getById(numericId);
        setRoom(data);
        setIsLoading(false);
      } catch (error) {
        toast.error('Failed to fetch course details');
        console.error('Error fetching course details:', error);
      }
    };

    fetchCourse();
  }, []);

  const goToUpdate = () => toast('Feature Not Yet Implemented'); //navigate(`/course/${course?.course_id}/edit`); //Todo Fix edit to work
  const goBack = () => navigate('/professors');

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div>
      <div className='relative w-full mb-4'>
        <BackButton handleClick={goBack}>Rooms</BackButton>
        <div className='flex justify-center items-center h-full'>
          <h1 className='flex items-center justify-center mb-0'>
            {`${room?.name}`}
            <UpdateButton handleClick={goToUpdate} />
          </h1>
        </div>
      </div>

      <RoomCard name={room!.name} capcity={room!.capacity} />
    </div>
  );
}

export default Room;
