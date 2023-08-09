from typing import List
from langchain.chat_models import ChatOpenAI # TODO replace with from langchain.chat_models import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from fastapi import FastAPI
from dotenv import load_dotenv
from google.cloud import aiplatform

import os
import json
import vertexai

from models import Clarification, Requirement, Epic, Story, Scenario
from utils import text_from_file, json_string_from_file, extract_json_array
from vertexai.language_models import TextGenerationModel

load_dotenv() # load OPENAI_API_KEY from .env 
app = FastAPI()

@app.get("/")
async def root():
    return {"usage": """
    /requirement with the problem-statement text in the post body.
    /epics with the requirement JSON in the post body.
    /user-stories with the epics JSON in the post body.
    /test-scenarios with the user-stories JSON in the post body.
    """}

# Generate detailed requirement for the given problem statement
@app.post("/requirement") # TODO change to PUT when state is stored in database
def requirement(problem: str):

    project_dir = "rule-engine" # TODO find closest project to the given requirement

    # Load the prompt parts from files
    system1 = text_from_file(os.path.join("assets", "prompts", "1-system.txt"))
    problem11 = text_from_file(os.path.join("assets", "prompts", project_dir, "11-problem.txt"))
    requirement12 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "12-requirement-questions.json"))
    chat = ChatOpenAI(temperature=0, max_tokens=2048, request_timeout=140, max_retries=2)
    messages = [
        SystemMessage(content=system1),
        HumanMessage(content=problem11),
        AIMessage(content=requirement12),
        HumanMessage(content=problem)
    ]
    print("\n\nCalling OpenAI ChatCompletion API with messages: {messages}".format(messages=messages))
    response = chat(messages)
    print("\n\nResponse: \n{response}".format(response=response))
    return extract_json_array(response.content)

# Generate epics for the given requirement
@app.post("/epics") # TODO change to PUT when state is stored in database
def epics(requirement: Requirement):

    project_dir = "rule-engine" # TODO find closest project to the given requirement

    # Load the prompt parts from files
    system2 = text_from_file(os.path.join("assets", "prompts", "2-system.txt"))
    requirement21 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "21-requirement-answers.json"))
    epics22 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "22-epics-questions.json"))
    chat = ChatOpenAI(temperature=0, max_tokens=2048, request_timeout=140, max_retries=2)

    messages = [
        SystemMessage(content=system2),
        HumanMessage(content=requirement21),
        AIMessage(content=epics22),
        HumanMessage(content=requirement.json())
    ]
    print("\n\nCalling OpenAI ChatCompletion API with messages: {messages}".format(messages=messages))
    response = chat(messages)
    print("\n\nResponse: \n{response}".format(response=response))
    return extract_json_array(response.content)

# Generate user stories for the given epic
@app.post("/stories") # TODO change to PUT when state is stored in database
def stories(epic: Epic):
    #TODO try including requirement details forgiving context
    project_dir = "rule-engine" # TODO find closest project to the given requirement

    # Load the prompt parts from files
    system3 = text_from_file(os.path.join("assets", "prompts", "3-system-marketing-analytics.txt"))
    epic31 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "31-epics-answers.json"))
    stories32 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "32-stories-questions.json"))
    chat = ChatOpenAI(temperature=0, max_tokens=2048, request_timeout=140, max_retries=2)
    messages = [
        SystemMessage(content=system3),
        HumanMessage(content=epic31),
        AIMessage(content=stories32),
        HumanMessage(content=epic.json())
    ]
    print("\n\nCalling OpenAI ChatCompletion API with messages: \n{messages}".format(messages=messages))
    response = chat(messages)
    print("\n\nResponse: \n{response}".format(response=response))
    return extract_json_array(response.content)

# Generate test scenarios for the given user story
@app.post("/scenarios") # TODO change to PUT when state is stored in database
def scenarios(stories: List[Story]):

    project_dir = "rule-engine" # TODO find closest project to the given requirement

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


# Generate detailed requirement for the given problem statement using Vertex AI
@app.post("/requirement-v") # TODO change to PUT when state is stored in database
def requirement(problem: str):

    project_dir = "rule-engine" # TODO find closest project to the given requirement

    # Load the prompt parts from files
    system1 = text_from_file(os.path.join("assets", "prompts", "1-system.txt"))
    problem11 = text_from_file(os.path.join("assets", "prompts", project_dir, "11-problem.txt"))
    requirement12 = json_string_from_file(os.path.join("assets", "prompts", project_dir, "12-requirement-questions.json"))

    model = TextGenerationModel.from_pretrained("text-bison@001")
    parameters = {"temperature": 0.2, "max_output_tokens": 1024, "top_p": 0.8, "top_k": 40}
    vertexai.init(project="generativai", location="us-central1")
    prompt = """{system1}
Problem Statement: {problem11}
Project Requirement: {requirement12}

Problem Statement: {problem}
Project Requirement:
""".format(system1=system1, problem11=problem11, requirement12=requirement12, problem=problem)
    print("\n\nCalling VertexAI Text API with prompt: {prompt}".format(prompt=prompt))
    response = model.predict(prompt, **parameters)
    print("\n\nResponse: \n{response}".format(response=response))
    return extract_json_array(response.text)
