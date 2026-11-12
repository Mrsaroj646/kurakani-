// Chat logic for the Kurakani web page

const chatForm = document.getElementById("chatForm");
const inputField = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const chatBox = document.getElementById("chatBox");

// Address of the FastAPI backend, used when this page is NOT served by it
// (opened as a file or through another dev server such as Live Server).
const BACKEND_URL = "http://127.0.0.1:8000";

/** POST to the chat API, falling back to BACKEND_URL if needed. */
async function postChat(message) {
    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
    };

    if (location.protocol === "file:") {
        return fetch(`${BACKEND_URL}/api/chat`, options);
    }

    try {
        const response = await fetch("/api/chat", options);
        // Our backend always answers with JSON. Anything else means this page
        // is being served by a different server (e.g. Live Server).
        const type = response.headers.get("content-type") || "";
        if (type.includes("application/json")) return response;
    } catch (error) {
        // network error - try the backend address below
    }
    return fetch(`${BACKEND_URL}/api/chat`, options);
}

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
        const response = await postChat(text);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(typeof data.detail === "string" ? data.detail : "Something went wrong.");
        }

        loading.textContent = data.reply;
        loading.classList.remove("loading");
    } catch (error) {
        const reason = error instanceof TypeError
            ? `Could not connect to the Kurakani server at ${BACKEND_URL}. Is it running?`
            : error.message;
        loading.textContent = `Error: ${reason}`;
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
