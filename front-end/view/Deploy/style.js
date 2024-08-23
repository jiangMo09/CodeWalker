import { css } from "styled-components";

const style = css`
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
    background-color: #4caf50;
    color: white;
    padding: 16px;
    border-radius: 4px;
    margin-top: 16px;
    text-align: center;
  }

  .success-message {
    margin-bottom: 8px;
  }

  .success-link {
    color: white;
    text-decoration: underline;
    font-weight: bold;

    &:hover {
      text-decoration: none;
    }
  }
`;

export default style;
