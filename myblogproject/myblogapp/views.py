from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Article
from .serializers import ArticleSerializer
from .forms import CustomLoginForm, ArticleForm
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
import re
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
from django.db.models import Q
import openai



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
    drafts = Article.objects.filter(is_saved=False).order_by("-created_at")
        
    if request.method == "POST":
        # 임시로 저장된 글 선택
        draft_id = request.POST.get("selected")
        if draft_id:
            return redirect("post_edit", id=draft_id)
        
        form = ArticleForm(request.POST)
        button_type = request.POST.get("button_type")
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if button_type == "tmp_save":
                post.save()
                return redirect("board-admin")

            post.is_saved = True
            post.save()
            return redirect("post", id=post.id)
    else:
        form = ArticleForm()
        print(form)
        context = {"form": form, "drafts": drafts}

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

def getPost(request, id):
    current_post = get_object_or_404(Article, id=id)

    # 현재 게시물 조회수 상승
    current_post.views += 1
    current_post.save()

    # 현재 게시물의 이전 게시물 가져오기
    prev_post = Article.objects.filter(id__lt=current_post.id).order_by('-id').first()

    # 현재 게시물의 다음 게시물 가져오기
    next_post = Article.objects.filter(id__gt=current_post.id).order_by('id').first()
    
    # 추천 게시물
    rec_posts = Article.objects.exclude(id=current_post.id).filter(topic=current_post.topic)[:2]
    print(rec_posts)
    if not rec_posts:
        excluded_ids = [x.id for x in [current_post, prev_post, next_post] if x is not None]
        # excluded_ids = [current_post.id, prev_post.id, next_post.id]
        rec_posts = Article.objects.exclude(Q(id__in=excluded_ids))[:2]

    for rec_post in rec_posts:
        soup = BeautifulSoup(rec_post.content, "html.parser")
        rec_post.img = img_tag.get("src") if (img_tag:=soup.find("img")) else False

    context = {
        "post": current_post,
        "prev_post": prev_post,
        "next_post": next_post,
        "rec_posts": rec_posts,
    }

    return render(request, "post.html", context)

@login_required
def post_edit(request, id):
    post = get_object_or_404(Article, id=id)  # 게시물을 가져옵니다.

    if request.method == 'POST':        
        form = ArticleForm(request.POST, instance=post)  # 폼을 POST 데이터로 초기화합니다.
        if form.is_valid():
            post.is_saved = True
            post.created_at = timezone.now()
            form.save() # 수정된 데이터를 저장합니다.
            return redirect("post", id=post.id)  # 수정이 완료된 후 게시물 상세 페이지로 리다이렉트
    else:
        form = ArticleForm(instance=post)  # 폼을 기존 게시물 데이터로 초기화합니다.

    return render(request, 'edit.html', {'form': form, 'post': post})

@login_required
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
    page = request.GET.get("page", "1") # 페이지
    most_viewed = Article.objects.filter(is_saved=True).order_by("-views").first()
    html = most_viewed.content
    soup = BeautifulSoup(html, "html.parser")
    most_viewed.img = soup.find("img").get("src")

    all_records = Article.objects.filter(is_saved=True).exclude(id=most_viewed.id).order_by("-created_at")  
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
    paginator = Paginator(all_records, 8)  # 페이지 당 8개씩 노출
    page_obj = paginator.get_page(page)
    context = {
        "most_viewed": most_viewed,
        # "all_records": all_records,
        "all_records": page_obj,
    }
    

    return render(request, "board-admin.html", context)

def topic_view(request, topic):
    articles = Article.objects.filter(topic=topic, is_saved=True)
    most_viewed = articles.order_by("-views").first()
    soup = BeautifulSoup(most_viewed.content, "html.parser")
    most_viewed.img = img_tag.get("src") if (img_tag:=soup.find("img")) else False
    all_records = articles.exclude(id=most_viewed.id).order_by("-created_at")
    for article in all_records:
        soup = BeautifulSoup(article.content, "html.parser")
        article.img = img_tag.get("src") if (img_tag:=soup.find("img")) else False

    context = {
        "most_viewed": most_viewed,
        "all_records": all_records,
    }
    return render(request, "board-admin.html", context)

def autocomplete(request):
    if request.method == "POST":

        #제목 필드값 가져옴
        prompt = request.POST.get('title')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            # 반환된 응답에서 텍스트 추출해 변수에 저장
            message = response['choices'][0]['message']['content']
        except Exception as e:
            message = str(e)
        return JsonResponse({"message": message})
    return render(request, 'write.html')

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