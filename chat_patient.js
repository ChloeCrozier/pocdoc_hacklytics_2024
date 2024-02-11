
document.getElementById('sendButton').addEventListener('click', () => {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() !== '') {
        displayMessage(userInput, 'user');
        
        // Send userInput to Flask endpoint
        fetch('/process_input', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userInput: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Display bot response
            displayMessage(data.message, 'bot');  // Adjust according to the actual response format
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});


function displayMessage(message, sender) {
    const chatbox = document.getElementById('chatbox');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.className = sender === 'user' ? 'text-right' : 'text-left';
    chatbox.appendChild(messageElement);
    // Scroll to the latest message
    chatbox.scrollTop = chatbox.scrollHeight;
}
