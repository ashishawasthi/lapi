# lapi
Langchain REST API, with FastAPI

## Install
```bash
pip install -r requirements.txt
```
Set OPENAI_API_KEY in .env

## Run
```bash
uvicorn main:app --reload
```

## Test
```bash
python -m unittest .\tests\test_utils.py
```

## API
### POST /epics/
#### Bash
```bash
curl -X 'POST' \
  'http://localhost:8000/epics' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
    {
        "description": "A self-service marketing rule-engine for business users to develop targeted marketing rules using AI model recommendations to send only relevant messages to customers. The platform ensures minimal spam and delivers messages via inbound and outbound channels.",
        "clarifications": []
    }
]'
```
#### Powershell
```powershell
Invoke-RestMethod -Method POST `
  -Uri 'http://localhost:8000/epics' `
  -Headers @{'accept'='application/json'; 'Content-Type'='application/json'} `
  -Body '[
    {
        "description": "A self-service marketing rule-engine for business users to develop targeted marketing rules using AI model recommendations to send only relevant messages to customers. The platform ensures minimal spam and delivers messages via inbound and outbound channels.",
        "clarifications": []
    }
]' 
```
#### Python
```python
import requests
import json

payload = {
    "description": "A self-service marketing rule-engine for business users to develop targeted marketing rules using AI model recommendations to send only relevant messages to customers. The platform ensures minimal spam and delivers messages via inbound and outbound channels.",
    "clarifications": []
}

response = requests.post(
    'http://localhost:8000/epics', 
    data=json.dumps([payload]), 
    headers={'accept': 'application/json', 'Content-Type': 'application/json'})
```
