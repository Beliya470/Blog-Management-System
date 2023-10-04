const baseURL = "http://localhost:5000";

const encodeFormData = (data) => {
  return Object.keys(data)
    .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key]))
    .join('&');
}

// Blog API
export const getBlogPosts = async () => {
  try {
    const response = await fetch(`${baseURL}/blogposts`);
    return response.json();
  } catch (error) {
    console.error("Error fetching blogs", error);
    throw error;
  }
};

export const createBlogPost = async (title, content) => {
  try {
    const response = await fetch(`${baseURL}/blogposts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content })
    });
    return response.json();
  } catch (error) {
    console.error("Error creating blog", error);
    throw error;
  }
};

export const getBlogPost = async (blogId) => {
  try {
    const response = await fetch(`${baseURL}/blogposts/${blogId}`);
    return response.json();
  } catch (error) {
    console.error("Error fetching blog", error);
    throw error;
  }
};

export const modifyBlogPost = async (blogId, title, content) => {
  try {
    const response = await fetch(`${baseURL}/blogposts/${blogId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content })
    });
    return response.json();
  } catch (error) {
    console.error("Error updating blog", error);
    throw error;
  }
};

export const deleteBlogPost = async (blogId) => {
  try {
    const response = await fetch(`${baseURL}/blogposts/${blogId}`, {
      method: 'DELETE',
    });
    return response.json();
  } catch (error) {
    console.error("Error deleting blog", error);
    throw error;
  }
};

// Auth API
export const signUp = async (username, password) => {
  try {
    const response = await fetch(`${baseURL}/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: encodeFormData({ username, password })
    });
    return response.json();
  } catch (error) {
    console.error("Error during sign up", error);
    throw error;
  }
};

export const login = async (username, password) => {
  try {
    const response = await fetch(`${baseURL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    return response.json();
  } catch (error) {
    console.error("Error during login", error);
    throw error;
  }
};

export const logout = async () => {
  try {
      const response = await fetch(`${baseURL}/logout`, { method: 'POST' });

      // Check if the response was not okay
      if (!response.ok) {
          // Try to parse the response body to get the server's error message
          let errMsg = 'Invalid response from server.';
          try {
              const data = await response.json();
              errMsg = data.message || errMsg;
          } catch (e) {}

          throw new Error(errMsg);
      }

      try {
          return await response.json();
      } catch (e) {
          return { message: 'Logged out successfully!' };  // Default success message
      }
  } catch (error) {
      console.error("Error during logout", error);
      throw error;
  }
};



// Review API
export const createReview = async (blogId, title, content) => {
  try {
    const response = await fetch(`${baseURL}/blogposts/${blogId}/reviews`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content })
    });
    return response.json();
  } catch (error) {
    console.error("Error creating review", error);
    throw error;
  }
};

export const getReviews = async (blogId) => {
  try {
    const response = await fetch(`${baseURL}/blogposts/${blogId}/reviews`);
    return response.json();
  } catch (error) {
    console.error("Error fetching reviews", error);
    throw error;
  }
};
