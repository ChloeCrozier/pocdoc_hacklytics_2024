document.getElementById('sendButton').addEventListener('click', async () => {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() !== '') {
        displayMessage(userInput, 'user');
        
        // Send userInput to the Flask backend
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userInput })
        });
        const data = await response.json();
        
        // Display bot response
        displayMessage(data.message, 'bot'); // Adjust according to the response structure
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
