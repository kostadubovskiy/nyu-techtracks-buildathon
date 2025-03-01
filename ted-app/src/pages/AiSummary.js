import React from "react";
import { useNavigate } from "react-router-dom"; // Import navigation hook
import styles from "../styles/AiSummary.module.css";
import tedOpen from "../Images/ted_open.png";
import dollarSign from "../Images/dollarSign.png";

const AiSummary = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.container}>
      <div className={styles.titleContainer}>
        <img src={dollarSign} alt="Dollar Sign" className={styles.dollarSign} />
        <h1 className={styles.title}>Financial Concept</h1>
      </div>
      <button className={styles.summaryBtn}>AI SUMMARY</button>
      <div className={styles.summaryBox}>
        <p>Generated AI content goes here...</p>
      </div>
      <img src={tedOpen} alt="Ted Open" className={styles.tedIcon} />

      {/* Add navigation buttons */}
      <button onClick={() => navigate("/roadmap")}>Back to Roadmap</button>
    </div>
  );
};

export default AiSummary;