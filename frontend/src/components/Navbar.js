import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/" className="navbar-brand">
          Library Management System
        </Link>
        {isAuthenticated ? (
          <div className="navbar-links">
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/books">Books</Link>
            <Link to="/issue">Issue Book</Link>
            <Link to="/return">Return Book</Link>
            {user && (
              <span style={{ marginRight: '10px' }}>
                {user.user?.first_name || user.user?.username}
              </span>
            )}
            <button onClick={handleLogout}>Logout</button>
          </div>
        ) : (
          <div className="navbar-links">
            <Link to="/login">Login</Link>
            <Link to="/signup">Signup</Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
