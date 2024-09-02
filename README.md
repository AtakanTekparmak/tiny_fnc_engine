# tiny_fnc_engine

tiny_fnc_engine is a minimal python library ([one file, 212 lines of code](https://github.com/AtakanTekparmak/tiny_fnc_engine/blob/main/tiny_fnc_engine/engine.py)) that provides a flexible engine for calling functions extracted from LLM (Large Language Model) outputs in JSON format. The engine stores functions and their outputs in memory, allowing for chained function calls and parameter referencing. It also supports using Pydantic models for type safety and validation.

## Features

- Add and call functions dynamically
- Parse function calls from JSON format
- Chain multiple function calls
- Store and reference function outputs
- Support for [Pydantic](https://github.com/pydantic/pydantic) models as function parameters and return values
- Reset session to clear stored outputs

## Documentation

The documentation is available at [https://atakantekparmak.github.io/tiny_fnc_engine/](https://atakantekparmak.github.io/tiny_fnc_engine/).

## Warning

Users are responsible for the functions they load in the interpreter.

## Project Structure

```
tiny_fnc_engine/
│
├── tiny_fnc_engine/
│   ├── __init__.py
│   └── engine.py
├── tests/
│   ├── __init__.py
│   └── test_engine.py
├── main.py
├── requirements.txt
├── package_requirements.txt
├── Makefile
└── LICENSE
```

## Requirements

- Python 3.10 or later

## Installation and Usage

### 1. Install from PyPI

1. The package is available on PyPI. You can install it using pip:
```
pip install tiny_fnc_engine
```
2. Then you can use it in your project as follows:
```python
from tiny_fnc_engine import FunctionCallingEngine
from pydantic import BaseModel

# Define a Pydantic model (optional)
class User(BaseModel):
    name: str
    age: int

def get_user() -> User:
    return User(name="Alice", age=30)

def greet_user(user: User) -> str:
    return f"Hello, {user.name}!"

# Initialize the engine and load functions 
engine = FunctionCallingEngine()
engine.add_functions([get_user, greet_user])
# Optionally, you can load functions from a file
# engine.add_functions_from_file('path/to/functions.py')

# Parse and call functions from an example model response
example_response = """
[
    {
        "name": "get_user",
        "parameters": {},
        "returns": [{"name": "user", "type": "User"}]
    },
    {
        "name": "greet_user",
        "parameters": {"user": "user"},  
        "returns": [{"name": "greeting", "type": "str"}]
    }
]
"""
results = engine.parse_and_call_functions(example_response, verbose=True)

# Print the results
print(results)

# Reset the session if needed
engine.reset_session()
```

### 2. Just grab the code

Since all the code in the library is located in [a single file](https://github.com/AtakanTekparmak/tiny_fnc_engine/blob/main/tiny_fnc_engine/engine.py), you can just download it and use it in your project as follows:
```bash
curl -o tiny_fnc_engine.py https://raw.githubusercontent.com/AtakanTekparmak/tiny_fnc_engine/main/tiny_fnc_engine/engine.py
```
and then use it the same way as in the PyPI installation.

### 3. Build from Source
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/tiny_fnc_engine.git
   cd tiny_fnc_engine
   ```

2. Install dependencies:
   ```
   make install
   ```

3. Run the main script:
    ```
    make run
    ```

4. Run the tests:
    ```
    make run_tests
    ```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.