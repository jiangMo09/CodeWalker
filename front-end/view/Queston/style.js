import { css } from "styled-components";

const style = css`
  max-height: 100vh;
  overflow: hidden;

  .main {
    display: flex;
    max-height: 100vh;
  }

  .right-part {
    flex: 1.27;
    display: flex;
    flex-direction: column;
    border-left: 1px solid #e8e8e8;
    min-width: 300px;
    margin-left: 6px;
    overflow: hidden;
  }
`;

export default style;
