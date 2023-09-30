import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Navbar from './Navbar';
import SignUp from './SignUp';
import LogIn from './LogIn';
import LogOut from './LogOut';
import BlogList from './BlogList';
import BlogPost from './BlogPost';
import CreateBlog from './CreateBlog';
import EditBlog from './EditBlog';
import CreateReview from './CreateReview';
import './App.css';

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
          <Route path="/blogposts/:id" element={<BlogPost />} />
          <Route path="/" element={<BlogList />} />
        </Routes>
    </div>
  );
}

export default App;
