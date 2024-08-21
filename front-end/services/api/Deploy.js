import { fetchData } from "../../utils/fetchData";

export const postPureJs = ({ repoUrl }) =>
  fetchData(`/pure_js`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url: repoUrl
    })
  });
