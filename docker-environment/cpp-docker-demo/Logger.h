#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class Logger {
public:
    static void log(const std::string& testCase, const json& result);
    static void logSummary(double totalRuntime, long totalMemory, bool isInfiniteLoop);
};

#endif // LOGGER_H