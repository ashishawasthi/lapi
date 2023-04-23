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
```bash
curl -X POST "http://localhost:8000/epics/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "[{\"description\":\"my test description\"}, \"clarifications\": []]"
```
