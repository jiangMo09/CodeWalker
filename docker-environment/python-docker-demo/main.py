import json
import os
from test_runner import create_user_function, run_tests
from logger import log_test_case, log_summary
from typing import List, Any


def run_code(data):
    data_dict = json.loads(data)
    typed_code = data_dict['typed_code']
    data_input = data_dict['data_input']
    correct_answer = data_dict['correct_answer']
    function_name = data_dict['function_name']
    parameters_count = data_dict['parameters_count']

    solution_instance = create_user_function(typed_code, 'Solution', List, Any)()
    user_function = getattr(solution_instance, function_name)

    inputs = parse_input(data_input)
    expected_outputs = parse_output(correct_answer)

    stats = run_tests(user_function, inputs, expected_outputs, parameters_count)

    for index, test_case_stats in enumerate(stats['test_case_results']):
        log_test_case(
            index + 1,
            test_case_stats,
            inputs[index * parameters_count : (index + 1) * parameters_count],
            expected_outputs[index]
        )

    log_summary(stats)

def parse_input(input_str):
    return [try_parse_json(item) for item in input_str.split("\n")]


def parse_output(output_str):
    return [parse_output_item(item) for item in output_str.split("\n")]


def parse_output_item(item):
    if item == "true":
        return True
    elif item == "false":
        return False
    return try_parse_json(item)


def try_parse_json(item):
    try:
        return json.loads(item)
    except json.JSONDecodeError:
        return item


if __name__ == "__main__":
    data_input = os.environ.get("DATA_INPUT")
    try:
        run_code(data_input)
    except Exception as error:
        print(f"Error: {str(error)}")
