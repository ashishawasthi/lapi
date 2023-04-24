import json

# Read from json file. Remove newlines and extra whitespaces 
def json_string_from_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        text = f.read()
    return json.dumps(json.loads(text)) 

# Read from text file. Remove extra whitespaces
def text_from_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        text = f.read()
    return text.strip()

# Extract json fron text by using substring between first "[" and last "]"
def extract_json_array(text):
    json_array = text[text.find("[") : text.rfind("]") + 1]
    #print("\n\nExtracted JSON: \n{json_array}".format(json_array=json_array))
    return json.loads(json_array)

# Convert text lines to json. Remove empty lines
def lines_to_json(text, item_name="title") -> str:
    json = []
    for line in text.splitlines():
        if(line and line.strip() != ""):
            json.append({item_name: line})
    return json
