import React from "react";
import { useNavigate } from "react-router-dom"; // Import navigation hook
import styles from "../styles/Roadmap.module.css";
import tedClosed from "../Images/ted_closed.png";

const Roadmap = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>ROADMAP TO Riches</h1>
      <p className={styles.startText}>Start Here!</p>
      <div className={styles.tree}>
        <div className={styles.node}>Concept</div>
        <div className={styles.node}>Concept</div>
        <div className={styles.node}>Concept</div>
      </div>
      <img src={tedClosed} alt="Ted Closed" className={styles.tedIcon} />
      
      {/* Add buttons to navigate between pages */}
      <button onClick={() => navigate("/")}>Back to Login</button>
      <button onClick={() => navigate("/ai-summary")}>Go to AI Summary</button>
    </div>
  );
};

export default Roadmap;