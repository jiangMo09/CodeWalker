import { useState } from "react";
import styled from "styled-components";
import { postTypedCode } from "../../../services/api/Question";
import style from "./style";

import User from "../../User";

const Header = ({
  className,
  questionId,
  selectedLanguage,
  userCode,
  setTestResults
}) => {
  const [isDisabled, setIsDisabled] = useState(false);

  const onButtonClick = async (submit) => {
    if (isDisabled) {
      alert("答案提交中，請耐心等待");
      return;
    }
    setIsDisabled(true);
    try {
      const response = await postTypedCode({
        submit,
        questionId,
        selectedLanguage,
        userCode
      });
      setTestResults(response);
    } catch (error) {
      console.error("Error posting code:", error);
      setTestResults({
        container_run_success: false,
        error: "An error occurred while processing your request."
      });
    } finally {
      setIsDisabled(false);
    }
  };

  const isButtonDisabled = isDisabled ? "disabled" : "";

  return (
    <div className={className}>
      <a href="/" className="logo">
        CodeWalker
      </a>
      <div className="buttons">
        <div
          className={`button run ${isButtonDisabled}`}
          onClick={() => {
            if (!isDisabled) onButtonClick(false);
          }}
        >
          <img className="run-icon icon" src="/images/run.svg" />
          run
        </div>
        <div
          className={`button submit ${isButtonDisabled}`}
          onClick={() => {
            if (!isDisabled) onButtonClick(true);
          }}
        >
          <img
            className="cloud-arrow-up-icon icon"
            src="/images/cloud-arrow-up.svg"
          />
          submit
        </div>
      </div>
      <User />
    </div>
  );
};

export default styled(Header)`
  ${style}
`;
