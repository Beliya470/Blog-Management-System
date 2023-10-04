import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { logout } from './apiService';

const LogOut = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        await logout();
        navigate('/login');
      } catch (err) {
        console.error("Error during logout", err);
        // Handle error during logout, maybe show a message to the user.
      }
    };
    handleLogout();
  }, [navigate]);

  return null;  // This component does not render anything visible to the user
};

export default LogOut;
