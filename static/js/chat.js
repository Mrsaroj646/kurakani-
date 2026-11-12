// Chat logic for the Kurakani web page

const chatForm = document.getElementById("chatForm");
const inputField = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const chatBox = document.getElementById("chatBox");

/**
 * Add a message bubble to the chat.
 * textContent is used (not innerHTML) so user input can never inject HTML.
 */
function addMessage(text, sender, extraClass = "") {
    const bubble = document.createElement("div");
    bubble.className = `message ${sender}-message ${extraClass}`.trim();
    bubble.textContent = text;
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
    return bubble;
}

async function sendMessage(text) {
    addMessage(text, "user");
    const loading = addMessage("Kurakani is thinking...", "ai", "loading");
    sendButton.disabled = true;

    try {
        // Relative URL: works on whatever host/port the server runs on
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text }),
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(typeof data.detail === "string" ? data.detail : "Something went wrong.");
        }

        loading.textContent = data.reply;
        loading.classList.remove("loading");
    } catch (error) {
        loading.textContent = `Error: ${error.message || "Could not connect to Kurakani server."}`;
        loading.classList.remove("loading");
        loading.classList.add("error");
    } finally {
        sendButton.disabled = false;
        inputField.focus();
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const text = inputField.value.trim();
    if (!text) return;
    inputField.value = "";
    sendMessage(text);
});
