# JOEAI

Weather and Information Assistant
This project is a conversational AI assistant powered by the Groq API. It can provide weather information, perform calculations, and answer general knowledge questions using a combination of function calling and reasoning techniques like Chain of Thought (CoT) and ReAct.

Features
Weather Information:

Get the current weather for a specific location.

Fetch a weather forecast for up to 10 days.

Calculations:

Evaluate mathematical expressions (e.g., 2 + 2, 5 * (3 + 2)).

General Knowledge:

Simulated web search for topics like weather forecasts, temperature conversions, and climate change.

Reasoning Modes:

Basic Mode: Simple weather assistant.

Chain of Thought (CoT): Breaks down complex queries into step-by-step reasoning.

ReAct Mode: Uses a reasoning-action loop to solve problems.

Setup
Prerequisites
Python 3.8+: Ensure Python is installed on your system.

API Keys:

Groq API Key: Sign up at Groq to get your API key.

WeatherAPI Key: Sign up at WeatherAPI to get your API key.

Installation
Clone the repository:

bash
Copy
git clone https://github.com/yourusername/weather-assistant.git
cd weather-assistant
Install dependencies:

bash
Copy
pip install -r requirements.txt
Create a .env file in the project root and add your API keys:

plaintext
Copy
GROQ_API_KEY=your_groq_api_key
WEATHER_API_KEY=your_weatherapi_key
LLM_MODEL=mixtral-8x7b-32768
Running the Assistant
Start the assistant:

bash
Copy
python main.py
Choose the agent type:

1: Basic: Weather assistant.

2: Chain of Thought: Weather and calculations with step-by-step reasoning.

3: ReAct: Weather, calculations, and general knowledge with reasoning-action loops.

Interact with the assistant:

Ask questions like:

"What's the weather like in New York?"

"What's the temperature difference between London and Paris?"

"Calculate 2 + 2."

"Tell me about climate change."

Exit the conversation by typing exit, quit, or bye.

Example Usage
Basic Mode
plaintext
Copy
Chatbot: Hello! Ask me about the weather.
You: What's the weather like in San Francisco?
Chatbot: It's currently 68°F (20°C) and sunny in San Francisco with 60% humidity.
Chain of Thought Mode
plaintext
Copy
Chatbot: Hello! Ask me about the weather or calculations.
You: What's the temperature difference between New York and London today?
Chatbot: Let me break this down step by step:
        1. First, I'll get the current temperature in New York.
        2. Then, I'll get the current temperature in London.
        3. Finally, I'll calculate the difference.
        It's currently 75°F in New York and 60°F in London. The temperature difference is 15°F.
ReAct Mode
plaintext
Copy
Chatbot: Hello! Ask me about the weather, calculations, or general information.
You: How do I convert 30°C to Fahrenheit?
Chatbot: Let me think:
        1. Thought: I need to use the formula for Celsius to Fahrenheit conversion.
        2. Action: Use the calculator to evaluate (30 * 9/5) + 32.
        3. Observation: The result is 86°F.
        30°C is equivalent to 86°F.
Tools and Functions
The assistant uses the following tools:

Weather Tools:

get_current_weather(location): Fetches current weather data.

get_weather_forecast(location, days): Fetches a weather forecast.

Calculator Tool:

calculator(expression): Evaluates mathematical expressions.

Web Search Tool:

web_search(query): Simulates a web search for general knowledge.

Configuration
Environment Variables:

GROQ_API_KEY: Your Groq API key.

WEATHER_API_KEY: Your WeatherAPI key.

LLM_MODEL: The Groq model to use (default: mixtral-8x7b-32768).

System Messages:

Customize the assistant's behavior by modifying the system_message in the code.

Dependencies
groq: Groq API client.

requests: For making HTTP requests to WeatherAPI.

python-dotenv: For loading environment variables from a .env file.
