
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

function newTopic() {
    const term = document.getElementById("topic-input").value;
    if (!term) {
        alert("Please enter a search term.");
        return;
    }
    
    fetch(`/research/new_topic/${encodeURIComponent(term)}`)
        .then(response => response.json())
        .then(data => {
            location.reload();
        });    
}

function subTopic() {
    const term = document.getElementById("topic-input").value;
    const overviewContainer = document.getElementById("topic-overview");
    const videoContainer = document.getElementById("video-results");
    const linksContainer = document.getElementById("links-container");
    const subtopicContainer = document.getElementById("subtopic-container");

    if (!term) {
        alert("Please enter a search term.");
        return;
    }
    
    fetch(`/research/subtopic/${encodeURIComponent(term)}`)
        .then(response => response.json())
        .then(data => {
            let summary = data.overview;
            overviewContainer.innerHTML = summary;
        });    
}
