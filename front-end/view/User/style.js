import { css } from "styled-components";

const style = css`
  .modal-background {
    width: 100%;
    height: 100%;
    background-color: #0f0f0f80;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 200;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 50px;
  }

  .modal-content {
    background-color: white;
    width: 340px;
    border-radius: 6px;
    overflow: hidden;
  }

  .decorator {
    width: 100%;
    height: 10px;
    background: linear-gradient(270deg, #0b410b 0%, #4caf50 100%);
  }

  .login,
  .register {
    padding: 25px 15px;
    text-align: center;
    color: #666666;

    .title {
      margin-bottom: 15px;
      font-size: 24px;
      font-weight: 700;
    }

    input {
      box-sizing: border-box;
      border: 1px solid #cccccc;
      padding-left: 15px;
      width: 310px;
      height: 47px;
      border-radius: 5px;
      margin-bottom: 10px;
      font-size: 16px;
    }

    #loginBtn,
    #signupBtn {
      width: 310px;
      height: 47px;
      background-color: #4caf50;
      color: white;
      font-size: 19px;
      border-radius: 5px;
      border: none;
      cursor: pointer;
    }

    .response-info {
      margin: 10px 0;
    }

    .success {
      color: green;
    }

    .error {
      color: red;
    }

    .signup,
    .signin {
      cursor: pointer;
    }
  }
`;

export default style;
