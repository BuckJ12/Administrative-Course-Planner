import http from './httpService';
import { apiUrl } from '../config';
import { room, roomDTO } from '@/types/roomTypes';
const apiEndpoint = `${apiUrl}/rooms`;

export default class RoomService {
  static https = http.create();

  static async getAll(): Promise<room[]> {
    const response = await RoomService.https.get(apiEndpoint);
    return response.data;
  }

  static async create(createRoom: roomDTO) {
    const response = await RoomService.https.post(apiEndpoint, createRoom);
    return response.data;
  }

  static async getById(id: number): Promise<room> {
    const response = await RoomService.https.get(`${apiEndpoint}/${id}`);
    return response.data;
  }

  static async update(id: number, updateRoom: roomDTO) {
    const response = await RoomService.https.put(
      `${apiEndpoint}/${id}`,
      updateRoom
    );
    return response.data;
  }

  static async delete(id: number) {
    const response = await RoomService.https.delete(`${apiEndpoint}/${id}`);
    return response.data;
  }
}
