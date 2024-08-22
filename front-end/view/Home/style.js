import { css } from "styled-components";

const style = css`
  background-color: #24262e;
  color: white;
  min-height: 100vh;
  font-size: 16px;

  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    height: 6vh;
  }

  .website-name {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    margin-right: -125px;
  }

  .main {
    margin: 70px auto;
    max-width: 1200px;
  }

  .description {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
  }

  .features {
    margin-top: 60px;
    display: flex;
  }

  .feature {
    width: 600px;
  }

  .title {
    font-size: 24px;
    text-align: center;
    font-weight: 700;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .coding-logo {
    width: 24px;
    margin-right: 5px;
  }

  .triangle-up {
    width: 0;
    height: 0;
    border-left: 12px solid transparent;
    border-right: 12px solid transparent;
    border-bottom: 20.8px solid white;
    margin-right: 5px;
  }

  .coach-container {
    padding: 0 50px;
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
    cursor: pointer;
    margin: 20px auto;
    text-align: center;
    border: 1px solid white;
    padding: 10px;
    border-radius: 5px;
    transition: background-color 0.3s, color 0.3s, box-shadow 0.3s;
    display: block;

    &:hover {
      box-shadow: 0 0 10px 2px rgba(0, 255, 0, 0.8);
    }
  }

  .tabs {
    display: flex;
    margin-top: 20px;

    button {
      background-color: transparent;
      border: none;
      color: #9ca1b2;
      padding: 10px 20px;
      margin: 0;

      cursor: pointer;
      transition: background-color 0.3s, color 0.3s;
      font-size: 16px;
      border-radius: 8px 8px 0 0;
      position: relative;

      &.active {
        background-color: #24262e;
        color: white;

        &::after {
          content: "";
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          height: 2px;
          background-color: rgba(0, 255, 0, 0.8);
        }
      }

      &:hover:not(.active) {
        background-color: #3a3d4a;
        color: white;
      }
    }
  }

  .tab-content {
    background-color: #24262e;
    border-radius: 0 0 8px 8px;
    position: relative;

    ul {
      max-height: 320px;
      overflow-y: auto;
      list-style-type: none;
      padding: 0;
      margin: 0;
    }

    li {
      margin-bottom: 10px;
      padding: 6px;
      background-color: #2d2f39;
      border-radius: 4px;

      a {
        display: block;
        padding: 10px;
        background-color: #2d2f39;
        border-radius: 4px;
        color: white;
        text-decoration: none;
        transition: all 0.3s ease;

        &:hover {
          background-color: #3a3d4a;
          transform: translateX(5px);
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
      }
    }
  }

  .ranking-list {
    list-style-type: none;
    padding: 0;

    li {
      display: flex;
      align-items: center;
      padding: 10px;
      margin-bottom: 10px;
      background-color: #2d2f39;
      border-radius: 4px;

      .rank {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        margin-right: 10px;
        font-weight: bold;
      }

      .username {
        flex-grow: 1;
      }

      .score {
        font-weight: bold;
      }

      &.top-1 .rank {
        background-color: gold;
        color: #24262e;
      }

      &.top-2 .rank {
        background-color: silver;
        color: #24262e;
      }

      &.top-3 .rank {
        background-color: #cd7f32;
        color: #24262e;
      }
    }
  }
`;

export default style;
