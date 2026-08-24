document.querySelectorAll('.vote-btn').forEach(button => {
    button.addEventListener('click', function () {      
        const postId = this.dataset.postId;
        const value = parseInt(this.dataset.value);

        const likeBtn = document.getElementById(`like-btn-${postId}`);
        const dislikeBtn = document.getElementById(`dislike-btn-${postId}`);

        fetch(`/vote/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `value=${value}`
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById(`likes-${postId}`).innerText = data.likes;
            document.getElementById(`dislikes-${postId}`).innerText = data.dislikes;

            likeBtn.classList.remove('active-like');
            dislikeBtn.classList.remove('active-dislike');

            if (data.user_vote === 1) {
                likeBtn.classList.add('active-like');
            } else if (data.user_vote === -1) {
                dislikeBtn.classList.add('active-dislike');
            }
        });
    });
});

// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}