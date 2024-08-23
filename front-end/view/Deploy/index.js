import { useState } from "react";
import styled from "styled-components";
import { postPureJs } from "../../services/api/Deploy";
import User from "../User";
import Options from "./Options";
import Rules from "./Rules";
import style from "./style";

const Deploy = ({ className }) => {
  const [repoUrl, setRepoUrl] = useState("");
  const [error, setError] = useState("");
  const [isDeploying, setIsDeploying] = useState(false);
  const [deploymentSuccess, setDeploymentSuccess] = useState(null);
  const [deploymentType, setDeploymentType] = useState("pureJs");
  const [storageTypes, setStorageTypes] = useState([]);

  const handleDeploy = async (e) => {
    e.preventDefault();
    setError("");
    setDeploymentSuccess(null);

    if (!repoUrl.startsWith("https://github.com/")) {
      setError("Please enter a valid GitHub repository URL.");
      return;
    }

    setIsDeploying(true);
    try {
      const response = await postPureJs({
        repoUrl,
        deploymentType,
        storageTypes
      });
      response.error
        ? setError(response.error)
        : setDeploymentSuccess(response);
    } catch (error) {
      setError("Deployment failed. Please try again.");
    } finally {
      setIsDeploying(false);
      setRepoUrl("");
    }
  };

  const handleDeploymentTypeChange = (e) => {
    setDeploymentType(e.target.value);
    setStorageTypes([]);
  };

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
