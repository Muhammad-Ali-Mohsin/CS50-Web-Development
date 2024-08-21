// Gets a page button list item
function getPageListItem(page, text, active) {
    let li = document.createElement('li');
    li.className = active ? "page-item active" : "page-item";
    if (active) {
        let span = document.createElement('span');
        span.className = "page-link";
        span.innerHTML = text;
        li.appendChild(span);
    } else {
        let button = document.createElement('button');
        button.className = "page-link";
        button.onclick = () => loadPosts(page);
        button.innerHTML = text === "" ? page : text;
        li.appendChild(button);
    }
    return li
}

// Likes or unlikes a post
function like(post_id) {
    fetch('/like', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({
            post_id: post_id
        })
    })
    .then(response => response.json())
    .then(result => {
        let postDiv = document.getElementById(`post_${post_id}`);
        let likeButton = postDiv.querySelector(".like-btn");
        let likesCounter = postDiv.querySelector(".likes");
        likeButton.innerHTML = result['result'] === "liked" ? "Unlike" : "Like";
        likesCounter.innerHTML = `Likes: ${result['likes']}`;
    })
}

// Loads new posts and appends them to the total posts
function loadPosts(page, users=null) {
    fetch('/get_posts', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({
            page: page,
            users: users
        })
    })
    .then(response => response.json())
    .then(result => {

        let is_authenticated = document.getElementById("is_authenticated").value === "True";
        let username = document.getElementById("username").value;

        // Gets the post template and clears the current posts
        let postTemplate = document.getElementById("post-template");
        let postsDiv = document.getElementById("posts");
        postsDiv.innerHTML = "";

        // Adds each post to the posts div
        let posts = result['posts'];
        Object.keys(posts).forEach(post => {

            // Clones the post template
            let newPost = postTemplate.cloneNode(true);
            newPost.id = `post_${posts[post].id}`;
            newPost.style.display = 'block';

            // Adds the author as a link
            let authorLink = newPost.querySelector("a");
            authorLink.href = `/profile/${posts[post].author}`;
            authorLink.innerHTML = posts[post].author;

            // Adds the post content, timestamp and likes
            newPost.querySelector("h6").innerHTML = posts[post].timestamp;
            newPost.querySelector("p").innerHTML = posts[post].content;
            newPost.querySelector(".likes").innerHTML = `Likes: ${posts[post].likes}`;

            // Adds the like button
            let likeButton = newPost.querySelector(".like-btn");
            likeButton.innerHTML = posts[post].is_liked ? "Unlike" : "Like";
            likeButton.onclick = () => like(posts[post].id);
            likeButton.style.display = is_authenticated ? "block" : "none"

            if (username === posts[post].author) {
                let editButton = newPost.querySelector(".edit-btn");
                editButton.insertAdjacentHTML("beforebegin", "<br>")
                editButton.innerHTML = "Edit Post";
                editButton.onclick = () => edit(posts[post].id);
                editButton.style.display = "block";
            }

            postsDiv.appendChild(newPost);
        });

        // Adds the page numbers
        let pageList = document.getElementById("page-list");
        pageList.innerHTML = "";

        // Adds Previous and Next buttons
        if (page > 1) {
            let li = getPageListItem(page - 1, "Previous");
            pageList.append(li);
        }

        if (result['pages'] > page) {
            let li = getPageListItem(page + 1, "Next");
            pageList.append(li);
        }

        // Adds individual page buttons
        if (result['pages'] > 1) {
            for (let i = 0; i < result['pages']; i++) {
                let li = getPageListItem(i + 1, text=`${i + 1}`, active=(i + 1 === page ? true : false));
                pageList.append(li);
            }
        } 

    })
}

// Edits a post
function edit(post_id) {

    // Adds the edit textarea
    let postDiv = document.getElementById(`post_${post_id}`);
    let p = postDiv.querySelector("p");
    let textarea = document.createElement("textarea");
    textarea.value = p.innerHTML;
    textarea.className = "form-control";
    textarea.setAttribute("placeholder", "Edit post");
    textarea.setAttribute("rows", 3);
    p.replaceWith(textarea);
    let editSpace = document.createElement("br");
    textarea.insertAdjacentHTML("afterend", "<br class='edit-space'>")

    // Adds the new button
    let editButton = postDiv.querySelector(".edit-btn");
    editButton.innerHTML = "Confirm Edit"
    editButton.onclick = () => {
        fetch('/edit_post', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body: JSON.stringify({
                post_id: post_id,
                new_content: textarea.value
            })
        })
        .then(response => response.json())
        .then(result => {
            p.innerHTML = textarea.value;
            textarea.replaceWith(p);
            editButton.innerHTML = "Edit Post";
            editButton.onclick = () => edit(post_id);
            postDiv.querySelector(".edit-space").remove()
        })
    }
}