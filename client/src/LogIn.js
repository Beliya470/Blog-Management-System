import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Replaced useHistory with useNavigate
import * as apiService from "./apiService";

const LogIn = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // Using useNavigate instead of useHistory
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await apiService.login(username, password);
      
      if (response && response.message === "Logged in successfully!") {
        // Storing the token in local storage
        localStorage.setItem("token", response.token);

        // Redirecting to the dashboard using navigate
        navigate("/dashboard");
      } else {
        // Notifying users of unsuccessful login attempts
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
