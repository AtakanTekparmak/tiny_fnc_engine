# tiny_fnc_engine

tiny_fnc_engine is a minimal python library ([one file, 177 lines of code](https://github.com/AtakanTekparmak/tiny_fnc_engine/blob/main/tiny_fnc_engine/engine.py)) that provides a flexible engine for calling functions extracted from LLM (Large Language Model) outputs in JSON format within an isolated environment. The engine stores functions and their outputs in memory, allowing for chained function calls and parameter referencing.

## Features

- Add and call functions dynamically
- Parse function calls from JSON format
- Chain multiple function calls
- Store and reference function outputs
- Isolated execution environment

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
├── Makefile
└── LICENSE
```

## Installation and Usage

### 1. Install from PyPI

1. The package is available on PyPI. You can install it using pip:
```
pip install tiny_fnc_engine
```
2. Then you can use it in your project as follows:
```python
from tiny_fnc_engine import FunctionCallingEngine

# Initialize the engine and load functions from a python file
engine = FunctionCallingEngine()
engine.add_functions_from_file('path/to/functions.py')

# Parse and call functions from an example model response
example_response = """
[
    {
        "name": "get_random_city",
        "parameters": {},
        "returns": [{"name": "random_city", "type": "str"}]
    },
    {
        "name": "get_weather_forecast",
        "parameters": {"city": "random_city"},  
        "returns": [{"name": "forecast", "type": "dict"}]
    }
]
"""
results = engine.parse_and_call_functions(example_response)

# Print the results
print(results)
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