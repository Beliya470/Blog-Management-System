import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import Navbar from './Navbar';
import SignUp from './SignUp';
import LogIn from './LogIn';
import LogOut from './LogOut';
import BlogList from './BlogList';
import BlogPost from './BlogPost';
import CreateBlog from './CreateBlog';
import EditBlog from './EditBlog';
import CreateReview from './CreateReview';
import Dashboard from './Dashboard';
import './App.css';

// ProtectedRoute Component
function ProtectedRoute({ children, ...rest }) {
  const isAuthenticated = true; // Placeholder. You'd typically check if the user is logged in here.

  return (
    <Route {...rest} element={
      isAuthenticated ? children : <Navigate to="/login" replace state={{ from: rest.path }} />
    } />
  );
}

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/logout" element={<LogOut />} />
        <Route path="/blogposts/new" element={<CreateBlog />} />
        <Route path="/blogposts/:id/edit" element={<EditBlog />} />
        <Route path="/blogposts/:id/reviews/new" element={<CreateReview />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<div>Welcome to the Blog Management System. Please log in to see blog posts.</div>} />
      </Routes>
    </div>
  );
}

export default App;
