import { css } from "styled-components";

export default css`
  display: flex;
  align-items: flex-start;
  background-color: #2d2e39;
  border: 1px solid #3a3b41;
  border-radius: 8px;
  padding: 16px;
  margin-top: 24px;

  .success-content {
    flex-grow: 1;
  }

  .success-title {
    display: flex;
    align-items: center;
  }

  .success-icon {
    font-size: 24px;
    color: #4caf50;
    margin-right: 16px;
  }

  .success-message {
    color: #e0e0e0;
    margin-bottom: 12px;
    font-weight: 500;
  }

  .success-actions {
    display: flex;
    align-items: center;
  }

  .success-url {
    flex-grow: 1;
    padding: 8px 12px;
    margin-right: 8px;
    background-color: #1e1f26;
    border: 1px solid #3a3b41;
    border-radius: 4px;
    color: #e0e0e0;
    font-size: 14px;
  }

  .success-open-button {
    padding: 8px 16px;
    background-color: #3a3b41;
    color: #e0e0e0;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s;

    &:hover {
      background-color: #4a4b51;
    }
  }
`;
