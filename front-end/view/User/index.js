import styled from "styled-components";
import { useState, useEffect } from "react";

import { getVerifyToken } from "../../services/api/User";

import LogIn from "./LogIn";
import Register from "./Register";
import style from "./style";

const User = ({ className }) => {
  const [loginStatus, setLoginStatus] = useState("Login / Register");
  const [isLogInView, setIsLogInView] = useState(true);
  const [isShowLogInView, setIsShowLogInView] = useState(false);

  const toggleLogInView = () => {
    setIsLogInView(!isLogInView);
  };

  const toggleShowLogInView = () => {
    if (loginStatus != "Login / Register") {
      const confirmLogout = window.confirm("Are you sure you want to log out?");

      if (!confirmLogout) {
        return;
      }

      localStorage.removeItem("authToken");
      setLoginStatus("Login / Register");
      alert("You have successfully logged out!");
      return;
    }

    setIsShowLogInView(!isShowLogInView);
  };

  const closeShowLogInView = () => {
    setIsShowLogInView(false);
  };

  const setUsername = (name) => {
    setLoginStatus("user : " + name);
  };

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const data = await getVerifyToken();

        setUsername(data.username);
      } catch (error) {
        console.error("Auth check failed:", error);
        localStorage.removeItem("authToken");
      }
    };

    checkAuth();
  }, []);

  return (
    <div className={className}>
      <div onClick={toggleShowLogInView}>{loginStatus}</div>
      {isShowLogInView && (
        <div className="modal-background" onClick={closeShowLogInView}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            {isLogInView ? (
              <LogIn
                toggleLogInView={toggleLogInView}
                closeShowLogInView={closeShowLogInView}
                setUsername={setUsername}
              />
            ) : (
              <Register toggleLogInView={toggleLogInView} />
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default styled(User)`
  ${style}
`;
