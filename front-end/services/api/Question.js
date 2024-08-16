import { fetchData } from "../../utils/fetchData";

export const getQuestionDescription = ({ kebabCaseName }) =>
  fetchData(`/question_description?name=${kebabCaseName}`);

export const getQuestionCode = ({ kebabCaseName }) =>
  fetchData(`/question_code?name=${kebabCaseName}`);

export const getQuestionsDataInput = ({ kebabCaseName }) =>
  fetchData(`/question_data_input?name=${kebabCaseName}`);

export const getLanguagesList = () => fetchData(`/languages_list`);

export const postTypedCode = ({
  submit,
  questionId,
  selectedLanguage,
  userCode
}) =>
  fetchData(`/question_code`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      submit: submit,
      question_id: questionId,
      lang: selectedLanguage,
      typed_code: userCode
    })
  });
