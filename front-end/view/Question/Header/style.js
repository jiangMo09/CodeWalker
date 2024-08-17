import { css } from "styled-components";

const style = css`
  height: 5vh;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #1e1f26;

  .logo {
    font-size: 24px;
    font-weight: 600;
    cursor: pointer;
  }

  .buttons {
    display: flex;
    gap: 10px;
  }

  .button {
    border: 1px solid white;
    padding: 5px 10px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    cursor: pointer;
  }

  .button.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .submit {
    border: 1px solid rgba(0, 255, 0, 0.8);
    color: rgba(0, 255, 0, 0.8);
  }

  .icon {
    margin-right: 5px;
  }

  .run-icon {
    width: 15px;
    height: 15px;
  }
`;

export default style;
