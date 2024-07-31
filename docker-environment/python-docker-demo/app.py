import os
import time
import psutil
import ast

def safe_eval(expr):
    try:
        # 解析表达式
        parsed = ast.parse(expr, mode='eval')
        
        # 检查是否是 lambda 函数
        if isinstance(parsed.body, ast.Lambda):
            # 编译并返回函数
            return eval(compile(parsed, '<string>', 'eval'))
        else:
            raise ValueError("Expression must be a lambda function")
    except SyntaxError:
        raise ValueError("Invalid syntax")

# 从环境变量中读取函数定义
greet_function_code = os.getenv("GREET_FUNCTION", 'lambda: "Default Hello"')

# 使用安全的方法评估函数
try:
    greet_func = safe_eval(greet_function_code)
except ValueError as e:
    print(f"Error: {e}")
    greet_func = lambda: "Default Hello"

# 测量执行时间和内存使用
start_time = time.perf_counter()
start_memory = psutil.Process().memory_info().rss

result = greet_func()

end_time = time.perf_counter()
end_memory = psutil.Process().memory_info().rss

run_time = (end_time - start_time) * 1000  # 转换为毫秒
memory_used = end_memory - start_memory

print(f"Function result: {result}")
print(f"Run time: {run_time:.3f} ms")
print(f"Memory used: {memory_used / 1024:.3f} KB")