import React from 'react';
import { logout } from './apiService';

const LogOut = () => {
  const handleLogout = async () => {
    try {
      await logout();
      // Handle logout, redirect to login or home page
    } catch (err) {
      // Handle error during logout
    }
  };

  return <button onClick={handleLogout}>Log Out</button>;
};

export default LogOut;
