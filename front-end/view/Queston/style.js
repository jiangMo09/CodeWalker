import { css } from "styled-components";

const style = css`
  display: flex;
  height: 100vh;

  .description {
    flex: 1;
    padding: 20px;
    min-width: 300px;
    overflow-y: auto;
  }

  .description h1 {
    font-size: 24px;
    font-weight: 500;
    margin-bottom: 20px;
  }

  .description p,
  .description pre,
  .description ul,
  .description ol {
    margin-bottom: 15px;
    line-height: 1.6;
  }

  .description code {
    padding: 2px 4px;
    border-radius: 4px;
    font-family: Consolas, "Courier New", monospace;
  }

  .description pre {
    padding: 10px;
    border-radius: 4px;
  }

  .description strong.example {
    font-weight: 600;
  }

  .right-part {
    flex: 1.2;
    display: flex;
    flex-direction: column;
    border-left: 1px solid #e8e8e8;
    min-width: 300px;
  }

  .typed-code {
    flex: 2;
    padding: 20px;
    min-height: 200px;
    display: flex;
    flex-direction: column;
  }

  .typed-code select {
    width: 200px;
    padding: 8px;
    margin-bottom: 15px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 14px;
  }

  .typed-code textarea {
    flex: 1;
    padding: 15px;
    border-radius: 4px;
    border: 1px solid #e8e8e8;
    font-family: Consolas, "Courier New", monospace;
    font-size: 14px;
    line-height: 1.5;
    margin-bottom: 15px;
  }

  .typed-code button {
    align-self: flex-start;
    padding: 8px 16px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }

  .typed-code button:hover {
    background-color: #45a049;
  }

  .test-case {
    flex: 1;
    padding: 20px;
    border-top: 1px solid #e8e8e8;
    overflow-y: auto;
    min-height: 150px;
  }

  .test-case-tabs {
    display: flex;
    margin-bottom: 15px;
  }

  .test-case-tabs button {
    padding: 8px 16px;
    border: none;

    cursor: pointer;
    font-size: 14px;
    margin-right: 5px;
    border-radius: 4px;
  }

  .test-case-tabs button.active {
    background-color: #e0e0e0;
    font-weight: bold;
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
`;

export default style;
