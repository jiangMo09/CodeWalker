const Results = ({ testResults, selectedTestCase }) => {
  if (!testResults) {
    return;
  }

  if (!testResults.container_run_success) {
    return (
      <div className="error-message">
        {testResults.error || "Error: Unknown error occurred"}
      </div>
    );
  }

  const currentResult = testResults.run_result[selectedTestCase];
  if (!currentResult) {
    return;
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

export default Results;
