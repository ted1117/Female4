from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Article
from .serializers import ArticleSerializer
from .forms import CustomLoginForm, ArticleForm
from django.http import HttpResponse
from rest_framework import generics
import re
from django.contrib import messages
from django.urls import reverse



# Create your views here.
@login_required
def write(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        topic = request.POST["topic"]
        imgfile = request.FILES.get("imgfile")
        Article.objects.create(title=title, content=content, topic=topic, imgfile=imgfile)
        return redirect("post")
    return render(request, "write.html")

# write.html / Summernote 에디터
@login_required
def note_post(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post")
    else:
        form = ArticleForm()
        print(form)
        context = {"form": form}

    return render(request, "write.html", context)


def post(request):
    post_id = request.GET.get('id')
    print(post_id)
    try:
        # PostgreSQL에서 해당 ID의 데이터를 불러옵니다.
        post = Article.objects.get(id=post_id)  # YourModel은 실제 모델 이름으로 변경해야 합니다.
    except Article.DoesNotExist:
        # 해당 ID로 데이터를 찾을 수 없을 경우 예외 처리
        post = None
    return render(request, "post.html", {'post': post})


def post_edit(request, id):
    post = get_object_or_404(Article, id=id)  # 게시물을 가져옵니다.

    if request.method == 'POST':        
        form = ArticleForm(request.POST, instance=post)  # 폼을 POST 데이터로 초기화합니다.
        if form.is_valid():
            form.save()  # 수정된 데이터를 저장합니다.
            post_url = reverse('post') + f'?id={post.id}'
            return redirect(post_url)  # 수정이 완료된 후 게시물 상세 페이지로 리다이렉트
    else:
        form = ArticleForm(instance=post)  # 폼을 기존 게시물 데이터로 초기화합니다.

    return render(request, 'edit.html', {'form': form, 'post': post})


def post_remove(request):
    # GET 요청을 통한 삭제 방지
    if request.method == 'POST':
        article_id = request.POST.get('id')
        print(article_id)
        article = get_object_or_404(Article, pk=article_id)
        article.delete()
        messages.success(request, '게시물이 삭제되었습니다.')
        
        # 권한 확인 코드 (예: 현재 로그인한 사용자와 게시물 작성자 비교)
        # if request.user == article.author:
        #     article.delete()
        #     messages.success(request, '게시물이 삭제되었습니다.')
        # else:
        #     messages.error(request, '게시물을 삭제할 권한이 없습니다.')
    
    return redirect('board-admin')
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
    all_records = Article.objects.all()    
    for record in all_records:
        pattern = r'<img[^>]*>'
        # img_tag = re.findall(pattern,record.content)
        pattern2 = r'src="([^"]+)"'
        # matches = re.search(pattern2, record.content)
        img_tag = re.findall(pattern2,record.content)
        print(img_tag)
        record.img = ' '.join(img_tag)
        result = re.sub(pattern, '', record.content)
        record.content = result
    

    return render(request, "board-admin.html",{'all_records':all_records})

def boardclient(request):
    return render(request, "board-client.html")

# 포스트리스트
def post_list(request, topic=None):
    
    # 특정 주제로 필터링
    if topic:
        posts = Article.objects.filter(topic=topic, publish='Y').order_by('-views')
    
    else:
        posts = Article.objects.filter(publish='Y').order_by('-views') 
    return render(request, 'blog_app/post_list.html', {'posts': posts})

# 포스트 RESTful API뷰 생성
class BlogPostList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer