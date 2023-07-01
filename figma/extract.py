import json

# recursive call to extract name and type from document JSON 
def extract_name_type(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if key in ['name', 'type']:
                new_dict[key] = value
            elif key == 'document':
                new_dict[key] = extract_name_type(value)
            elif key == 'children':
                new_dict[key] = [extract_name_type(child) for child in value]
        return new_dict
    elif isinstance(data, list):
        return [extract_name_type(item) for item in data]
    else:
        return data

# TODO replace with dynamic data input from figma\fetch.py
with open('response.json', 'r') as infile:
    data = json.load(infile)

extracted_data = extract_name_type(data)

# TODO replace with return statement
with open('extract.json', 'w') as outfile:
    json.dump(extracted_data, outfile, indent=2)
    