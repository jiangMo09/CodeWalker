const { performance } = require("perf_hooks");

const greetFunc = new Function("return " + process.env.GREET_FUNCTION)();

const startTime = performance.now();
const startMemory = process.memoryUsage().heapUsed;

const result = greetFunc();

const endTime = performance.now();
const endMemory = process.memoryUsage().heapUsed;

const runTime = endTime - startTime;
const memoryUsed = endMemory - startMemory;

console.log(`Function result: ${result}`);
console.log(`Run time: ${runTime.toFixed(3)} ms`);
console.log(`Memory used: ${memoryUsed / 1024} KB`);
