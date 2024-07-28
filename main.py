from src.engine import FunctionCallingEngine, FunctionCall, Parameter
import random
from typing import Dict, Any

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

    # Create function call for get_random_city
    random_city_call = FunctionCall(
        name='get_random_city',
        parameters={},
        returns=[Parameter(name='city', type='str')]
    )

    # Call get_random_city function
    city_result = engine.call_function(random_city_call)
    print(f"Random city selected: {city_result}")

    # Create function call for get_weather_forecast using the result from get_random_city
    weather_forecast_call = FunctionCall(
        name='get_weather_forecast',
        parameters={'city': city_result},
        returns=[Parameter(name='forecast', type='dict')]
    )

    # Call get_weather_forecast function
    forecast_result = engine.call_function(weather_forecast_call)
    print(f"Weather forecast: {forecast_result}")

    # Demonstrate chaining these functions using parse_and_call_functions
    chained_function_calls = [
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
    ]

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