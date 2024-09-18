#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <vector>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class Logger {
public:
    static void logTestCase(int index, const json& result, bool passed);
    static void logSummary(const std::vector<json>& allResults);
    static int totalCorrect;
    static int totalTestcases;
private:
    static double totalRuntime;
    static double totalMemory;
    static bool allTestsPassed;
    static json summaryJson;
};

#endif