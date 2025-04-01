import { useEffect, useState } from 'react';
import TimeSlotsService from '@/Services/timeSlotsService';
import TimeSlotChart from '@/Shared/components/TimeSlotChart';
import { timeSlot } from '@/types/timeTypes';

export default function Testpage() {
  const [timeSlots, setTimeSlots] = useState<timeSlot[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);

  useEffect(() => {
    TimeSlotsService.getAll().then((response) => {
      setTimeSlots(response);
    });
  }, []);

  // Callback to toggle selection of a time slot by id.
  const toggleSelection = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  return (
    <div>
      <h2>Time Slot Chart</h2>
      <TimeSlotChart
        timeSlots={timeSlots}
        selectedIds={selectedIds}
        onToggle={toggleSelection}
      />
    </div>
  );
}
