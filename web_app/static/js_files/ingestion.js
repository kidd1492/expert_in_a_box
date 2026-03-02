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

