import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as apiService from "./apiService";

const LogIn = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await apiService.login(username, password);
      if (response && response.message === "Logged in successfully!") {
        localStorage.setItem("token", response.token);
        navigate("/dashboard");  // Redirect to dashboard if logged in
      } else {
        alert("Login failed. Please check your credentials.");
      }
    } catch (error) {
      console.error("Error during login", error);
      alert("An error occurred during login. Please try again.");
    }
  };

  return (
    <div>
      <input 
        type="text" 
        placeholder="Username" 
        onChange={(e) => setUsername(e.target.value)} 
      />
      <input 
        type="password" 
        placeholder="Password" 
        onChange={(e) => setPassword(e.target.value)} 
      />
      <button onClick={handleLogin}>Log In</button>
    </div>
  );
};

export default LogIn;
