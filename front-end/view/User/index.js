import styled from "styled-components";
import { useState } from "react";
import { useGlobalContext } from "../../providers/GlobalProvider";

import LogIn from "./LogIn";
import Register from "./Register";
import style from "./style";

const User = ({ className }) => {
  const { username, isLogin, logout } = useGlobalContext();
  const [isLogInView, setIsLogInView] = useState(true);
  const [isShowLogInView, setIsShowLogInView] = useState(false);

  const toggleLogInView = () => {
    setIsLogInView(!isLogInView);
  };

  const toggleShowLogInView = () => {
    if (isLogin) {
      const confirmLogout = window.confirm("Are you sure you want to log out?");
      if (confirmLogout) {
        logout();
        alert("You have successfully logged out!");
      }
    } else {
      setIsShowLogInView(!isShowLogInView);
    }
  };

  const closeShowLogInView = () => {
    setIsShowLogInView(false);
  };

  return (
    <div className={className}>
      <div onClick={toggleShowLogInView}>{username}</div>
      {isShowLogInView && !isLogin && (
        <div className="modal-background" onClick={closeShowLogInView}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            {isLogInView ? (
              <LogIn
                toggleLogInView={toggleLogInView}
                closeShowLogInView={closeShowLogInView}
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
