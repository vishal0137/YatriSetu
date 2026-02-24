// Chatbot Widget Functions
function toggleChatbot() {
    const panel = document.getElementById('chatbotPanel');
    const notification = document.getElementById('chatNotification');
    panel.classList.toggle('active');
    
    if (panel.classList.contains('active')) {
        document.getElementById('chatInput').focus();
        if (notification) notification.style.display = 'none';
    }
}

function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    addChatMessage(message, 'user');
    input.value = '';
    
    const typingIndicator = document.getElementById('typingIndicator');
    typingIndicator.classList.add('active');
    scrollChatToBottom();
    
    fetch('/chatbot/api/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        typingIndicator.classList.remove('active');
        
        if (data.success) {
            addChatMessage(data.response.message, 'bot', data.response.suggestions);
        } else {
            addChatMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    })
    .catch(error => {
        typingIndicator.classList.remove('active');
        addChatMessage('Sorry, I\'m having trouble connecting. Please try again.', 'bot');
    });
}

function addChatMessage(text, sender, suggestions = []) {
    const messagesContainer = document.getElementById('chatbotMessages');
    const typingIndicator = document.getElementById('typingIndicator');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'chat-bubble';
    bubbleDiv.innerHTML = text.replace(/\n/g, '<br>');
    
    messageDiv.appendChild(bubbleDiv);
    
    if (suggestions && suggestions.length > 0 && sender === 'bot') {
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'chat-suggestions';
        
        suggestions.forEach(suggestion => {
            const chip = document.createElement('span');
            chip.className = 'suggestion-chip';
            chip.textContent = suggestion;
            chip.onclick = () => sendQuickMessage(suggestion);
            suggestionsDiv.appendChild(chip);
        });
        
        messageDiv.appendChild(suggestionsDiv);
    }
    
    messagesContainer.insertBefore(messageDiv, typingIndicator);
    scrollChatToBottom();
}

function sendQuickMessage(message) {
    document.getElementById('chatInput').value = message;
    sendChatMessage();
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

function scrollChatToBottom() {
    const messagesContainer = document.getElementById('chatbotMessages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Show notification alert
function showAlert(message, type = 'warning') {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) return;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        <strong>${type === 'warning' ? 'Warning!' : type === 'danger' ? 'Error!' : 'Info:'}</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}
