import { css } from "styled-components";

export default css`
  margin-top: 20px;
  padding: 15px;
  background-color: #2d2e39;
  border: 1px solid #3a3b41;
  border-radius: 4px;

  h3 {
    margin-bottom: 10px;
    color: #e0e0e0;
  }

  p {
    margin-bottom: 10px;
    color: #9ca1b2;
  }

  progress {
    width: 100%;
    height: 20px;
    -webkit-appearance: none;
    appearance: none;
  }

  progress::-webkit-progress-bar {
    background-color: #1e1f26;
    border-radius: 4px;
  }

  progress::-webkit-progress-value {
    background-color: #4caf50;
    border-radius: 4px;
  }

  progress::-moz-progress-bar {
    background-color: #4caf50;
    border-radius: 4px;
  }
`;
