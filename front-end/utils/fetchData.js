const API_BASE_URL = "http://127.0.0.1:8000";

export const fetchData = async (endpoint, options = {}) => {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      method: options.method || "GET",
      headers: {
        "Content-Type": "application/json",
        ...options.headers
      },
      ...options
    });

    const data = await response.json();
    return data.data;
  } catch (err) {
    console.error(`Error fetching ${endpoint}:`, err);
    throw new Error("An error occurred while fetching data");
  }
};
