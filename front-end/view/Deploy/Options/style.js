import { css } from "styled-components";

const style = css`
  display: flex;
  align-items: center;

  .select-wrapper {
    width: 200px;
    margin: 0 20px 20px 0;
  }

  select {
    padding: 12px;
    background-color: #2d2f39;
    border: 1px solid #444;
    border-radius: 4px;
    color: white;
    width: 100%;
  }

  .checkbox-group {
    display: flex;
    flex-grow: 1;
  }

  label {
    margin-right: 16px;
    display: flex;
    color: white;
  }

  input[type="checkbox"] {
    margin-right: 8px;
  }
`;

export default style;
