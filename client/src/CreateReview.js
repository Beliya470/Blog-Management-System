import React, { useState } from 'react';
import { createReview } from './apiService';

const CreateReview = ({ blogPostId }) => {
  const [content, setContent] = useState('');
  const [error, setError] = useState('');

  const handleCreateReview = async () => {
    try {
      await createReview(blogPostId, content);
      // Handle successful review creation (e.g., clear the form or redirect)
    } catch (err) {
      setError('Invalid Input!');
    }
  };

  return (
    <div>
      <textarea placeholder="Content" onChange={(e) => setContent(e.target.value)} />
      <button onClick={handleCreateReview}>Create Review</button>
      {error && <p>{error}</p>}
    </div>
  );
};

export default CreateReview;
