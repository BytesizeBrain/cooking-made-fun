import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../utils/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

function ProtectedRoute({ children }: ProtectedRouteProps) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

export default ProtectedRoute;
