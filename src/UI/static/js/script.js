const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const robot = document.getElementById('robot');
const robotAccessory = document.getElementById('robot-accessory');

function changeRobotState(state, accessory = '') {
    console.log(`Changing robot state to: ${state} with accessory: ${accessory}`);
    robot.style.animation = `${state} 1s infinite alternate`;
    robotAccessory.style.display = accessory ? 'block' : 'none';
    robotAccessory.textContent = accessory;
}

sendButton.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message) {
        console.log(`User message: ${message}`);
        addMessage(message, true);
        userInput.value = '';

        // User is typing
        changeRobotState('reading', '📖');

        // Send message to the backend
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            console.log(`Received response: ${data.response}`);
            // Bot is thinking
            changeRobotState('thinking', '?');
            setTimeout(() => {
                // Bot is responding
                changeRobotState('responding', '💬');
                addMessage(data.response, false);
                changeRobotState('idle');
            }, 1000);
        })
        .catch(error => console.error('Error:', error));
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
    console.log(`Added message: ${message} (isUser: ${isUser})`);
}