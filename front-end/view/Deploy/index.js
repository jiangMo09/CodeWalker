import { useState } from "react";
import styled from "styled-components";
import { useGlobalContext } from "../../providers/GlobalProvider";
import useDeployment from "./hooks/useDeployment";
import Header from "./Header";
import Options from "./Options";
import Rules from "./Rules";
import Env from "./Env";
import DeployForm from "./DeployForm";
import DeploymentStatus from "./DeploymentStatus";
import SuccessMessage from "./SuccessMessage";
import style from "./style";

const Deploy = ({ className }) => {
  const { isLogin } = useGlobalContext();
  const [repoUrl, setRepoUrl] = useState("");
  const [deploymentType, setDeploymentType] = useState("pureJs");
  const [storageTypes, setStorageTypes] = useState([]);
  const [rootDir, setRootDir] = useState("");
  const [envVars, setEnvVars] = useState([{ key: "", value: "" }]);
  const [buildCommand, setBuildCommand] = useState("");

  const {
    error,
    isDeploying,
    deploymentSuccess,
    deploymentStatus,
    handleDeploy
  } = useDeployment(
    isLogin,
    repoUrl,
    deploymentType,
    storageTypes,
    rootDir,
    buildCommand,
    envVars
  );

  const handleStorageTypeChange = (newStorageTypes, changedType) => {
    setStorageTypes(newStorageTypes);
    if (changedType === "redis") {
      if (newStorageTypes.includes("redis")) {
        setEnvVars((prevEnvVars) => [
          { key: "REDIS_HOST", value: "redis" },
          { key: "REDIS_PORT", value: "6379" },
          { key: "REDIS_DB", value: "0" },
          ...prevEnvVars.filter(
            (env) => !["REDIS_HOST", "REDIS_PORT", "REDIS_DB"].includes(env.key)
          )
        ]);
      } else {
        setEnvVars((prevEnvVars) =>
          prevEnvVars.filter(
            (env) => !["REDIS_HOST", "REDIS_PORT", "REDIS_DB"].includes(env.key)
          )
        );
      }
    }
  };

  return (
    <div className={className}>
      <Header />
      <main className="deploy-main">
        <h2 className="deploy-title">Deploy Your Project Now.</h2>
        <Options
          deploymentType={deploymentType}
          onDeploymentTypeChange={(e) => setDeploymentType(e.target.value)}
          storageTypes={storageTypes}
          onStorageTypeChange={handleStorageTypeChange}
        />
        <Rules deploymentType={deploymentType} storageTypes={storageTypes} />
        {deploymentType === "fastApi" && (
          <Env
            rootDir={rootDir}
            envVars={envVars}
            buildCommand={buildCommand}
            onRootDirChange={setRootDir}
            onEnvVarsChange={setEnvVars}
            onBuildCommandChange={setBuildCommand}
          />
        )}
        <DeployForm
          repoUrl={repoUrl}
          setRepoUrl={setRepoUrl}
          isDeploying={isDeploying}
          onDeploy={handleDeploy}
        />
        {error && <div className="error-message">{error}</div>}
        {deploymentStatus && <DeploymentStatus status={deploymentStatus} />}
        {deploymentSuccess && <SuccessMessage success={deploymentSuccess} />}
      </main>
    </div>
  );
};

export default styled(Deploy)`
  ${style}
`;
