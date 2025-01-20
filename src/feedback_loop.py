from src.json_gpt import query_gpt, load_json

prompt = "Based on the JSON data provided, compare the expected and actual outputs for each test case. Analyze if these passed or failed, and generate new test cases if it failed."
prompt_file_path = "../json_prompts/test_cases_with_actual_output.json"

json_string = load_json(prompt_file_path)
query_gpt(prompt, json_string)