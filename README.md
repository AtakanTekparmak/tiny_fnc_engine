# tiny_fnc_engine

tiny_fnc_engine is a minimal python library (one file, 177 lines of code) that provides a flexible engine for calling functions extracted from LLM (Large Language Model) outputs in JSON format within an isolated environment. The engine stores functions and their outputs in memory, allowing for chained function calls and parameter referencing.

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
├── src/
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

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/tiny_fnc_engine.git
   cd tiny_fnc_engine
   ```

2. Install dependencies:
   ```
   make install
   ```

## Usage

Run the main script:
```
make run
```

This will demonstrate the usage of tiny_fnc_engine with example functions.

## Running Tests

To run the test suite:
```
make run_tests
```

## Cleaning Up

To remove the virtual environment:
```
make clean
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.