import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import * as apiService from "./apiService";
import './Dashboard.css';

const Dashboard = () => {

    // 1. State hook definitions
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [image, setImage] = useState(null);
    const [blogPosts, setBlogPosts] = useState([]);
    // const [reviewText, setReviewText] = useState("");
    const [reviewTexts, setReviewTexts] = useState({});

    const [reviews, setReviews] = useState([]);
    const [successMessage, setSuccessMessage] = useState("");
    const navigate = useNavigate();
    const location = useLocation();

    // 2. fetchBlogPosts function
    const fetchBlogPosts = async () => {
        try {
            const data = await apiService.getBlogPosts();
            setBlogPosts(data);
        } catch (error) {
            console.error("Failed to fetch blog posts:", error);
        }
    };

    // 3. useEffect hooks
    useEffect(() => {
        fetchBlogPosts();
    }, []);    

    useEffect(() => {
        if (!localStorage.getItem("token") && location.pathname === "/dashboard") {
            navigate("/login");
        }
    }, [location, navigate]);

    useEffect(() => {
        console.log(blogPosts);
    }, [blogPosts]);

    const handlePostCreate = async () => {
        const formData = new FormData();
        // console.log("Title:", title);
        // console.log("Content:", content);
        formData.append('title', title.toString());
        formData.append('content', content.toString());

        // formData.append('title', title);
        // formData.append('content', content);
        formData.append('image', image);
    
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
        }

        try {
            const response = await apiService.createBlogPost(formData);
            console.log("Newly created blog post:", response.blogPost);
            if (response.success) {
                // Blog post created successfully, update the state
                fetchBlogPosts();

                // setBlogPosts(prevPosts => [...prevPosts, response.blogPost]);
                setTitle("");
                setContent("");
                setImage(null);
                setSuccessMessage("Blog post created successfully!");
            } else {
                console.error('Failed to create the blog post');
            }
        } catch (error) {
            console.error('Error creating blog post:', error);
        }
    };

    const handleDeletePost = async (blogId) => {
        try {
            await apiService.deleteBlogPost(blogId);
            // Blog post deleted successfully, update the state
            setBlogPosts(prevPosts => prevPosts.filter(post => post.id !== blogId));
        } catch (error) {
            console.error("Failed to delete post:", error);
        }
    };

    const handleCreateReview = async (blogId, reviewText) => {
        try {
            const response = await apiService.createReview(blogId, reviewText);
            if (response.success) {
                // Review created successfully, update the state
                setReviews(prevReviews => [...prevReviews, response.review]);
                setReviewTexts(prev => ({ ...prev, [blogId]: '' }));
                
                // Fetch the blog posts again to update them with new reviews
                fetchBlogPosts();
            } else {
                console.error('Failed to create the review');
            }
        } catch (error) {
            console.error('Error creating review:', error);
        }
    };
    
    const handleLogout = async () => {
        try {
            const response = await apiService.logout();
            if (response.success) {
                navigate("/login");  // Redirect to home page
            } else {
                console.error('Failed to logout');
            }
        } catch (error) {
            console.error('Error during logout:', error);
        }
    };
     

    return (
        <div className="dashboard-container">
            <h1>Welcome to Your Blogging Hub 🌟!</h1>
            <p className="introduction">
                Dive into a world of stories, insights, and experiences. Read captivating blogs from others, share your 
                own tales, interact through comments, and manage your masterpieces—all from this dashboard.
            </p>
            
            {successMessage && <p className="success-message">{successMessage}</p>}
            <img src="Image1.jpeg" alt="Blogging Odyssey Begins!" className="dashboard-image" />
            <p>Create and Post your Blog!</p>
            
            <div className="post-form">
                <input type="text" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
                <textarea placeholder="Content" value={content} onChange={(e) => setContent(e.target.value)}></textarea>
                <input type="file" onChange={(e) => setImage(e.target.files[0])} />
                <button onClick={handlePostCreate}>Create Post</button>
            </div>
            <div className="blog-posts">
                
                
                
                <h2>Your Blog Posts</h2>
                {blogPosts.filter(Boolean).map(post => (

                // {blogPosts && blogPosts.map(post => (
                    <div key={post.id} className="post-item">
                        <h3>{post.title}</h3>
                        {/* Display other details of the blog post as needed */}
                        <img src={`/uploads/${post?.image_file}`} alt={post?.title} />
                        <p>{post?.content}</p>
                        <button onClick={() => handleDeletePost(post.id)}>Delete</button>
                        <div>
                            <textarea
                                placeholder="Leave a review..."
                                // value={reviewText}
                                value={reviewTexts[post.id] || ""}
                                onChange={(e) => setReviewTexts(prev => ({ ...prev, [post.id]: e.target.value }))}
                            />
                                {/* onChange={(e) => setReviewTexts(e.target.value)}
                            /> */}
                            <button onClick={() => handleCreateReview(post.id, reviewTexts[post.id] || "")}>Post Review</button>

                            {/* <button onClick={() => handleCreateReview(post.id)}>Post Review</button> */}
                        </div>
                        <div className="reviews">
                            {post.reviews && post.reviews.map(review => (
                            
                                <div key={review.id} className="review-item">
                                    <p>{review.text}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Dashboard;
