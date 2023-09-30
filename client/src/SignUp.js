import React, { useState } from 'react';
import { Navigate } from 'react-router-dom'; // Using Navigate instead of useHistory
import { signUp } from './apiService'; // Correct import from apiService

function SignUp() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await signUp(username, password);
    if (res.status === 201) return <Navigate to='/login' />; // Using Navigate instead of history
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Username: <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} /></label>
      <label>Password: <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
      <button type="submit">Sign Up</button>
    </form>
  );
}

export default SignUp;
