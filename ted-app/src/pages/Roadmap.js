import React from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/Roadmap.module.css";
import tedClosed from "../images/ted_closed.png";
import titleImg from "../images/title.png"; // Import title image

const Roadmap = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.container}>
      <img src={titleImg} alt="Title" className={styles.titleImage} /> {/* Use Image Instead */}
      <p className={styles.startText}>Start Here!</p>
      <div className={styles.tree}>
        <div className={styles.node}>Concept</div>
        <div className={styles.node}>Concept</div>
        <div className={styles.node}>Concept</div>
      </div>
      <img src={tedClosed} alt="Ted Closed" className={styles.tedIcon} />
      <button onClick={() => navigate("/")}>Back to Login</button>
      <button onClick={() => navigate("/ai-summary")}>Go to AI Summary</button>
    </div>
  );
};

export default Roadmap;