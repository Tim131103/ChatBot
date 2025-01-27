const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const robot = document.getElementById('robot');
const robotAccessory = document.getElementById('robot-accessory');

function changeRobotState(state, accessory = '') {
    robot.style.animation = `${state} 1s infinite alternate`;
    robotAccessory.style.display = accessory ? 'block' : 'none';
    robotAccessory.textContent = accessory;
}

sendButton.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message) {
        // User is typing
        changeRobotState('reading', '📖');
        setTimeout(() => {
            // Bot is thinking
            changeRobotState('thinking', '?');
            setTimeout(() => {
                // Bot is responding
                changeRobotState('responding', '💬');
                addMessage('Ich bin der Chatbot. Wie kann ich Ihnen helfen?', false);
                changeRobotState('idle');
            }, 2000);
        }, 1000);
        addMessage(message, true);
        userInput.value = '';
    }
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});

function addMessage(message, isUser) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', isUser ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}