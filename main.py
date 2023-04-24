from langchain.chat_models import ChatOpenAI # TODO replace with from langchain.chat_models import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from fastapi import FastAPI
from dotenv import load_dotenv
import os

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

# Generate requirements for the given problem statement
@app.post("/requirements") # TODO change to PUT when state is stored in database
def requirements(problem: str):

    project_dir = "rule-engine" # TODO find closest project to the given requirements

    # Load the prompt parts from files
    system1 = text_from_file(os.path.join("assets", "prompts", "1-system.txt"))
    problem11 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "11-problem.json"))
    requirements12 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "12-requirements-questions.json"))
    chat = ChatOpenAI(temperature=0, max_tokens=2048, request_timeout=140, max_retries=2)
    messages = [
        SystemMessage(content=system1),
        HumanMessage(content=problem11),
        AIMessage(content=requirements12),
        HumanMessage(content="Problem Statement:\n{problem}".format(problem=problem)),
    ]
    print("\n\nCalling OpenAI ChatCompletion API with messages: {messages}".format(messages=messages))
    response = chat(messages)
    print("\n\nResponse: \n{response}".format(response=response))
    return extract_json_array(response.content)

# Generate epics for the given requirements
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
    print("\n\nResponse: \n{response}".format(response=response))
    return extract_json_array(response.content)

# Generate user stories for the given epic
@app.post("/stories") # TODO change to PUT when state is stored in database
def stories(epic: Epic):

    project_dir = "rule-engine" # TODO find closest project to the given requirements

    # Load the prompt parts from files
    system3 = text_from_file(os.path.join("assets", "prompts", "3-system.txt"))
    #epic31 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "21-requirements-answers.json"))
    #stories32 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "22-epics-questions.json"))
    chat = ChatOpenAI(temperature=0, max_tokens=2048, request_timeout=140, max_retries=2)
    messages = [
        SystemMessage(content=system3),
        #HumanMessage(content=epic31),
        #AIMessage(content=stories32),
        HumanMessage(content="Epic:\n{epic}".format(epic=epic)),
    ]
    print("\n\nCalling OpenAI ChatCompletion API with messages: \n{messages}".format(messages=messages))
    response = chat(messages)
    print("\n\nResponse: \n{response}".format(response=response))
    return extract_json_array(response.content)

# Generate test scenarios for the given user story
@app.post("/scenarios") # TODO change to PUT when state is stored in database
def scenarios(stories: list[Story]):

    project_dir = "rule-engine" # TODO find closest project to the given requirements

    # Load the prompt parts from files
    system4 = text_from_file(os.path.join("assets", "prompts", "4-system.txt"))
    chat = ChatOpenAI(temperature=0, max_tokens=2048, request_timeout=140, max_retries=2)
    messages = [
        SystemMessage(content=system4),
        HumanMessage(content="Epic:\n{stories}".format(stories=stories)),
    ]
    print("\n\nCalling OpenAI ChatCompletion API with messages: \n{messages}".format(messages=messages))
    response = chat(messages)
    print("\n\nResponse: \n{response}".format(response=response))
    return extract_json_array(response.content)
