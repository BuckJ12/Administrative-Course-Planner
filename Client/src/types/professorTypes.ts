import { courses } from './courseTypes';

export interface professor {
  id: number;
  name: string;
  max_credit_hours: number;
  courses: courses[];
}

export interface profDTO {
  name: string;
  max_credit_hours: number;
  courses: number[];
  timeSlotRestrictions: number[];
}

export interface profFullDTO {
  id: number;
  name: string;
  max_credit_hours: number;
  courses: courses[];
  timeSlotRestrictions: number[];
}
