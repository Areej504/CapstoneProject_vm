import json
import os

from src import dispatcher, run_td, input_parser, output_parser


def log_step(step_name):
    """Formats and prints step headers."""
    print(f"\n{'*' * 20} {step_name} {'*' * 20}\n")

def log_failures(analysis_filename, iteration):
    """Logs failed test cases into failure_log.json based on the analysis results."""
    try:
        # Read and print analysis data
        with open(analysis_filename, 'r') as analysis_file:
            analysis_data = json.load(analysis_file)
        print(json.dumps(analysis_data, indent=4))

        # Initialize the structure for the failure log if it doesn't exist or is empty
        failure_log = {}
        if os.path.exists("../outputs/failure_log.json"):
            with open("../outputs/failure_log.json", 'r') as failure_file:
                failure_log = json.load(failure_file)

        # If failure_log is empty, initialize it with an empty iterations key
        if not failure_log.get("iterations"):
            failure_log["iterations"] = []

        # Initialize failure data for the current iteration
        failure_data = {
            "iteration": iteration + 1,
            "failed_cases": []
        }

        # Process the test cases and check if there are failures
        for test_case, result in analysis_data.items():
            if not result.get("pass"):  # Check for failed cases
                failure_data["failed_cases"].append(result)

        # If there are failed cases, add them to the failure log
        if failure_data["failed_cases"]:
            failure_log["iterations"].append(failure_data)
            # Write the updated failure log back to the file
            with open("../outputs/failure_log.json", 'w') as failure_file:
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
    log_failures(analysis_filename, iteration)
    failed = log_failures(analysis_filename, iteration)

    if not failed:
        print(f"Stopping feedback loop: No failures logged in iteration {iteration + 1}.")
        return None

    return dispatcher.feedback_loop(analysis_filename)


if __name__ == '__main__':
    #step 1: generate initial test cases with ChatGPT
    log_step("TEST CASE GENERATION")
    tc_file_path = dispatcher.generate_test_cases()

    num_iterations = 2
    for i in range(num_iterations):
        tc_file_path = run_test_iteration(tc_file_path, i)
        if tc_file_path is None:
            break # no failures were logged
