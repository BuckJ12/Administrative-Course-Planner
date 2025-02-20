// AuthContext.tsx
import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { jwtDecode } from "jwt-decode";

// Define the shape of your context
interface AuthContextType {
  isAuthenticated: boolean;
  userPermissions: string[] | null;
  setToken: (token: string | null) => void;
}

// Create the context with default values
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Create a provider component
export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [userPermissions, setUserPermissions] = useState<string[] | null>(null);

  const setToken = (token: string | null) => {
    if (token) {
      localStorage.setItem("token", token);
      const decodedToken: { permissions: string[]; exp: number } =
        jwtDecode(token);
      setIsAuthenticated(true);
      setUserPermissions(decodedToken.permissions);
    } else {
      localStorage.removeItem("token");
      setIsAuthenticated(false);
      setUserPermissions(null);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      const decodedToken: { permissions: string[]; exp: number } =
        jwtDecode(token);
      const currentTime = Math.floor(Date.now() / 1000);
      if (decodedToken.exp > currentTime) {
        setIsAuthenticated(true);
        setUserPermissions(decodedToken.permissions);
      } else {
        setIsAuthenticated(false);
        setUserPermissions(null);
      }
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, userPermissions, setToken }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the AuthContext
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
