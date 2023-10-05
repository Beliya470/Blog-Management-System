// // // App.js

// // import React from 'react';
// // import { Route, Routes } from 'react-router-dom';
// // import Navbar from './Navbar';
// // import SignUp from './SignUp';
// // import LogIn from './LogIn';
// // import LogOut from './LogOut';
// // import BlogList from './BlogList';
// // import BlogPost from './BlogPost';
// // import CreateBlog from './CreateBlog';
// // import EditBlog from './EditBlog';
// // import CreateReview from './CreateReview';
// // import Dashboard from './Dashboard';
// // import Home from './Home';
// // import ProtectedWrapper from './ProtectedWrapper'; // <- Import this
// // import './App.css';

// // function App() {
// //   return (
// //     <div className="App">
// //       <Navbar />
// //       <Routes>
// //         <Route path="/dashboard" element={<Dashboard />} /> 
// //         <Route path="/signup" element={<SignUp />} />
// //         <Route path="/login" element={<LogIn />} />
// //         <Route path="/logout" element={<LogOut />} />
// //         <Route path="/blogposts/new" element={<CreateBlog />} />
// //         <Route path="/blogposts/:id/edit" element={<EditBlog />} />
// //         <Route path="/blogposts/:id/reviews/new" element={<CreateReview />} />
        
        
        
// //         {/* <Route path="/dashboard" element={<ProtectedWrapper><Dashboard /></ProtectedWrapper>} /> */}
// //         <Route path="*" element={<Home />} />
        
// //       </Routes>
// //     </div>
// //   );
// // }

// // export default App;



// import React from 'react';
// import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
// import Navbar from './Navbar';
// import SignUp from './SignUp';
// import LogIn from './LogIn';
// import LogOut from './LogOut';
// import BlogList from './BlogList';
// import BlogPost from './BlogPost';
// import CreateBlog from './CreateBlog';
// import EditBlog from './EditBlog';
// import CreateReview from './CreateReview';
// import Dashboard from './Dashboard';
// import Home from './Home';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <Navbar />
//       <Routes>
//         <Route path="/dashboard" element={<Dashboard />} /> 
//         <Route path="/signup" element={<SignUp />} />
//         <Route path="/login" element={<LogIn />} />
//         <Route path="/logout" element={<LogOut />} />
//         <Route path="/blogposts/new" element={<CreateBlog />} />
//         <Route path="/blogposts/:id/edit" element={<EditBlog />} />
//         <Route path="/blogposts/:id/reviews/new" element={<CreateReview />} />
        
//         {/* If you don't want the Home page to appear for unmatched routes, you can remove this */}
//         {/* <Route path="*" element={<Home />} /> */}
//       </Routes>
//     </div>
//   );
// }

// export default App;
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './Navbar';
import SignUp from './SignUp';
import LogIn from './LogIn';
import Dashboard from './Dashboard';
// import Home from './Home';
import HomePage from './HomePage';
import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<HomePage />} />
        {/* Other routes here */}
      </Routes>
    </div>
  );
}


export default App;
