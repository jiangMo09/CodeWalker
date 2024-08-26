import { fetchData } from "../../utils/fetchData";

export const postPureJs = ({ repoUrl, deploymentType, storageTypes }) =>
  fetchData(`/deploy/pure_js`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url: repoUrl,
      deploymentType: deploymentType,
      storageTypes: storageTypes
    })
  });

export const postFastApi = ({
  repoUrl,
  deploymentType,
  storageTypes,
  rootDir,
  buildCommand,
  envVars
}) =>
  fetchData(`/deploy/fast_api`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
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
