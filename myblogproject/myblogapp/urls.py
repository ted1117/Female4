from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("write/", views.note_post, name="write"),
    # path("post", views.post, name="post"),
    path("post/<int:id>", views.getPost, name="post"),
    path("post_remove", views.post_remove, name="post_remove"),
    path('post_edit/<int:id>/', views.post_edit, name="post_edit"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.boardadmin, name="board-admin"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # 미디어파일을 제공하기위한 설정
                                                                    # settings.MEDIA_URL은 미디어 파일의 URL을 설정
                                                                    # settings.MEDIA_ROOT는 미디어 파일이 저장되는 경로


