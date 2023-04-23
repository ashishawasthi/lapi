import json

def json_string_from_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        raw = f.read()
    # remove extra whitespaces and newlines
    return json.dumps(json.loads(raw)) 

def text_from_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        raw = f.read()
    return raw.strip()

# get substring between first "[" and last "]"
def extract_json_array(raw):
    return raw[raw.find("[") : raw.rfind("]") + 1]

# split response.content by new lines. for each non-empty line, make it title of an epic
def lines_to_json(raw, item_name="title"):
    json = []
    for line in raw.splitlines():
        if(line and line.strip() != ""):
            json.append({item_name: line})