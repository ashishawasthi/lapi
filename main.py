from langchain.chat_models import ChatOpenAI # TODO replace with from langchain.chat_models import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import json

from models import Clarification, Requirement, Epic, Story, Scenario
from utils import text_from_file, json_string_from_file, extract_json_array

load_dotenv() # load OPENAI_API_KEY from .env 
app = FastAPI()

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

    # Load the prompt parts from files
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
    print("\n\nResponse: {response}".format(response=response))
    epics_str = extract_json_array(response.content)
    print("\n\nEpics JSON:\n{epics_str}\n".format(epics_str=epics_str))
    epics_json = json.loads(epics_str)
    print("\n\n{epics_length} epics received from OpenAI ChatCompletion API".format(epics_length=len(epics_json)))
    return epics_json
