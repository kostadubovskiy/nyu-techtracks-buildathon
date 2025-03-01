// components/NodeComponent.jsx
import React, { useContext } from "react";
import { ProgressContext } from "../context/ProgressContext";
import { useNavigate } from "react-router-dom";

function NodeComponent({ id, title, completed }) {
  const { completeConcept } = useContext(ProgressContext);
  const navigate = useNavigate();

  const handleClick = () => {
    completeConcept(id);     // update global progress state
    navigate("/summary");    // go to summary page for this concept
  };

  return (
    <div 
      className={`p-4 border rounded-lg flex items-center justify-between 
                  cursor-pointer transition ${completed ? "bg-green-100" : "bg-white"}`}
      onClick={handleClick}
    >
      <span className={`font-medium ${completed ? "text-gray-500 line-through" : "text-gray-800"}`}>
        {title}
      </span>
      {completed ? (
        <svg className="w-6 h-6 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" clipRule="evenodd" 
            d="M16.707 5.293a1 1 0 00-1.414 0L8 12.586 4.707 9.293a1 1 0 10-1.414 1.414l4 4a1 1 0 001.414 
            0l8-8a1 1 0 000-1.414z" 
            />
        </svg>
        ) : (
        <span className="text-blue-500">▶</span>
        )}
    </div>
  );
}

export default NodeComponent;