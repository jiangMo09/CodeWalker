import styled from "styled-components";
import style from "./style";

const DeploymentStatus = ({ className, status }) => (
  <div className={className}>
    <h3>Deployment Status: {status.status}</h3>
    <p>{status.message}</p>
    {status.status === "pending" && (
      <progress value={status.elapsed_time} max="600"></progress>
    )}
  </div>
);

export default styled(DeploymentStatus)`
  ${style}
`;
