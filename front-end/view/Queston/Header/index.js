import styled from "styled-components";
import { postTypedCode } from "../../../services/api/Question";
import style from "./style";

const Header = ({ className, questionId, selectedLanguage, userCode }) => {
  const onButtonClick = async (submit) => {
    await postTypedCode({ submit, questionId, selectedLanguage, userCode });
  };

  return (
    <div className={className}>
      <div className="logo">CodeWalker</div>
      <div className="buttons">
        <div
          className="button run"
          onClick={() => {
            onButtonClick(false);
          }}
        >
          <img className="run-icon icon" src="/images/run.svg" />
          run
        </div>
        <div
          className="button submit"
          onClick={() => {
            onButtonClick(true);
          }}
        >
          <img
            className="cloud-arrow-up-icon icon"
            src="/images/cloud-arrow-up.svg"
          />
          submit
        </div>
      </div>
      <div className="user">user : Leona</div>
    </div>
  );
};

export default styled(Header)`
  ${style}
`;
