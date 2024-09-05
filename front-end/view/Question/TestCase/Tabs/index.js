const Tabs = ({
  testCases,
  paramCount,
  selectedTestCase,
  setSelectedTestCase,
  testResults
}) => {
  const getTestCaseStatus = (index) => {
    if (!testResults || !testResults.container_run_success) {
      return "pending";
    }
    const result = testResults.run_result[index];
    return result ? (result.passed ? "passed" : "failed") : "pending";
  };

  return (
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
  );
};

export default Tabs;
