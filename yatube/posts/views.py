from django.shortcuts import render, HttpResponse
from .models import Post


def index(request: str) -> HttpResponse:
    main: str = "Это главная страница проекта Yatube"
    posts = Post.objects.order_by('-pub_date')[:10]
    context: dict = {
        'posts': posts,
        'main': main
    }
    template: str = 'posts/index.html'
    return render(request, template, context)


def group_posts(request) -> HttpResponse:
    group: str = "Здесь будет информация о группах проекта Yatube"
    context: dict = {
        'group': group
    }
    template: str = 'posts/group_list.html'
    return render(request, template, context)


def group_posts_detal(request: str, slug: str) -> HttpResponse:
    return HttpResponse(f'А это пост {slug}')
