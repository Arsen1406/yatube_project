from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    main = "Последние обновления на сайте"
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'posts': posts,
        'main': main
    }
    template: str = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)
