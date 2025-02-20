import React, { useEffect, useState } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const RequireAuth: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [userPermission, setUserPermission] = useState<number | null>(null);
  const location = useLocation();

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem("token");

      if (!token) {
        setIsAuthenticated(false);
        return;
      }

      try {
        // Decode the token to extract user information
        const decodedToken: {
          user_id: string;
          permissionLevel: number;
          exp: number;
        } = jwtDecode(token);

        // Check if the token has expired
        const currentTime = Math.floor(Date.now() / 1000);
        if (decodedToken.exp < currentTime) {
          console.warn("Token has expired.");
          setIsAuthenticated(false);
          return;
        }

        // Set authentication state and user permission
        setIsAuthenticated(true);
        setUserPermission(decodedToken.permissionLevel);
      } catch (error) {
        console.error("Failed to decode token:", error);
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  if (isAuthenticated === null) {
    return <div>Loading...</div>; // Prevents flashing an unauthorized page while checking
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
};

export default RequireAuth;
