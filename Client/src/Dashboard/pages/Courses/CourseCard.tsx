import DetailItem from '@/Shared/components/DetailItem';

interface CourseCardProps {
  name: string;
  creditHours: number;
  meeting_Days: string;
  max_students: number;
  numberOfSections: number;
}

function ContactCard({
  name,
  creditHours,
  meeting_Days,
  numberOfSections,
  max_students,
}: CourseCardProps) {
  return (
    <div className='card shadow-md mb-4'>
      <div className='card-body'>
        <h4 className='mb-4'>Course Information</h4>
        <DetailItem label='Name' value={name} />
        <DetailItem label='Credit Hours' value={creditHours.toString()} />
        <DetailItem label='Meeting Day' value={meeting_Days} />
        <DetailItem label='Sections' value={numberOfSections.toString()} />
        <DetailItem label='Max Students' value={max_students.toString()} />
      </div>
    </div>
  );
}

export default ContactCard;
