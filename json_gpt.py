import openai
import json

# Set up OpenAI API key
openai.api_key = "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"  # Replace with your API key


def load_json(file_path):
    """Load JSON data from a file and return it as a string."""
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json.dumps(json_data)  # Convert JSON to a string


def query_gpt(prompt, json_string):
    """Query OpenAI GPT with the provided prompt and JSON data."""
    # Combine the prompt and JSON data into a single input
    input_text = f"{prompt}\n{json_string}"

    # Send request to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=150,  # Adjust the token limit based on the response length
        temperature=0.7  # Adjust creativity level; 0.7 is moderate creativity
    )

    return response.choices[0].text.strip()


# Main function to run the script
def main():
    json_file_path = "test1.json"  # Path to your JSON file
    prompt = "Process this input and provide expected output in JSON format"  # Customize as needed

    # Load JSON data and query GPT
    json_string = load_json(json_file_path)
    result = query_gpt(prompt, json_string)

    print("GPT Response:", result)


if __name__ == "__main__":
    main()
