import json

# recursive call to extract name and type from document JSON 
def extract_summary(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if key in ['name', 'type']:
                new_dict[key] = value
            elif key == 'document':
                new_dict[key] = extract_summary(value)
            elif key == 'children':
                new_dict[key] = [extract_summary(child) for child in value]
        return new_dict
    elif isinstance(data, list):
        return [extract_summary(item) for item in data]
    else:
        return data

# TODO replace with dynamic data input from figma\fetch.py
with open('response.json', 'r') as infile:
    data = json.load(infile)

summary = extract_summary(data)

# TODO replace with return statement
with open('summary.json', 'w') as outfile:
    json.dump(summary, outfile, indent=2)
