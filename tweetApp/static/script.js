document.addEventListener('DOMContentLoaded', () => {
    const message = document.querySelector('#message');
    if (message) {
        setTimeout(() => {
            message.style.opacity = '0'; // Fade out the message
            setTimeout(() => {
                message.style.display = 'none'; // Remove it from the layout
            }, 500); // Match the CSS transition duration (0.5s = 500ms)
        }, 3000); // Wait for 3 seconds before fading out
    }
});
