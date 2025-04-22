import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ClickableTable from '@/Shared/components/ClickableTable';
import roomService from '@/Services/roomService';
import { room } from '@/types/roomTypes';
import { toast } from 'react-toastify';
import CreateButton from '@/Shared/components/CreateButton';

function RoomDash() {
  const [room, setRoom] = useState<room[]>([]);
  const navigate = useNavigate();

  const columns = [
    { title: 'Name', field: 'name' },
    { title: 'Capacity', field: 'capacity' },
  ];

  useEffect(() => {
    const fetchData = async () => {
      const data = await roomService.getAll();
      setRoom(data);
    };
    fetchData();
  }, []);

  const handleRowClick = (row: room) => {
    navigate(`/room/${row.id}`);
  };

  const deleteProfessor = async (id: number) => {
    await roomService.delete(id);
  };

  const handleDeleteClick = async (r: room) => {
    const originalRooms = [...room];
    try {
      setRoom(room.filter((room) => room.id !== r.id));
      await deleteProfessor(r.id);
      toast.success('Professor deleted successfully');
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      setRoom(originalRooms);
      toast.error('Error deleting Professor, please try again');
    }
  };

  return (
    <>
      <h1 className='flex justify-center align-items-center'>
        Rooms
        <CreateButton handleClick={() => navigate('/rooms/add')}></CreateButton>
      </h1>
      <ClickableTable
        columns={columns}
        data={room}
        onRowClick={handleRowClick}
        onRowDelete={handleDeleteClick}
        deleteModalRenderer={undefined}
      />
    </>
  );
}
export default RoomDash;
