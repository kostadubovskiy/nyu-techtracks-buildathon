// App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ProgressProvider } from "./context/ProgressContext";
import AuthPage from "./pages/AuthPage";
import RoadmapPage from "./pages/RoadmapPage";
import AISummaryPage from "./pages/AISummaryPage";

function App() {
  return (
    <ProgressProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AuthPage />} /> 
          <Route path="/roadmap" element={<RoadmapPage />} />
          <Route path="/summary" element={<AISummaryPage />} />
          {/* Redirect any unknown routes to login */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ProgressProvider>
  );
}

export default App;