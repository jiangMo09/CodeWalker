const vm = require("vm");
const { performance } = require("perf_hooks");

const executeTestCase = (userFunction, inputs, expectedOutput) => {
  const startTime = performance.now();
  const startMemory = process.memoryUsage().heapUsed;

  let result, error;
  try {
    result = userFunction(...inputs);
  } catch (err) {
    error = err.message;
  }

  const endTime = performance.now();
  const endMemory = process.memoryUsage().heapUsed;

  return {
    runTime: endTime - startTime,
    memoryUsed: endMemory - startMemory,
    passed: JSON.stringify(result) === JSON.stringify(expectedOutput),
    result,
    error
  };
};

const createUserFunction = (code, functionName) => {
  const sandbox = { console };
  const context = vm.createContext(sandbox);
  new vm.Script(code).runInContext(context);

  const userFunction = sandbox[functionName];
  if (typeof userFunction !== "function") {
    throw new Error(`Function '${functionName}' not found`);
  }

  return userFunction;
};

const runTests = (userFunction, inputs, expectedOutputs, parametersCount) => {
  const stats = {
    allTestsPassed: true,
    totalRunTime: 0,
    totalMemoryUsed: 0,
    testCaseResults: []
  };

  for (let i = 0; i < inputs.length; i += parametersCount) {
    const testInputs = inputs.slice(i, i + parametersCount);
    const testCaseStats = executeTestCase(
      userFunction,
      testInputs,
      expectedOutputs[i / parametersCount]
    );

    stats.testCaseResults.push(testCaseStats);
    stats.totalRunTime += testCaseStats.runTime;
    stats.totalMemoryUsed += testCaseStats.memoryUsed;
    stats.allTestsPassed &&= testCaseStats.passed;
  }

  return stats;
};

module.exports = { createUserFunction, runTests };
