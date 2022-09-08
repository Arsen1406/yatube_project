from django.contrib.auth import get_user_model
from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Post, Group
from django import forms

User = get_user_model()
POST_ID = '1'
POST_TEXT = 'Тестовый пост'
USER_NAME = 'TestUser'
USER_NAME_2 = 'TestUser_2'
GROUP_TITLE = 'Тестовая группа'
GROUP_SLUG = 'test-slug'
GROUP_DISCRIPTION = 'Тестовое описание'

TEMLATES_PAGES = {
    reverse('posts:index'): 'posts/index.html',
    (reverse('posts:group', kwargs={'slug': GROUP_SLUG})):
        'posts/group_list.html',
    (reverse('posts:profile', kwargs={'username': USER_NAME})):
        'posts/profile.html',
}


def create_user(username):
    user = User.objects.create_user(username=username)
    return user


def group_create():
    Group.objects.create(
        title=GROUP_TITLE,
        slug=GROUP_SLUG,
        description=GROUP_DISCRIPTION
    )


def post_create(user):
    Post.objects.create(
        text='Тестовый пост',
        group=Group.objects.get(title=GROUP_TITLE),
        author=user
    )


class PostPagesTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        group_create()
        post_create(create_user(USER_NAME))
        post_create(create_user(USER_NAME_2))

    def setUp(self):
        self.guest_client = Client()
        self.autorized_client = Client()
        self.user = User.objects.get(username=USER_NAME)
        self.autorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            (reverse('posts:group', kwargs={'slug': GROUP_SLUG})):
                'posts/group_list.html',
            (reverse('posts:profile', kwargs={'username': USER_NAME})):
                'posts/profile.html',
            (reverse('posts:post_detail', kwargs={'post_id': POST_ID})):
                'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            (reverse('posts:edit', kwargs={'post_id': POST_ID})):
                'posts/create_post.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.autorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_correct_context(self):
        response = self.autorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_posts_list_page_show_correct_context(self):
        first_obj = 0
        for reverse_name, template in TEMLATES_PAGES.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.autorized_client.get(reverse_name)
                first_object = response.context['page_obj'][first_obj]
                self.assertEqual(first_object.text,
                                 POST_TEXT,
                                 f'page_obg неверно передается в {template}')
                self.assertEqual(first_object.group.title,
                                 GROUP_TITLE,
                                 f'page_obg неверно передается в {template}')

    def test_posts_correct_context_post_detail(self):
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'post_id': POST_ID})
        )
        first_object = response.context['post']
        self.assertEqual(first_object.text,
                         POST_TEXT,
                         f'post неверно передается в {response}')
        self.assertEqual(first_object.group.title,
                         GROUP_TITLE,
                         f'post неверно передается в {response}')

    def test_posts_correct_context_post_edit(self):
        rev_http = reverse('posts:edit', kwargs={'post_id': POST_ID})
        response = self.autorized_client.get(rev_http)
        first_object = response.context['form']
        group = Group.objects.get(pk=first_object.initial['group'])
        self.assertEqual(first_object.initial['text'],
                         POST_TEXT,
                         f'form неверно передается пост в {rev_http}')
        self.assertEqual(group.title,
                         GROUP_TITLE,
                         f'form неверно передается группа в {rev_http}')

    def test_posts_correct_context_post_create_edit_guest(self):
        response_create = self.guest_client.get(reverse('posts:post_create'))
        response_edit = self.guest_client.get(
            reverse('posts:edit', kwargs={'post_id': POST_ID}))
        self.assertEqual(HTTPStatus(response_create.status_code).phrase,
                         'Found',
                         'Гость не может создать пост'
                         )
        self.assertEqual(HTTPStatus(response_edit.status_code).phrase,
                         'Found',
                         'Гость не может менять посты'
                         )

    def test_posts_correct_context_post_edit_user_post(self):
        post_id = 2
        response = self.autorized_client.get(
            reverse('posts:edit', kwargs={'post_id': post_id}))
        self.assertEqual(HTTPStatus(response.status_code).phrase,
                         'Found',
                         'Юзер может редактировать только свои посты'
                         )


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        COUNT_POST = 13
        super().setUpClass()
        group_create()
        user = create_user(USER_NAME)

        for i in range(COUNT_POST):
            post_create(user)

    def setUp(self):
        self.autorized_client = Client()
        self.user = User.objects.get(username=USER_NAME)
        self.autorized_client.force_login(self.user)

    def test_first_page_contains_paginator(self):
        ten_pages = 10
        three_pages = 3
        for reverse_name, template in TEMLATES_PAGES.items():
            with self.subTest(reverse_name=reverse_name):
                response_one = self.client.get(reverse_name)
                response_two = self.client.get(
                    f'{reverse_name}?page=2'
                )
                self.assertEqual(
                    len(response_one.context['page_obj']),
                    ten_pages,
                    f'Paginator страницы - 1, '
                    f'{reverse_name} работает не правильно'
                )
                self.assertEqual(
                    len(response_two.context['page_obj']),
                    three_pages,
                    f'Paginator страницы - 2, '
                    f'{reverse_name} работает не правильно'
                )
