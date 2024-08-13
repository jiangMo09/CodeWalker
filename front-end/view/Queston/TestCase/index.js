import styled from "styled-components";
import { useState } from "react";
import style from "./style";

const TestCase = ({ dataInput, className }) => {
  const [selectedTestCase, setSelectedTestCase] = useState(0);

  if (!dataInput?.example_testcase_List?.[0] || !dataInput.meta_data) {
    return null;
  }

  const testCases = dataInput.example_testcase_List[0].split("\n");
  const metaData = JSON.parse(dataInput.meta_data);
  const paramCount = metaData.params.length;

  return (
    <div className={className}>
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

export default styled(TestCase)`
  ${style}
`;
