import React from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/AiSummary.module.css";
import tedOpen from "../images/ted_open.png";
import dollarSign from "../images/dollarSign.png";

const AiSummary = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.container}>
      <div className={styles.titleContainer}>
        <img src={dollarSign} alt="Dollar Sign" className={styles.dollarSign} />
        <h1 className={styles.title}>Financial Concept</h1>
      </div>
      <button className={styles.summaryBtn}>AI SUMMARY</button>
      
      {/* Speech Bubble Container */}
      <div className={styles.speechBubble}>
        <p>Generated AI content goes here...</p>
      </div>

      <img src={tedOpen} alt="Ted Open" className={styles.tedIcon} />

      <button onClick={() => navigate("/roadmap")}>Back to Roadmap</button>
    </div>
  );
};

export default AiSummary;