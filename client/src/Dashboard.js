import React, { useState, useEffect } from 'react';
import * as apiService from './apiService';

function Dashboard() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // Fetch the user's posts (or whatever data you want to display in the dashboard)
    async function fetchData() {
      try {
        const data = await apiService.getBlogPosts(); // Assuming this fetches the user's posts
        setPosts(data);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    }

    fetchData();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <ul>
        {posts.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
