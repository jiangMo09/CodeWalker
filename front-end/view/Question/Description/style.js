import { css } from "styled-components";

const style = css`
  flex: 1;
  padding: 20px;
  min-width: 300px;

  overflow-y: auto;
  height: 80vh;

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

  h1 {
    font-size: 24px;
    font-weight: 500;
    margin-bottom: 20px;
  }

  p,
  pre,
  ul,
  ol {
    margin-bottom: 15px;
    line-height: 1.6;
  }

  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
  }

  code {
    padding: 2px 4px;
    border-radius: 4px;
    font-family: Consolas, "Courier New", monospace;
  }

  pre {
    padding: 10px;
    border-radius: 4px;
  }

  strong.example {
    font-weight: 600;
  }
`;

export default style;
