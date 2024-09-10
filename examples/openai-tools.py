import json

from openai import OpenAI
from tiny_fnc_engine import FunctionCallingEngine, OpenAIToolCall, OpenAIFunction

# Declare constants
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search for items",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                }
            }
        }
    }
]

def search(query: str) -> str:
    return f"Search results for {query}"

# Initialize OpenAI client
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama'
)

# Define user message
messages = [
    {"role": "system", "content": "You are a helpful assistant that can access external functions."},
    {"role": "user", "content": "Hello, I am looking for shirts."},
]

# Call OpenAI API
response = client.chat.completions.create(
    model="mistral-nemo:12b",
    messages=messages,
    tools=TOOLS,
    tool_choice="auto",
)

# Extract tool calls
tool_calls = response.choices[0].message.tool_calls

# Initialize the FunctionCallingEngine and add functions
engine = FunctionCallingEngine()
engine.add_functions([search])

# Parse and call the functions
function_calls = []
for tool_call in tool_calls:
    tool_call_id = tool_call.id
    function_name = tool_call.function.name
    arguments = tool_call.function.arguments
    # Create an OpenAIToolCall object
    tool_call = OpenAIToolCall(
        id=tool_call_id,
        function=OpenAIFunction(name=function_name, arguments=json.loads(arguments) if isinstance(arguments, str) else arguments),
        type="function"
    )
    function_calls.append(tool_call)

# Convert function calls to dictionaries
function_calls = [call.model_dump() for call in function_calls]
 

# Parse and call the functions
results = engine.parse_and_call_functions(function_calls)

# Print the results
for result in results:
    print(result)

# Results should be:
# Search results for shirts
