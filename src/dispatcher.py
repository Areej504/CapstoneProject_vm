import openai
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("../key.env")

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_json(file_path):
    """Load JSON data from a file and return it as a string."""
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json.dumps(json_data)

def save_json(output_data, output_file_path):
    """Save the output data to a JSON file."""
    with open(output_file_path, 'w') as file:
        json.dump(output_data, file, indent=4)

def query_gpt(prompt, json_string):
    """Query OpenAI GPT with the provided prompt and JSON data."""
    # Combine the prompt and JSON data into a single input
    input_text = f"{prompt}\n\nJSON data:\n{json_string}"

    # Send request to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that formats output in JSON schema."},
            {"role": "user", "content": input_text}
        ],
        max_completion_tokens=1000,  # Increased token limit for longer responses
        temperature=0.7# Set to 0 for more predictable responses
    )

    return response.choices[0].message['content'].strip()

def generate_test_cases():
    """function to load prompt, query chatgpt and save the response in /outputs.
        :return the output file path containing generated test cases
    """
    prompt_file_path = "../json_prompts/multiplier_prompt.json"  # Path to JSON input file

    # Generate a timestamp for the output file name
    timestamp = datetime.now().strftime("%b-%d-%Y_%H-%M-%S")  # Format: Nov-06-2024_15-05-50
    output_file_path = f"../outputs/demo/output_{timestamp}.json"  # Path to your JSON output file with formatted timestamp

    prompt = "Based on the JSON data provided, generate input test cases for black box testing of a DEVS (Discrete Event System Specification) model in raw JSON format. Do not include Markdown formatting, code blocks, or any additional text. Only return valid JSON."

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Load JSON data and query GPT
    json_string = load_json(prompt_file_path)
    response = query_gpt(prompt, json_string)

    # Parse the GPT response into JSON format if it's valid JSON

    try:
        output_data = json.loads(response)
    except json.JSONDecodeError:
        # If the result is not valid JSON, wrap it in a dictionary
        output_data = {"response": response}

    # Save the result to an output JSON file
    save_json(output_data, output_file_path)

    print(f"GPT response saved to {output_file_path}")

    return output_file_path

def analyze_test_results():
    """
    Analyzes the pass/fail status of test cases in results.json using adder_prompt.json as context.
    """

    adder_prompt_path = "../json_prompts/multiplier_prompt.json"
    results_path = "../json_prompts/test_cases_with_actual_output.json"

    # Load JSON data from the specified paths
    adder_prompt = load_json(adder_prompt_path)
    results = load_json(results_path)

    # Prompt for GPT analysis
    analysis_prompt = (
        "Given the prompt JSON containing the model description and the test results JSON provided, analyze the pass/fail status of each test case for the value result, ignoring the time result and analyze any trends with failed results. "
        "Provide the analysis in the following raw JSON format. Do not include Markdown formatting, code blocks, or any additional text. Only return valid JSON.:\n"
        "{\n"
        "  \"test_case_id\": {\n"
        "    \"expected_result\": \"<expected result>\",\n"
        "    \"actual_result\": \"<actual result>\",\n"
        "    \"pass\": true/false,\n"
        "    \"remarks\": \"<reason for failure and diagnosis of the issue, if applicable>\"\n"
        "  },\n"
        "  ...\n"
        "}"
    )

    # Query GPT for analysis
    combined_json = f"Prompt:\n{adder_prompt}\n\nTest Results:\n{results}"
    response = query_gpt(analysis_prompt, combined_json)

    # Generate a timestamp for the output file name
    timestamp = datetime.now().strftime("%b-%d-%Y_%H-%M-%S")
    output_file_path = f"../outputs/demo/analysis_{timestamp}.json"

    # Parse the GPT response into JSON format if it's valid JSON
    try:
        analysis_data = json.loads(response)
    except json.JSONDecodeError:
        analysis_data = {"error": "Failed to parse GPT response as JSON", "raw_response": response}

    # Save to an output JSON file
    save_json(analysis_data, output_file_path)

    print(f"Test analysis saved to {output_file_path}")

    return output_file_path

def feedback_loop(results_path):
    """
    Initiates a feedback loop to generate more tests cases.
    """

    adder_prompt_path = "../json_prompts/multiplier_prompt.json"

    # Load JSON data from the specified paths
    adder_prompt = load_json(adder_prompt_path)
    results = load_json(results_path)

    # Prompt for GPT analysis
    feedback_prompt = ("Based on the JSON data provided and generate new test cases in the same JSON format to help diagnose the issue if any test cases failed."
                       "Provide the analysis in the given raw JSON format. Do not include Markdown formatting, code blocks, or any additional text. Only return valid JSON.")

    # Query GPT for analysis
    combined_json = f"Prompt:\n{adder_prompt}\n\nTest Results:\n{results}"
    response = query_gpt(feedback_prompt, combined_json)

    # Generate a timestamp for the output file name
    timestamp = datetime.now().strftime("%b-%d-%Y_%H-%M-%S")
    output_file_path = f"../outputs/feedback/feedback_{timestamp}.json"

    # Parse the GPT response into JSON format if it's valid JSON
    try:
        feedback_data = json.loads(response)
    except json.JSONDecodeError:
        feedback_data = {"error": "Failed to parse GPT response as JSON", "raw_response": response}

    # Save to an output JSON file
    save_json(feedback_data, output_file_path)

    print(f"Feedback saved to {output_file_path}")


if __name__ == "__main__":
    analyze_test_results()
