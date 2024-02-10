import asyncio
from openai import OpenAI
import requests
from datetime import datetime
client = OpenAI(api_key="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")

llm = OpenAI(api_key="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")

async def create_medical_assistant():
    assistant =client.beta.assistants.create(
model="gpt-3.5-turbo",  # Use an appropriate model; "text-davinci-003" is an example
name="Medical Assistant",
description="A specialized assistant for providing medical information, advice, and insights. Always remind users that this is a traige.",
instructions="Analyze user-reported symptoms to provide possible diagnoses or health insights.",
tools=[
    {
        "type": "function",
        "function": {
            "name": "fetch_medical_guidelines",
            "description": "Fetches the latest medical guidelines and information relevant to the user's query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The medical query or topic for which guidelines are requested."
                    }
                },
                "required": ["query"]
            }
        }
    },
    # You can define additional tools here as needed
]

)
    return assistant

async def create_thread():
    thread = client.beta.threads.create()  # This should be adjusted if client.Thread.create is not the correct call
    return thread.id 

async def add_message_to_thread(thread_id, message_content):
    # Ensure this is an async call or properly awaited if necessary
    message = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=message_content)
    return message

async def create_run(assistant_id, thread_id):
    # Assuming synchronous call for simplicity
    return client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

async def poll_run_status(thread_id, run_id):
    while True:
        run_status = client.beta.threads.runs.retrieve(run_id=run_id, thread_id=thread_id)
        if run_status.status == 'completed':
            break
        elif run_status.status in ['failed', 'cancelled']:
            print(f"Run ended with status: {run_status.status}")
            return
        await asyncio.sleep(1)  # Sleep for a bit before polling again

    

async def display_thread_messages(thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for message in messages.data:
        print(f"{message.role.capitalize()}: {message.content}")

async def interact_with_user(assistant_id):
    print("Hello, how are you feeling and where are you located?")
    count = 0
    

    thread_id = await create_thread()

    while True:
        user_input = input("You: ")
        if count == 0:
            address = await parse_address(user_input)
            print(f"Extracted Address: {address}")
            geocoded_address = await geocode_address(address)
            print(f"Geocoded Address: {geocoded_address}")
            count += 1
        if user_input.lower() == "what is my severity level":
            chat_history_messages = client.beta.threads.messages.list(thread_id)
            chat_history = "\n".join([f"{msg.role.capitalize()}: {msg.content}" for msg in chat_history_messages])

            severity = classify_severity_with_gpt4(chat_history)
            print(f"Severity: {severity}, Geocoded Address: {geocoded_address}, Time: {datetime.now().isoformat()}")
            
            return {"severity": severity, "address": address, "geocoded_address": geocoded_address, "time": datetime.now().isoformat()}
            
            

        await add_message_to_thread(thread_id, user_input)
        run_info = await create_run(assistant_id, thread_id)
        await poll_run_status(thread_id, run_info.id)
        await display_thread_messages(thread_id)
        
       



async def parse_address(description):
    prompt = f"Extract the address from the following input: {description}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            
        ]
    )
    address = response.choices[0].message.content
    return address

async def geocode_address(address):
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
    # return response.choices[0].text.strip()

async def main():
    assistant = await create_medical_assistant()
    return await interact_with_user(assistant.id)

if __name__ == "__main__":
    asyncio.run(main())
