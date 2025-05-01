const chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/' + roomId + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageElement = document.createElement('div');
    messageElement.classList.add('mb-2');
    messageElement.innerHTML = `
        <strong>${data.sender}</strong>
        <small class="text-muted">${data.timestamp}</small>
        <div>${data.message}</div>
    `;
    document.querySelector('#chat-messages').appendChild(messageElement);
};

document.querySelector('#chat-form').onsubmit = function(e) {
    e.preventDefault();
    const messageInput = document.querySelector('textarea[name="content"]');
    const message = messageInput.value;
    
    chatSocket.send(JSON.stringify({
        'message': message,
        'sender_id': currentUserId
    }));
    
    messageInput.value = '';
};