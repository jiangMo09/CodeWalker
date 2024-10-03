import { fetchData } from "../../utils/fetchData";
import { getAuthToken } from "../../utils/getAuthToken";

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
}) => {
  const authToken = getAuthToken();

  if (!authToken) {
    return Promise.reject("No valid auth token found");
  }

  return fetchData(`/question_code`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      authToken: authToken
    },
    body: JSON.stringify({
      submit: submit,
      question_id: questionId,
      lang: selectedLanguage,
      typed_code: userCode
    })
  });
};

export const getQuestionResult = (question_result_id) => {
  const authToken = getAuthToken();

  if (!authToken) {
    return Promise.reject("No valid auth token found");
  }

  return fetchData(`/execution_result/${question_result_id}`, {
    headers: {
      "Content-Type": "application/json",
      authToken: authToken
    }
  });
};
