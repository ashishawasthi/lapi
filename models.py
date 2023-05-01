from typing import List, Optional
from pydantic import BaseModel

class Clarification(BaseModel):
    question: str
    answer: Optional[str]

class Requirement(BaseModel):
    # TODO add problem_id when state is stored in database
    description: str
    department: Optional[str]
    clarifications: List[Clarification]

class Epic(BaseModel):
    # TODO add requirement_id when state is stored in database
    title: str
    description: str
    clarifications:List[Clarification]

class Story(BaseModel):
    # TODO add epic_id when state is stored in database
    title: str
    user: str
    description: str
    clarifications: List[Clarification]

class Scenario(BaseModel):
    # TODO add story_id when state is stored in database
    title: str
    description: str
