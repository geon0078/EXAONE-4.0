from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import re

model_name = "LGAI-EXAONE/EXAONE-4.0-1.2B"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="bfloat16",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Check if tokenizer supports tool calling
print("Tokenizer attributes:")
print(f"Has chat_template: {hasattr(tokenizer, 'chat_template')}")
print(f"Chat template: {tokenizer.chat_template if hasattr(tokenizer, 'chat_template') else 'None'}")

# Tool implementations
def get_weather(location):
    """Mock weather API - returns fake weather data"""
    weather_data = {
        "Seoul": "Sunny, 22°C",
        "Tokyo": "Cloudy, 18°C", 
        "New York": "Rainy, 15°C",
        "London": "Foggy, 12°C"
    }
    return weather_data.get(location, f"Weather data not available for {location}")

def calculate(operation, a, b):
    """Simple calculator function"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b != 0:
            return a / b
        else:
            return "Error: Division by zero"
    else:
        return f"Error: Unknown operation {operation}"

# Available tools definition
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The location to get weather for"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "calculate",
            "description": "Perform basic mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "description": "The operation to perform: add, subtract, multiply, divide"},
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["operation", "a", "b"]
            }
        }
    }
]

# Function to execute tool calls
def execute_tool_call(tool_name, arguments):
    """Execute a tool call and return the result"""
    if tool_name == "get_weather":
        return get_weather(**arguments)
    elif tool_name == "calculate":
        return calculate(**arguments)
    else:
        return f"Error: Unknown tool {tool_name}"

# Function to parse tool calls from model output
def parse_tool_calls(text):
    """Extract tool calls from model output"""
    tool_calls = []
    pattern = r'<tool_call>(.*?)</tool_call>'
    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            tool_call = json.loads(match.strip())
            tool_calls.append(tool_call)
        except json.JSONDecodeError:
            print(f"Failed to parse tool call: {match}")
    
    return tool_calls

# Test tool calling with multiple examples
def test_tool_calling(query):
    """Test tool calling with a given query"""
    print(f"\n{'='*50}")
    print(f"Query: {query}")
    print(f"{'='*50}")
    
    messages = [{"role": "user", "content": query}]
    
    # Generate model response
    input_ids = tokenizer.apply_chat_template(
        messages,
        tools=tools,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    )
    
    output = model.generate(
        input_ids.to(model.device),
        max_new_tokens=128,
        do_sample=False,
    )
    
    response = tokenizer.decode(output[0])
    print(f"Model response:\n{response}")
    
    # Parse and execute tool calls
    tool_calls = parse_tool_calls(response)
    
    if tool_calls:
        print(f"\nFound {len(tool_calls)} tool call(s):")
        for i, tool_call in enumerate(tool_calls):
            print(f"Tool call {i+1}: {tool_call}")
            
            tool_name = tool_call.get("name")
            arguments = tool_call.get("arguments", {})
            
            if tool_name:
                try:
                    result = execute_tool_call(tool_name, arguments)
                    print(f"Tool result: {result}")
                except Exception as e:
                    print(f"Error executing tool: {e}")
    else:
        print("No tool calls found in response")

# Run test cases
test_queries = [
    "What's the weather like in Seoul?",
    "Calculate 25 + 17",
    "What's 144 divided by 12?",
    "Show me the weather in Tokyo and calculate 50 * 3"
]

for query in test_queries:
    test_tool_calling(query)