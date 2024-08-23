import styled from "styled-components";
import style from "./style";

const Rules = ({ className, deploymentType, storageTypes }) => {
  const getRules = () => {
    if (deploymentType === "fastApi") {
      return (
        <ul>
          <li>GitHub project must be public.</li>
          <li>The project root directory must have requirements.txt.</li>
          {storageTypes.includes("sqlite") && (
            <li>There must be a sql file in the project.</li>
          )}
          <li>Login required.</li>
          <li>
            <a href="https://github.com/Padax/team-practice">
              👉 Example GitHub Repository Link 👈
            </a>
          </li>
        </ul>
      );
    }
    if (deploymentType === "pureJs") {
      return (
        <ul>
          <li>GitHub project must be public.</li>
          <li>The GitHub project can only contain HTML, JS, and CSS files.</li>
          <li>index.html must be in the root directory.</li>
          {storageTypes.includes("CloudFront") && <li>Login required.</li>}
          <li>
            <a href="https://github.com/Padax/team-practice">
              👉 Example GitHub Repository Link 👈
            </a>
          </li>
        </ul>
      );
    }
  };

  return (
    <div className={className}>
      <h3>Deployment Rules :</h3>
      {getRules()}
    </div>
  );
};

export default styled(Rules)`
  ${style}
`;
