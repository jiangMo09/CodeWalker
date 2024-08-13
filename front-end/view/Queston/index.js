import { useState, useEffect } from "react";
import {
  getQuestionCode,
  getLanguagesList,
  getQuestionDescription,
  getQuestionsDataInput
} from "../../services/api/Question";
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

  const getCodeForLanguage = () => {
    return (
      codeSnippets.find((c) => c.langSlug === selectedLanguage)?.code || ""
    );
  };

  const handleCodeChange = (event) => {
    setUserCode(event.target.value);
  };

  const handleSubmit = () => {
    // 這裡之後會處理提交代碼到後端的邏輯
    console.log("Submitting code:", userCode);
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
          <textarea
            value={userCode}
            onChange={handleCodeChange}
            spellCheck="false"
          />
          <button onClick={handleSubmit}>Submit</button>
        </div>
        <div className="test-case">
          <div className="test-case-tabs">
            {dataInput?.example_testcase_List?.[0]
              ?.split("\n")
              ?.map((_, index, array) => {
                if (index % 3 === 0) {
                  return (
                    <button
                      key={index}
                      className={selectedTestCase === index / 3 ? "active" : ""}
                      onClick={() => setSelectedTestCase(index / 3)}
                    >
                      Test Case {index / 3 + 1}
                    </button>
                  );
                }
                return null;
              })}
          </div>
          <pre>
            {dataInput?.example_testcase_List?.[0]
              ?.split("\n")
              ?.slice(selectedTestCase * 3, selectedTestCase * 3 + 3)
              .join("\n")}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default styled(Question)`
  ${style}
`;
