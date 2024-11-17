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
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that formats output in JSON schema."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1000,  # Increased token limit for longer responses
        temperature=0  # Set to 0 for more predictable responses
    )

    return response.choices[0].message['content'].strip()

def compare_and_decide(expected_results, actual_results):
    """Compare expected and actual results, marking each test case as pass or fail."""
    analysis = []

    for i, expected in enumerate(expected_results):
        # Get the corresponding actual result, if it exists
        actual = actual_results[i] if i < len(actual_results) else None

        # Compare expected and actual results, marking pass/fail
        if actual == expected:
            result = {"test_case": i + 1, "status": "pass"}
        else:
            result = {"test_case": i + 1, "status": "fail", "expected": expected, "actual": actual}

        analysis.append(result)

    return analysis

# Main function to run the script
def main():
    prompt_file_path = "../json_prompts/VMprompt.json"  # Path to JSON input file
    actual_results_file_path = "actual_results.json"  # Path to the actual output JSON file from the test driver

    # Generate a timestamp for the output file name
    timestamp = datetime.now().strftime("%b-%d-%Y_%H-%M-%S")  # Format: Nov-06-2024_15-05-50
    output_file_path = f"outputs/output_{timestamp}.json"  # Path to your JSON output file with formatted timestamp

    prompt = "Based on the JSON data provided, generate input test cases for black box testing of a DEVS (Discrete Event System Specification) coupled model in the output_format specified."

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Load JSON data and query GPT
    json_string = load_json(prompt_file_path)
    result = query_gpt(prompt, json_string)

    # Parse the GPT response into JSON format if it's valid JSON
    try:
        output_data = json.loads(result)
    except json.JSONDecodeError:
        # If the result is not valid JSON, wrap it in a dictionary
        output_data = {"response": result}

    # Save the result to an output JSON file
    save_json(output_data, output_file_path)

    print(f"GPT response saved to {output_file_path}")

    # -------------------------------------------------------------------
    # This area will be the code for passing the JSON test cases to the driver
    # and getting the actual output of the Model to feed back to ChatGPT
    # Load actual results from the test driver output
    # actual_results = load_json(actual_results_file_path)
    # ------------------------------------------------------------------

    # Manually Analyze the results
    # pass_fail_analysis = compare_and_decide(expected_results, actual_results)

    # Save the pass/fail analysis to a new JSON file
    #analysis_output_path = f"outputs/analysis_{timestamp}.json"
    #save_json(pass_fail_analysis, analysis_output_path)
    #print(f"Pass/fail analysis saved to {analysis_output_path}")

if __name__ == "__main__":
    main()
