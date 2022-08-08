from django.shortcuts import render, HttpResponse


def index(request) -> HttpResponse:
    main = "Это главная страница проекта Yatube"
    context = {
        'main': main
    }
    template = 'posts/index.html'
    return render(request, template, context)

def group_posts(request) -> HttpResponse:
    group = "Здесь будет информация о группах проекта Yatube"
    context = {
        'group': group
    }
    template = 'posts/group_list.html'
    return render(request, template, context)


def group_posts_detal(request, slug: str) -> HttpResponse:
    return HttpResponse(f'А это пост {slug}')