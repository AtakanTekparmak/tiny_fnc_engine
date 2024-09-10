import ollama
from tiny_fnc_engine import FunctionCallingEngine
from pydantic import BaseModel
from typing import List

# Declare constants
MOCK_DB = []

class Paper(BaseModel):
    title: str
    author: str
    content: str

def add_paper_to_db(paper: dict):
    paper_model = Paper(**paper)
    MOCK_DB.append(paper_model)
    return f"Paper {paper_model.title} by {paper_model.author} has been added to the database."

def get_papers_from_db() -> List[Paper]:
    return MOCK_DB

# Declare constants
SYSTEM_PTOMPT = """
You are a helpful assistant that provides information about weather and suggests activities. 
You have access to the following functions:
- add_paper_to_db(paper: Paper) -> str
- get_papers_from_db() -> List[Paper]
and the following types:
- Paper(title: str, author: str, content: str)
Always use function calls for these tasks. The function calls should be in the following format:
[
    {"name": "function_name_1", "parameters": {"arg1": value1, "arg2": value2}, "returns": [{"name": "return_variable_name_1", "type": "type_1"}]},
    {"name": "function_name_2", "parameters": {"arg2": "return_variable_name_1", "arg3": value2}, "returns": [{"name": "return_variable_name_2", "type": "type_2"}]},
    {"name": "function_name_3", "parameters": {"arg4": "return_variable_name_2"}, "returns": [{"name": "return_variable_name_3", "type": "type_3"}]},
    ...
]
DO NOT USE the ${return_variable_name_1} syntax UNDER ANY CIRCUMSTANCES, 
use only the name of the return variable like in the given example.
"""

# Define user message
user_message = """
Add the following paper to the database and then retrieve all papers from the database.

Title: "The Impact of AI on Jobs"
Author: "John Doe"
Content: "This paper explores the impact of AI on jobs and the future of work."
"""

# Call ollama API
response = ollama.chat(
    model="mistral-nemo:12b", 
    messages=[
        {"role": "system", "content": SYSTEM_PTOMPT},
        {"role": "user", "content": user_message}
    ]
)["message"]["content"]

# Initialize the FunctionCallingEngine and add functions
engine = FunctionCallingEngine()
engine.add_functions([add_paper_to_db, get_papers_from_db])

# Parse and call the functions
results = engine.parse_and_call_functions(response)

# Print the results
for result in results:
    print(result)

# The results should be similar to:
# Paper The Impact of AI on Jobs by John Doe has been added to the database.
# [Paper(title='The Impact of AI on Jobs', author='John Doe', content='This paper explores the impact of AI on jobs and the future of work.')]
