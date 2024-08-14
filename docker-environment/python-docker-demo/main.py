import os
import json
import sys
from test_runner import create_user_function, run_tests
from logger import log_test_case, log_summary, log_error


def run_code(data):
    try:
        typed_code = data.get("typed_code", "")
        function_name = data.get("function_name", "")
        data_input = data.get("data_input", "")
        correct_answer = data.get("correct_answer", "")
        parameters_count = data.get("parameters_count", 1)

        user_function = create_user_function(typed_code, function_name)

        input_lines = data_input.split("\n")
        inputs = []
        for i in range(0, len(input_lines), parameters_count):
            test_case_inputs = [
                json.loads(input_lines[i + j]) for j in range(parameters_count)
            ]
            inputs.append(test_case_inputs)
        expected_outputs = [json.loads(x) for x in correct_answer.split("\n")]

        stats = run_tests(user_function, inputs, expected_outputs)

        for i, test_case_stats in enumerate(stats["test_case_results"]):
            log_test_case(i + 1, test_case_stats, inputs[i], expected_outputs[i])

        log_summary(stats)
    except Exception as e:
        log_error(str(e))


if __name__ == "__main__":
    try:
        data_input = os.environ.get("DATA_INPUT")
        if not data_input:
            raise ValueError("DATA_INPUT environment variable is not set")

        data = json.loads(data_input)
        run_code(data)
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in DATA_INPUT: {str(e)}")
    except Exception as e:
        log_error(str(e))
