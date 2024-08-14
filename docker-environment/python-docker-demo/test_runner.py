import time
import json
import tracemalloc
from typing import List, Dict, Any, Callable


def execute_test_case(
    user_function: Callable, inputs: List[Any], expected_output: Any
) -> Dict[str, Any]:
    tracemalloc.start()
    start_time = time.perf_counter_ns()
    start_memory = tracemalloc.get_traced_memory()[0]

    result = None
    error = None
    try:
        result = user_function(*inputs)
    except Exception as err:
        error = str(err)

    end_time = time.perf_counter_ns()
    end_memory = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()

    return {
        "run_time": (end_time - start_time) / 1e6,  # Convert to milliseconds
        "memory_used": end_memory - start_memory,
        "passed": json.dumps(result) == json.dumps(expected_output),
        "result": result,
        "error": error,
    }


def create_user_function(code: str, function_name: str) -> Callable:
    if "class Solution:" not in code:
        code = f"class Solution:\n{code}"

    code = "from typing import List, Dict, Any\n" + code

    namespace = {}
    exec(code, namespace)

    solution_class = namespace["Solution"]
    solution_instance = solution_class()

    user_function = getattr(solution_instance, function_name, None)
    if not callable(user_function):
        raise ValueError(f"Function '{function_name}' not found in Solution class")

    return user_function


def run_tests(
    user_function: Callable,
    inputs: List[Any],
    expected_outputs: List[Any],
    parameters_count: int,
) -> Dict[str, Any]:
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
