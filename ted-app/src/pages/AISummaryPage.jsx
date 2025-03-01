// pages/AISummaryPage.jsx
import React, { useContext } from "react";
import { ProgressContext } from "../context/ProgressContext";

function AISummaryPage() {
  const { currentConcept, completedNodes } = useContext(ProgressContext);

  // For demo, define some static summaries for each concept ID:
  const summaries = {
    1: "Finance Introduction: This covers the basics of financial literacy and why it matters.",
    2: "Budgeting Basics: Learn how to create and manage a personal budget, track expenses, and save money.",
    3: "Investing 101: An overview of investment vehicles, risk vs reward, and starting an investment portfolio."
  };

  // If no currentConcept (e.g., direct access), we could redirect or show a message.
  if (!currentConcept) {
    return <p className="p-4">Please select a concept from the roadmap to see its summary.</p>;
  }

  return (
    <div className="p-4 md:p-8">
      <h2 className="text-xl md:text-2xl font-bold mb-4">AI Summary</h2>
      <div className="bg-white shadow rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-2">{summaries[currentConcept] ? `${summaries[currentConcept].split(':')[0]}:` : "Concept Summary"}</h3>
        <p className="text-gray-700">
          {summaries[currentConcept] || "No summary available for this concept."}
        </p>
      </div>
      <button 
        onClick={() => window.history.back()} 
        className="mt-4 inline-block text-blue-600 hover:underline"
      >
        ← Back to Roadmap
      </button>
    </div>
  );
}

export default AISummaryPage;