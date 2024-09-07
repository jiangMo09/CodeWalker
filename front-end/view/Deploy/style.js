import { css } from "styled-components";

const style = css`
  padding-bottom: 20px;

  .deploy-header {
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #1e1f26;
  }

  .logo {
    font-size: 24px;
    font-weight: 600;
    cursor: pointer;
  }

  .deploy-main {
    max-width: 800px;
    margin: 32px auto;
    padding: 0 16px;
  }

  .deploy-title {
    text-align: center;
    margin-bottom: 32px;
  }

  .deploy-form {
    display: flex;
    flex-direction: column;
  }

  .deploy-input {
    padding: 12px;
    margin-bottom: 16px;
    background-color: #2d2f39;
    border: 1px solid #444;
    border-radius: 4px;
    color: white;

    &::placeholder {
      color: #9ca1b2;
    }
  }

  .deploy-button {
    padding: 12px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover:not(:disabled) {
      background-color: #45a049;
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }

  .error-message {
    color: #ffffff;
    background-color: #ff6b6b;
    padding: 16px;
    border-radius: 4px;
    margin-top: 16px;
    text-align: center;
  }

  .success {
    display: flex;
    align-items: flex-start;
    background-color: #2d2e39;
    border: 1px solid #3a3b41;
    border-radius: 8px;
    padding: 16px;
    margin-top: 24px;
  }

  .success-icon {
    font-size: 24px;
    color: #4caf50;
    margin-right: 16px;
  }

  .success-content {
    flex-grow: 1;
  }

  .success-title {
    display: flex;
    align-items: center;
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

export default style;
