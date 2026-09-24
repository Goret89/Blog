from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_post_event(post_id, event, **data):
    """Broadcast an event to everyone currently viewing this post."""
    channel_layer = get_channel_layer()

    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        f'post_{post_id}',
        {
            'type': 'post.event',
            'event': event,
            **data,
        },
    )