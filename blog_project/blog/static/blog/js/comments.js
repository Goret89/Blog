document.addEventListener('DOMContentLoaded', () => {
    // Reply buttons
    document.querySelectorAll('.reply-btn').forEach(button => {
        button.addEventListener('click', () => {
            const commentId = button.dataset.commentId;

            const form = document.getElementById(`reply-form-${commentId}`);

            form.classList.toggle('d-none');
        });
    });

    // Comment likes
    document.querySelectorAll('.comment-like-btn').forEach(button => {
        button.addEventListener('click', async () => {
            const commentId = button.dataset.commentId;

            const response = await fetch(
                `/comment/${commentId}/like/`,
                {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                }
            );

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            document.getElementById(`comment-likes-${commentId}`).innerText = data.likes;

            if (data.user_liked) {
                button.classList.add('active-like');
            } else {
                button.classList.remove('active-like');
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