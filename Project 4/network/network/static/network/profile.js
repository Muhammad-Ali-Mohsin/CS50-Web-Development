document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("follow-btn").onclick = () => follow();

    // Loads the posts
    loadPosts(1, users=[getUsername()]);
})

function getUsername() {
    const url = new URL(window.location.href);
    return url.pathname.split('/')[2].replace("%20", " ");
}

function follow() {
    fetch('/follow', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({
            username: getUsername(),
        })
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById("follow-btn").innerHTML = result['result'] === "followed" ? "Unfollow" : "Follow";
        document.getElementById("followers").innerHTML = `Followers: ${result['followers']}`;
    })
}