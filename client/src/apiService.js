const baseURL = "http://localhost:5000/routes";

const defaultHeaders = () => ({
  'Authorization': `Bearer ${localStorage.getItem('token')}`
});

const encodeFormData = (data) => {
  return Object.keys(data)
    .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key]))
    .join('&');
}

// Blog API
export const getBlogPosts = async () => {
  try {
    const response = await fetch(`${baseURL}/routes/blogposts`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("Error fetching blog posts:", error);
    throw error;
  }
};

export const getBlogPost = async (blogId) => {
  try {
    const response = await fetch(`${baseURL}/routes/blogposts/${blogId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("Error fetching blog post:", error);
    throw error;
  }
};

export const modifyBlogPost = async (blogId, title, content) => {
  try {
    const response = await fetch(`${baseURL}/routes/blogposts/${blogId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', ...defaultHeaders() },
      body: JSON.stringify({ title, content })
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("Error modifying blog post:", error);
    throw error;
  }
};

export const deleteBlogPost = async (blogId) => {
  try {
    const response = await fetch(`${baseURL}/routes/blogposts/${blogId}`, {
      method: 'DELETE',
      headers: defaultHeaders()
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("Error deleting blog post:", error);
    throw error;
  }
};

// Auth API
export const signUp = async (username, password) => {
  try {
    const response = await fetch(`${baseURL}/routes/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: encodeFormData({ username, password })
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("Error signing up:", error);
    throw error;
  }
};

export const login = async (username, password) => {
  try {
    const response = await fetch(`${baseURL}/routes/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
};

export const logout = async () => {
  try {
    const response = await fetch(`${baseURL}/routes/logout`, { 
      method: 'POST', 
      headers: defaultHeaders() 
    });
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || 'Invalid response from server.');
    }
    return response.json();
  } catch (error) {
    console.error("Error logging out:", error);
    throw error;
  }
};

export const createBlogPost = async (formData) => {
  try {
    const response = await fetch(`${baseURL}/routes/blogposts`, {
      method: 'POST',
      body: formData,
      headers: {
        ...defaultHeaders(),
        // Do not explicitly set 'Content-Type' here; 
        // let the browser set it with the proper boundary for FormData
      }
      
    });
    if (!response.ok) {
      throw new Error(`Failed to create blog post (HTTP ${response.status})`);
    }
    return response.json();
  } catch (error) {
    console.error("Error creating blog post:", error);
    throw error;
  }
};




export const getUserBlogPosts = async () => {
  try {
    const response = await fetch(`${baseURL}/routes/blogposts`, {
      headers: defaultHeaders()
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("Error fetching user blog posts:", error);
    throw error;
  }
};

// Review API
export const createReview = async (blogId, reviewText) => {
  try {
    const response = await fetch(`${baseURL}/blogposts/${blogId}/reviews`, {
      method: 'POST',
      headers: {
        ...defaultHeaders(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: reviewText })  // assuming your backend expects the key to be "text"
    });
    if (!response.ok) {
      throw new Error(`Failed to create review (HTTP ${response.status})`);
    }
    return response.json();
  } catch (error) {
    console.error("Error creating review:", error);
    throw error;
  }
};


export const getReviews = async (blogId) => {
  try {
    const response = await fetch(`${baseURL}/blogposts/${blogId}/reviews`, {
      headers: defaultHeaders()
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("Error fetching reviews:", error);
    throw error;
  }
};
