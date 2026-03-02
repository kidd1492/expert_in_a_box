function loadVideos() {
    const term = document.getElementById("video-input").value.trim();
    if (!term) {
        alert("Enter a search term");
        return;
    }

    fetch(`/research/youtube/${term}`)
        .then(res => res.json())
        .then(videos => {
            const container = document.getElementById("video-results");
            container.innerHTML = "";

            videos.forEach(v => {
                const div = document.createElement("div");
                div.className = "video-card";

                div.innerHTML = `
                    <img src="${v.thumbnail}" class="thumb"/>
                    <h4>${v.title}</h4>
                    <p>${v.description}</p>
                    <a href="https://www.youtube.com/watch?v=${v.videoId}" target="_blank">
                        Watch on YouTube
                    </a>
                `;

                container.appendChild(div);
            });
        })
        .catch(err => {
            console.error("Video fetch error:", err);
        });
}


function runWikiSearch() {
    const term = document.getElementById("wiki-input").value.trim();
    if (!term) {
        alert("Please enter a search term.");
        return;
    }

    fetch(`research/wiki/${term}`)
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