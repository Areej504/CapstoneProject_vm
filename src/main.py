import json
import os

from src import dispatcher, run_td, input_parser, output_parser


def log_step(step_name):
    """Formats and prints step headers."""
    print(f"\n{'*' * 20} {step_name} {'*' * 20}\n")


def reset_failure_log():
    """Clears the failure_log.json file at the beginning of a new test suite."""
    failure_log_path = os.path.join(os.path.dirname(__file__), "../outputs/failure_log.json")

    try:
        with open(failure_log_path, 'w') as failure_file:
            json.dump({"iterations": []}, failure_file, indent=4)
        print("log reset for a new test suite.")
    except Exception as e:
        print(f"Error resetting failure log: {e}")


def log_failures(analysis_filename, iteration):
    """Logs failed test cases into failure_log.json based on the analysis results."""
    try:
        # Read and print analysis data
        with open(analysis_filename, 'r') as analysis_file:
            analysis_data = json.load(analysis_file)
        print(json.dumps(analysis_data, indent=4))

        # Define failure log file path
        failure_log_path = os.path.join(os.path.dirname(__file__), "../outputs/failure_log.json")

        # Initialize or load failure log
        try:
            with open(failure_log_path, 'r') as failure_file:
                failure_log = json.load(failure_file)
        except (FileNotFoundError, json.JSONDecodeError):
            failure_log = {"iterations": []}

        # Initialize failure data for the current iteration
        failure_data = {
            "iteration": iteration + 1,
            "failed_cases": []
        }

        # Process test cases and check for failures
        for test_case, result in analysis_data.items():
            if not result or not result.get("pass", False):  # Ensure result exists and check failure
                failure_data["failed_cases"].append({"test_case": test_case, "result": result})

        # If failures exist, update the log
        if failure_data["failed_cases"]:
            failure_log["iterations"].append(failure_data)
            with open(failure_log_path, 'w') as failure_file:
                json.dump(failure_log, failure_file, indent=4)

            print(f"Failures logged for iteration {iteration + 1}.")
            return True
        else:
            print(f"No failures detected for iteration {iteration + 1}.")
            return False

    except FileNotFoundError:
        print(f"Error: Analysis file '{analysis_filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{analysis_filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False


def run_test_iteration(tc_file_path, iteration):
    """Runs a single test iteration with feedback loop."""

    log_step(f"TESTING ITERATION {iteration + 1}")

    # Step 2: Inject inputs into test_data.hpp
    log_step("PARSING INPUTS TO TEST DRIVER")
    input_parser.main(tc_file_path)

    # Step 3: Run the test driver to execute DEVS model
    log_step("RUNNING TEST DRIVER")
    run_td.build_and_run_test_driver()

    # Step 4: Parse log file results into a JSON format
    log_step("PARSING OUTPUTS")
    output_parser.main(tc_file_path)

    # Step 5: Analyze results
    log_step("RESULT ANALYSIS")
    analysis_filename = dispatcher.analyze_test_results()

    #Step 6: Log Failures
    failed = log_failures(analysis_filename, iteration)

    if not failed:
        print(f"Stopping feedback loop: No failures logged in iteration {iteration + 1}.")
        return None

    return dispatcher.feedback_loop(analysis_filename)


if __name__ == '__main__':
    reset_failure_log() #clear the log file for a new test

    #step 1: generate initial test cases with ChatGPT
    log_step("TEST CASE GENERATION")
    tc_file_path = dispatcher.generate_test_cases()

    num_iterations = 3
    for i in range(num_iterations):
        tc_file_path = run_test_iteration(tc_file_path, i)
        if tc_file_path is None:
            break # no failures were logged
