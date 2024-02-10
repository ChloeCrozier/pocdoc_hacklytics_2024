// chat.js
document.getElementById('sendButton').addEventListener('click', () => {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() !== '') {
        displayMessage(userInput, 'user');
        // Simulate a chatbot response
        setTimeout(() => {
            displayMessage(`Analyzing: "${userInput}"...`, 'bot');
            // Here you would typically send the userInput to your backend for processing
        }, 1000);
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
