function loadVideos() {
    const term = document.getElementById("video-input").value.trim();
    if (!term) {
        alert("Enter a search term");
        return;
    }

    fetch(`/youtube/${term}`)
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