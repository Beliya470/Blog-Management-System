import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function BlogPost() {
    const { id } = useParams();
    const [post, setPost] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchPost = async () => {
            try {
                const res = await axios.get(`/blogposts/${id}`);
                setPost(res.data);
            } catch (err) {
                setError(err.response.data.message);
            }
        };
        fetchPost();
    }, [id]);

    return post ? (
        <div>
            <h1>{post.title}</h1>
            <p>{post.content}</p>
        </div>
    ) : error ? <p>{error}</p> : <p>Loading...</p>;
}

export default BlogPost;
