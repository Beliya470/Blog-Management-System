import axios from 'axios';

// Blog API
export const getBlogPosts = async () => {
  try {
    const response = await axios.get('/api/blogs');
    return response.data;
  } catch (error) {
    console.error("Error fetching blogs", error);
    return error.response;
  }
};

export const createBlogPost = async (title, content) => {
  try {
    const response = await axios.post('/api/blogs', { title, content });
    return response.data;
  } catch (error) {
    console.error("Error creating blog", error);
    return error.response;
  }
};

export const getBlogPost = async (blogId) => {
  try {
    const response = await axios.get(`/api/blogs/${blogId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching blog", error);
    return error.response;
  }
};

export const modifyBlogPost = async (blogId, title, content) => {
  try {
    const response = await axios.put(`/api/blogs/${blogId}`, { title, content });
    return response.data;
  } catch (error) {
    console.error("Error updating blog", error);
    return error.response;
  }
};

// Auth API
export const signUp = async (username, password) => {
  try {
    const response = await axios.post('/api/signup', { username, password });
    return response.data;
  } catch (error) {
    console.error("Error during sign up", error);
    return error.response;
  }
};

export const login = async (username, password) => {
  try {
    const response = await axios.post('/api/login', { username, password });
    return response.data;
  } catch (error) {
    console.error("Error during login", error);
    return error.response;
  }
};

export const logout = async () => {
  try {
    const response = await axios.post('/api/logout');
    return response.data;
  } catch (error) {
    console.error("Error during logout", error);
    return error.response;
  }
};

// Review API
export const fetchAllReviews = async (blogId) => {
  try {
    const response = await axios.get(`/api/blogs/${blogId}/reviews`);
    return response.data;
  } catch (error) {
    console.error("Error fetching reviews", error);
    return error.response;
  }
};

export const createReview = async (blogId, content) => {
  try {
    const response = await axios.post(`/api/blogs/${blogId}/reviews`, { content });
    return response.data;
  } catch (error) {
    console.error("Error creating review", error);
    return error.response;
  }
};

export const updateReview = async (reviewId, content) => {
  try {
    const response = await axios.put(`/api/reviews/${reviewId}`, { content });
    return response.data;
  } catch (error) {
    console.error("Error updating review", error);
    return error.response;
  }
};

export const deleteReview = async (reviewId) => {
  try {
    const response = await axios.delete(`/api/reviews/${reviewId}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting review", error);
    return error.response;
  }
};
