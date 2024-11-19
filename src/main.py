from src import json_gpt, run_td, update_test_data, update_json_output

if __name__ == '__main__':
    #step 1
    json_gpt.main()
    #step 2
    update_test_data.main()
    #step 3
    run_td.build_and_run_test_driver()
    #step 4
    update_json_output.main()

