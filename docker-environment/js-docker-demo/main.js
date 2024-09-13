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
  const inputs = parseInput(data_input);
  const expectedOutputs = parseOutput(correct_answer);

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

const parseInput = (input) => {
  return input.split("\n").map((item) => {
    try {
      return JSON.parse(item);
    } catch (e) {
      return item;
    }
  });
};

const parseOutput = (output) => {
  return output.split("\n").map((item) => {
    if (item === "true" || item === "false") {
      return item === "true";
    }
    try {
      return JSON.parse(item);
    } catch (e) {
      return item;
    }
  });
};

const dataInput = process.env.DATA_INPUT;

try {
  runCode(dataInput);
} catch (error) {
  console.error("Error:", error.message);
}
