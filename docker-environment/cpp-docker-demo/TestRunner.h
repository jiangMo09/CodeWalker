#ifndef TEST_RUNNER_H
#define TEST_RUNNER_H

#include <nlohmann/json.hpp>
#include <string>

using json = nlohmann::json;

class TestRunner {
public:
    void runTests(const json& dataInput, const json& correctAnswer, 
                  const std::string& functionName, int parametersCount);
};

#endif // TEST_RUNNER_H