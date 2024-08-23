import { css } from "styled-components";

const style = css`
  background-color: #2d2f39;
  padding: 16px;
  border-radius: 5px;
  margin-bottom: 32px;

  h3 {
    margin-top: 0;
  }

  ul {
    padding-left: 24px;
    line-height: 32px;
  }

  a {
    position: relative;
  }

  a::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -2px;
    width: 100%;
    height: 1px;
    background-color: rgba(0, 255, 0, 0.8);
    box-shadow: 0 0 6px 1px rgba(0, 255, 0, 0.8);
  }
`;

export default style;
