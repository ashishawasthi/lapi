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
### POST /epics/ Examples of request and response
#### Bash Example
```bash
curl -X 'POST' \
  'http://localhost:8000/epics' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"description": "A self-service marketing rule-engine for business users to develop targeted marketing rules using AI model recommendations to send only relevant messages to customers. The platform ensures minimal spam and delivers messages via inbound and outbound channels.", "clarifications": []}'
```

#### Powershell Example
```powershell
Invoke-RestMethod -Method POST `
  -Uri 'http://localhost:8000/epics' `
  -Headers @{'accept'='application/json'; 'Content-Type'='application/json'} `
  -Body '{"description": "A self-service marketing rule-engine for business users to develop targeted marketing rules using AI model recommendations to send only relevant messages to customers. The platform ensures minimal spam and delivers messages via inbound and outbound channels.", "clarifications": []}' 
```

#### Python Example
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

#### TypeScript Example
```typescript
import axios from 'axios';

const payload = {
  description: 'A self-service marketing rule-engine for business users to develop targeted marketing rules using AI model recommendations to send only relevant messages to customers. The platform ensures minimal spam and delivers messages via inbound and outbound channels.',
  clarifications: []
};

const headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json'
};

axios.post('http://localhost:8000/epics', [payload], { headers })
  .then(response => {
    console.log(response);
  })
```

#### Response Format Example
content-type: application/json 
```json
[
  {
    "title": "Marketing rules interface for targeted messages",
    "description": "Rules based on AI model recommendations and customer data to deliver targeted messages via inbound and outbound channels. The rules should allow me to filter customers based on product-propensities, demographics, behavior, recent usage of services, and transaction history. The rules should also comply with regulatory requirements and prevent spamming customers. The system should provide a user-friendly interface to create, edit, and delete rules.",
    "clarifications": [
      {
        "question": "List of events to be available in the system."
      },
      {
        "question": "List of spam prevention rules."
      }
    ]
  },
  {
    "title": "Arbitration between inbound and outbound channels",
    "description": "Rules to arbitrate across all inbound and outbound channels. Inbound channels should include mobile apps, website and support calls. Outbound channels should include push-notes, email and SMS. The rules should allow me to specify the priority of channels and the conditions under which a channel should be used. The system should integrate with Arbitration-Layer and provide options to setup routing to one or multiple channels of Arbitration-Layer. Rules should be able to use a mix of AI model recommended touch points/channels, product/offer information and customer data to determine the best channel to contact a customer.",
    "clarifications": [
      {
        "question": "List of all inbound and outbound channels to support."
      }
    ]
  }
]
```
