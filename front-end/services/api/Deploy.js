import { fetchData } from "../../utils/fetchData";
import { getAuthToken } from "../../utils/getAuthToken";

export const postPureJs = ({ repoUrl, deploymentType, storageTypes }) => {
  const authToken = getAuthToken();

  if (!authToken) {
    return Promise.reject("No valid auth token found");
  }

  return fetchData(`/deploy/pure_js`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      authToken: authToken
    },
    body: JSON.stringify({
      url: repoUrl,
      deploymentType: deploymentType,
      storageTypes: storageTypes
    })
  });
};

export const postFastApi = ({
  repoUrl,
  deploymentType,
  storageTypes,
  rootDir,
  buildCommand,
  envVars
}) => {
  const authToken = getAuthToken();

  if (!authToken) {
    return Promise.reject("No valid auth token found");
  }

  return fetchData(`/deploy/fast_api`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      authToken: authToken
    },
    body: JSON.stringify({
      url: repoUrl,
      deploymentType: deploymentType,
      storageTypes: storageTypes,
      rootDir: rootDir || ".",
      buildCommand:
        buildCommand || "uvicorn main:app --host 0.0.0.0 --port 8000",
      envVars: envVars
    })
  });
};

export const getDeploymentStatus = (deploymentId) => {
  const authToken = getAuthToken();

  if (!authToken) {
    return Promise.reject("No valid auth token found");
  }

  return fetchData(`/deploy/status/${deploymentId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authToken: authToken
    }
  });
};
