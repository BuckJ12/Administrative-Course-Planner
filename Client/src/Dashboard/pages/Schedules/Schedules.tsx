import schedulerService from '@/Services/schedulerService';
import { useEffect, useState } from 'react';
import ClickableTable from '@/Shared/components/ClickableTable';
import Loading from '@/Shared/components/Loading';

export default function Schedules() {
  const [schedulerData, setSchedulerData] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  const scheduleColumns = [
    { title: 'Course', field: 'course_name' },
    { title: 'Professor', field: 'professor' },
    { title: 'Room', field: 'room' },
    { title: 'Day', field: 'days' },
    { title: 'Time', field: 'time' },
  ];

  useEffect(() => {
    const fetchData = async () => {
      const data = await schedulerService.getNew();
      setSchedulerData(data.schedule);
      setIsLoading(false);
    };
    fetchData();
  }, []);
  if (isLoading) {
    return <Loading />;
  }

  return (
    <div>
      <h1>Schedules</h1>
      <ClickableTable
        columns={scheduleColumns}
        data={schedulerData}
        onRowClick={undefined}
        onRowDelete={undefined}
        deleteModalRenderer={undefined}
      />
    </div>
  );
}
