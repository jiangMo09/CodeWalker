import { useRef, useState, useEffect } from "react";
import { postLogin } from "../../../services/api/User";

const LogIn = ({
  className,
  toggleLogInView,
  closeShowLogInView,
  setUsername
}) => {
  const emailRef = useRef();
  const passwordRef = useRef();
  const [responseMessage, setResponseMessage] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);

  const saveToken = (token) => {
    const now = new Date();
    const item = {
      value: token,
      expiry: now.getTime() + 30 * 60 * 1000
    };
    localStorage.setItem("authToken", JSON.stringify(item));
  };

  const onSubmit = async (e) => {
    e.preventDefault();

    const email = emailRef.current.value;
    const password = passwordRef.current.value;

    try {
      const response = await postLogin(email, password);

      if (response.success && response.token.access_token) {
        saveToken(response.token.access_token);
        setIsSuccess(true);
        setUsername(response.username);
        setResponseMessage(response.message);
        closeShowLogInView();
      } else {
        setIsSuccess(false);
        setResponseMessage(response.error || "Login failed");
      }
    } catch (error) {
      setIsSuccess(false);
      setResponseMessage("Login failed. Please try again.");
    }
  };

  useEffect(() => {
    let timer;
    if (responseMessage) {
      timer = setTimeout(() => {
        setResponseMessage("");
        setIsSuccess(false);
      }, 5000);
    }
    return () => clearTimeout(timer);
  }, [responseMessage]);

  return (
    <div className={className}>
      <div className="decorator"></div>
      <div className="login">
        <div className="title">Login Account</div>
        <form onSubmit={onSubmit}>
          <input
            type="email"
            id="email"
            placeholder="Enter email address"
            ref={emailRef}
            required
          />
          <br />
          <input
            type="password"
            id="password"
            placeholder="Enter password"
            ref={passwordRef}
            required
          />
          <br />
          <button type="submit" id="loginBtn">
            Login account
          </button>
        </form>
        <div className={`response-info ${isSuccess ? "success" : "error"}`}>
          {responseMessage}
        </div>
        <div className="signup" onClick={toggleLogInView}>
          Click here to register
        </div>
      </div>
    </div>
  );
};

export default LogIn;
