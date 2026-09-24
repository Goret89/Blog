from django.urls import path
from .consumers import PostConsumer


websocket_urlpatterns = [
    path('ws/post/<int:post_id>/', PostConsumer.as_asgi()),
]