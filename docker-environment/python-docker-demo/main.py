import json
import os
from test_runner import create_user_function, run_tests
from logger import log_test_case, log_summary


def parse_input(input_str, question_id):
    if question_id in ["3", "5"]:
        return input_str.split("\n")
    return [json.loads(line) for line in input_str.split("\n")]


def parse_output(output_str, question_id):
    if question_id == "3":
        return [int(line) for line in output_str.split("\n")]
    elif question_id == "5":
        return [line.lower() == "true" for line in output_str.split("\n")]
    return [json.loads(line) for line in output_str.split("\n")]


def run_code(data):
    data_dict = json.loads(data)
    typed_code = data_dict["typed_code"]
    data_input = data_dict["data_input"]
    correct_answer = data_dict["correct_answer"]
    function_name = data_dict["function_name"]
    parameters_count = data_dict["parameters_count"]
    question_id = data_dict["question_id"]

    user_function = create_user_function(typed_code, function_name)
    inputs = parse_input(data_input, question_id)
    expected_outputs = parse_output(correct_answer, question_id)

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
        print(json.dumps({"error": str(error)}))
