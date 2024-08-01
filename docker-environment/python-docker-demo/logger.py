def log_test_case(index, stats):
    print(
        f"Test case {index}: {'Passed' if stats['passed'] else 'Failed'}. "
        f"Inputs: {stats['inputs']}. "
        f"Output: {stats['result']}. "
        f"Expected: {stats['expected']}"
    )
    print(f"Run time: {stats['run_time']:.3f} ms")
    print(f"Memory used: {stats['memory_used'] / 1024:.3f} KB")


def log_summary(stats):
    print(
        "All test cases passed!"
        if stats["all_tests_passed"]
        else "Some test cases failed."
    )
    print(f"Total run time: {stats['total_run_time']:.3f} ms")
    print(f"Total memory used: {stats['total_memory_used'] / 1024:.3f} KB")
