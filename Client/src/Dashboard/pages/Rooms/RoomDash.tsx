import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ClickableTable from '@/Shared/components/ClickableTable';
import roomService from '@/Services/roomService';
import { room } from '@/types/roomTypes';
import { toast } from 'react-toastify';

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

  const handleDeleteClick = () => {
    toast('Feature Not Yet Implemented');
    // TODO: implement click functionality
  };

  return (
    <>
      <h1>Rooms</h1>
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
