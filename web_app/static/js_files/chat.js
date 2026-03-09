function chatAsk() {
    runChatMode("answer");
}

function chatSummarize() {
    runChatMode("summarize");
}

function chatOutline() {
    runChatMode("outline");
}


function runChatMode(mode) {
    const query = document.getElementById("query-input").value.trim();
    const docs = getSelectedDocuments();
    const titles = docs.length > 0 ? docs.join(",") : "all";

    fetch(`chat_route/chat?query=${encodeURIComponent(query)}&titles=${encodeURIComponent(titles)}&mode=${mode}`)
        .then(res => res.json())
        .then(data => {
            const viewer = document.getElementById("doc-viewer");
            const title = document.getElementById("viewer-title");

            viewer.innerHTML = "";
            title.textContent = mode.toUpperCase();

            let answerDiv = document.createElement("div");
            answerDiv.className = "answer-block";
            answerDiv.textContent = data.answer;
            viewer.appendChild(answerDiv);

            let ctxHeader = document.createElement("h4");
            ctxHeader.textContent = "Retrieved Context:";
            viewer.appendChild(ctxHeader);

            data.context.forEach(chunk => {
                let div = document.createElement("div");
                div.className = "chunk-block";
                div.innerHTML = `
                    <h4>${chunk.metadata?.title} — Page ${chunk.metadata?.page_number}</h4>
                    <p>${chunk.content}</p>
                `;
                viewer.appendChild(div);
            });
        });
}

function conversation() {
    const question = document.getElementById("ask-chatbot").value.trim();
    const viewer = document.getElementById("chat-viewer");

    if (!question) return;

    // Show user message
    let userDiv = document.createElement("div");
    userDiv.className = "question-block";
    userDiv.textContent = question;
    viewer.appendChild(userDiv);

    // Call Flask route
    fetch(`/chat_route/chatbot?query=${encodeURIComponent(question)}`)
        .then(res => res.json())
        .then(data => {
            let botDiv = document.createElement("div");
            botDiv.className = "answer-block";
            botDiv.innerHTML = `<p>${data.answer}</p>`;
            viewer.appendChild(botDiv);

            // Auto-scroll
            viewer.scrollTop = viewer.scrollHeight;
        })
        .catch(err => console.error("Chat error:", err));

    // Clear input
    document.getElementById("ask-chatbot").value = "";
}
