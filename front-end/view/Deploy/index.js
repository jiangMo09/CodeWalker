import { useState } from "react";
import styled from "styled-components";
import { postPureJs } from "../../services/api/Deploy";
import style from "./style";

const Deploy = ({ className }) => {
  const [repoUrl, setRepoUrl] = useState("");
  const [error, setError] = useState("");
  const [isDeploying, setIsDeploying] = useState(false);
  const [deploymentSuccess, setDeploymentSuccess] = useState(null);

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
        repoUrl
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

  return (
    <div className={className}>
      <header>
        <a href="/" className="logo">
          CodeWalker
        </a>
        <div className="user">user : Leona</div>
      </header>
      <main>
        <h2>Deploy Your Project Now.</h2>
        <div className="rules">
          <h3>Deployment Rules :</h3>
          <ul>
            <li>GitHub project must be public.</li>
            <li>
              The GitHub project can only contain HTML, JS, and CSS files.
            </li>
            <li>index.html must be in the root directory.</li>
            <li>
              <a href="https://github.com/Padax/team-practice">
                👉 Example GitHub Repository Link 👈
              </a>
            </li>
          </ul>
        </div>
        <form onSubmit={handleDeploy}>
          <input
            type="text"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="Enter GitHub repository URL"
            required
          />
          <button type="submit" disabled={isDeploying}>
            {isDeploying ? "Deploying..." : "Deploy"}
          </button>
        </form>
        {error && <div className="error">{error}</div>}
        {deploymentSuccess && (
          <div className="success">
            <p>{deploymentSuccess.message}</p>
            <a
              href={deploymentSuccess.cloudfront_path}
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
