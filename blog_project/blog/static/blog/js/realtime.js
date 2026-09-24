document.addEventListener('DOMContentLoaded', () => {
    const postPage = document.getElementById('post-page');

    if (!postPage) {
        return;
    }

    const postId = postPage.dataset.postId;

    const protocol = window.location.protocol === "https:" ? 'wss' : 'ws';
    const socketUrl = `${protocol}://${window.location.host}/ws/post/${postId}/`;

    console.log('WebSocket URL:', socketUrl);

    let socket;
    let reconnectTimer;

    function connect() {
        socket = new WebSocket(socketUrl);

        socket.onopen = () => {
            console.log('WebSocket connected');
        }

        socket.onmessage = async (event) => {
            const data = JSON.parse(event.data);

            if (data.event === 'post_vote_changed') {
                updatePostVotes(data);
            }

            if (data.event === 'comment_vote_changed') {
                updateCommentVotes(data);
            }

            if (data.event === 'comments_changed') {
                await refreshComments();
            }
        };

        socket.onclose = (event) => {
            console.log('WebSocket closed:', event.code, event.reason);

            clearInterval(reconnectTimer);

            reconnectTimer = setTimeout(connect, 2000);
        };

        socket.onerror = (error) => {
            console.log('WebSocket error:', error);
            socket.close();
        };
    }

    function updatePostVotes(data) {
        const likes = document.getElementById(`likes-${postId}`);
        const dislikes = document.getElementById(`dislikes-${postId}`);

        if (likes) {
            likes.textContent = data.likes;
        }

        if (dislikes) {
            dislikes.textContent = data.dislikes;
        }
    }

    function updateCommentVotes(data) {
        const likes = document.getElementById(`comment-likes-${data.comment_id}`);
        const dislikes = document.getElementById(`comment-dislikes-${data.comment_id}`);

        if (likes) {
            likes.textContent = data.likes;
        }

        if (dislikes) {
            dislikes.textContent = data.dislikes;
        }
    }

    async function refreshComments() {
        const response = await fetch(
            `/post/${postId}/comments/fragment/`,
            {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            }
        );

        if (!response.ok) {
            return;
        }

        const html = await response.text();
        const commentsContainer = document.getElementById('comments-container');

        if (commentsContainer) {
            commentsContainer.innerHTML = html;
        }
    }

    connect();
});