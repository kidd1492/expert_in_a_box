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

    fetch(`/chat?query=${encodeURIComponent(query)}&titles=${encodeURIComponent(titles)}&mode=${mode}`)
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
                    <strong>${chunk.title} — Page ${chunk.page_number}</strong><br>
                    ${chunk.text}
                `;
                viewer.appendChild(div);
            });
        });
}

function runQuery() {
    const query = document.getElementById("query-input").value.trim();
    if (!query) {
        alert("Please enter a query.");
        return;
    }

    const docs = getSelectedDocuments();
    const titles = docs.length > 0 ? docs.join(",") : "all";

    fetch(`/retrieve?query=${encodeURIComponent(query)}&titles=${encodeURIComponent(titles)}`)
        .then(response => response.json())
        .then(data => {
            const viewer = document.getElementById("doc-viewer");
            const title = document.getElementById("viewer-title");

            title.innerText = "Retrieved Chunks";
            viewer.innerHTML = "";

            if (!data || data.length === 0) {
                viewer.innerHTML = "<p>No results found.</p>";
                return;
            }

            data.forEach((chunk, index) => {
                let div = document.createElement("div");
                div.classList.add("chunk-block");
                div.innerHTML = `
                    <h4>${chunk.title} — Page ${chunk.page_number}</h4>
                    <p>${chunk.text}</p>
                `;

                viewer.appendChild(div);
            });
        })
        .catch(err => {
            console.error("Retrieval error:", err);
        });
}


function triggerFileUpload() {
    document.getElementById("file-input").click();
}
