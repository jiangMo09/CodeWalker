#include "TestRunner.h"
#include "Logger.h"
#include <chrono>
#include <dlfcn.h>
#include <any>
#include <functional>
#include <type_traits>
#include <vector>
#include <stdexcept>

template<typename T>
T convertToType(const json& value) {
    if constexpr (std::is_same_v<T, int>) {
        return value.is_number() ? value.get<int>() : std::stoi(value.get<std::string>());
    } else if constexpr (std::is_same_v<T, long>) {
        return value.is_number() ? value.get<long>() : std::stol(value.get<std::string>());
    } else if constexpr (std::is_same_v<T, double>) {
        return value.is_number() ? value.get<double>() : std::stod(value.get<std::string>());
    } else if constexpr (std::is_same_v<T, float>) {
        return value.is_number() ? value.get<float>() : std::stof(value.get<std::string>());
    } else if constexpr (std::is_same_v<T, bool>) {
        return value.get<bool>();
    } else if constexpr (std::is_same_v<T, char>) {
        return value.get<std::string>()[0];
    } else if constexpr (std::is_same_v<T, std::string>) {
        return value.get<std::string>();
    } else if constexpr (std::is_same_v<T, std::vector<int>>) {
        std::vector<int> result;
        for (const auto& elem : value) {
            result.push_back(convertToType<int>(elem));
        }
        return result;
    } else {
        throw std::runtime_error("Unsupported type");
    }
}

void TestRunner::runTests(const json& dataInput, const json& correctAnswer, 
                          void* functionPtr, int parametersCount, const std::string& functionName) {
    for (size_t i = 0; i < dataInput.size(); i += parametersCount) {
        auto start = std::chrono::steady_clock::now();
        
        json result;
        json input = json::array();
        for (int j = 0; j < parametersCount; ++j) {
            input.push_back(dataInput[i + j]);
        }
        result["input"] = input;
        result["expected"] = correctAnswer[i / parametersCount];

        std::any output;
        if (parametersCount == 2) {
            std::vector<int> (*func)(std::vector<int>&, int) = reinterpret_cast<std::vector<int> (*)(std::vector<int>&, int)>(functionPtr);
            std::vector<int> vec = convertToType<std::vector<int>>(input[0]);
            int arg = convertToType<int>(input[1]);
            output = func(vec, arg);
        } else {
            throw std::runtime_error("Unsupported number of parameters: " + std::to_string(parametersCount));
        }

        if (output.type() == typeid(std::vector<int>)) {
            result["output"] = std::any_cast<std::vector<int>>(output);
        } else if (output.type() == typeid(int)) {
            result["output"] = std::any_cast<int>(output);
        } else if (output.type() == typeid(bool)) {
            result["output"] = std::any_cast<bool>(output);
        } else if (output.type() == typeid(std::string)) {
            result["output"] = std::any_cast<std::string>(output);
        } else {
            result["output"] = nullptr;
        }

        auto end = std::chrono::steady_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

        result["runtime"] = duration.count();

        Logger::log("Test case " + std::to_string(i / parametersCount + 1) + ":", result);
    }
}