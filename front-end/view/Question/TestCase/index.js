import styled from "styled-components";
import Tabs from "./Tabs";
import Content from "./Content";
import useTestCase from "../hooks/useTestCase";
import style from "./style";

const TestCase = ({ className, dataInput, testResults }) => {
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
      {!testResults?.container_run_success && testResults?.is_infinite_loop && (
        <div className="title">
          <span className="status">Time Limit Exceeded</span>
        </div>
      )}

      {testResults?.container_run_success && (
        <div className="title">
          {testResults?.all_passed && (
            <>
              <span className="status passed">Accepted</span>
              <span className="run-time">
                Runtime: {testResults?.total_run_time}
              </span>
              <span className="run-time">
                Better than: {testResults?.percentile}%
              </span>
            </>
          )}

          {!testResults?.all_passed && (
            <>
              <span className="status">Wrong Answer</span>
              {testResults?.run_result.length !=
                testResults?.total_testcases && (
                <>
                  <span className="run-time">
                    Total Test Cases: {testResults?.total_testcases}
                  </span>
                  <span className="run-time">
                    Right Cases: {testResults?.total_correct}
                  </span>
                </>
              )}
            </>
          )}
        </div>
      )}
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
