// ProtectedRoute.tsx
import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "./Context/AuthContext";

interface ProtectedRouteProps {
  requiredPermissions?: string[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  requiredPermissions = [],
}) => {
  const { isAuthenticated, userPermissions } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect unauthenticated users to the login page
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredPermissions.length > 0 && userPermissions) {
    const hasRequiredPermissions = requiredPermissions.every((permission) =>
      userPermissions.includes(permission)
    );

    if (!hasRequiredPermissions) {
      // Redirect users without the required permissions
      return <Navigate to="/unauthorized" replace />;
    }
  }

  // Render the protected route's children
  return <Outlet />;
};

export default ProtectedRoute;
