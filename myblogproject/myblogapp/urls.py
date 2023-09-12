from django.urls import path, include
from . import views

urlpatterns = [
    path("write", views.write, name="write"),
    path("post", views.post, name="post"),
    path("login", views.login, name="login"),
    path("board-admin", views.boardadmin, name="board-admin"),
    path("board-client", views.boardclient, name="board-client"),
]


