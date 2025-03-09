import { professor } from './professorTypes';
import { room } from './roomTypes';

export interface courses {
  id: number;
  name: string;
  credit_hours: number;
  meeting_Days: string;
  max_students: number;
  numberOfSections: number;
  professors: string[];
}

export interface courseDTO {
  name: string;
  credit_hours: number;
  meeting_Days: string;
  numberOfSections: number;
  max_students: number;
  professors: number[];
}

export interface courseFullDTO {
  id: number;
  name: string;
  credit_hours: number;
  meeting_days: string;
  number_of_sections: number;
  max_students: number;
  professors: professor[];
  rooms: room[];
}
