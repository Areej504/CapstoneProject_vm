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
            test_name = filename.replace(".csv", "").strip()
            with open(os.path.join(simulation_dir, filename), 'r') as file:
                reader = csv.reader(file, delimiter=';')
                outputs = {"o_change": [], "o_dispense_id": []}

                for row in reader:
                    if len(row) > 4:  # Ensure there's enough data in the row
                        port_name = row[3].strip()
                        value = row[4].strip()

                        # Convert to appropriate data type (float for change, int for dispense ID)
                        if port_name == "o_change":
                            outputs["o_change"].append({"value": float(value)})
                        elif port_name == "o_dispense_id":
                            outputs["o_dispense_id"].append({"value": int(value)})

                actual_outputs[test_name] = outputs
                print("Outputs: ", outputs)
    return actual_outputs


def generate_test_cases_with_actual_output(test_cases, actual_outputs):
    """
    Merge actual outputs into the test cases and update descriptions to match file names.
    """
    updated_test_cases = []
    for test_case in test_cases["test_cases"]:
        test_case_id = test_case["test_case_id"]
        # Update the test_case_id to match the filename format
        updated_description = test_case_id.replace("_", " ")
        test_case["test_case_id"] = updated_description

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
    simulation_dir = "../model/vending_machine/test/Vending_Machine/simulation_results"
    output_file = "../json_prompts/test_cases_with_actual_output.json"

    # Process data
    test_cases = load_test_cases(test_cases_file)
    actual_outputs = extract_actual_outputs(simulation_dir)
    test_cases_with_actual_output = generate_test_cases_with_actual_output(test_cases, actual_outputs)

    # Save the final JSON
    save_test_cases_with_actual_output(output_file, test_cases_with_actual_output)
    print(f"Generated {output_file}")


if __name__ == "__main__":
    main('../outputs/tests/output_Mar-05-2025_15-17-13.json')
