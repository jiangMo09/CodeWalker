#include <iostream>
#include <cstdlib>
#include <lua.hpp>
#include <chrono>

int main() {
    // 從環境變數中讀取函數定義
    const char* greetFunctionCode = std::getenv("GREET_FUNCTION");
    if (!greetFunctionCode) {
        std::cerr << "GREET_FUNCTION environment variable not set." << std::endl;
        return 1;
    }

    // 創建一個Lua狀態機
    lua_State* L = luaL_newstate();
    luaL_openlibs(L);

    // 評估函數定義
    std::string script = std::string("greetFunc = ") + greetFunctionCode;
    
    // 測量執行時間和記憶體使用
    auto start = std::chrono::high_resolution_clock::now();
    size_t startMem = lua_gc(L, LUA_GCCOUNT, 0) * 1024 + lua_gc(L, LUA_GCCOUNTB, 0);

    if (luaL_dostring(L, script.c_str())) {
        std::cerr << "Error executing script: " << lua_tostring(L, -1) << std::endl;
        lua_close(L);
        return 1;
    }

    // 調用函數
    lua_getglobal(L, "greetFunc");
    if (lua_pcall(L, 0, 1, 0)) {
        std::cerr << "Error calling function: " << lua_tostring(L, -1) << std::endl;
        lua_close(L);
        return 1;
    }

    auto end = std::chrono::high_resolution_clock::now();
    size_t endMem = lua_gc(L, LUA_GCCOUNT, 0) * 1024 + lua_gc(L, LUA_GCCOUNTB, 0);

    // 獲取結果
    const char* result = lua_tostring(L, -1);

    // 計算執行時間和記憶體使用
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    double runTime = duration.count() / 1000.0; // 轉換為毫秒
    long memoryUsed = endMem - startMem;

    // 輸出結果
    std::cout << "Function result: " << result << std::endl;
    std::printf("Run time: %.3f ms\n", runTime);
    std::printf("Memory used: %.3f KB\n", memoryUsed / 1024.0);

    // 關閉Lua狀態機
    lua_close(L);
    return 0;
}