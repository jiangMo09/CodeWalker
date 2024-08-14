import json
import sys

test_cases = []
total_correct = 0
total_testcases = 0


def log_test_case(index, stats, inputs, expected_output):
    global total_correct, total_testcases
    total_testcases += 1
    if stats["passed"]:
        total_correct += 1

    test_case_result = {
        "test_case": index,
        "passed": stats["passed"],
        "inputs": json.dumps(inputs),
        "output": (
            json.dumps(stats["result"]) if stats["result"] is not None else "undefined"
        ),
        "expected": json.dumps(expected_output),
        "run_time": f"{stats['run_time']:.3f} ms",
        "memory": f"{stats['memory_used'] / 1024:.3f} KB",
    }

    test_cases.append(test_case_result)


def log_summary(stats):
    summary = {
        "container_run_success": True,
        "run_result": test_cases,
        "total_correct": total_correct,
        "total_testcases": total_testcases,
        "total_run_time": f"{stats['total_run_time']:.3f} ms",
        "total_run_memory": f"{stats['total_memory_used'] / (1024 * 1024):.3f} MB",
        "all_passed": stats["all_tests_passed"],
        "is_infinite_loop": False,
    }

    json.dump(summary, sys.stdout)
    sys.stdout.flush()


def log_error(error_message):
    error_summary = {"container_run_success": False, "error": error_message}
    json.dump(error_summary, sys.stdout)
    sys.stdout.flush()
