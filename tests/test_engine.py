import unittest
from typing import Dict, Any, Union
import sys
import os
import tempfile
import json

# Add the tiny_fnc_engine directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tiny_fnc_engine')))

from tiny_fnc_engine.engine import FunctionCallingEngine, FunctionCall, Parameter
from pydantic import BaseModel

def helper_function(a: int, b: int) -> int:
    return a + b

def helper_function_with_dict(data: Union[Dict[str, Any], BaseModel]) -> str:
    if isinstance(data, Person):
        return f"Name: {data.name}, Age: {data.age}"
    elif isinstance(data, dict):
        return f"Name: {data['name']}, Age: {data['age']}"
    else:
        raise ValueError("Invalid data type")

class Person(BaseModel):
    name: str
    age: int

class TestFunctionCallingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FunctionCallingEngine()
        self.engine.add_functions([helper_function, helper_function_with_dict])

    def tearDown(self):
        self.engine.reset_session()

    def test_call_function(self):
        function_call = FunctionCall(
            name='helper_function',
            parameters={'a': 2, 'b': 3},
            returns=[Parameter(name='result', type='int')]
        )
        result = self.engine.call_function(function_call)
        self.assertEqual(result, 5)
        self.assertEqual(self.engine.outputs['result'], 5)  # Check for 'result' key instead of 'helper_function'

    def test_call_functions(self):
        function_calls = [
            FunctionCall(
                name='helper_function',
                parameters={'a': 2, 'b': 3},
                returns=[Parameter(name='result1', type='int')]
            ),
            FunctionCall(
                name='helper_function_with_dict',
                parameters={'data': {'name': 'Alice', 'age': 30}},
                returns=[Parameter(name='result2', type='str')]
            )
        ]
        results = self.engine.call_functions(function_calls)
        self.assertEqual(results, [5, "Name: Alice, Age: 30"])
        self.assertEqual(self.engine.outputs['result1'], 5)
        self.assertEqual(self.engine.outputs['result2'], "Name: Alice, Age: 30")

    def test_parse_function_calls_single_dict(self):
        function_call = {
            'name': 'helper_function',
            'parameters': {'a': 2, 'b': 3},
            'returns': [{'name': 'result', 'type': 'int'}]
        }
        parsed = self.engine.parse_function_calls(function_call)
        self.assertIsInstance(parsed[0], FunctionCall)
        self.assertEqual(parsed[0].name, 'helper_function')

    def test_parse_function_calls_list_of_dicts(self):
        function_calls = [
            {
                'name': 'helper_function',
                'parameters': {'a': 2, 'b': 3},
                'returns': [{'name': 'result1', 'type': 'int'}]
            },
            {
                'name': 'helper_function_with_dict',
                'parameters': {'data': {'name': 'Alice', 'age': 30}},
                'returns': [{'name': 'result2', 'type': 'str'}]
            }
        ]
        parsed = self.engine.parse_function_calls(function_calls)
        self.assertEqual(len(parsed), 2)
        self.assertIsInstance(parsed[0], FunctionCall)
        self.assertIsInstance(parsed[1], FunctionCall)

    def test_parse_function_calls_invalid_input(self):
        with self.assertRaises(ValueError) as context:
            self.engine.parse_function_calls({'invalid': 'format'})
        self.assertIn("The function call is invalid", str(context.exception))

    def test_parse_function_calls_invalid_type(self):
        with self.assertRaises(TypeError):
            self.engine.parse_function_calls("not a dict or list")

    def test_parse_and_call_functions(self):
        function_calls = [
            {
                'name': 'helper_function',
                'parameters': {'a': 2, 'b': 3},
                'returns': [{'name': 'result1', 'type': 'int'}]
            },
            {
                'name': 'helper_function_with_dict',
                'parameters': {'data': {'name': 'Alice', 'age': 30}},
                'returns': [{'name': 'result2', 'type': 'str'}]
            }
        ]
        results = self.engine.parse_and_call_functions(function_calls)
        self.assertEqual(results, [5, "Name: Alice, Age: 30"])
        self.assertEqual(self.engine.outputs['result1'], 5)
        self.assertEqual(self.engine.outputs['result2'], "Name: Alice, Age: 30")

    def test_function_not_found(self):
        function_call = FunctionCall(
            name='non_existent_function',
            parameters={'a': 1},
            returns=[Parameter(name='result', type='int')]
        )
        with self.assertRaises(KeyError):
            self.engine.call_function(function_call)

    def test_add_functions_from_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write("""
import math

def circle_area(radius):
    return math.pi * radius ** 2

def square_area(side):
    return side ** 2
            """)
        
        temp_file_path = temp_file.name
        temp_file.close()  # Close the file to ensure it's written to disk
        
        try:
            self.engine.add_functions_from_file(temp_file_path)
            
            self.assertIn('circle_area', self.engine.functions)
            self.assertIn('square_area', self.engine.functions)
            
            circle_result = self.engine.call_function(FunctionCall(
                name='circle_area',
                parameters={'radius': 2},
                returns=[Parameter(name='result', type='float')]
            ))
            self.assertAlmostEqual(circle_result, 12.566370614359172)

            square_result = self.engine.call_function(FunctionCall(
                name='square_area',
                parameters={'side': 4},
                returns=[Parameter(name='result', type='int')]
            ))
            self.assertEqual(square_result, 16)
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_add_functions_from_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.engine.add_functions_from_file('non_existent_file.py')

    def test_parse_and_call_functions_dict(self):
        function_call = {
            'name': 'helper_function',
            'parameters': {'a': 2, 'b': 3},
            'returns': [{'name': 'result', 'type': 'int'}]
        }
        result = self.engine.parse_and_call_functions(function_call)
        self.assertEqual(result, [5])

    def test_parse_and_call_functions_list(self):
        function_calls = [
            {
                'name': 'helper_function',
                'parameters': {'a': 2, 'b': 3},
                'returns': [{'name': 'result1', 'type': 'int'}]
            },
            {
                'name': 'helper_function_with_dict',
                'parameters': {'data': {'name': 'Alice', 'age': 30}},
                'returns': [{'name': 'result2', 'type': 'str'}]
            }
        ]
        results = self.engine.parse_and_call_functions(function_calls)
        self.assertEqual(results, [5, "Name: Alice, Age: 30"])

    def test_parse_and_call_functions_json_string(self):
        json_string = json.dumps({
            'name': 'helper_function',
            'parameters': {'a': 4, 'b': 5},
            'returns': [{'name': 'result', 'type': 'int'}]
        })
        result = self.engine.parse_and_call_functions(json_string)
        self.assertEqual(result, [9])

    def test_parse_and_call_functions_json_string_list(self):
        json_string = json.dumps([
            {
                'name': 'helper_function',
                'parameters': {'a': 4, 'b': 5},
                'returns': [{'name': 'result1', 'type': 'int'}]
            },
            {
                'name': 'helper_function_with_dict',
                'parameters': {'data': {'name': 'Bob', 'age': 25}},
                'returns': [{'name': 'result2', 'type': 'str'}]
            }
        ])
        results = self.engine.parse_and_call_functions(json_string)
        self.assertEqual(results, [9, "Name: Bob, Age: 25"])

    def test_parse_and_call_functions_verbose(self):
        function_call = {
            'name': 'helper_function',
            'parameters': {'a': 2, 'b': 3},
            'returns': [{'name': 'result', 'type': 'int'}]
        }
        
        # Redirect stdout to capture print statements
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.engine.parse_and_call_functions(function_call, verbose=True)
        
        output = f.getvalue()
        self.assertIn("Calling function: helper_function", output)
        self.assertIn("Parameters: {'a': 2, 'b': 3}", output)
        self.assertIn("Returns: [Parameter(name='result', type='int')]", output)

    def test_call_function_with_pydantic_model(self):
        function_call = FunctionCall(
            name='helper_function_with_dict',
            parameters={'data': Person(name='Alice', age=30)},
            returns=[Parameter(name='result', type='str')]
        )
        result = self.engine.call_function(function_call)
        self.assertEqual(result, "Name: Alice, Age: 30")
        self.assertEqual(self.engine.outputs['result'], "Name: Alice, Age: 30")

    def test_parse_and_call_functions_with_pydantic_model_as_json(self):
        json_string = json.dumps({
            'name': 'helper_function_with_dict',
            'parameters': {'data': {'name': 'Alice', 'age': 30}},
            'returns': [{'name': 'result', 'type': 'str'}]
        })
        result = self.engine.parse_and_call_functions(json_string)
        self.assertEqual(result, ["Name: Alice, Age: 30"])

    def test_reset_session(self):
        function_call = FunctionCall(
            name='helper_function',
            parameters={'a': 2, 'b': 3},
            returns=[Parameter(name='result', type='int')]
        )
        self.engine.call_function(function_call)
        self.assertEqual(self.engine.outputs['result'], 5)
        
        self.engine.reset_session()
        self.assertEqual(self.engine.outputs, {})

    def test_chained_function_calls(self):
        function_calls = [
            {
                'name': 'helper_function',
                'parameters': {'a': 2, 'b': 3},
                'returns': [{'name': 'sum', 'type': 'int'}]
            },
            {
                'name': 'helper_function',
                'parameters': {'a': 'sum', 'b': 4},
                'returns': [{'name': 'final_result', 'type': 'int'}]
            }
        ]
        results = self.engine.parse_and_call_functions(function_calls)
        self.assertEqual(results, [5, 9])
        self.assertEqual(self.engine.outputs['sum'], 5)
        self.assertEqual(self.engine.outputs['final_result'], 9)

    def test_parse_openai_tool_call(self):
        tool_calls = [
            {   
                "id": "call_FthC9qRpsL5kBpwwyw6c7j4k",
                "function": {
                        "arguments": '{"location": "San Francisco, CA"}',
                        "name": "get_rain_probability"
                },
                "type": "function"
            }
        ]
        parsed = self.engine.parse_function_calls(tool_calls)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0].name, 'get_rain_probability')
        self.assertEqual(parsed[0].parameters, {"location": "San Francisco, CA"})

    def test_parse_and_call_openai_tool_call(self):
        def get_rain_probability(location: str) -> str:
            return f"Rain probability for {location} is 20%"

        self.engine.add_functions([get_rain_probability])

        tool_call = [
            {
                "id": "call_FthC9qRpsL5kBpwwyw6c7j4k",
                "function": {
                    "arguments": '{"location": "San Francisco, CA"}',
                    "name": "get_rain_probability"
                },
                "type": "function"
            }
        ]
        results = self.engine.parse_and_call_functions(tool_call)
        self.assertEqual(results, ["Rain probability for San Francisco, CA is 20%"])

    def test_parse_and_call_openai_tool_call_multiple(self):
        def get_rain_probability(location: str) -> str:
            return f"Rain probability for {location} is 20%"

        def get_temperature(location: str) -> str:
            return f"Temperature for {location} is 68°F"

        self.engine.add_functions([get_rain_probability, get_temperature])

        tool_calls = [
            {
                "id": "call_1",
                "function": {
                    "arguments": '{"location": "San Francisco, CA"}',
                    "name": "get_rain_probability"
                },
                "type": "function"
            },
            {
                "id": "call_2",
                "function": {
                    "arguments": '{"location": "San Francisco, CA"}',
                    "name": "get_temperature"
                },
                "type": "function"
            }
        ]
        results = self.engine.parse_and_call_functions(tool_calls)
        self.assertEqual(results, [
            "Rain probability for San Francisco, CA is 20%",
            "Temperature for San Francisco, CA is 68°F"
        ])

    def test_parse_and_call_openai_tool_call_with_pydantic_model(self):
        tool_calls = [
            {
                "id": "call_1",
                "function": {
                    "arguments": '{"data": {"name": "Alice", "age": 30}}',
                    "name": "helper_function_with_dict"
                },
                "type": "function"
            }
        ]
        results = self.engine.parse_and_call_functions(tool_calls)
        self.assertEqual(results, ["Name: Alice, Age: 30"])

if __name__ == '__main__':
    unittest.main()