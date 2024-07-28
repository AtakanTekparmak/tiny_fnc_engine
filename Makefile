# Set default target
.DEFAULT_GOAL := help

# Variables

## Python
PYTHON := python3
PIP := pip
VENV_NAME := venv

# .env file
ENV_FILE := .env

# Help target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  1. install           Install dependencies and set up the environment (should be run first)"
	@echo "  2. run               Run the main.py script 
	@echo "  3. run_tests         Run the tests"
	@echo "  4. clean             Remove the virtual environment and its contents"

# Install dependencies and set up the environment
install: 
	$(PYTHON) -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && \
	$(PIP) install -r requirements.txt 

# Run the main.py script
run: 
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py

# Run the tests
run_tests:
	. $(VENV_NAME)/bin/activate && \
	pytest tests/test_engine.py
# Clean the virtual environment
clean:
	rm -rf $(VENV_NAME)