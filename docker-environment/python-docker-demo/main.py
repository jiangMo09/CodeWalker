import json
import os
from test_runner import create_user_function, run_tests
from logger import log_test_case, log_summary


def run_code(data):
    data_dict = json.loads(data)
    typed_code = data_dict["typed_code"]
    data_input = data_dict["data_input"]
    correct_answer = data_dict["correct_answer"]
    function_name = data_dict["function_name"]
    parameters_count = data_dict["parameters_count"]

    user_function = create_user_function(typed_code, function_name)
    inputs = [json.loads(line) for line in data_input.split("\n")]
    expected_outputs = [json.loads(line) for line in correct_answer.split("\n")]

    stats = run_tests(user_function, inputs, expected_outputs, parameters_count)

    for index, test_case_stats in enumerate(stats["test_case_results"]):
        log_test_case(
            index + 1,
            test_case_stats,
            inputs[index * parameters_count : (index + 1) * parameters_count],
            expected_outputs[index],
        )

    log_summary(stats)


if __name__ == "__main__":
    data_input = os.environ.get("DATA_INPUT")
    try:
        run_code(data_input)
    except Exception as error:
        print(f"Error: {str(error)}")
