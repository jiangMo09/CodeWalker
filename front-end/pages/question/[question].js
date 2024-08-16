import { useRouter } from "next/router";
import Question from "../../view/Question";

const QuestionPage = () => {
  const router = useRouter();
  const { question } = router.query;

  return <Question questionName={question} />;
};

export default QuestionPage;
