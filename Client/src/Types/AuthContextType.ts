export interface AuthContextType {
  isAuthenticated: boolean;
  userPermissions: number | null;
  setToken: (token: string | null) => void;
}
