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
            <li>
              There must be a SQL file in the root directory of the project.
            </li>
          )}
          {storageTypes.includes("redis") && (
            <li>
              You must provide Redis connection details in the Environment
              Variables.
            </li>
          )}
          <li>Login required.</li>
          <li>
            <a href="https://github.com/jiangMo09/FastAPI">
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
          <li>Login required.</li>
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
