import time
import psutil
import json
from typing import List, Any

def execute_test_case(user_function, inputs, expected_output):
    start_time = time.time() * 1000
    start_memory = psutil.Process().memory_info().rss

    result = None
    error = None
    try:
        result = user_function(*inputs)
    except Exception as err:
        error = str(err)

    end_time = time.time() * 1000
    end_memory = psutil.Process().memory_info().rss

    passed = compare_outputs(result, expected_output)

    return {
        "run_time": end_time - start_time,
        "memory_used": end_memory - start_memory,
        "passed": passed,
        "result": result,
        "error": error,
    }


def compare_outputs(result, expected):
    if isinstance(result, list) and isinstance(expected, list):
        return json.dumps(result) == json.dumps(expected)
    if isinstance(result, bool) and isinstance(expected, bool):
        return result == expected
    return result == expected


def create_user_function(code, function_name, List, Any):
    namespace = {"List": List, "Any": Any}
    exec(code, namespace)
    user_function = namespace.get(function_name)
    if not callable(user_function):
        raise ValueError(f"Function '{function_name}' not found")
    return user_function


def run_tests(user_function, inputs, expected_outputs, parameters_count):
    stats = {
        "all_tests_passed": True,
        "total_run_time": 0,
        "total_memory_used": 0,
        "test_case_results": [],
    }

    for i in range(0, len(inputs), parameters_count):
        test_inputs = inputs[i : i + parameters_count]
        test_case_stats = execute_test_case(
            user_function, test_inputs, expected_outputs[i // parameters_count]
        )

        stats["test_case_results"].append(test_case_stats)
        stats["total_run_time"] += test_case_stats["run_time"]
        stats["total_memory_used"] += test_case_stats["memory_used"]
        stats["all_tests_passed"] &= test_case_stats["passed"]

    return stats
