#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <vector>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class Logger {
public:
    static void log(const std::string& testCase, const json& result, bool passed);
    static void logSummary(const std::vector<json>& allResults);
private:
    static double totalRuntime;
    static long totalMemory;
    static bool allTestsPassed;
};

#endif // LOGGER_H