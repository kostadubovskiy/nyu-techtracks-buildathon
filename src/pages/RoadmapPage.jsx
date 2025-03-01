// pages/RoadmapPage.jsx
import React, { useContext } from "react";
import { ProgressContext } from "../context/ProgressContext";
import NodeComponent from "../components/NodeComponent";

function RoadmapPage() {
  const { completedNodes } = useContext(ProgressContext);

  // Example roadmap data: an array of concept nodes
  const concepts = [
    { id: 1, title: "Intro to Finance" },
    { id: 2, title: "Budgeting Basics" },
    { id: 3, title: "Investing 101" }
    // ... add more concepts or nested structure as needed
  ];

  return (
    <div className="p-4 md:p-8">
      <h2 className="text-xl md:text-2xl font-bold mb-6">Your Finance Learning Roadmap</h2>
      <div className="space-y-4">
        {concepts.map(concept => (
          <NodeComponent 
            key={concept.id} 
            id={concept.id} 
            title={concept.title} 
            completed={completedNodes.includes(concept.id)} 
          />
        ))}
      </div>
    </div>
  );
}

export default RoadmapPage;