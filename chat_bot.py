#HOWDY YA'LL! 

from langchain_openai import OpenAI
from transformers import pipeline
import requests
import aiohttp
import asyncio

from openai import OpenAI


# API_URL = "https://api-inference.huggingface.co/models/Zabihin/Symptom_to_Diagnosis"
# API_URL = "https://j4xijzwb7kge37vq.us-east-1.aws.endpoints.huggingface.cloud"
API_URL = "https://b2owhcmfemgfhf66.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
	"Accept" : "application/json",
	"Authorization": "Bearer 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",
	"Content-Type": "application/json" 
}

llm = OpenAI(api_key="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")

def classify_severity_with_gpt4(chat_history):
    conversation_context = f"""
    {chat_history}
   
    """
    question = """Given the patient's condition described above, classify the issues into one of the following stages below. 
         Please provide the stage number directly:
    - Stage 1: No complications or problems of minimal severity.
    - Stage 2: Problems limited to a single organ or system; significantly increased risk of complications.
    - Stage 3: Multiple site involvement; generalized systemic involvement; poor prognosis.
    - Stage 4: Death."""

    client = OpenAI(api_key="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")

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a medical assistant."},
        {"role": "user", "content": conversation_context},
        {"role": "system", "content": question}
    ]
    )

    return completion.choices[0].message.content

import requests


async def query_hf_api_async(description):
    payload = {"inputs": description
               }
    async with aiohttp.ClientSession() as session:
        retries = 10  # Maximum number of retries
        wait_time = 20  # Default wait time in seconds, in case estimated_time is not provided
        
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
    diagnosis_payload = {"inputs": description}
    chat_history = await query_hf_api_async(diagnosis_payload)

    print(chat_history)

    # Step 2: Classify Severity with GPT-4
    severity = await classify_severity_with_gpt4(chat_history, description)

    
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
    

    

async def interactive_chat():
    chat_history = ""
    while True:
        user_input = input("You: ")
        if "what is my severity" in user_input.lower():
            # User asks for severity, classify using GPT-4 with the chat history
            severity_response = classify_severity_with_gpt4(chat_history)[0]
            print(f"GPT-4: {severity_response}")
            break  # End the chat after classifying severity
        else:
            # Continue diagnosis conversation with Hugging Face model
            hf_response = await query_hf_api_async(user_input)
            # Update chat history with both user input and model response (simplified for example)
            chat_history += f"User: {user_input}\nHF Model: {hf_response}\n"
            print(f"HF Model: {hf_response}")

async def main():
    await interactive_chat()




# Create the chain
# async def main():
#     user_description = "I've been having severe headaches and throwing up and just moved to 123 Main St, Anytown."
#     prompt = f"""
#     Given the patient's condition described below, diagnose the issue to the best of your ability?
#     {user_description}
#     """

#     payload = {"inputs": prompt}
#     result = await execute_chain_with_history(payload)
#     print("Chain Result:", result)


if __name__ == "__main__":
    asyncio.run(main())


