import json

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
            "undefined" if stats["result"] is None else json.dumps(stats["result"])
        ),
        "expected": json.dumps(expected_output),
        "run_time": f"{stats['run_time']:.3f} ms",
        "memory": f"{stats['memory_used'] / 1024:.3f} KB",
    }

    test_cases.append(test_case_result)


def log_summary(stats):
    summary = {
        "run_result": test_cases,
        "total_correct": total_correct,
        "total_testcases": total_testcases,
        "total_run_time": f"{stats['total_run_time']:.3f} ms",
        "total_run_memory": f"{stats['total_memory_used'] / 1024:.3f} MB",
        "all_passed": stats["all_tests_passed"],
    }

    print(json.dumps(summary, default=lambda x: "undefined" if x is None else x))
