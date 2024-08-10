import { useState, useEffect } from "react";
import {
  getQuestionCode,
  getLanguagesList,
  getQuestionDescription,
  getQuestionsDataInput
} from "../../services/api/Question";

const Question = ({ questionName }) => {
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

  return <div>Question</div>;
};

export default Question;
