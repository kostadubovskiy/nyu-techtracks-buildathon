// context/ProgressContext.jsx
import { createContext, useState } from "react";

export const ProgressContext = createContext();

export function ProgressProvider({ children }) {
  const [completedNodes, setCompletedNodes] = useState([]);    // IDs of completed concepts
  const [currentConcept, setCurrentConcept] = useState(null);  // currently selected concept for summary

  // Mark a concept as completed and set it as current
  const completeConcept = (id) => {
    setCompletedNodes(prev => prev.includes(id) ? prev : [...prev, id]);
    setCurrentConcept(id);
  };

  return (
    <ProgressContext.Provider value={{ completedNodes, currentConcept, completeConcept }}>
      {children}
    </ProgressContext.Provider>
  );
}