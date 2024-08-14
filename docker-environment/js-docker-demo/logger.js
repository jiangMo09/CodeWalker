let testCases = [];
let totalCorrect = 0;
let totalTestcases = 0;

const logTestCase = (index, stats, inputs, expectedOutput) => {
  totalTestcases++;
  if (stats.passed) totalCorrect++;

  const testCaseResult = {
    test_case: index,
    passed: stats.passed,
    inputs: JSON.stringify(inputs),
    output: stats.result === undefined ? "undefined" : JSON.stringify(stats.result),
    expected: JSON.stringify(expectedOutput),
    run_time: `${stats.runTime.toFixed(3)} ms`,
    memory: `${(stats.memoryUsed / 1024).toFixed(3)} KB`
  };

  testCases.push(testCaseResult);
};

const logSummary = (stats) => {
  const summary = {
    run_result: testCases,
    total_correct: totalCorrect,
    total_testcases: totalTestcases,
    total_run_time: `${stats.totalRunTime.toFixed(3)} ms`,
    total_run_memory: `${(stats.totalMemoryUsed / 1024).toFixed(3)} MB`,
    all_passed: stats.allTestsPassed
  };

  console.log(JSON.stringify(summary, (key, value) => 
    value === undefined ? "undefined" : value
  ));
};

module.exports = { logTestCase, logSummary };
