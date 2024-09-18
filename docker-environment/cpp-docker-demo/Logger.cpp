#include "Logger.h"
#include <iostream>
#include <iomanip>
#include <sstream>

double Logger::totalRuntime = 0.0;
double Logger::totalMemory = 0.0;
bool Logger::allTestsPassed = true;
int Logger::totalCorrect = 0;
int Logger::totalTestcases = 0;
json Logger::summaryJson;

void Logger::logTestCase(int index, const json& result, bool passed) {
    totalTestcases++;
    if (passed) totalCorrect++;

    json testCaseResult;
    testCaseResult["test_case"] = index;
    testCaseResult["passed"] = passed;
    testCaseResult["inputs"] = result["input"];
    testCaseResult["output"] = result["output"];
    testCaseResult["expected"] = result["expected"];

    std::stringstream ss;
    ss << std::fixed << std::setprecision(3) << result["runtime"].get<double>() / 1000.0;
    testCaseResult["run_time"] = ss.str() + " ms";

    ss.str("");  // 清空 stringstream
    ss << std::fixed << std::setprecision(3) << result["memory"].get<double>();
    testCaseResult["memory"] = ss.str() + " KB";

    summaryJson["run_result"].push_back(testCaseResult);

    totalRuntime += result["runtime"].get<double>() / 1000.0;
    totalMemory += result["memory"].get<double>();

    if (!passed) allTestsPassed = false;
}

void Logger::logSummary(const std::vector<json>& allResults) {
    summaryJson["total_correct"] = totalCorrect;
    summaryJson["total_testcases"] = totalTestcases;
    
    std::stringstream ss;
    ss << std::fixed << std::setprecision(3) << totalRuntime;
    summaryJson["total_run_time"] = ss.str() + " ms";
    
    ss.str("");  // 清空 stringstream
    ss << std::fixed << std::setprecision(3) << totalMemory / 1024.0;
    summaryJson["total_run_memory"] = ss.str() + " MB";
    
    summaryJson["all_passed"] = allTestsPassed;

    std::cout << summaryJson.dump() << std::endl;
}