from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Article
from .serializers import ArticleSerializer
from .forms import CustomLoginForm, BlogPostForm



# Create your views here.
def write(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        topic = request.POST["topic"]
        imgfile = request.FILES["imgfile"]
        Article.objects.create(title=title, content=content, topic=topic, imgfile=imgfile)
        return redirect("post")
    return render(request, "write.html")

def post(request):
    return render(request, "post.html")
def post_edit(request):
    return render(request, "post_edit.html")


def post_remove(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('post_list')
# <a href="{% url 'post_remove' pk=article.pk %}">삭제하기</a> html 테그



# 로그인
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('blog_app:post_list')
    else:
        form = CustomLoginForm(data=request.POST or None)  # 커스텀 로그인 폼 사용
        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                # 위 정보로 사용자 인증(authenticate 사용하여 superuser사용)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('blog_app:post_list')  # 슈퍼유저와 일반 사용자 모두 동일한 페이지로 리다이렉션
        return render(request, 'registration/login.html', {'form': form})

def boardadmin(request):
    return render(request, "board-admin.html")

def boardclient(request):
    return render(request, "board-client.html")
