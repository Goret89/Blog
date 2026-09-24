document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', async (event) => {
        const replyButton = event.target.closest('.reply-btn');

        if (replyButton) {
            const commentId = replyButton.dataset.commentId;

            const form = document.getElementById(`reply-form-${commentId}`);

            if (form) {  
                form.classList.toggle('d-none');
            }

            return;
        }

        const voteButton = event.target.closest('.comment-vote-btn');

        if (!voteButton) {
            return;
        }

        const commentId = voteButton.dataset.commentId;
        const value = parseInt(voteButton.dataset.value, 10);

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

        updateCommentVoteUI(commentId, data);
    });
});

function updateCommentVoteUI(commentId, data) {
    const likes = document.getElementById(`comment-likes-${commentId}`);
    const dislikes = document.getElementById(`comment-dislikes-${commentId}`);

    if (likes) {
        likes.textContent = data.likes;
    }

    if (dislikes) {
        dislikes.textContent = data.dislikes;
    }

    const likeButton = document.querySelector(`.comment-vote-btn[data-comment-id="${commentId}"][data-value="1"]`);
    const dislikeButton = document.querySelector(`.comment-vote-btn[data-comment-id="${commentId}"][data-value="-1"]`);

    likeButton?.classList.remove('active-like');
    dislikeButton?.classList.remove('active-dislike');

    if (data.user_vote === 1) {
        likeButton?.classList.add('active-like');
    } else if (data.user_vote === -1) {
        dislikeButton?.classList.add('active-dislike');
    }
}

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