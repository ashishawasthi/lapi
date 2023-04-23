from langchain.chat_models import ChatOpenAI # TODO replace with from langchain.chat_models import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import os

load_dotenv() # load OPENAI_API_KEY from .env 
app = FastAPI()

class Clarification(BaseModel):
    question: str
    answer: str | None = None

class Requirement(BaseModel):
    # TODO add problem_id when state is stored in database
    description: str
    clarifications: list[Clarification]

class Epic(BaseModel):
    # TODO add requirement_id when state is stored in database
    title: str
    description: str
    clarifications: list[Clarification]

class Story(BaseModel):
    # TODO add epic_id when state is stored in database
    title: str
    user: str
    description: str
    clarifications: list[Clarification]

class Scenario(BaseModel):
    # TODO add story_id when state is stored in database
    title: str
    description: str

@app.get("/")
async def root():
    return {"usage": """
    /requirements with the problem-statement text in the post body.
    /epics with the requirements JSON in the post body.
    /user-stories with the epics JSON in the post body.
    /test-scenarios with the user-stories JSON in the post body.
    """}

# Generate epics for the given requirements using OpenAI ChatCompletion API
@app.post("/epics") # TODO change to PUT when state is stored in database
def epics(requirements: list[Requirement]):

    project_dir = "rule-engine" # TODO find closest project to the given requirements

    # Load the prompt parts from files at startup
    system2 = text_from_file(os.path.join("assets", "prompts", "2-system.txt"))
    requirement21 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "21-requirements-answers.json"))
    epics22 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "22-epics-questions.json"))
    chat = ChatOpenAI(temperature=0, max_tokens=2048, request_timeout=140, max_retries=2)
    messages = [
        SystemMessage(content=system2),
        HumanMessage(content=requirement21),
        AIMessage(content=epics22),
        HumanMessage(content="Business Requirements:\n{requirements}".format(requirements=requirements)),
    ]
    print("\n\nCalling OpenAI ChatCompletion API with messages: {messages}".format(messages=messages))
    response = chat(messages)
    print("\n\nResponse:" + response)
    try:
        epics_json = json.loads(response.content)
        print("\n\n{epics_length} epics received from OpenAI ChatCompletion API".format(epics_length=len(epics_json)))
    except ValueError as e:
        print("\n\nError parsing epics JSON from OpenAI ChatCompletion API response: {e}".format(e=e))
        epics_json = []
        # split response.content by new lines. for each non-empty line, make it title of an epic
        for line in response.content.splitlines():
            if(line and line.strip() != ""):
                epics_json.append({"title": line})
    return epics_json

def json_string_from_file(file_path: str) -> str:
    with open(os.path.join(file_path), "r") as f:
        raw = f.read()
    # remove extra whitespaces and newlines
    return json.dumps(json.loads(raw)) 

def text_from_file(file_path: str) -> str:
    with open(os.path.join(file_path), "r") as f:
        raw = f.read()
    return raw.strip()
