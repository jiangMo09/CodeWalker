const logTestCase = (index, stats, inputs, expectedOutput) => {
  console.log(
    `Test case ${index}: ${
      stats.passed ? "Passed" : "Failed"
    }. Inputs: ${JSON.stringify(inputs)}. Output: ${JSON.stringify(
      stats.result
    )}. Expected: ${JSON.stringify(expectedOutput)}`
  );
  console.log(`Run time: ${stats.runTime.toFixed(3)} ms`);
  console.log(`Memory used: ${(stats.memoryUsed / 1024).toFixed(3)} KB`);

  if (stats.error) {
    console.log(`Error: ${stats.error}`);
  }
};

const logSummary = (stats) => {
  console.log(
    stats.allTestsPassed ? "All test cases passed!" : "Some test cases failed."
  );
  console.log(`Total run time: ${stats.totalRunTime.toFixed(3)} ms`);
  console.log(
    `Total memory used: ${(stats.totalMemoryUsed / 1024).toFixed(3)} KB`
  );
};

module.exports = { logTestCase, logSummary };
