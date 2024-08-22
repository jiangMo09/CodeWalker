import { fetchData } from "../../utils/fetchData";

export const postLogin = (email, password) =>
  fetchData(`/login`, {
    method: "POST",
    body: JSON.stringify({
      email,
      password
    })
  });

export const postRegister = (username, email, password) =>
  fetchData(`/register`, {
    method: "POST",
    body: JSON.stringify({
      username,
      email,
      password
    })
  });

export const getVerifyToken = () => {
  const tokenJson = localStorage.getItem("authToken");
  if (!tokenJson) {
    return Promise.reject("No token found");
  }

  const tokenInfo = JSON.parse(tokenJson);
  const now = new Date();

  if (now.getTime() > tokenInfo.expiry) {
    localStorage.removeItem("authToken");
    return Promise.reject("Token expired");
  }

  return fetchData(`/verify_token`, {
    headers: {
      authToken: tokenInfo.value
    }
  });
};
