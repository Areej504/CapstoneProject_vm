from src import json_gpt, run_td, update_test_data, update_json_output

if __name__ == '__main__':

    for i in range(5):
        #step 1 : query chatgpt to generate test case inputs
        tc_file_path = json_gpt.generate_test_cases()
        #step 2 : inject generated inputs into test_data.hpp
        update_test_data.main(tc_file_path)
        #step 3 : run the test driver to execute the DEVS Model and generate log file
        run_td.build_and_run_test_driver()
        #step 4 : parse log file results into a JSON format
        update_json_output.main(tc_file_path)
        #step 5 : feedback loop -> query chatgpt to analyze results (pass/fail)
        json_gpt.analyze_test_results()
