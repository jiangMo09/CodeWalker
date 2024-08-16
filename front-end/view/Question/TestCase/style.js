import { css } from "styled-components";

const style = css`
  flex: 1;
  padding: 2vh 20px 20px;
  margin-top: 2vh;
  border-top: 1px solid #e8e8e8;
  overflow-y: auto;
  min-height: 150px;

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.5);
  }

  .test-case-tabs {
    display: flex;
    margin-bottom: 15px;

    button {
      position: relative;
      padding: 8px 16px;
      border: none;
      cursor: pointer;
      font-size: 14px;
      margin-right: 5px;
      border-radius: 4px;

      &.active {
        background-color: #e0e0e0;
        font-weight: bold;
      }

      .status-dot {
        position: absolute;
        left: 8px;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 4px;
        border-radius: 50%;
      }

      &.passed .status-dot {
        background-color: #4caf50;
      }

      &.failed .status-dot {
        background-color: #f44336;
      }

      &.pending .status-dot {
        display: none;
      }
    }
  }

  .test-case-content {
    border-radius: 4px;
    padding: 15px;
  }

  .param-row {
    margin-bottom: 10px;
  }

  .param-name {
    font-weight: bold;
    margin-right: 10px;
  }

  .param-value {
    background-color: #ffffff;
    color: black;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 5px 10px;
    font-family: Consolas, "Courier New", monospace;
    display: inline-block;
  }

  .error-message {
    color: #f44336;
    background-color: #ffebee;
    border: 1px solid #f44336;
    border-radius: 4px;
    padding: 10px;
    margin-top: 10px;
    font-family: Consolas, "Courier New", monospace;
  }
`;

export default style;
