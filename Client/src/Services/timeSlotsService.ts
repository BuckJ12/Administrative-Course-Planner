import http from './httpService';
import { apiUrl } from '../config';
import { timeSlot } from '@/types/timeTypes';

const apiEndpoint = `${apiUrl}/time_slots`;

export default class TimeSlotsService {
  static https = http.create();

  static async getAll(): Promise<timeSlot[]> {
    const response = await TimeSlotsService.https.get(`${apiEndpoint}`);
    return response.data;
  }
}
