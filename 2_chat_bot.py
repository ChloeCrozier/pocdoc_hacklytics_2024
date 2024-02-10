#HOWDY YA'LL! 

from langchain_openai import OpenAI
from transformers import pipeline
import requests
import aiohttp
import asyncio


API_TOKEN = ("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")
API_URL = "https://api-inference.huggingface.co/models/ThisIs-Developer/Llama-2-GGML-Medical-Chatbot"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

async def query_hf_api_async(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            text = await response.text()
            print("Body:", text[:1000], "...")
            return await response.json()
    

# Initialize the LLM with OpenAI GPT-4
llm = OpenAI(api_key="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")

# Define your tasks
# Initialize the medical question-answering pipeline with Medalpaca

# A mock function to simulate fetching conversational history
# In a real-world scenario, this would fetch history from a database or in-memory store


from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import requests



async def query_hf_api_async(payload):
    async with aiohttp.ClientSession() as session:
        retries = 3  # Maximum number of retries
        wait_time = 5  # Default wait time in seconds, in case estimated_time is not provided
        
        for attempt in range(retries):
            async with session.post(API_URL, headers=headers, json=payload) as response:
                if response.status == 503:  # Model is loading
                    response_json = await response.json()
                    print("Model is loading, waiting for it to be ready...")
                    # Use the estimated_time from the response, if available
                    wait_time = response_json.get("estimated_time", 20)
                    print(f"Waiting for {wait_time} seconds before retrying...")
                    await asyncio.sleep(wait_time)
                elif response.status == 200:  # Success
                    return await response.json()
                else:  # Other errors
                    print(f"Error: Received status code {response.status}")
                    return await response.json()
        print("Maximum retries reached, unable to get a response.")
        return None

# Assuming parse_address and geocode_address functions are defined as before

# Mock function to simulate the execution of tasks in a chain, considering the history-aware approach isn't directly supported here
async def execute_chain_with_history(description):
    severity = await query_hf_api_async(description)
    address = parse_address(description)  # Assuming this function extracts and returns the address correctly
    geocoded_address = geocode_address(address)
    return {
        "severity": severity,
        "geocoded_address": geocoded_address
    }

# Execute the enhanced chain with user input


def parse_address(description):
    prompt = f"Extract the address from the following input: {description}"
    response = llm(prompt)
    print(response)
    return response

def geocode_address(address):
    api_key = "be3896ce2fb6414f8820ebc45cc753ea"
    base_url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": address,
        "apiKey": api_key
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Assuming the first result is the most relevant one
        if data["features"]:
            first_result = data["features"][0]
            coordinates = first_result["geometry"]["coordinates"]
            return {"latitude": coordinates[1], "longitude": coordinates[0]}
        else:
            return "Address not found."
    else:
        return f"Error: {response.status_code}"

# Create the chain
async def main():
    user_description = "I've been having severe headaches and just moved to 123 Main St, Anytown."
    result = await execute_chain_with_history(user_description)
    print("Chain Result:", result)

if __name__ == "__main__":
    asyncio.run(main())


