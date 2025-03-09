import DetailItem from '@/Shared/components/DetailItem';

interface ProfCardProps {
  name: string;
  maxCreditHours: number;
}

function ProfCard({ name, maxCreditHours }: ProfCardProps) {
  return (
    <div className='card shadow-md mb-4'>
      <div className='card-body'>
        <h4 className='mb-4'>Course Information</h4>
        <DetailItem label='Name' value={name} />
        <DetailItem
          label='Max Credit Hours'
          value={maxCreditHours.toString()}
        />
      </div>
    </div>
  );
}

export default ProfCard;
