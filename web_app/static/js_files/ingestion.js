function uploadFile() {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file.");
        return;
    }

    const allowedExtensions = ["pdf", "txt", "md"];
    const ext = file.name.split(".").pop().toLowerCase();

    if (!allowedExtensions.includes(ext)) {
        alert("Unsupported file type: " + ext);
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("ingestion/ingest", {
        method: "POST",
        body: formData
    })
    .then(async response => {
        const data = await response.json();

        if (!response.ok) {
            alert("Upload failed: " + (data.error || data.status));
            return;
        }

        alert("File uploaded and ingested successfully");
        location.reload();
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

    fetch(`ingestion/add_wiki/${encodeURIComponent(term)}`)
        .then(async response => {
            const data = await response.json();

            if (!response.ok) {
                alert("Wiki ingestion failed: " + (data.error || data.status));
                return;
            }

            alert("Wiki article ingested successfully");
            document.getElementById("wiki-results").innerHTML = `<p>${data.status}</p>`;
        })
        .catch(err => {
            console.error("Add document error:", err);
            alert("Network error while adding wiki document");
        });
}


function removeFile() {
    const docs = getSelectedDocuments();
    const titles = docs.length > 0 ? docs.join(",") : "all";

    fetch(`/ingestion/remove_selected/${encodeURIComponent(titles)}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        console.log("Removed:", data);
    })
    .catch(err => console.error("Error:", err));
}

    
