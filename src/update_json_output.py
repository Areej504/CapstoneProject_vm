import os
import csv
import json


def load_test_cases(json_file):
    """Load test cases from a JSON file."""
    with open(json_file, 'r') as file:
        return json.load(file)


def extract_actual_outputs(simulation_dir):
    """
    Extract actual outputs from .csv files in the simulation directory.
    The file names should match the descriptions in the test cases.
    """
    actual_outputs = {}
    for filename in os.listdir(simulation_dir):
        if filename.endswith(".csv"):
            test_name = filename.replace("_", " ").replace(".csv", "").strip()
            with open(os.path.join(simulation_dir, filename), 'r') as file:
                reader = csv.reader(file, delimiter=';')
                outputs = []
                for row in reader:
                    if len(row) > 3 and row[3] == "sum":
                        outputs.append({"time": int(row[0]), "value": int(row[4])})
                actual_outputs[test_name] = {"sum": outputs}
    return actual_outputs


def generate_test_cases_with_actual_output(test_cases, actual_outputs):
    """
    Merge actual outputs into the test cases and update descriptions to match file names.
    """
    updated_test_cases = []
    for test_case in test_cases["test_cases"]:
        description = test_case["description"]
        # Update the description to match the filename format
        updated_description = description.replace("_", " ")
        test_case["description"] = updated_description

        # Inject actual outputs if they exist
        if updated_description in actual_outputs:
            test_case["actual_output"] = actual_outputs[updated_description]
        else:
            test_case["actual_output"] = {}
            print(f"Warning: Could not find actual outputs for test case '{updated_description}'")

        updated_test_cases.append(test_case)
    return {"test_cases": updated_test_cases}


def save_test_cases_with_actual_output(output_file, data):
    """Save the merged test cases with actual outputs to a JSON file."""
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)


def main(test_cases_file: str):
    # File paths
    simulation_dir = "../model/capstone_models/test/td_Basic_Adder/simulation_results"
    output_file = "../json_prompts/test_cases_with_actual_output.json"

    # Process data
    test_cases = load_test_cases(test_cases_file)
    actual_outputs = extract_actual_outputs(simulation_dir)
    test_cases_with_actual_output = generate_test_cases_with_actual_output(test_cases, actual_outputs)

    # Save the final JSON
    save_test_cases_with_actual_output(output_file, test_cases_with_actual_output)
    print(f"Generated {output_file}")


if __name__ == "__main__":
    main()
