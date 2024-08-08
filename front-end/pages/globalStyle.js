import { createGlobalStyle } from "styled-components";

export default createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    font-family: PingFangTC, Arial, Helvetica, Microsoft JhengHei;
  }
  
  html{
    height: -webkit-fill-available;
    scroll-behavior: smooth;
  }

  a {
    text-decoration: none;
  }

  .pointer {
    cursor: pointer;
  }

  img {
    width: 100%;
    height: 100%;
  }
`;
