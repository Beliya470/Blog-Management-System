import React, { useState } from 'react';
import { createBlogPost } from './apiService';

const CreateBlog = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState('');

  const handleCreateBlogPost = async () => {
    try {
      await createBlogPost(title, content);
      // Handle successful blog post creation (e.g., redirect to blog list)
    } catch (err) {
      setError('Invalid Input!');
    }
  };

  return (
    <div>
      <input type="text" placeholder="Title" onChange={(e) => setTitle(e.target.value)} />
      <textarea placeholder="Content" onChange={(e) => setContent(e.target.value)} />
      <button onClick={handleCreateBlogPost}>Create Blog Post</button>
      {error && <p>{error}</p>}
    </div>
  );
};

export default CreateBlog;
