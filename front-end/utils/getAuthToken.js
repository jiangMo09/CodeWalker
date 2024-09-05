export const getAuthToken = () => {
  const tokenJson = localStorage.getItem("authToken");
  if (!tokenJson) {
    return null;
  }

  const tokenInfo = JSON.parse(tokenJson);
  const now = new Date();

  if (now.getTime() > tokenInfo.expiry) {
    localStorage.removeItem("authToken");
    return null;
  }

  return tokenInfo.value;
};
