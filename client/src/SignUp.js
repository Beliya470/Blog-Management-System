import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signUp } from './apiService';

function SignUp() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState(''); // Add error message state
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await signUp(username, password);
      if (res.status === 201) {
        setSuccessMessage('User created successfully! Please proceed to login.');
        setTimeout(() => {
          navigate('/login');
        }, 5000); // Wait for 5 seconds before navigating
      } else {
        setErrorMessage(res.message || 'Error during sign up. Please try again.'); // Display server message or a generic error
      }
    } catch (error) {
      console.error("Error signing up:", error);
      setErrorMessage('Error during sign up. Please try again.'); // Display a generic error to the user
    }
  };

  return (
    <div>
      {successMessage && 
        <p style={{ color: 'green', border: '1px solid green', padding: '10px', borderRadius: '5px' }}>
          {successMessage}
        </p>
      }
      {errorMessage && 
        <p style={{ color: 'red', border: '1px solid red', padding: '10px', borderRadius: '5px' }}>
          {errorMessage}
        </p>
      }
      <form onSubmit={handleSubmit}>
        <label>
          Username: 
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label>
          Password: 
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default SignUp;
