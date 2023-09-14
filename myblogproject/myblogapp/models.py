from django.db import models
# 사용자 정보 불러오기
from django.contrib.auth.models import User
# Summernote
from django.utils import timezone


# Create your models here.
class Article(models.Model):
    """
    title: 글 제목
    content: 글 내용
    created_at: 작성일
    topic: 주제
    author: 작성자
    """
    title = models.CharField(max_length=200)             
    content = models.TextField()            
    created_at = models.DateTimeField(auto_now_add=True)    
    topic = models.CharField(max_length=50)    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    imgfile = models.ImageField(upload_to='images/', blank = True, null = True)

    def __str__(self) -> str:
        return self.content