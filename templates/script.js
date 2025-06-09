document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("start-btn").addEventListener("click", function () {
        fetch("/start", { method: "POST" })
            .then(response => response.json())
            .then(data => {
                if (data.status === "started") {
                    document.getElementById("video-feed").src = "/video_feed";
                    document.getElementById("start-btn").disabled = true;

                    setTimeout(() => {
                        window.location.href = "/result";
                    }, 10000);
                } else {
                    console.error("Error: Unexpected response", data);
                }
            })
            .catch(error => console.error("Error starting video:", error));
    });
});
