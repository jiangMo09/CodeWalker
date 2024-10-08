import { useState } from "react";
import styled from "styled-components";
import {
  postTypedCode,
  getQuestionResult
} from "../../../services/api/Question";
import { useGlobalContext } from "../../../providers/GlobalProvider";
import User from "../../User";
import style from "./style";

const Header = ({
  className,
  questionId,
  selectedLanguage,
  userCode,
  setTestResults
}) => {
  const { isLogin } = useGlobalContext();
  const [isDisabled, setIsDisabled] = useState(false);

  const onButtonClick = async (submit) => {
    if (!isLogin) {
      alert("Please Login.");
      return;
    }
    if (isDisabled) {
      alert("The answer is being submitted, please wait patiently.");
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

      const question_result_id = response.question_result_id;
      const pollResult = async () => {
        try {
          const result = await getQuestionResult(question_result_id);

          if (result?.status === "running") {
            setTimeout(pollResult, 1000);
          } else {
            setTestResults(result);
            setIsDisabled(false);
          }
        } catch (error) {
          console.error("Error getting question result:", error);
          setTestResults({
            container_run_success: false,
            error: "An error occurred while fetching the results."
          });
          setIsDisabled(false);
        }
      };

      pollResult();
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
            if (isDisabled) {
              return;
            }
            onButtonClick(false);
          }}
        >
          <img className="run-icon icon" src="/images/run.svg" />
          run
        </div>
        <div
          className={`button submit ${isButtonDisabled}`}
          onClick={() => {
            if (isDisabled) {
              return;
            }
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
      <User />
    </div>
  );
};

export default styled(Header)`
  ${style}
`;
