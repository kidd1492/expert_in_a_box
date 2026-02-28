function loadDocument(title) {
    fetch(`/document/${title}`)
        .then(response => response.json())
        .then(data => {
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


function runWikiSearch() {
    const term = document.getElementById("wiki-input").value.trim();
    if (!term) {
        alert("Please enter a search term.");
        return;
    }

    fetch(`/wiki/${term}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById("wiki-results");

            let formatted = data.status
                .replace(/==\s*(.*?)\s*==/g, "<h3>$1</h3>")
                .replace(/===\s*(.*?)\s*===/g, "<h4>$1</h4>");

            resultsDiv.innerHTML = formatted;
        })

        .catch(err => {
            console.error("Wiki search error:", err);
            document.getElementById("wiki-results").innerHTML = "<p>Error performing wiki search.</p>";
        });
}

function addWikiSearch() {
    const term = document.getElementById("wiki-input").value.trim();
    if (!term) {
        alert("Please enter a search term.");
        return;
    }

    fetch(`/add_wiki/${term}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById("wiki-results");
            resultsDiv.innerHTML = `<p>${data.status}</p>`;
        })
        .catch(err => {
            console.error("Add document error:", err);
            document.getElementById("wiki-results").innerHTML = "<p>Error adding document.</p>";
        });
}


function toggleSelectAll() {
    const checked = document.getElementById("select-all").checked;
    document.querySelectorAll(".doc-checkbox").forEach(cb => cb.checked = checked);
}

function getSelectedDocuments() {
    const selected = [];
    document.querySelectorAll(".doc-checkbox:checked").forEach(cb => {
        selected.push(cb.value);
    });
    return selected;
}

function uploadFile() {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    fetch("/ingest", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert("File uploaded and ingested successfully");
        location.reload(); // refresh document list
    })
    .catch(err => {
        console.error(err);
        alert("Error uploading file");
    });
}

