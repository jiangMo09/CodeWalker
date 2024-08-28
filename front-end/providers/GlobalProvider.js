import { createContext, useEffect, useState, useContext } from "react";
import { getVerifyToken } from "../services/api/User";

export const GlobalContext = createContext({});

const GlobalProvider = ({ children }) => {
  const [username, setUsername] = useState("Login / Register");
  const [isLogin, setIsLogin] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const data = await getVerifyToken();
        console.log(data);
        setUsername("user : " + data.username);
        setIsLogin(true);
      } catch (error) {
        console.error("Auth check failed:", error);
        localStorage.removeItem("authToken");
        setUsername("Login / Register");
        setIsLogin(false);
      }
    };

    checkAuth();
  }, []);

  const logout = () => {
    localStorage.removeItem("authToken");
    setUsername("Login / Register");
    setIsLogin(false);
  };

  return (
    <GlobalContext.Provider
      value={{ username, isLogin, logout, setUsername, setIsLogin }}
    >
      {children}
    </GlobalContext.Provider>
  );
};

export const useGlobalContext = () => {
  const context = useContext(GlobalContext);
  if (context === undefined) {
    throw new Error("useGlobalContext must be used within a GlobalProvider");
  }
  return context;
};

export default GlobalProvider;
