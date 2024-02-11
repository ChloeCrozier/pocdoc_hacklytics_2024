# app.py (Flask Application)
from flask import Flask, request, jsonify
import asyncio
from your_python_script import interact_with_user, create_medical_assistant  # Import your async function

app = Flask(__name__)

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.json
    user_input = data['userInput']

    # Since Flask doesn't support async views natively, use asyncio to run the async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    assistant = loop.run_until_complete(create_medical_assistant())
    response = loop.run_until_complete(interact_with_user(assistant.id, user_input))
    loop.close()

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
