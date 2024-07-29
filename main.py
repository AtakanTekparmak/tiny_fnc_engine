from src.engine import FunctionCallingEngine
import random
from typing import Dict, Any
import json

# Simulated functions for demonstration purposes
def get_random_city() -> str:
    cities = ["New York", "London", "Tokyo", "Paris", "Sydney"]
    return random.choice(cities)

def get_weather_forecast(city: str) -> Dict[str, Any]:
    # This is a mock function. In a real scenario, you'd call an actual weather API.
    weather_conditions = ["Sunny", "Rainy", "Cloudy", "Snowy"]
    temperature = random.randint(0, 35)  # Celsius
    return {
        "city": city,
        "condition": random.choice(weather_conditions),
        "temperature": temperature
    }

def main():
    # Initialize the FunctionCallingEngine
    engine = FunctionCallingEngine()

    # Add functions to the engine
    engine.add_functions([get_random_city, get_weather_forecast])

    # Create string-based function call for get_random_city
    random_city_call = json.dumps({
        'name': 'get_random_city',
        'parameters': {},
        'returns': [{'name': 'city', 'type': 'str'}]
    })

    # Call get_random_city function
    city_result = engine.parse_and_call_functions(random_city_call)[0]
    print(f"Random city selected: {city_result}")

    # Create string-based function call for get_weather_forecast using the result from get_random_city
    weather_forecast_call = json.dumps({
        'name': 'get_weather_forecast',
        'parameters': {'city': city_result},
        'returns': [{'name': 'forecast', 'type': 'dict'}]
    })

    # Call get_weather_forecast function
    forecast_result = engine.parse_and_call_functions(weather_forecast_call)[0]
    print(f"Weather forecast: {forecast_result}")

    # Demonstrate chaining these functions using parse_and_call_functions with a JSON string
    chained_function_calls = json.dumps([
        {
            'name': 'get_random_city',
            'parameters': {},
            'returns': [{'name': 'random_city', 'type': 'str'}]
        },
        {
            'name': 'get_weather_forecast',
            'parameters': {'city': 'random_city'},  # Use the output of get_random_city
            'returns': [{'name': 'forecast', 'type': 'dict'}]
        }
    ])

    print("\nDemonstrating chained function calls:")
    results = engine.parse_and_call_functions(chained_function_calls)
    
    # Print results
    random_city = results[0]
    weather_forecast = results[1]
    print(f"Random city: {random_city}")
    print(f"Weather forecast for {weather_forecast['city']}:")
    print(f"  Condition: {weather_forecast['condition']}")
    print(f"  Temperature: {weather_forecast['temperature']}°C")

if __name__ == "__main__":
    main()