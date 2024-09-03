import { useState, useEffect } from "react";
import styled from "styled-components";
import { postPureJs, postFastApi } from "../../services/api/Deploy";
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

  const handleDeploy = async (e) => {
    e.preventDefault();
    if (!isLogin) {
      setError("Please login for deploy.");
      return;
    }
    setError("");
    setDeploymentSuccess(null);

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

      let response;
      if (deploymentType === "pureJs") {
        response = await postPureJs(deploymentData);
      }
      if (deploymentType === "fastApi") {
        response = await postFastApi(deploymentData);
      }

      response.error
        ? setError(response.error)
        : setDeploymentSuccess(response);
    } catch (error) {
      setError("Deployment failed. Please try again.");
      console.error("Deployment error:", error);
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
        {deploymentSuccess && (
          <div className="success">
            <p className="success-message">{deploymentSuccess.message}</p>
            <a
              className="success-link"
              href={deploymentSuccess.deploy_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              View Deployed Site
            </a>
          </div>
        )}
      </main>
    </div>
  );
};

export default styled(Deploy)`
  ${style}
`;
