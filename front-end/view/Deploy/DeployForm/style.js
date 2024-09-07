import { css } from "styled-components";

export default css`
  display: flex;
  flex-direction: column;

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
`;
