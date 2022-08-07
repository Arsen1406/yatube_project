from typing import Any
from django.shortcuts import render, HttpResponse

def index(request) -> HttpResponse:
    return HttpResponse('Привет. Это наша главная страница. Добро пожаловать мой друг!))')

def group_posts(request) -> HttpResponse:
    return HttpResponse('Вот здесь будут все ваши и наши блоги')


def group_posts_detal(request, slug: str) -> HttpResponse:
    return HttpResponse(f'А это пост {slug}')