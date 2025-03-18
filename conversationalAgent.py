import os
import json
import requests
import groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

# Initialize Groq client
client = groq.Client(api_key=GROQ_API_KEY)

def get_current_weather(location):
    """Fetch current weather for a location."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    weather_info = data["current"]
    return json.dumps({
        "location": data["location"]["name"],
        "temperature_c": weather_info["temp_c"],
        "temperature_f": weather_info["temp_f"],
        "condition": weather_info["condition"]["text"],
        "humidity": weather_info["humidity"],
        "wind_kph": weather_info["wind_kph"]
    })

def get_weather_forecast(location, days=3):
    """Fetch weather forecast for a location."""
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    forecast_days = data["forecast"]["forecastday"]
    forecast_data = []
    for day in forecast_days:
        forecast_data.append({
            "date": day["date"],
            "max_temp_c": day["day"]["maxtemp_c"],
            "min_temp_c": day["day"]["mintemp_c"],
            "condition": day["day"]["condition"]["text"],
            "chance_of_rain": day["day"]["daily_chance_of_rain"]
        })
    return json.dumps({
        "location": data["location"]["name"],
        "forecast": forecast_data
    })

def calculator(expression):
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def web_search(query):
    """Simulated web search function."""
    search_db = {
        "weather forecast": "Weather forecasts predict atmospheric conditions including temperature, precipitation, and wind.",
        "temperature conversion": "To convert Celsius to Fahrenheit: (C * 9/5) + 32. To convert Fahrenheit to Celsius: (F - 32) * 5/9.",
        "climate change": "Climate change refers to significant changes in climate over several decades, including temperature and precipitation shifts.",
        "severe weather": "Severe weather includes thunderstorms, tornadoes, hurricanes, blizzards, and high winds that can cause damage and loss of life."
    }
    best_match = None
    best_match_score = 0
    for key in search_db:
        # Simple matching algorithm
        words_in_query = set(query.lower().split())
        words_in_key = set(key.lower().split())
        match_score = len(words_in_query.intersection(words_in_key))
        if match_score > best_match_score:
            best_match = key
            best_match_score = match_score
    if best_match_score > 0:
        return json.dumps({"query": query, "result": search_db[best_match]})
    else:
        return json.dumps({"query": query, "result": "No relevant information found."})

# Define tools for Groq API
weather_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA or country e.g., France",
                    },
                },
                "required": ["location"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "Get the weather forecast for a location for a specific number of days",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA or country e.g., France",
                    },
                    "days": {
                        "type": "integer",
                        "description": "The number of days to forecast (1-10)",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["location"],
            },
        },
    },
]

calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Evaluate a mathematical expression",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g., '2 + 2' or '5 * (3 + 2)'",
                }
            },
            "required": ["expression"],
        },
    }
}

search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search for information on the web",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query",
                }
            },
            "required": ["query"],
        },
    }
}

cot_system_message = """You are a helpful assistant that can answer questions about weather and perform calculations.
                        When responding to complex questions, please follow these steps:
                        1. Think step-by-step about what information you need
                        2. Break down the problem into smaller parts
                        3. Use the appropriate tools to gather information
                        4. Explain your reasoning clearly
                        5. Provide a clear final answer
                        
                        IMPORTANT: When you receive information from tools, DO NOT show the raw JSON data to the user.
                        Instead, create natural, conversational responses using the data.
                        
                        For example, instead of showing JSON weather data, say something like:
                        "It's currently 72°F (22°C) and sunny in New York with 45% humidity."
                        
                        For example, if someone asks about temperature conversions or
                        comparisons between cities, first get the weather data, then
                        use the calculator if needed, showing your work in a natural way.
                        """

react_system_message = """You are a helpful weather and information assistant that uses the ReAct (Reasoning and Acting) approach to solve problems.
                          When responding to questions, follow this pattern:
                          1. Thought: Think about what you need to know and what steps to take
                          2. Action: Use a tool to gather information (weather data, search, calculator)
                          3. Observation: Review what you learned from the tool
                          4. ... (repeat the Thought, Action, Observation steps as needed)
                          5. Final Answer: Provide your response based on all observations
                          
                          IMPORTANT: For the final answer to the user, DO NOT show the raw JSON data, the Thought/Action/Observation steps,
                          or any technical details. Instead, create natural, conversational responses using the information you gathered.
                          
                          For example, instead of showing the reasoning process and raw data, your final response might be:
                          "The temperature difference between New York and London today is 15 degrees. New York is currently at 75°F with sunny conditions,
                          while London is experiencing 60°F with light rain."
                          
                          Always make your reasoning explicit during your internal steps, but present only the helpful final answer to the user.
                          """


# Function lookup
available_functions = {
    "get_current_weather": get_current_weather,
    "get_weather_forecast": get_weather_forecast,
    "calculator": calculator,
    "web_search": web_search
}


def process_messages(client, messages, tools=None):
    """Process messages and invoke tools."""
    
    # Step 1: Send the messages to the model with the tool definitions
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        tools=tools,
    )
    response_message = response.choices[0].message
    
    # Step 2: Append the model's response to the conversation
    messages.append(response_message)
    
    # Step 3: Check if the model wanted to use a tool
    if response_message.tool_calls:
        # Step 4: Extract tool invocation and make evaluation
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            
            # Step 5: Extend conversation with function response
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
        
        # Step 6: Get the final response based on tool results
        final_response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            tools=tools,
        )
        final_message = final_response.choices[0].message
        messages.append(final_message)
        
        # Return the final user-facing message
        return messages
    
    # If no tool was called, return the original response
    return messages

def run_conversation(client, system_message):
    """Run a conversation loop."""
    messages = [
        {
            "role": "system",
            "content": system_message
        }
    ]
    
    if choice == 1:
        print("Chatbot: Hello! Ask me about the weather.")
    elif choice == 2:
        print("Chatbot: Hello! Ask me about the weather or calculations.")
    elif choice == 3:
        print("Chatbot: Hello! Ask me about the weather, calculations or general information.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        messages.append(
            {
                "role": "user", 
                "content": user_input
            }
        )
        messages = process_messages(client, messages, tools)
        print(f"Chatbot: {messages[-1].content}")
    return messages

if __name__ == "__main__":
    choice = int(input("Choose agent type \n1: Basic \n2: Chain of Thought \n3: ReAct \n"))

    if choice == 1:
        tools = weather_tools
        system_message = """You are a helpful weather assistant.
                         IMPORTANT: When providing weather information, create natural, conversational responses.
                         DO NOT show raw JSON data to users. Instead, present the information in a friendly,
                         readable format. For example, say "It's currently 72°F and sunny in New York" rather than
                         showing the raw weather data structure."""
    elif choice == 2:
        tools = weather_tools + [calculator_tool]
        system_message = cot_system_message
    elif choice == 3:
        tools = weather_tools + [calculator_tool, search_tool]
        system_message = react_system_message
    else:
        print("Invalid choice. Defaulting to Basic agent.")
        tools = weather_tools
        system_message = """You are a helpful weather assistant.
                         IMPORTANT: Create natural, conversational responses instead of showing raw data."""
        
    run_conversation(client, system_message)