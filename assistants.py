from openai import OpenAI
import asyncio
import time
client = OpenAI(api_key="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")


assistant =client.beta.assistants.create(
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
    

async def create_thread_and_run(assistant_id):
    # Create a thread
    thread = client.beta.threads.create()

    # Run the thread with an assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    return thread.id, run.id

async def add_message_to_thread(thread_id, message_content):
    # Adapt this based on actual usage; assuming synchronous call for simplicity
    return client.Message.create(thread_id=thread_id, role="user", content=message_content)

async def create_run(assistant_id, thread_id):
    # Assuming synchronous call for simplicity
    return client.Run.create(thread_id=thread_id, assistant_id=assistant_id)

async def poll_run_status(thread_id, run_id):
    # Initial wait time in seconds, this could be adjusted based on your needs
    wait_time = 5

    while True:
        run = client.beta.threads.runs.retrieve(run_id, thread_id=thread_id)
        status = run.status

        if status in ['completed', 'failed', 'cancelled']:
            print(f"Run completed with status: {status}")
            if status == 'completed':
                # Fetch all messages from the thread
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                for message in messages.data:
                    print(f"{message.role.capitalize()}: {message.content}")
            break
        elif status == 'requires_action':
            # Handle required action for function calls if applicable
            print("Run requires action.")
            # Implement action handling logic here
            break
        else:
            print(f"Run is {status}, waiting for {wait_time} seconds...")
            time.sleep(wait_time)

async def interact_with_user(assistant_id):
    thread = await create_thread_and_run()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting.")
            break
        await add_message_to_thread(thread.id, user_input)
        run = await create_run(assistant_id, thread.id)
        await poll_run_status(thread.id, run.id)

async def main():
    assistant_id = assistant.id
    thread_id, run_id = await create_thread_and_run(assistant_id)
    await poll_run_status(thread_id, run_id)
    

if __name__ == "__main__":
    asyncio.run(main())
