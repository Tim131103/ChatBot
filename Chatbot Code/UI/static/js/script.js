// DOM elements for chat interaction
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

/**
 * Add a message to the chat interface.
 * @param {string} message - The message text.
 * @param {boolean} isUser - Whether the message is from the user.
 */
function addMessage(message, isUser) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', isUser ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Event listener for the send button
sendButton.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, true);
        userInput.value = '';
        // Simulate chatbot response
        setTimeout(() => {
            addMessage('Ich bin der Chatbot. Wie kann ich Ihnen helfen?', false);
        }, 1000);
    }
});

// Event listener for the Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});