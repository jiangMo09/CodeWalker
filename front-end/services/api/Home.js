import { fetchData } from "../../utils/fetchData";

export const getQuestionsList = () => fetchData(`/questions_list`);
export const getRanking = () => fetchData(`/ranking`);
