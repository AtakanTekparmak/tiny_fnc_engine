import unittest
from typing import Dict, Any
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.engine import FunctionCallingEngine, FunctionCall, Parameter

def helper_function(a: int, b: int) -> int:
    return a + b

def helper_function_with_dict(data: Dict[str, Any]) -> str:
    return f"Name: {data['name']}, Age: {data['age']}"

class TestFunctionCallingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FunctionCallingEngine()
        self.engine.add_functions([helper_function, helper_function_with_dict])

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
        with self.assertRaises(ValueError):
            self.engine.parse_function_calls({'invalid': 'format'})

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

if __name__ == '__main__':
    unittest.main()