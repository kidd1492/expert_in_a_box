function loadDocument(title) {
    fetch(`retrieval/document/${title}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert(data.error || "Failed to load document");
                return;
            }
            document.getElementById("viewer-title").innerText = data.title;

            let viewer = document.getElementById("doc-viewer");
            viewer.innerHTML = "";

            if (data.chunks.length === 0) {
                viewer.innerHTML = "<p>No content found.</p>";
                return;
            }

            data.chunks.forEach((chunk, index) => {
                let div = document.createElement("div");
                div.classList.add("chunk-block");
                div.innerHTML = `<h4>Chunk ${index + 1}</h4><p>${chunk[0]}</p>`;
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

    fetch(`retrieval/retrieve?query=${encodeURIComponent(query)}&titles=${encodeURIComponent(titles)}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert(data.error || "Retrieval failed");
                return;
            }

            const results = data.results;
            const viewer = document.getElementById("doc-viewer");
            const title = document.getElementById("viewer-title");

            title.innerText = "Retrieved Chunks";
            viewer.innerHTML = "";

            if (!results || results.length === 0) {
                viewer.innerHTML = "<p>No results found.</p>";
                return;
            }

            results.forEach((chunk, index) => {
                let div = document.createElement("div");
                div.classList.add("chunk-block");
                div.innerHTML = `
                    <h4>${chunk.metadata?.title} — Page ${chunk.metadata?.page_number}</h4>
                    <p>${chunk.content}</p>
                `;
                viewer.appendChild(div);
            });
        })
        .catch(err => {
            console.error("Retrieval error:", err);
            alert("Retrieval failed");
        });

}


function triggerFileUpload() {
    document.getElementById("file-input").click();
}