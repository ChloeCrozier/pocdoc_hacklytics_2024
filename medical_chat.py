
from openai import OpenAI
import json
import aiohttp
import asyncio

client = OpenAI(api_key="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")






def create_medical_assistant_and_thread():
    # Create an assistant
    assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo",  # Use an appropriate model; "text-davinci-003" is an example
    name="Medical Assistant",
    description="A specialized assistant for providing medical information, advice, and insights. Not a substitute for professional medical consultation.",
    instructions="Provide accurate, up-to-date medical information and advice based on user queries. Always remind users to consult a healthcare professional for diagnoses or treatment decisions.",
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

    # Initialize a thread
    thread = client.beta.threads.create()

    return assistant, thread

def interact_with_user(assistant_id, thread_id):
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Add user's message to the thread
        client.beta.threads.messages.create(
            thread_id,
            role='user',
            content=user_input,
        )

        # Create a run instance for the thread
        run = client.beta.threads.runs.create(thread_id, assistant_id=assistant_id)

        # Polling logic for run completion
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id, run.id)
            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(thread_id)
                # Display messages or process further
                break
            asyncio.sleep(1)  # Simple delay for polling

def main():
    assistant, thread = create_medical_assistant_and_thread()
    interact_with_user(assistant.id, thread.id)

if __name__ == "__main__":
    main()


