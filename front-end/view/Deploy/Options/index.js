import styled from "styled-components";
import style from "./style";

const Options = ({
  className,
  deploymentType,
  onDeploymentTypeChange,
  storageTypes,
  onStorageTypeChange
}) => {
  const handleStorageTypeChange = (type) => {
    const newStorageTypes = storageTypes.includes(type)
      ? storageTypes.filter((t) => t !== type)
      : [...storageTypes, type];
    onStorageTypeChange(newStorageTypes);
  };

  return (
    <div className={className}>
      <div className="select-wrapper">
        <select value={deploymentType} onChange={onDeploymentTypeChange}>
          <option value="pureJs">Pure JS</option>
          <option value="fastApi">Fast API</option>
        </select>
      </div>
      <div className="checkbox-group">
        {deploymentType === "pureJs" && (
          <label>
            <input
              type="checkbox"
              checked={storageTypes.includes("CloudFront")}
              onChange={() => handleStorageTypeChange("CloudFront")}
            />
            CloudFront
          </label>
        )}
        {deploymentType === "fastApi" && (
          <>
            <label>
              <input
                type="checkbox"
                checked={storageTypes.includes("sqlite")}
                onChange={() => handleStorageTypeChange("sqlite")}
              />
              SQLite
            </label>
            <label>
              <input
                type="checkbox"
                checked={storageTypes.includes("elasticache")}
                onChange={() => handleStorageTypeChange("elasticache")}
              />
              Redis
            </label>
          </>
        )}
      </div>
    </div>
  );
};

export default styled(Options)`
  ${style}
`;