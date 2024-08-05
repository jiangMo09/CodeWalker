#ifndef TEST_RUNNER_H
#define TEST_RUNNER_H

#include <nlohmann/json.hpp>

using json = nlohmann::json;

class TestRunner {
public:
    void runTests(const json& dataInput, const json& correctAnswer, 
                  void* functionPtr, int parametersCount, const std::string& functionName);
};

#endif // TEST_RUNNER_H