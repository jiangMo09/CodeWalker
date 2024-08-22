import { useRef, useState, useEffect } from "react";
import { postRegister } from "../../../services/api/User";

const Register = ({ className, toggleLogInView }) => {
  const usernameRef = useRef();
  const emailRef = useRef();
  const passwordRef = useRef();
  const [responseMessage, setResponseMessage] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);

  const onRegisterClick = async (e) => {
    e.preventDefault();

    const username = usernameRef.current.value;
    const email = emailRef.current.value;
    const password = passwordRef.current.value;

    try {
      const response = await postRegister(username, email, password);

      if (response.message) {
        setIsSuccess(true);
        usernameRef.current.value = "";
        emailRef.current.value = "";
        passwordRef.current.value = "";
      } else {
        setIsSuccess(false);
      }

      setResponseMessage(response.message || response.error);
    } catch (error) {
      setIsSuccess(false);
      setResponseMessage("Registration failed. Please try again.");
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
      <div className="register">
        <div className="title">Register Account</div>
        <form onSubmit={onRegisterClick}>
          <input
            type="text"
            id="name"
            placeholder="Enter username"
            required
            ref={usernameRef}
          />
          <br />
          <input
            type="email"
            id="email"
            placeholder="Enter email"
            required
            ref={emailRef}
          />
          <br />
          <input
            type="password"
            id="password"
            placeholder="Enter password"
            required
            ref={passwordRef}
          />
          <br />
          <button type="submit" id="signupBtn">
            Register New Account
          </button>
        </form>
        <div className={`response-info ${isSuccess ? "success" : "error"}`}>
          {responseMessage}
        </div>
        <div className="signin" onClick={toggleLogInView}>
          Click here to login
        </div>
      </div>
    </div>
  );
};

export default Register;
