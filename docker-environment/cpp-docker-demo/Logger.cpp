#include "Logger.h"
#include <iostream>
#include <iomanip>

void Logger::log(const std::string& testCase, const json& result) {
    std::cout << testCase << std::endl;
    std::cout << "Inputs: " << result["input"] << std::endl;
    std::cout << "Output: " << result["output"] << std::endl;
    std::cout << "Expected: " << result["expected"] << std::endl;
    std::cout << "Run time: " << std::fixed << std::setprecision(2) 
              << result["runtime"].get<double>() / 1000.0 << " ms" << std::endl;
    std::cout << "Memory used: " << "XXX KB" << std::endl;  // 這裡需要實際測量內存使用
    std::cout << std::endl;
}

void Logger::logSummary(double totalRuntime, long totalMemory, bool isInfiniteLoop) {
    std::cout << "Total run time: " << std::fixed << std::setprecision(2) 
              << totalRuntime << " ms" << std::endl;
    std::cout << "Total memory used: " << totalMemory << " KB" << std::endl;
    std::cout << "是否為無窮迴圈: " << (isInfiniteLoop ? "是" : "否") << std::endl;
}