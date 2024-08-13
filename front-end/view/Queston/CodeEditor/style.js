import { css } from "styled-components";

const style = css`
  flex: 2;
  padding: 20px;
  min-height: 200px;
  display: flex;
  flex-direction: column;

  select {
    width: 200px;
    padding: 8px;
    margin-bottom: 15px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 14px;
  }

  .monaco-editor {
    flex: 1;
    border-radius: 4px;
    border: 1px solid #e8e8e8;
    margin-bottom: 15px;
  }

  button {
    align-self: flex-start;
    padding: 8px 16px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;

    &:hover {
      background-color: #45a049;
    }
  }
`;

export default style;
