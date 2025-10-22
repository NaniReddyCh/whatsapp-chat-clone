import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Placeholder components - to be implemented
function Login() {
  return <div>Login Page - Coming Soon</div>;
}

function Register() {
  return <div>Register Page - Coming Soon</div>;
}

function Chat() {
  return <div>Chat Interface - Coming Soon</div>;
}

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
