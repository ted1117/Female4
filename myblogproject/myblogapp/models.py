from django.db import models
# 사용자 정보 불러오기
from django.contrib.auth.models import User
# Summernote
from django.utils import timezone


# Create your models here.
class Article(models.Model):
    """Summary

    블로그 포스트를 표현하는 모델
    
    Attributes:
        title (str): _글 제목
        content (str): _글 내용
        created_at (datetime): _작성일
        topic (str): _주제. 기본값은 "전체".
        author (User): _작성자
        imgfile (ImageField): _이미지 경로(?)
        views (int): _조회수
    """
    title = models.CharField(max_length=200)             
    content = models.TextField()            
    created_at = models.DateTimeField(auto_now_add=True)    
    topic = models.CharField(max_length=50, default="전체")    
    # author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    imgfile = models.ImageField(upload_to='images/', blank = True, null = True)
    views = models.IntegerField(default=0)
    is_saved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.content
    
    # content 길이가 210자 이상이면 210자 까지만 나오게
    def is_content_more210(self):
        return len(self.content) > 210
    
    def get_content_under300(self):
        return self.content[:210]
    
    def save(self, *args, **kwargs):
        # '..' 문자열이 포함된 content 필드를 변경
        self.content = self.content.replace('"..', '"')
        super().save(*args, **kwargs)