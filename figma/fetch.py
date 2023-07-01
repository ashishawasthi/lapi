import requests
import json

access_token = '' #TODO get the access token from secret store or environment variable
file_key = 'dYpUAJcZRXIhPSJvPcB5O9' #TODO get the file key dynamically from user input (hint: URL of the file)

response = requests.get(f'https://api.figma.com/v1/files/{file_key}', headers={'X-Figma-Token': access_token})

if response.status_code == 200:
    with open('response.json', 'w') as outfile:
        json.dump(response.json(), outfile)
else:
    print(f'Fetch failed with status {response.status_code}')
