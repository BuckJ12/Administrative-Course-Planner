import React from 'react';
import { Table } from 'react-bootstrap';
import { timeSlot } from '@/types/timeTypes';
import IconCheckbox from './IconCheckbox';

interface TimeSlotChartProps {
  timeSlots: timeSlot[];
  selectedIds: number[];
  onToggle: (id: number) => void;
  readOnly?: boolean;
}

const TimeSlotChart: React.FC<TimeSlotChartProps> = ({
  timeSlots,
  selectedIds,
  onToggle,
  readOnly = false,
}) => {
  // Generate a sorted list of unique times from the timeSlots data.
  const uniqueTimes = Array.from(
    new Set(timeSlots.map((slot) => slot.time))
  ).sort((a, b) => {
    const [aH, aM, aS] = a.split(':').map(Number);
    const [bH, bM, bS] = b.split(':').map(Number);
    return aH * 3600 + aM * 60 + aS - (bH * 3600 + bM * 60 + bS);
  });

  // Build lookup maps for each meeting days group.
  const mwfLookup = timeSlots
    .filter((slot) => slot.meeting_days === 'MWF')
    .reduce((acc, slot) => {
      acc[slot.time] = slot;
      return acc;
    }, {} as Record<string, timeSlot>);

  const tthLookup = timeSlots
    .filter((slot) => slot.meeting_days === 'TTh')
    .reduce((acc, slot) => {
      acc[slot.time] = slot;
      return acc;
    }, {} as Record<string, timeSlot>);

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>Time</th>
          <th>MWF</th>
          <th>TTh</th>
        </tr>
      </thead>
      <tbody>
        {uniqueTimes.map((time) => (
          <tr key={time}>
            <td>{time}</td>
            <td>
              {mwfLookup[time] && (
                <IconCheckbox
                  checked={selectedIds.includes(mwfLookup[time].id)}
                  onClick={() => onToggle(mwfLookup[time].id)}
                  readOnly={readOnly}
                />
              )}
            </td>
            <td>
              {tthLookup[time] && (
                <IconCheckbox
                  checked={selectedIds.includes(tthLookup[time].id)}
                  onClick={() => onToggle(tthLookup[time].id)}
                  readOnly={readOnly}
                />
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default TimeSlotChart;
