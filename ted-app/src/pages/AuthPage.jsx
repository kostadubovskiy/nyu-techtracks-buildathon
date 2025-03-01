// pages/AuthPage.jsx
import React from "react";
import { useNavigate } from "react-router-dom";

function AuthPage() {
  const navigate = useNavigate();
  const handleLogin = (e) => {
    e.preventDefault();
    // In a real app, authenticate user here
    navigate("/roadmap");  // navigate to the roadmap after login
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-sm bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">Welcome Back</h1>
        <form onSubmit={handleLogin} className="space-y-4">
          <input 
            type="email" 
            placeholder="Email" 
            className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
            required 
          />
          <input 
            type="password" 
            placeholder="Password" 
            className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
            required 
          />
          <button 
            type="submit" 
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          >
            Login
          </button>
        </form>
        <p className="mt-4 text-sm text-center">
          New here? <span className="text-blue-600 cursor-pointer" onClick={() => {/* handle sign up */}}>Create an account</span>
        </p>
      </div>
    </div>
  );
}

export default AuthPage;