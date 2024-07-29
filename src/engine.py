from typing import Optional, Union
import importlib.util
import os
import json

from pydantic import BaseModel

# Declare type aliases
ValidParameter = Union[str, int, float, bool, dict, list]
ValidOutput = ValidParameter

# Declare constants
INVALID_FUNCTION_CALL_ERROR = """
The function call is invalid. The parameter must be a either a
dictionary or a list of dictionaries, following a JSON schema
where "returns" is optional. The schema is as follows:

{
    "name": "function_name",
    "parameters": [
        {
            "name": "parameter_name",
            "type": "parameter_type"
        }
    ],
    "returns": [
        {
            "name": "return_name",
            "type": "return_type"
        }
    ]
}
"""

class Parameter(BaseModel):
    """
    Schema for the parameters of a function
    schema and function call. Used in the fields
    parameters and returns.

    name: str
        The name of the parameter.
    type: str
        The type of the parameter.
    """
    name: str
    type: str

class FunctionCall(BaseModel):
    """
    Schema for the function call.

    name: str
        The name of the function.
    parameters: list[Parameter]
        The parameters of the function.
    returns: Optional[list[Parameter]]
        The return values of the function. If the
        used function call format does not support
        the "returns" field, this schema will still
        be valid.

    """
    name: str
    parameters: dict[str, ValidParameter]
    returns: Optional[list[Parameter]] = None

class FunctionCallingEngine:
    """
    Engine to call functions extracted 
    from LLM outputs in JSON format in
    an isolated environment. The engine
    will store the functions and their
    outputs in memory. 
    """
    def __init__(self):
        self.functions = {}
        self.outputs = {}

    def reset_session(self) -> None:
        """
        Reset the session of the engine.
        """
        self.outputs = {}
    
    def add_functions(self, functions: list[callable]) -> None:
        """
        Add functions to the engine.

        functions: list[callable]
            List of functions to be added to the engine.
        """
        for function in functions:
            self.functions[function.__name__] = function

    def add_functions_from_file(self, file_path: str) -> None:
        """
        Add functions to the engine from a specified .py file.

        file_path: str
            The path to the .py file containing the functions to be added.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")

        # Use importlib.util to load the module
        module_name = os.path.basename(file_path).split('.')[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the user defined functions
        for name, obj in module.__dict__.items():
            if callable(obj) and not name.startswith("__") and name != "add_functions_from_file":
                self.functions[name] = obj

    def call_function(self, function_call: FunctionCall) -> ValidOutput:
        """
        Call a function from the engine.

        function_call: FunctionCall
            The function call to be executed.
        """
        # Get the function and its parameters
        function = self.functions[function_call.name]
        parameters = function_call.parameters  # This is already a dict, no need to process it

        # Check if any of the parameters are outputs from previous functions
        for key, value in parameters.items():
            if isinstance(value, str) and value in self.outputs:
                parameters[key] = self.outputs[value]

        # Call the function
        output = function(**parameters)  # Use ** to unpack the dictionary as keyword arguments

        # Store the output
        if len(function_call.returns) == 1:
            self.outputs[function_call.returns[0].name] = output
        elif len(function_call.returns) > 1:
            for i, return_value in enumerate(function_call.returns):
                self.outputs[return_value.name] = output[i]
        else:
            raise ValueError(INVALID_FUNCTION_CALL_ERROR)
        
        return output
    
    def call_functions(self, function_calls: list[FunctionCall]) -> list[ValidOutput]:
        """
        Call multiple functions from the engine.

        function_calls: list[FunctionCall]
            The function calls to be executed.
        """
        outputs = []
        for function_call in function_calls:
            output = self.call_function(function_call)
            outputs.append(output)
        return outputs
    
    def parse_function_calls(self, function_calls: Union[dict, list[dict]]) -> list[FunctionCall]:
        """
        Parse either a single function call or
        a list of function calls.

        function_calls: Union[dict, list[dict]]
            The function call(s) to be parsed.
        """
        if isinstance(function_calls, dict):
            try:
                return [FunctionCall(**function_calls)]
            except Exception as _:
                raise ValueError(INVALID_FUNCTION_CALL_ERROR)
        elif isinstance(function_calls, list):
            try:
                return [FunctionCall(**function_call) for function_call in function_calls]
            except Exception as _:
                raise ValueError(INVALID_FUNCTION_CALL_ERROR)
        else:
            raise TypeError(INVALID_FUNCTION_CALL_ERROR)
        
    def parse_and_call_functions(
            self, 
            function_calls: Union[dict, list[dict], str],
            verbose: bool = False
        ) -> list[ValidOutput]:
        """
        Parse and call either a single function call or
        a list of function calls.

        function_calls: Union[dict, list[dict]]
            The function call(s) to be parsed and called.
        """
        if isinstance(function_calls, str): 
            function_calls = json.loads(function_calls)

        function_calls = self.parse_function_calls(function_calls)

        if verbose:
            for function_call in function_calls:
                print(f"Calling function: {function_call.name}")
                print(f"Parameters: {function_call.parameters}")
                print(f"Returns: {function_call.returns}")

        return self.call_functions(function_calls)
        