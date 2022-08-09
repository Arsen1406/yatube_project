from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Post, Group


def index(request: str) -> HttpResponse:
    main: str = "Это главная страница проекта Yatube"
    posts = Post.objects.order_by('-pub_date')[:10]
    context: dict = {
        'posts': posts,
        'main': main
    }
    template: str = 'posts/index.html'
    return render(request, template, context)


def group_posts(request: str, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context: dict = {
        'group': group,
        'posts': posts,
    }
    template: str = 'posts/group_list.html'
    return render(request, template, context)
