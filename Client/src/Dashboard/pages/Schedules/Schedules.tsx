import schedulerService from '@/Services/schedulerService';
import { useEffect, useState } from 'react';
import ClickableTable from '@/Shared/components/ClickableTable';
import Loading from '@/Shared/components/Loading';

export default function Schedules() {
  const [schedulerData, setSchedulerData] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  const scheduleColumns = [
    {
      title: 'Time Slots',
      field: 'time_slots',
      render: (rowData: any) =>
        Array.isArray(rowData.time_slots)
          ? rowData.time_slots.join(', ')
          : rowData.time_slots,
    },
    { title: 'Day', field: 'days' },
    { title: 'Course', field: 'course_name' },
    { title: 'Professor', field: 'professor' },
    { title: 'Room', field: 'room' },
  ];

  useEffect(() => {
    const fetchData = async () => {
      const data = await schedulerService.getNew();
      //console.log(data.schedule);
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
