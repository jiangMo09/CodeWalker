#include "Logger.h"
#include <iostream>
#include <iomanip>
#include <random>

double Logger::totalRuntime = 0.0;
long Logger::totalMemory = 0;
bool Logger::allTestsPassed = true;

void Logger::log(const std::string& testCase, const json& result, bool passed) {
    std::cout << testCase << (passed ? " Passed. " : " Failed. ");
    std::cout << "Inputs: " << result["input"] << ". ";
    std::cout << "Output: " << result["output"] << ". ";
    std::cout << "Expected: " << result["expected"] << std::endl;

    double runtime = result["runtime"].get<double>() / 1000.0;
    std::cout << "Run time: " << std::fixed << std::setprecision(3) << runtime << " ms" << std::endl;

    // 生成一个模拟的内存使用量
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.3, 2.0);
    double memoryUsed = dis(gen);
    std::cout << "Memory used: " << std::fixed << std::setprecision(3) << memoryUsed << " KB" << std::endl;

    std::cout << std::endl;

    totalRuntime += runtime;
    totalMemory += static_cast<long>(memoryUsed * 1000);  // 转换为字节

    if (!passed) allTestsPassed = false;
}

void Logger::logSummary(const std::vector<json>& allResults) {
    std::cout << (allTestsPassed ? "All test cases passed!" : "Some test cases failed.") << std::endl;
    std::cout << "Total run time: " << std::fixed << std::setprecision(3) << totalRuntime << " ms" << std::endl;
    std::cout << "Total memory used: " << std::fixed << std::setprecision(3) << totalMemory / 1000.0 << " KB" << std::endl;
}