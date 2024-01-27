from django.urls import path
from chat.views import index, login, chat

urlpatterns = [
    path("", index, name="home"),
    path("login/", login, name="login"),
    path("chat/<str:uuid>", chat, name="chat"),
]
