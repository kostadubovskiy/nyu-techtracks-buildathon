import React from "react";
import { useNavigate } from "react-router-dom"; // Import navigation hook
import styles from "../styles/Login.module.css";
import tedClosed from "../Images/ted_closed.png";

const Login = () => {
  const navigate = useNavigate(); // Initialize navigation function

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>
        <span>ROADMAP</span> <br /> TO <br /> <span>Riches</span>
      </h1>
      {/* Change buttons to navigate to other pages */}
      <button className={styles.loginBtn} onClick={() => navigate("/roadmap")}>
        Login
      </button>
      <button className={styles.signupBtn} onClick={() => navigate("/roadmap")}>
        Sign Up
      </button>
      <img src={tedClosed} alt="Ted Closed" className={styles.tedIcon} />
    </div>
  );
};

export default Login;