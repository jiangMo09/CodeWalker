#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <dlfcn.h>
#include <nlohmann/json.hpp>
#include <filesystem>
#include <stdexcept>
#include <algorithm>
#include "TestRunner.h"
#include "Logger.h"

using json = nlohmann::json;
namespace fs = std::filesystem;

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

json parseInputString(const std::string& input) {
    std::istringstream iss(input);
    std::string line;
    json result = json::array();
    while (std::getline(iss, line)) {
        if (!line.empty()) {
            try {
                if (line.front() == '[' && line.back() == ']') {
                    // 這是一個數組
                    result.push_back(json::parse(line));
                } else {
                    // 這可能是一個數字或者字符串
                    try {
                        result.push_back(std::stoi(line));
                    } catch (const std::invalid_argument&) {
                        result.push_back(line);
                    }
                }
            } catch (const json::exception& e) {
                std::cerr << "JSON parsing error: " << e.what() << std::endl;
                throw;
            }
        }
    }
    return result;
}

bool compile(const std::string& filename, const std::string& functionName, int parametersCount) {
    std::ofstream wrapper(filename + ".wrapper.cpp");
    wrapper << "#include <vector>\n"
            << "#include <string>\n"
            << "#include <unordered_map>\n"
            << "#include <algorithm>\n"
            << "#include <stack>\n"
            << "using namespace std;\n\n"
            << std::ifstream(filename).rdbuf() << "\n"
            << "extern \"C\" {\n";

    if (parametersCount == 1) {
        wrapper << "    auto " << functionName << "_wrapper(";
        if (functionName == "isPalindrome") {
            wrapper << "int x) {\n";
        } else {
            wrapper << "const char* s) {\n        string str(s);\n";
        }
        wrapper << "        Solution sol;\n"
                << "        return sol." << functionName << "(";
        if (functionName == "isPalindrome") {
            wrapper << "x);\n    }\n";
        } else {
            wrapper << "str);\n    }\n";
        }
    } else if (parametersCount == 2) {
        wrapper << "    auto " << functionName << "_wrapper(const int* nums, int numsSize, int target) {\n"
                << "        vector<int> vec(nums, nums + numsSize);\n"
                << "        Solution sol;\n"
                << "        return sol." << functionName << "(vec, target);\n"
                << "    }\n";
    }
    wrapper << "}\n";
    wrapper.close();

    std::string compileCmd = "g++ -std=c++17 -shared -fPIC -o temp_solution.so " + filename + ".wrapper.cpp";
    return system(compileCmd.c_str()) == 0;
}

int main() {
    std::string input = std::getenv("DATA_INPUT");
    json data = json::parse(input);

    std::string typedCode = data["typed_code"];
    std::string functionName = data["function_name"];
    json dataInput = parseInputString(data["data_input"]);
    json correctAnswer = parseInputString(data["correct_answer"]);
    int parametersCount = data["parameters_count"];

    fs::path tempFile = fs::temp_directory_path() / "temp_solution.cpp";
    std::ofstream file(tempFile);
    file << typedCode;
    file.close();

    if (!compile(tempFile.string(), functionName, parametersCount)) {
        std::cerr << "Compilation error" << std::endl;
        return 1;
    }

    try {
        TestRunner runner;
        runner.runTests(dataInput, correctAnswer, functionName, parametersCount);
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    fs::remove(tempFile);
    fs::remove("temp_solution.so");

    return 0;
}