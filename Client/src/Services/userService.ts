import http from "./httpService";
import { AuthResponse } from "../Types/AuthResponse";
import { apiUrl } from "../config";

const apiEndpoint = `${apiUrl}`;

export default class UserService {
  static http = http.create();

  static async CheckID() {
    const response = await http.get(`${apiEndpoint}/validate-token`);
    return response.data;
  }

  static async login(username: string, password: string) {
    const response = await http.post<AuthResponse>(`${apiEndpoint}/login`, {
      username,
      password,
    });
    return response;
  }
}
