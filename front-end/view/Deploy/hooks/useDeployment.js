import { useState } from "react";
import {
  postPureJs,
  postFastApi,
  getDeploymentStatus
} from "../../../services/api/Deploy";

const useDeployment = (
  isLogin,
  repoUrl,
  deploymentType,
  storageTypes,
  rootDir,
  buildCommand,
  envVars
) => {
  const [error, setError] = useState("");
  const [isDeploying, setIsDeploying] = useState(false);
  const [deploymentSuccess, setDeploymentSuccess] = useState(null);
  const [deploymentStatus, setDeploymentStatus] = useState(null);

  const checkDeploymentStatus = async (id) => {
    if (!id) {
      console.log("No deployment ID, cannot check status");
      return;
    }
    console.log("Checking deployment status for ID:", id);

    try {
      const statusResponse = await getDeploymentStatus(id);
      console.log("Status response:", statusResponse);
      setDeploymentStatus(statusResponse);

      if (["completed", "failed"].includes(statusResponse.status)) {
        if (statusResponse.status === "completed") {
          setDeploymentSuccess(statusResponse);
        } else {
          setError("Deployment failed. Please try again.");
        }
      } else {
        console.log(
          "Deployment still in progress, checking again in 5 seconds"
        );
        setTimeout(() => checkDeploymentStatus(id), 5000);
      }
    } catch (error) {
      console.error("Error checking deployment status:", error);
      setError("Error checking deployment status. Please try again.");
    }
  };

  const handleDeploy = async (e) => {
    e.preventDefault();
    if (!isLogin) {
      setError("Please login to deploy.");
      return;
    }
    setError("");
    setDeploymentSuccess(null);
    setDeploymentStatus(null);

    if (!repoUrl.startsWith("https://github.com/")) {
      setError("Please enter a valid GitHub repository URL.");
      return;
    }

    setIsDeploying(true);
    try {
      const deploymentData = {
        repoUrl,
        deploymentType,
        storageTypes,
        rootDir,
        buildCommand,
        envVars
      };

      console.log("Deployment data:", deploymentData);

      let response;
      if (deploymentType === "pureJs") {
        response = await postPureJs(deploymentData);
      } else if (deploymentType === "fastApi") {
        response = await postFastApi(deploymentData);
      } else {
        throw new Error("Invalid deployment type");
      }

      console.log("API response:", response);

      if (response.success) {
        setDeploymentStatus({
          status: "starting",
          message: "Deployment started"
        });
        console.log(
          "Starting to check deployment status for ID:",
          response.deployment_id
        );
        checkDeploymentStatus(response.deployment_id);
      } else {
        setError(response.message || "Deployment failed. Please try again.");
      }
    } catch (error) {
      console.error("Deployment error:", error);
      setError(error.message || "Deployment failed. Please try again.");
    } finally {
      setIsDeploying(false);
    }
  };

  return {
    error,
    isDeploying,
    deploymentSuccess,
    deploymentStatus,
    handleDeploy
  };
};

export default useDeployment;
