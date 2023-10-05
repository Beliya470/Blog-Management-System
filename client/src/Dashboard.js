import React, { useState, useEffect } from "react";
import * as apiService from "./apiService";
import './Dashboard.css'; // Importing the CSS file

const Dashboard = () => {
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [image, setImage] = useState(null);
    const [blogPosts, setBlogPosts] = useState([]);

    useEffect(() => {
        const fetchBlogPosts = async () => {
            const data = await apiService.getUserBlogPosts();
            if (Array.isArray(data)) {
                setBlogPosts(data);
            } else {
                console.error("Fetched blog posts data is not an array:", data);
            }
        };
        fetchBlogPosts();
    }, []);

    const handlePostCreate = async () => {
        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', content);
        formData.append('image', image);
        const response = await apiService.createBlogPost(formData);
        if (response.success) {
            setBlogPosts(prevPosts => [...prevPosts, response.blogPost]);
        } else {
            console.error('Failed to create the blog post');
        }
    };

    return (
        <div className="dashboard-container">
            <h1>Dashboard</h1>
            <img src="/path/to/image1.jpg" alt="Placeholder Image 1" className="dashboard-image"/> {/* Placeholder image */}
            <p>Welcome to your dashboard. Here you can manage your blog posts and view statistics.</p>
            <img src="/path/to/image2.jpg" alt="Placeholder Image 2" className="dashboard-image"/> {/* Placeholder image */}
            <div className="post-form">
                <input type="text" placeholder="Title" onChange={(e) => setTitle(e.target.value)} />
                <textarea placeholder="Content" onChange={(e) => setContent(e.target.value)}></textarea>
                <input type="file" onChange={(e) => setImage(e.target.files[0])} />
                <button onClick={handlePostCreate}>Create Post</button>
            </div>
            <div className="blog-posts">
                <h2>Your Blog Posts</h2>
                {Array.isArray(blogPosts) && blogPosts.map(post => (
                    <div key={post.id} className="post-item">
                        <h3>{post.title}</h3>
                        <img src={`/uploads/${post.image_file}`} alt={post.title} />
                        <p>{post.content}</p>
                        {/* Add edit, delete buttons, and review sections here */}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Dashboard;
