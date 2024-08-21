document.addEventListener("DOMContentLoaded", () => {

    // Loads the posts
    fetch('/get_followers', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
    })
    .then(response => response.json())
    .then(result => {
        loadPosts(1, users=result['followers']);
    })
})