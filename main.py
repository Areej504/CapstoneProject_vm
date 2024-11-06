import json

file_path = 'VMprompt.json'

# Read the JSON file and store it as a string
with open(file_path, 'r') as file:
    json_data = file.read()

# Alternatively, if you want to load the JSON data as a Python dictionary
data_dict = json.loads(json_data)

# Output the JSON text as a string
print(json_data)
