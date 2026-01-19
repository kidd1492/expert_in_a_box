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