#include "TestRunner.h"
#include "Logger.h"
#include <chrono>
#include <dlfcn.h>
#include <any>
#include <vector>
#include <stdexcept>

class DynamicLibrary {
public:
    DynamicLibrary(const std::string& path) : handle(dlopen(path.c_str(), RTLD_LAZY)) {
        if (!handle) {
            throw std::runtime_error("Cannot load dynamic library: " + std::string(dlerror()));
        }
    }

    void* getSymbol(const std::string& name) {
        return dlsym(handle, name.c_str());
    }

    ~DynamicLibrary() {
        if (handle) dlclose(handle);
    }

private:
    void* handle;
};

template<typename T>
T convertToType(const json& value) {
    if constexpr (std::is_same_v<T, int>) {
        return value.is_number() ? value.get<int>() : std::stoi(value.get<std::string>());
    } else if constexpr (std::is_same_v<T, bool>) {
        return value.get<bool>();
    } else if constexpr (std::is_same_v<T, std::string>) {
        return value.get<std::string>();
    } else if constexpr (std::is_same_v<T, std::vector<int>>) {
        return value.get<std::vector<int>>();
    } else if constexpr (std::is_same_v<T, std::vector<std::string>>) {
        return value.get<std::vector<std::string>>();
    } else {
        throw std::runtime_error("Unsupported type");
    }
}

void TestRunner::runTests(const json& dataInput, const json& correctAnswer, 
                          const std::string& functionName, int parametersCount) {
    DynamicLibrary lib("./temp_solution.so");
    std::string wrapperName = functionName + "_wrapper";
    void* sym = lib.getSymbol(wrapperName.c_str());
    if (!sym) {
        throw std::runtime_error("Cannot find function: " + wrapperName);
    }

    std::vector<json> allResults;

    for (size_t i = 0; i < dataInput.size(); i += parametersCount) {
        auto start = std::chrono::steady_clock::now();
        
        json result;
        if (parametersCount == 2) {
            result["input"] = json::array({dataInput[i], dataInput[i+1]});
        } else {
            result["input"] = dataInput[i];
        }

        // 處理期望值
        json expected = correctAnswer[i / parametersCount];
        if (expected.is_string()) {
            std::string expectedStr = expected.get<std::string>();
            if (expectedStr == "true") {
                result["expected"] = true;
            } else if (expectedStr == "false") {
                result["expected"] = false;
            } else {
                result["expected"] = expected;
            }
        } else {
            result["expected"] = expected;
        }

        std::any output;
        if (parametersCount == 1) {
            if (functionName == "isPalindrome") {
                auto func = reinterpret_cast<bool (*)(int)>(sym);
                int arg = convertToType<int>(dataInput[i]);
                output = func(arg);
            } else {
                auto func = reinterpret_cast<std::any (*)(const char*)>(sym);
                std::string arg = convertToType<std::string>(dataInput[i]);
                output = func(arg.c_str());
            }
        } else if (parametersCount == 2) {
            auto func = reinterpret_cast<std::vector<int> (*)(const int*, int, int)>(sym);
            std::vector<int> vec = convertToType<std::vector<int>>(dataInput[i]);
            int target = convertToType<int>(dataInput[i+1]);
            output = func(vec.data(), vec.size(), target);
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

        // 比較結果
        bool passed;
        if (result["expected"].is_boolean() && result["output"].is_boolean()) {
            passed = result["output"].get<bool>() == result["expected"].get<bool>();
        } else {
            passed = result["output"] == result["expected"];
        }

        allResults.push_back(result);
        Logger::log("Test case " + std::to_string(i / parametersCount + 1) + ":", result, passed);
    }

    Logger::logSummary(allResults);
}