import Results from "../Results";

const Content = ({
  metaData,
  testCases,
  selectedTestCase,
  paramCount,
  testResults,
}) => {
  return (
    <div className="test-case-content">
      {metaData.params.map((param, index) => (
        <div key={param.name} className="param-row">
          <span className="param-name">{param.name} =</span>
          <div className="param-value">
            {testCases[selectedTestCase * paramCount + index]}
          </div>
        </div>
      ))}
      <Results testResults={testResults} selectedTestCase={selectedTestCase} />
    </div>
  );
};

export default Content;