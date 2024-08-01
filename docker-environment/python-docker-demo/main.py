import os
import json
from test_runner import create_user_function, run_tests
from logger import log_test_case, log_summary

def run_code(data):
    typed_code = data.get("typed_code", "")
    function_name = data.get("function_name", "")
    data_input = data.get("data_input", "")
    correct_answer = data.get("correct_answer", "")
    parameters_count = data.get("parameters_count", 1)

    try:
        user_function = create_user_function(typed_code, function_name)
        inputs = [json.loads(x) for x in data_input.split("\n")]
        expected_outputs = [json.loads(x) for x in correct_answer.split("\n")]

        stats = run_tests(user_function, inputs, expected_outputs, parameters_count)

        for i, test_case_stats in enumerate(stats["test_case_results"]):
            log_test_case(i + 1, test_case_stats)

        log_summary(stats)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    data_input = os.environ.get("DATA_INPUT")
    try:
        data = json.loads(data_input)
        run_code(data)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in DATA_INPUT")
    except Exception as e:
        print(f"Error: {str(e)}")