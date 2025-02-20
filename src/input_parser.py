import json
import os
import shutil

def update_test_data(json_file, output_file):
    """
    Reads the JSON test cases and rewrites the test_data.hpp file.
    """
    # Load JSON test cases
    with open(json_file, 'r') as file:
        test_cases_data = json.load(file)

    test_cases = test_cases_data["output_format"]["test_cases"]

    with open(output_file, 'w') as file:
        # Header guards and includes
        file.write("#ifndef TEST_DATA_Vending_Machine\n")
        file.write("#define TEST_DATA_Vending_Machine\n\n")
        file.write("#include <iostream>\n#include <vector>\n#include <tuple>\n#include <map>\n#include <string>\n#include <variant>\n")
        file.write('#include "Vending_Machine_Variant_Goblin.hpp"\n\n')

        # Generate `get_test_names()`
        file.write("std::map<int, std::string> get_test_names()\n{\n")
        file.write("    std::map<int, std::string> names;\n")
        for i, test_case in enumerate(test_cases, start=1):
            file.write(f"    names[{i}] = \"{test_case['test_case_id']}\";\n")
        file.write("    return names;\n")
        file.write("}\n\n")

        # Generate `get_test_cases()`
        file.write("std::map<int, std::map<std::string, std::vector<std::tuple<double, Variant_Goblin>>>> get_test_cases()\n{\n")
        file.write("    std::map<int, std::map<std::string, std::vector<std::tuple<double, Variant_Goblin>>>> test_cases;\n")

        for i, test_case in enumerate(test_cases, start=1):
            file.write(f"    // Test Case {i} Input Data\n")
            file.write(f"    std::map<std::string, std::vector<std::tuple<double, Variant_Goblin>>> tc{i};\n")

            for input_name, input_values in test_case["input"].items():
                file.write(f"    std::vector<std::tuple<double, Variant_Goblin>> {input_name}_{i};\n")
                for value in input_values:
                    time = value["time"]
                    val = value["value"]

                    # Handle item_selection_t case (list of two values: [price, item_id])
                    if isinstance(val, list) and len(val) == 2:
                        file.write(f"    {input_name}_{i}.push_back(std::make_tuple({time}, item_selection_t({val[0]}, {val[1]})));\n")
                    else:
                        # Handle single float values (e.g., `i_money`)
                        file.write(f"    {input_name}_{i}.push_back(std::make_tuple({time}, float({val})));\n")

                file.write(f"    tc{i}[\"{input_name}\"] = {input_name}_{i};\n")
            file.write(f"    test_cases[{i}] = tc{i};\n")

        file.write("    return test_cases;\n")
        file.write("}\n\n")

        # Generate `get_comparator_data()`
        file.write("std::map<int, std::map<std::string, std::vector<std::tuple<int, Variant_Goblin>>>> get_comparator_data()\n{\n")
        file.write("    std::map<int, std::map<std::string, std::vector<std::tuple<int, Variant_Goblin>>>> comparator_data;\n")

        for i, test_case in enumerate(test_cases, start=1):
            file.write(f"    // Test Case {i} Expected Outputs\n")
            file.write(f"    std::map<std::string, std::vector<std::tuple<int, Variant_Goblin>>> eo{i};\n")

            for output_name, output_values in test_case["expected_output"].items():
                file.write(f"    std::vector<std::tuple<int, Variant_Goblin>> {output_name}_{i}_eo;\n")
                for value in output_values:
                    time = value["time"]
                    val = value["value"]
                    file.write(f"    {output_name}_{i}_eo.push_back(std::make_tuple({time}, float({val})));\n")
                file.write(f"    eo{i}[\"{output_name}\"] = {output_name}_{i}_eo;\n")
            file.write(f"    comparator_data[{i}] = eo{i};\n")

        file.write("    return comparator_data;\n")
        file.write("}\n\n")

        # Generate `get_path_data()`
        file.write("std::map<int, std::map<std::string, std::vector<std::string>>> get_path_data()\n{\n")
        file.write("    std::map<int, std::map<std::string, std::vector<std::string>>> path_data;\n")
        for i in range(1, len(test_cases) + 1):
            file.write(f"    std::map<std::string, std::vector<std::string>> test_paths_tc{i};\n")
            file.write(f"    std::vector<std::string> Vending_Machine_st_{i};\n")
            file.write(f"    test_paths_tc{i}[\"Vending_Machine\"] = Vending_Machine_st_{i};\n")
            file.write(f"    path_data[{i}] = test_paths_tc{i};\n")
        file.write("    return path_data;\n")
        file.write("}\n\n")

        # Generate `get_constructor_data()`
        file.write("std::map<int, std::map<int, Variant_Goblin>> get_constructor_data()\n{\n")
        file.write("    std::map<int, std::map<int, Variant_Goblin>> con_args_data;\n")
        for i in range(1, len(test_cases) + 1):
            file.write(f"    std::map<int, Variant_Goblin> Vending_Machine_ca_{i};\n")
            file.write(f"    con_args_data[{i}] = Vending_Machine_ca_{i};\n")
        file.write("    return con_args_data;\n")
        file.write("}\n\n")

        # Generate `get_test_set_size()`
        file.write("int get_test_set_size()\n{\n")
        file.write(f"    return {len(test_cases)};\n")
        file.write("}\n\n")

        # Close the header guard
        file.write("#endif\n")

def move_to_capstone_models(test_data_file, capstone_dir):
    """
    Move the generated test_data.hpp to the correct directory.
    """
    destination = os.path.join(capstone_dir, "test_data.hpp")
    shutil.move(test_data_file, destination)
    print(f"Moved test_data.hpp to {destination}")

def main(test_cases_file: str):
    output_file = "test_data.hpp"
    capstone_dir = "../model/vending_machine/"

    update_test_data(test_cases_file, output_file)
    move_to_capstone_models(output_file, capstone_dir)

if __name__ == "__main__":
    test_cases_file = "/Users/javeriasohail/Desktop/CapstoneProject_vm/json_prompts/test_cases_with_actual_output.json"  # Update with correct path
    main(test_cases_file)

