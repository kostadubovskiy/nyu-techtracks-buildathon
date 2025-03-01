import React from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/Login.module.css";
import tedClosed from "../images/ted_closed.png";
import titleImg from "../images/title.png"; // Import title image

const Login = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.container}>
      <img src={titleImg} alt="Title" className={styles.titleImage} /> {/* Use Image Instead */}
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