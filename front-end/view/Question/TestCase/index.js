import styled from "styled-components";
import Tabs from "./Tabs";
import Content from "./Content";
import useTestCase from "../hooks/useTestCase";
import style from "./style";

const TestCase = ({ dataInput, className, testResults }) => {
  const {
    selectedTestCase,
    setSelectedTestCase,
    testCases,
    metaData,
    paramCount
  } = useTestCase(dataInput);

  if (!testCases || !metaData) {
    return;
  }

  return (
    <div className={className}>
      <Tabs
        testCases={testCases}
        paramCount={paramCount}
        selectedTestCase={selectedTestCase}
        setSelectedTestCase={setSelectedTestCase}
        testResults={testResults}
      />
      <Content
        metaData={metaData}
        testCases={testCases}
        selectedTestCase={selectedTestCase}
        paramCount={paramCount}
        testResults={testResults}
      />
    </div>
  );
};

export default styled(TestCase)`
  ${style}
`;
