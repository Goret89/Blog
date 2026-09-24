from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PostConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.group_name = f'post_{self.post_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def post_event(self, event):
        await self.send_json({
            'event': event['event'],
            **{
                key: value
                for key, value in event.items()
                if key not in {'type', 'event'}
            },
        })