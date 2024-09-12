import styled from "styled-components";
import style from "./style";

const Rules = ({ className, deploymentType, storageTypes }) => {
  const isRedis = storageTypes.includes("redis");
  const link = () => {
    if (isRedis) {
      return "https://github.com/jiangMo09/FastAPIWithRedis";
    }
    return "https://github.com/jiangMo09/FastAPI";
  };

  const getRules = () => {
    if (deploymentType === "fastApi") {
      return (
        <ul>
          <li>GitHub project must be public.</li>
          <li>The project root directory must have requirements.txt.</li>
          {storageTypes.includes("redis") && (
            <li>
              You must provide Redis connection details in the Environment
              Variables.
            </li>
          )}
          <li>Login required.</li>
          <li>
            <a href={link()}>👉 Example GitHub Repository Link 👈</a>
          </li>
        </ul>
      );
    }
    if (deploymentType === "pureJs") {
      return (
        <ul>
          <li>GitHub project must be public.</li>
          <li>
            The GitHub project can only contain HTML, JS, CSS and MD files.
          </li>
          <li>index.html must be in the root directory.</li>
          <li>Login required.</li>
          <li>
            <a href="https://github.com/WendyWang1031/greedySnakeGame">
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
