import { useState, useEffect } from "react";
import {
  getQuestionDescription,
  getQuestionsDataInput
} from "../../../services/api/Question";

export const useQuestionData = (questionName) => {
  const [description, setDescription] = useState("");
  const [dataInput, setDataInput] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!questionName) return;

    const fetchQuestionData = async () => {
      setLoading(true);
      try {
        const descriptionData = await getQuestionDescription({
          kebabCaseName: questionName
        });
        const testCases = await getQuestionsDataInput({
          kebabCaseName: questionName
        });
        setDescription(descriptionData);
        setDataInput(testCases);
      } catch (error) {
        console.error("Error fetching question data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestionData();
  }, [questionName]);

  return { description, dataInput, loading };
};
