import { fetchData } from "../../utils/fetchData";

export const getQuestionsList = () => fetchData(`/api/questions_list`);
