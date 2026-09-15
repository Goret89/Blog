document.addEventListener('DOMContentLoaded', () => {
    // Reply buttons
    document.querySelectorAll('.reply-btn').forEach(button => {
        button.addEventListener('click', () => {
            const commentId = button.dataset.commentId;

            const form = document.getElementById(`reply-form-${commentId}`);

            form.classList.toggle('d-none');
        });
    });

    // Comment votes
    document.querySelectorAll('.comment-vote-btn').forEach(button => {
        button.addEventListener('click', async () => {
            const commentId = button.dataset.commentId;
            const value = parseInt(button.dataset.value);

            const response = await fetch(
                `/comment/${commentId}/vote/`,
                {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `value=${value}`,
                }
            );

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            document.getElementById(`comment-likes-${commentId}`).innerText = data.likes;
            document.getElementById(`comment-dislikes-${commentId}`).innerText = data.dislikes;

            const likeButton = document.querySelector(`.comment-vote-btn[data-comment-id="${commentId}"][data-value="1]`);
            const dislikeButton = document.querySelector(`.comment-vote-btn[data-comment-id="${commentId}"][data-value="-1"]`);

            likeButton.classList.remove('active-like');
            dislikeButton.classList.remove('active-dislike');

            if (data.user_vote === 1) {
                likeButton.classList.add('active-like');
            } else if (data.user_vote === -1) {
                button.classList.add('active-dislike');
            }
        });
    });
});


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