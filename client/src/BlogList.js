import React, { useEffect, useState } from 'react';
import { getBlogPosts } from './apiService';

const BlogList = () => {
  const [blogPosts, setBlogPosts] = useState([]);

  useEffect(() => {
    const fetchBlogPosts = async () => {
      try {
        const posts = await getBlogPosts();
        console.log(posts); // log the posts to debug the API response
        if(Array.isArray(posts)) { // check if posts is an array
          setBlogPosts(posts);
        } else {
          console.error('API response is not an array:', posts);
        }
      } catch (err) {
        console.error('Error fetching blog posts:', err);
      }
    };

    fetchBlogPosts();
  }, []);

  return (
    <div>
      {Array.isArray(blogPosts) && blogPosts.map((post) => (
        <div className="blogPost" key={post.id}>
          <h3>{post.title}</h3>
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
};

export default BlogList;
