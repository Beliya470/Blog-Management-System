import React, { useState } from "react";
import * as apiService from "./apiService"; // Correct import of all named exports from apiService

const LogIn = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await apiService.login(username, password);
      // Handle successful login
    } catch (error) {
      // Handle error during login
    }
  };

  return (
    <div>
      <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Log In</button>
    </div>
  );
};

export default LogIn;
