import { createGlobalStyle } from "styled-components";

export default createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
    "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue",
    sans-serif;
    background-color: #24262e;
    color: white;
    min-height: 100vh;
    font-size: 16px;
  }
  
  html{
    height: -webkit-fill-available;
    scroll-behavior: smooth;
  }

  a {
    text-decoration: none;
    color: white;
  }

  .pointer {
    cursor: pointer;
  }

  img {
    width: 100%;
    height: 100%;
  }
`;
