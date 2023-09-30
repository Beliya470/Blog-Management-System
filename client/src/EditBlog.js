import React, { useState, useEffect } from 'react';
import { getBlogPost, modifyBlogPost } from './apiService';

const EditBlog = ({ blogPostId }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBlogPost = async () => {
      try {
        const response = await getBlogPost(blogPostId);
        setTitle(response.data.title);
        setContent(response.data.content);
      } catch (err) {
        // Handle error during fetching blog post
      }
    };

    fetchBlogPost();
  }, [blogPostId]);

  const handleModifyBlogPost = async () => {
    try {
      await modifyBlogPost(blogPostId, title, content);
      // Handle successful blog post modification (e.g., redirect to blog list)
    } catch (err) {
      setError('Invalid Input!');
    }
  };

  return (
    <div>
      <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
      <textarea value={content} onChange={(e) => setContent(e.target.value)} />
      <button onClick={handleModifyBlogPost}>Modify Blog Post</button>
      {error && <p>{error}</p>}
    </div>
  );
};

export default EditBlog;
