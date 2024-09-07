import { useState, useEffect } from "react";
import styled from "styled-components";
import {
  postPureJs,
  postFastApi,
  getDeploymentStatus
} from "../../services/api/Deploy";
import { useGlobalContext } from "../../providers/GlobalProvider";
import User from "../User";
import Options from "./Options";
import Rules from "./Rules";
import Env from "./Env";
import style from "./style";

const Deploy = ({ className }) => {
  const { isLogin } = useGlobalContext();

  const [repoUrl, setRepoUrl] = useState("");
  const [error, setError] = useState("");
  const [isDeploying, setIsDeploying] = useState(false);
  const [deploymentSuccess, setDeploymentSuccess] = useState(null);
  const [deploymentType, setDeploymentType] = useState("pureJs");
  const [storageTypes, setStorageTypes] = useState([]);
  const [rootDir, setRootDir] = useState("");
  const [envVars, setEnvVars] = useState([{ key: "", value: "" }]);
  const [buildCommand, setBuildCommand] = useState("");
  const [deploymentStatus, setDeploymentStatus] = useState(null);

  const handleDeploymentTypeChange = (e) => {
    setDeploymentType(e.target.value);
    setStorageTypes([]);
  };

  const handleRootDirChange = (newRootDir) => {
    setRootDir(newRootDir);
  };

  const handleEnvVarsChange = (newEnvVars) => {
    setEnvVars(newEnvVars);
  };

  const handleBuildCommandChange = (newBuildCommand) => {
    setBuildCommand(newBuildCommand);
  };

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
      setError("Please login for deploy.");
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
        checkDeploymentStatus(response.deployment_id); // 直接傳入 deployment_id
      } else {
        setError(response.message || "Deployment failed. Please try again.");
      }
    } catch (error) {
      console.error("Deployment error:", error);
      setError(error.message || "Deployment failed. Please try again.");
    } finally {
      setIsDeploying(false);
      setRepoUrl("");
    }
  };

  useEffect(() => {
    if (!storageTypes.includes("redis")) {
      setEnvVars([{ key: "", value: "" }]);
      return;
    }

    setEnvVars([
      { key: "REDIS_HOST", value: "redis" },
      { key: "REDIS_PORT", value: 6379 },
      { key: "REDIS_DB", value: 0 }
    ]);
  }, [storageTypes]);

  return (
    <div className={className}>
      <header className="deploy-header">
        <a href="/" className="logo">
          CodeWalker
        </a>
        <User />
      </header>
      <main className="deploy-main">
        <h2 className="deploy-title">Deploy Your Project Now.</h2>
        <Options
          deploymentType={deploymentType}
          onDeploymentTypeChange={handleDeploymentTypeChange}
          storageTypes={storageTypes}
          onStorageTypeChange={setStorageTypes}
        />
        <Rules deploymentType={deploymentType} storageTypes={storageTypes} />
        <form className="deploy-form" onSubmit={handleDeploy}>
          {deploymentType === "fastApi" && (
            <Env
              rootDir={rootDir}
              envVars={envVars}
              buildCommand={buildCommand}
              onRootDirChange={handleRootDirChange}
              onEnvVarsChange={handleEnvVarsChange}
              onBuildCommandChange={handleBuildCommandChange}
            />
          )}
          <input
            className="deploy-input"
            type="text"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="Enter GitHub repository URL"
            required
          />
          <button
            className="deploy-button"
            type="submit"
            disabled={isDeploying}
          >
            {isDeploying ? "Deploying..." : "Deploy"}
          </button>
        </form>
        {error && <div className="error-message">{error}</div>}
        {deploymentStatus && (
          <div className="deployment-status">
            <h3>Deployment Status: {deploymentStatus.status}</h3>
            <p>{deploymentStatus.message}</p>
            {deploymentStatus.status === "pending" && (
              <progress
                value={deploymentStatus.elapsed_time}
                max="600"
              ></progress>
            )}
          </div>
        )}
        {deploymentSuccess && (
          <div className="success">
            <div className="success-content">
              <div className="success-title">
                <div className="success-icon">✓</div>
                <p className="success-message">{deploymentSuccess.message}</p>
              </div>
              <div className="success-actions">
                <input
                  className="success-url"
                  type="text"
                  value={deploymentSuccess.deploy_url}
                  readOnly
                />
                <button
                  className="success-open-button"
                  onClick={() =>
                    window.open(deploymentSuccess.deploy_url, "_blank")
                  }
                >
                  Open
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default styled(Deploy)`
  ${style}
`;
