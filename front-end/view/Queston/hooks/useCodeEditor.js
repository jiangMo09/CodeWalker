import { useState, useEffect } from "react";
import {
  getLanguagesList,
  getQuestionCode
} from "../../../services/api/Question";

export const useCodeEditor = (questionName) => {
  const [languages, setLanguages] = useState([]);
  const [codeSnippets, setCodeSnippets] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState("");
  const [userCode, setUserCode] = useState("");
  const [editorLanguage, setEditorLanguage] = useState("cpp");

  useEffect(() => {
    if (!questionName) return;

    const fetchCodeData = async () => {
      try {
        const languagesList = await getLanguagesList();
        const prototypeCode = await getQuestionCode({
          kebabCaseName: questionName
        });

        setLanguages(languagesList);
        setCodeSnippets(prototypeCode.code_snippets);

        if (languagesList.length > 0) {
          setSelectedLanguage(languagesList[0].name);
        }
      } catch (error) {
        console.error("Error fetching code data:", error);
      }
    };

    fetchCodeData();
  }, [questionName]);

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
    const languageMap = {
      java: "java",
      cpp: "cpp",
      javascript: "javascript",
      python3: "python"
    };
    return languageMap[lang] || "javascript";
  };

  const handleEditorChange = (value) => {
    setUserCode(value);
  };

  return {
    languages,
    selectedLanguage,
    setSelectedLanguage,
    userCode,
    handleEditorChange,
    editorLanguage
  };
};
