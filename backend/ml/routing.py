from django.conf.urls import url
from .socket import DocumentSocketListener

websocket_urlpatterns = [
    url(r'^ws/documents/', DocumentSocketListener.as_asgi()),
]
