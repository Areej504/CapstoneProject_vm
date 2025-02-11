from src import dispatcher, run_td, input_parser, output_parser

if __name__ == '__main__':
    #step 1 : query chatgpt to generate test case inputs
    print("\n***************** TEST CASE GENERATION *****************")
    tc_file_path = dispatcher.generate_test_cases()

    #step 2 : inject generated inputs into test_data.hpp
    print("\n***************** PARSING INPUTS TO TEST DRIVER *****************")
    input_parser.main(tc_file_path)

    #step 3 : run the test driver to execute the DEVS Model and generate log file
    print("\n***************** RUNNING TEST DRIVER *****************")
    run_td.build_and_run_test_driver()

    #step 4 : parse log file results into a JSON format
    print("\n***************** PARSING OUTPUTS *****************")
    output_parser.main(tc_file_path)

    #step 5 : feedback loop -> query chatgpt to analyze results (pass/fail) and return more test cases
    print("\n***************** RESULT ANALYSIS *****************")
    analysis_filename = dispatcher.analyze_test_results()
    dispatcher.feedback_loop(analysis_filename)
