// Function to handle sending messages and receiving responses
async function sendMessage() {
    const input = document.getElementById('message-input');
    const messagesContainer = document.getElementById('messages');

    // Get the message content from the input field
    const messageContent = input.value.trim();
    if (messageContent === '') {
        return; // Don't send empty messages
    }

    // Append the user's message to the chat interface
    messagesContainer.innerHTML += `<div>User: ${messageContent}</div>`;

    // Send the message to the server
    try {
        const response = await fetch('/chat-with-assistant/', { // Make sure this URL matches your Django view URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Fetch the CSRF token
            },
            body: JSON.stringify({ message: messageContent })
        });

        const data = await response.json();

        // Append the AI's response to the chat
        if (data.response) {
            messagesContainer.innerHTML += `<div>AI: ${data.response}</div>`;
        } else {
            alert('Error: Could not get a response from the AI.');
        }
    } catch (error) {
        console.error('Failed to send message:', error);
        alert('Error: Could not send the message.');
    }

    // Clear the input field and focus it for the next message
    input.value = '';
    input.focus();

    // Auto-scroll to the latest message
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
