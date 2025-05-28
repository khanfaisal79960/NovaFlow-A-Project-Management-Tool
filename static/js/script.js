// Initialize Markdown-it parser
const md = window.markdownit();

/**
 * Renders markdown content in elements with a specific class.
 * This is useful if you fetch markdown content dynamically via AJAX,
 * but for this Flask app, markdown is rendered server-side for initial load
 * and client-side if you were to implement dynamic content loading.
 * The `project_detail.html` already renders markdown server-side using `markdown.markdown()`.
 * This client-side code is included for completeness and future dynamic features.
 */
function renderMarkdownElements() {
    document.querySelectorAll('.markdown-content-raw').forEach(element => {
        const markdownText = element.textContent;
        element.innerHTML = md.render(markdownText);
    });
}

// Function to handle custom confirmation dialogs instead of `confirm()`
function showCustomConfirm(message, callback) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 animate-fade-in';
    overlay.id = 'custom-confirm-overlay';

    // Create modal
    const modal = document.createElement('div');
    modal.className = 'bg-gray-800 p-8 rounded-2xl shadow-2xl border border-purple-700 max-w-sm w-full text-center transform scale-95 animate-zoom-in';

    // Message
    const msgPara = document.createElement('p');
    msgPara.className = 'text-gray-200 text-lg mb-6';
    msgPara.textContent = message;

    // Buttons container
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'flex justify-center space-x-4';

    // Yes button
    const yesButton = document.createElement('button');
    yesButton.className = 'bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 text-white font-bold py-2 px-5 rounded-lg shadow-md transform transition-all duration-200 ease-in-out hover:scale-105';
    yesButton.textContent = 'Yes';
    yesButton.onclick = () => {
        document.body.removeChild(overlay);
        callback(true);
    };

    // No button
    const noButton = document.createElement('button');
    noButton.className = 'bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white font-bold py-2 px-5 rounded-lg shadow-md transform transition-all duration-200 ease-in-out hover:scale-105';
    noButton.textContent = 'No';
    noButton.onclick = () => {
        document.body.removeChild(overlay);
        callback(false);
    };

    buttonContainer.appendChild(noButton);
    buttonContainer.appendChild(yesButton);
    modal.appendChild(msgPara);
    modal.appendChild(buttonContainer);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);

     // Add animations for the modal
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes zoomIn {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        .animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
        .animate-zoom-in { animation: zoomIn 0.3s ease-out forwards; }
    `;
    document.head.appendChild(style);
}


// Event listener for DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
    // Call markdown rendering if needed (e.g., for dynamically loaded content)
    // renderMarkdownElements(); // Uncomment if you add client-side markdown inputs

    // Intercept form submissions that use `confirm()`
    document.querySelectorAll('form[onsubmit*="confirm("]').forEach(form => {
        form.originalOnsubmit = form.onsubmit; // Store original handler
        form.onsubmit = null; // Disable original handler

        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default submission

            // Extract the message from the original onsubmit attribute
            const confirmMessageMatch = this.originalOnsubmit.toString().match(/confirm\(['"]([^'"]+)['"]\)/);
            const message = confirmMessageMatch ? confirmMessageMatch[1] : 'Are you sure?';

            showCustomConfirm(message, (result) => {
                if (result) {
                    // If confirmed, submit the form programmatically
                    this.submit();
                } else {
                    // Do nothing, form submission cancelled
                }
            });
        });
    });
});
