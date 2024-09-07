import styled from "styled-components";
import style from "./style";

const SuccessMessage = ({ className, success }) => (
  <div className={className}>
    <div className="success-content">
      <div className="success-title">
        <div className="success-icon">✓</div>
        <p className="success-message">{success.message}</p>
      </div>
      <div className="success-actions">
        <input
          className="success-url"
          type="text"
          value={success.deploy_url}
          readOnly
        />
        <button
          className="success-open-button"
          onClick={() => window.open(success.deploy_url, "_blank")}
        >
          Open
        </button>
      </div>
    </div>
  </div>
);

export default styled(SuccessMessage)`
  ${style}
`;
