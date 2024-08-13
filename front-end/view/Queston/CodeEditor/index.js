import styled from "styled-components";
import Editor from "@monaco-editor/react";
import style from "./style";

const CodeEditor = ({
  languages,
  selectedLanguage,
  setSelectedLanguage,
  userCode,
  handleEditorChange,
  editorLanguage,
  className
}) => (
  <div className={className}>
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
        formatOnType: true
      }}
    />
  </div>
);

export default styled(CodeEditor)`
  ${style}
`;
