document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("new-post-input").addEventListener("keyup", () => updateButton());
    document.getElementById("new-post-btn").onclick = () => createPost();
    loadPosts(1);
})

// Disables the button when the post content is empty
function updateButton() {
    let btn = document.getElementById("new-post-btn");
    if (document.getElementById("new-post-input").value === "") {
        btn.disabled = true;
        btn.className = "btn btn-secondary";
    } else {
        btn.disabled = false;
        btn.className = "btn btn-primary";
    }
}

// Creates a boostrap alert message
function createAlert(message, type) {
    let alertDiv = document.createElement('div');
    alertDiv.innerHTML = message;
    alertDiv.className = `alert alert-${type}`;
    return alertDiv
}

// Creates a post
function createPost() {
    let postInput = document.getElementById("new-post-input");
    fetch('/create', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({
            content: postInput.value,
        })
    })
    .then(response => response.json())
    .then(result => {
        loadPosts(1);
        document.getElementById("message-div").append(createAlert("Post successfully created!", "success"))
        postInput.value = "";
    })
}