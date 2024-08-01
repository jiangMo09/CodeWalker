const { createUserFunction, runTests } = require("./testRunner");
const { logTestCase, logSummary } = require("./logger");

const runCode = (data) => {
  const {
    typed_code,
    data_input,
    correct_answer,
    function_name,
    parameters_count
  } = JSON.parse(data);

  const userFunction = createUserFunction(typed_code, function_name);
  const inputs = data_input.split("\n").map(JSON.parse);
  const expectedOutputs = correct_answer.split("\n").map(JSON.parse);

  const stats = runTests(
    userFunction,
    inputs,
    expectedOutputs,
    parameters_count
  );

  stats.testCaseResults.forEach((testCaseStats, index) => {
    logTestCase(
      index + 1,
      testCaseStats,
      inputs.slice(index * parameters_count, (index + 1) * parameters_count),
      expectedOutputs[index]
    );
  });

  logSummary(stats);
};

const dataInput = process.env.DATA_INPUT;

try {
  runCode(dataInput);
} catch (error) {
  console.error("Error:", error.message);
}
