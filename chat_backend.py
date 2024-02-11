from flask import Flask, request, jsonify
import asyncio
from final_chat import create_medical_assistant, interact_with_user # Import your async functions

app = Flask(__name__)

# Initialize your OpenAI assistant (consider doing this inside the route if it needs to be dynamic)
assistant = asyncio.run(create_medical_assistant())

@app.route('http://localhost:5000//analyze', methods=['POST'])
def analyze_input():
    data = request.json
    user_input = data['userInput']
    
    # Since Flask doesn't support async handlers by default, we use asyncio.run
    # Be cautious with asyncio.run() in production with Flask, consider using Quart or another async web framework
    response = asyncio.run(interact_with_user(assistant.id, user_input))
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)