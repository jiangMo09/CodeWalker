import { useState, useEffect } from "react";
import {
  getQuestionCode,
  getLanguagesList,
  getQuestionDescription,
  getQuestionsDataInput
} from "../../services/api/Question";

import Editor from "@monaco-editor/react";
import styled from "styled-components";

import style from "./style";

const Question = ({ className, questionName }) => {
  const [description, setDescription] = useState("");
  const [languages, setLanguages] = useState([]);
  const [codeSnippets, setCodeSnippets] = useState([]);
  const [dataInput, setDataInput] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState("");
  const [loading, setLoading] = useState(true);
  const [selectedTestCase, setSelectedTestCase] = useState(0);
  const [userCode, setUserCode] = useState("");
  const [metaData, setMetaData] = useState(null);
  const [editorLanguage, setEditorLanguage] = useState("cpp");

  useEffect(() => {
    if (!questionName) {
      return;
    }

    const fetchQuestionData = async () => {
      setLoading(true);
      try {
        const description = await getQuestionDescription({
          kebabCaseName: questionName
        });
        const languagesList = await getLanguagesList();
        const prototypeCode = await getQuestionCode({
          kebabCaseName: questionName
        });
        const testCases = await getQuestionsDataInput({
          kebabCaseName: questionName
        });

        setDescription(description.data.description);
        setLanguages(languagesList.data);
        setCodeSnippets(prototypeCode.data.code_snippets);
        setDataInput(testCases.data);
        setMetaData(JSON.parse(testCases.data.meta_data));

        if (languagesList.data.length > 0) {
          setSelectedLanguage(languagesList.data[0].name);
        }
      } catch (error) {
        console.error("Error fetching question data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestionData();
  }, [questionName]);

  useEffect(() => {
    setUserCode(getCodeForLanguage());
  }, [selectedLanguage]);

  useEffect(() => {
    setUserCode(getCodeForLanguage());
    setEditorLanguage(getMonacoLanguage(selectedLanguage));
  }, [selectedLanguage]);

  const getCodeForLanguage = () => {
    return (
      codeSnippets.find((c) => c.langSlug === selectedLanguage)?.code || ""
    );
  };

  const getMonacoLanguage = (lang) => {
    switch (lang) {
      case "java":
        return "java";
      case "cpp":
        return "cpp";
      case "javascript":
        return "javascript";
      case "python3":
        return "python";
      default:
        return "javascript";
    }
  };

  const handleEditorChange = (value) => {
    setUserCode(value);
  };

  const handleCodeChange = (event) => {
    setUserCode(event.target.value);
  };

  // const handleSubmit = () => {
  //   // 這裡之後會處理提交代碼到後端的邏輯
  //   console.log("Submitting code:", userCode);
  // };

  const renderTestCase = () => {
    if (!dataInput?.example_testcase_List?.[0] || !metaData) {
      return null;
    }

    const testCases = dataInput.example_testcase_List[0].split("\n");
    const paramCount = metaData.params.length;

    return (
      <div className="test-case">
        <div className="test-case-tabs">
          {testCases.map(
            (_, index) =>
              index % paramCount === 0 && (
                <button
                  key={index}
                  className={
                    selectedTestCase === index / paramCount ? "active" : ""
                  }
                  onClick={() => setSelectedTestCase(index / paramCount)}
                >
                  Case {index / paramCount + 1}
                </button>
              )
          )}
        </div>
        <div className="test-case-content">
          {metaData.params.map((param, index) => (
            <div key={param.name} className="param-row">
              <span className="param-name">{param.name} =</span>
              <div className="param-value">
                {testCases[selectedTestCase * paramCount + index]}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  if (loading) {
    return <div className={className}>Loading...</div>;
  }

  return (
    <div className={className}>
      <div className="description">
        <h1>{dataInput?.title}</h1>
        <div dangerouslySetInnerHTML={{ __html: description }} />
      </div>
      <div className="right-part">
        <div className="typed-code">
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
          >
            {languages.map((lang) => (
              <option key={lang.id} value={lang.name}>
                {lang.pretty_name}
              </option>
            ))}
          </select>
          <Editor
            height="55vh"
            language={editorLanguage}
            value={userCode}
            onChange={handleEditorChange}
            options={{
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              fontSize: 14,
              wordWrap: "on",
              automaticLayout: true,
              formatOnPaste: true,
              formatOnType: true,
            }}
          />
          {/* <button onClick={handleSubmit}>Submit</button> */}
        </div>
        {renderTestCase()}
      </div>
    </div>
  );
};

export default styled(Question)`
  ${style}
`;
