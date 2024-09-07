import styled from "styled-components";
import style from "./style";

const DeployForm = ({
  className,
  repoUrl,
  setRepoUrl,
  isDeploying,
  onDeploy
}) => (
  <form className={className} onSubmit={onDeploy}>
    <input
      className="deploy-input"
      type="text"
      value={repoUrl}
      onChange={(e) => setRepoUrl(e.target.value)}
      placeholder="Enter GitHub repository URL"
      required
    />
    <button className="deploy-button" type="submit" disabled={isDeploying}>
      {isDeploying ? "Deploying..." : "Deploy"}
    </button>
  </form>
);

export default styled(DeployForm)`
  ${style}
`;
