function addMessage(role, text, avatar) {
    const chatContainer = document.getElementById('chat');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', role.toLowerCase());

    const avatarDiv = document.createElement('div');
    avatarDiv.classList.add('avatar');
    avatarDiv.style.backgroundImage = `url('${avatar}')`;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('bubble');
    bubbleDiv.textContent = text;

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(bubbleDiv);

    chatContainer.appendChild(messageDiv);

    const maxMessages = 8;
    while (chatContainer.children.length > maxMessages) {
        chatContainer.removeChild(chatContainer.firstChild);
    }

    chatContainer.scrollTop = chatContainer.scrollHeight;
}
