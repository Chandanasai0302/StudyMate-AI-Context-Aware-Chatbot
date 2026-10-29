
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const sendButton = document.getElementById("send-button");
const newChatButton = document.getElementById("new-chat");

let conversationId = createConversationId();
let isSending = false;

function createConversationId() {
    return "chat-" + Date.now() + "-" +
        Math.random().toString(36).slice(2, 8);
}

function addMessage(text, role, extraClass = "") {
    const message = document.createElement("div");
    message.className = `message ${role} ${extraClass}`.trim();
    message.textContent = text;
    messages.appendChild(message);
    message.scrollIntoView({ behavior: "smooth", block: "nearest" });
    return message;
}

function setLoading(loading) {
    isSending = loading;
    sendButton.disabled = loading;
    sendButton.innerHTML = loading ? "…" : "<span>↑</span>";
    messageInput.disabled = loading;
}

async function sendMessage(text) {
    const userMessage = text.trim();

    if (!userMessage || isSending) return;

    welcome.hidden = true;
    addMessage(userMessage, "user");
    messageInput.value = "";
    messageInput.style.height = "auto";
    setLoading(true);

    const typing = addMessage("StudyMate is thinking…", "assistant");
    typing.classList.add("typing");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                message: userMessage
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "The request failed.");
        }

        typing.remove();

        // Adjust this field if your backend uses a different response format.
        const answer = data.response ?? data.answer ?? data.reply;

        if (typeof answer !== "string" || !answer.trim()) {
            throw new Error("The server responded, but no answer was found.");
        }

        addMessage(answer, "assistant");
    } catch (error) {
        typing.remove();
        console.error("Chat error:", error);
        addMessage(
            error.message || "Could not connect to StudyMate. Check the backend.",
            "assistant",
            "error"
        );
    } finally {
        setLoading(false);
        messageInput.focus();
    }
}

chatForm.addEventListener("submit", function (event) {
    event.preventDefault();
    sendMessage(messageInput.value);
});

messageInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});

messageInput.addEventListener("input", function () {
    messageInput.style.height = "auto";
    messageInput.style.height =
        Math.min(messageInput.scrollHeight, 150) + "px";
});

document.querySelectorAll(".suggestion").forEach(function (button) {
    button.addEventListener("click", function () {
        sendMessage(button.dataset.message);
    });
});


newChatButton.addEventListener("click", async function () {
    if (isSending) return;

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/new-chat",
            { method: "POST" }
        );

        if (!response.ok) {
            throw new Error("Could not reset the conversation.");
        }

        const data = await response.json();
        conversationId = data.conversation_id;
    } catch (error) {
        console.error("New chat error:", error);
        conversationId = createConversationId();
    }

    messages.replaceChildren();
    welcome.hidden = false;
    messageInput.value = "";
    messageInput.focus();
});
