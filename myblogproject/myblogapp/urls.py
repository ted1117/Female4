from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("write/", views.write, name="write"),
    path("post/", views.post, name="post"),
    path('login/', views.login_view, name='login'),
    path("board-admin/", views.boardadmin, name="board-admin"),
    path("", views.boardclient, name="board-client"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # 미디어파일을 제공하기위한 설정
                                                                    # settings.MEDIA_URL은 미디어 파일의 URL을 설정
                                                                    # settings.MEDIA_ROOT는 미디어 파일이 저장되는 경로


