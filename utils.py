import json

# Read from json file. Remove newlines and extra whitespaces 
def json_string_from_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        raw = f.read()
    return json.dumps(json.loads(raw)) 

# Read from text file. Remove extra whitespaces
def text_from_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        raw = f.read()
    return raw.strip()

# Extract json fron text by using substring between first "[" and last "]"
def extract_json_array(raw) -> str:
    return raw[raw.find("[") : raw.rfind("]") + 1]

# Convert text lines to json. Remove empty lines
def lines_to_json(raw, item_name="title") -> str:
    json = []
    for line in raw.splitlines():
        if(line and line.strip() != ""):
            json.append({item_name: line})
    return json
