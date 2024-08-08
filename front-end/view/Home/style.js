import { css } from "styled-components";
const style = css`
  background-color: #24262e;
  color: white;
  height: 100vh;
  font-size: 16px;

  .website-name {
    text-align: center;
    font-size: 48px;
    font-size: 900;
    padding-top: 20px;
  }

  .main {
    margin: 70px auto;
    max-width: 1200px;
  }

  .description {
    text-align: center;
    font-size: 24px;
    font-size: 700;
  }

  .features {
    margin-top: 60px;
    display: flex;
  }

  .feature {
    width: 600px;

    .title {
      font-size: 24px;
      text-align: center;
      font-size: 700;
    }

    .feature-description {
      margin-top: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;

      li {
        margin-bottom: 10px;
      }
    }

    .entry {
      width: fit-content;
      margin: 20px auto;
      text-align: center;
      border: 1px solid white;
      padding: 10px;
      border-radius: 5px;
      transition: background-color 0.3s, color 0.3s, box-shadow 0.3s;
    }

    .entry:hover {
      box-shadow: 0 0 10px 2px rgba(0, 255, 0, 0.8);
    }
  }
`;

export default style;
