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
                    // 嘗試解析為數字，如果失敗則作為字符串處理
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

bool compile(const std::string& filename) {
    // 創建一個臨時文件來包裝用戶的代碼
    std::ofstream wrapper(filename + ".wrapper.cpp");
    wrapper << "#include <vector>\n"
            << "#include <unordered_map>\n"
            << "#include <algorithm>\n"
            << "using namespace std;\n\n"
            << std::ifstream(filename).rdbuf();
    wrapper.close();

    std::string compileCmd = "g++ -std=c++17 -shared -fPIC -o temp_solution.so " + filename + ".wrapper.cpp";
    return system(compileCmd.c_str()) == 0;
}

void runTests(const std::string& functionName, const json& dataInput, 
              const json& correctAnswer, int parametersCount) {
    DynamicLibrary lib("./temp_solution.so");
    void* sym = lib.getSymbol(functionName);
    if (!sym) {
        throw std::runtime_error("Cannot find function: " + functionName);
    }

    TestRunner runner;
    runner.runTests(dataInput, correctAnswer, sym, parametersCount, functionName);
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
    file << "extern \"C\" {\n"
         << typedCode
         << "\n}\n"
         << "extern \"C\" std::vector<int> twoSum(std::vector<int>& nums, int target) {\n"
         << "    Solution solution;\n"
         << "    return solution.twoSum(nums, target);\n"
         << "}\n";
    file.close();

    if (!compile(tempFile.string())) {
        std::cerr << "Compilation error" << std::endl;
        return 1;
    }

    try {
        runTests(functionName, dataInput, correctAnswer, parametersCount);
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    fs::remove(tempFile);
    fs::remove("temp_solution.so");

    return 0;
}