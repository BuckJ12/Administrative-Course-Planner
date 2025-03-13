import http from './httpService';
import { apiUrl } from '../config';

const apiEndpoint = `${apiUrl}/schedules`;

export default class schedulerService {
  static https = http.create();

  static async getNew() {
    const response = await schedulerService.https.get(
      `${apiEndpoint}/generate`
    );
    return response.data;
  }
}
