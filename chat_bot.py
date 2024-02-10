#HOWDY YA'LL! 

from langchain.llms import OpenAI
from langchain.chains import Chain
from transformers import pipeline
import requests

# Initialize the LLM with OpenAI GPT-4
llm = OpenAI(api_key="your_openai_api_key")

# Define your tasks
def classify_severity(description):
    pl = pipeline("text-generation", model="medalpaca/medalpaca-13b", tokenizer="medalpaca/medalpaca-13b")

    # Craft your prompt
    description = "The patient reports feeling very thirsty, urinating frequently, and losing weight without trying."
    prompt = f"""
    Based on the medical condition described below, classify the severity into one of the following stages:
    - Stage 1: No complications or problems of minimal severity.
    - Stage 2: Problems limited to a single organ or system; significantly increased risk of complications.
    - Stage 3: Multiple site involvement; generalized systemic involvement; poor prognosis.
    - Stage 4: Death.

    Where the medical condition is a description of what the patient is feeling: {description}
    """

# Generate the answer
    answer = pl(prompt)

def parse_address(description):
    prompt = f"Extract the address from the following input: {description}"
    response = llm(prompt)
    return response

def geocode_address(address):
    api_key = "your_geoapify_api_key"
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
chain = Chain([classify_severity, parse_address, geocode_address])

# Execute the chain with user input
user_description = "I've been having severe headaches and just moved to 123 Main St, Anytown."
result = chain.run(user_description)

