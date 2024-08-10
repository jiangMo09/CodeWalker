import { fetchData } from "../../utils/fetchData";

export const getQuestionDescription = ({ kebabCaseName }) =>
  fetchData(`/api/question_description?name=${kebabCaseName}`);

export const getQuestionCode = ({ kebabCaseName }) =>
  fetchData(`/api/question_code?name=${kebabCaseName}`);

export const getQuestionsDataInput = ({ kebabCaseName }) =>
  fetchData(`/api/question_data_input?name=${kebabCaseName}`);

export const getLanguagesList = () => fetchData(`/api/languages_list`);
