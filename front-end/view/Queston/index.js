import { useState, useEffect } from "react";
import {
  getQuestionCode,
  getLanguagesList,
  getQuestionDescription,
  getQuestionsDataInput
} from "../../services/api/Question";
import styled from "styled-components";

import style from "./style";

const Question = ({ className, questionName }) => {
  const [description, setDescription] = useState("");
  const [languages, setLanguages] = useState([]);
  const [code, setCode] = useState("");
  const [dataInput, setDataInput] = useState("");

  useEffect(() => {
    if (!questionName) {
      return;
    }

    const fetchQuestionData = async () => {
      try {
        setDescription(
          await getQuestionDescription({ kebabCaseName: questionName })
        );
        setLanguages(await getLanguagesList());
        setCode(await getQuestionCode({ kebabCaseName: questionName }));
        setDataInput(
          await getQuestionsDataInput({ kebabCaseName: questionName })
        );
      } catch (error) {
        console.error("Error fetching question data:", error);
      }
    };

    fetchQuestionData();
  }, [questionName]);

  return (
    <div className={className}>
      <div className="description">Description</div>
      <div className="right-part">
        <div className="typed-code">typed-code</div>
        <div className="test-case">test-case</div>
      </div>
    </div>
  );
};

export default styled(Question)`
  ${style}
`;
