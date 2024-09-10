import ollama
from tiny_fnc_engine import FunctionCallingEngine

# Declare constants
SYSTEM_PTOMPT = """
You are a helpful assistant that provides information about weather and suggests activities. 
You have access to the following functions:
- get_weather(location: str) -> str
- plan_activity(weather: str) -> str
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

# Define functions
def get_weather(location: str) -> str:
    # Simulated weather API call
    return f"Sunny, 25°C in {location}"

def plan_activity(weather: str) -> str:
    # Simulated activity planning based on weather
    return f"Given the weather is {weather}, I recommend going for a picnic."


# Define user message
user_message = "What's the weather like in New York, and what should I do today?"

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
engine.add_functions([get_weather, plan_activity])

# Parse and call the functions
results = engine.parse_and_call_functions(response)

# Print the results
for result in results:
    print(result)

# The results should be similar to:
# Sunny, 25°C in New York
# Given the weather is Sunny, 25°C in New York, I recommend going for a picnic.
