import styled from "styled-components";
import { useQuestionData } from "./hooks/useQuestionData";
import { useCodeEditor } from "./hooks/useCodeEditor";
import Description from "./Description";
import CodeEditor from "./CodeEditor";
import TestCase from "./TestCase";
import Header from "./Header";
import style from "./style";

const Question = ({ className, questionName }) => {
  const { description, dataInput, loading } = useQuestionData(questionName);

  const {
    languages,
    selectedLanguage,
    setSelectedLanguage,
    userCode,
    handleEditorChange,
    editorLanguage
  } = useCodeEditor(questionName);

  if (loading) {
    return <div className={className}>Loading...</div>;
  }

  const title = description.id + ". " + description.pretty_name;

  return (
    <div className={className}>
      <Header />
      <div className="main">
        <Description description={description.description} title={title} />
        <div className="right-part">
          <CodeEditor
            languages={languages}
            selectedLanguage={selectedLanguage}
            setSelectedLanguage={setSelectedLanguage}
            userCode={userCode}
            handleEditorChange={handleEditorChange}
            editorLanguage={editorLanguage}
          />
          <TestCase dataInput={dataInput} />
        </div>
      </div>
    </div>
  );
};

export default styled(Question)`
  ${style}
`;
