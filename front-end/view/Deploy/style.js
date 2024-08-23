import { css } from "styled-components";

const style = css`
  header {
    height: 6vh;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #1e1f26;
  }

  .logo {
    font-size: 24px;
    font-weight: 600;
    cursor: pointer;
  }

  main {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
  }

  h2 {
    text-align: center;
    margin-bottom: 2rem;
  }

  form {
    display: flex;
    flex-direction: column;
  }

  input {
    padding: 0.75rem;
    margin-bottom: 1rem;
    background-color: #2d2f39;
    border: 1px solid #444;
    border-radius: 4px;
    color: white;

    &::placeholder {
      color: #9ca1b2;
    }
  }

  button {
    padding: 0.75rem;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover:not(:disabled) {
      background-color: #45a049;
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }

  .error {
    color: #ffffff;
    background-color: #ff6b6b;
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
    text-align: center;
  }

  .success {
    background-color: #4caf50;
    color: white;
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
    text-align: center;

    p {
      margin-bottom: 0.5rem;
    }

    a {
      color: white;
      text-decoration: underline;
      font-weight: bold;

      &:hover {
        text-decoration: none;
      }
    }
  }
`;

export default style;