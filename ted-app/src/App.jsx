import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Roadmap from "./pages/Roadmap";
import AiSummary from "./pages/AiSummary";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/roadmap" element={<Roadmap />} />
        <Route path="/ai-summary" element={<AiSummary />} />
      </Routes>
    </Router>
  );
}

export default App;