import openai
import json
from datetime import datetime
import os

# Set up OpenAI API key
openai.api_key = "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"  # Replace with your actual API key


def load_json(file_path):
    """Load JSON data from a file and return it as a string."""
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json.dumps(json_data)  # Convert JSON to a string

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


# Main function to run the script
def main():
    json_file_path = "VMprompt.json"  # Path to your JSON input file

    # Generate a timestamp for the output file name
    timestamp = datetime.now().strftime("%b-%d-%Y_%H-%M-%S")  # Format: Nov-06-2024_15-05-50
    output_file_path = f"outputs/output_{timestamp}.json"  # Path to your JSON output file with formatted timestamp

    prompt = "Based on the JSON data provided, generate input test cases for black box testing of a DEVS (Discrete Event System Specification) coupled model in the output_format specified."

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Load JSON data and query GPT
    json_string = load_json(json_file_path)
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


if __name__ == "__main__":
    main()
