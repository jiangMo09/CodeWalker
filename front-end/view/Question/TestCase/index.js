import styled from "styled-components";
import { useState } from "react";
import style from "./style";

const TestCase = ({ dataInput, className, testResults }) => {
  const [selectedTestCase, setSelectedTestCase] = useState(0);

  if (!dataInput?.example_testcase_List?.[0] || !dataInput.meta_data) {
    return null;
  }

  const testCases = dataInput.example_testcase_List[0].split("\n");
  const metaData = JSON.parse(dataInput.meta_data);
  const paramCount = metaData.params.length;

  const renderTestResults = () => {
    if (!testResults) {
      return null;
    }

    if (!testResults.container_run_success) {
      return (
        <div className="error-message">
          Error: {testResults.error || "Unknown error occurred"}
        </div>
      );
    }

    const currentResult = testResults.run_result[selectedTestCase];
    if (!currentResult) {
      return null;
    }

    return (
      <>
        <div className="param-row">
          <span className="param-name">output =</span>
          <div className="param-value">{currentResult.output}</div>
        </div>
        <div className="param-row">
          <span className="param-name">expected =</span>
          <div className="param-value">{currentResult.expected}</div>
        </div>
      </>
    );
  };

  const getTestCaseStatus = (index) => {
    if (!testResults || !testResults.container_run_success) return "pending";
    const result = testResults.run_result[index];
    return result ? (result.passed ? "passed" : "failed") : "pending";
  };

  return (
    <div className={className}>
      <div className="test-case-tabs">
        {testCases.map(
          (_, index) =>
            index % paramCount === 0 && (
              <button
                key={index}
                className={`${
                  selectedTestCase === index / paramCount ? "active" : ""
                } ${getTestCaseStatus(index / paramCount)}`}
                onClick={() => setSelectedTestCase(index / paramCount)}
              >
                <span className="status-dot"></span>
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
        {renderTestResults()}
      </div>
    </div>
  );
};

export default styled(TestCase)`
  ${style}
`;