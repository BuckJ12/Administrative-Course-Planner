import DetailItem from '@/Shared/components/DetailItem';

interface RoomCardProps {
  name: string;
  capcity: number;
}

function RoomCard({ name, capcity }: RoomCardProps) {
  return (
    <div className='card shadow-md mb-4'>
      <div className='card-body'>
        <h4 className='mb-4'>Room Information</h4>
        <DetailItem label='Name' value={name} />
        <DetailItem label='Capcity' value={capcity.toString()} />
      </div>
    </div>
  );
}

export default RoomCard;
