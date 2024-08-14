import time
import psutil
import ast
from typing import List, Dict, Tuple, Any


def safe_eval(expr):
    try:
        parsed = ast.parse(expr, mode="eval")
        if isinstance(parsed.body, ast.Lambda):
            return eval(compile(parsed, "<string>", "eval"))
        else:
            raise ValueError("Expression must be a lambda function")
    except SyntaxError:
        raise ValueError("Invalid syntax")


def create_user_function(code, function_name):
    setup_code = """
from typing import List, Dict, Tuple, Any
"""
    full_code = setup_code + "\n" + code

    local_vars = {}
    exec(full_code, globals(), local_vars)
    if "Solution" in local_vars:
        solution = local_vars["Solution"]()
        if hasattr(solution, function_name):
            return getattr(solution, function_name)
    elif function_name in local_vars:
        return local_vars[function_name]
    raise ValueError(f"Function '{function_name}' not found")


def execute_test_case(user_function, inputs):
    start_time = time.perf_counter()
    start_memory = psutil.Process().memory_info().rss

    try:
        result = user_function(*inputs)
    except Exception as e:
        result = str(e)

    end_time = time.perf_counter()
    end_memory = psutil.Process().memory_info().rss

    run_time = (end_time - start_time) * 1000
    memory_used = end_memory - start_memory

    return {"result": result, "run_time": run_time, "memory_used": memory_used}


def run_tests(user_function, inputs, expected_outputs):
    stats = {
        "all_tests_passed": True,
        "total_run_time": 0,
        "total_memory_used": 0,
        "test_case_results": [],
    }

    for test_inputs, expected_output in zip(inputs, expected_outputs):
        test_case_stats = execute_test_case(user_function, test_inputs)

        passed = test_case_stats["result"] == expected_output
        stats["all_tests_passed"] &= passed
        stats["total_run_time"] += test_case_stats["run_time"]
        stats["total_memory_used"] += test_case_stats["memory_used"]

        stats["test_case_results"].append(
            {
                "passed": passed,
                "inputs": test_inputs,
                "expected": expected_output,
                "result": test_case_stats["result"],
                "run_time": test_case_stats["run_time"],
                "memory_used": test_case_stats["memory_used"],
            }
        )

    return stats
