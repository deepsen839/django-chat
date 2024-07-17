from django.urls import path
from .consumers import ActiveInactiveConsumer

websocket_urlpatterns = [
    path('ws/activity/', ActiveInactiveConsumer.as_asgi()),
]