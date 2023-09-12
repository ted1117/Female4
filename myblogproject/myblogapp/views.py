from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def write(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        Article.objects.create(title=title, content=content)
        return redirect("post")
    return render(request, "write.html")

def post(request):
    return render(request, "post.html")

def login(request):
    return render(request, "login.html")

def boardadmin(request):
    return render(request, "board-admin.html")

def boardclient(request):
    return render(request, "board-client.html")
