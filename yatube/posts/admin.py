from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text_post', 'pub_date', 'author_post') 
    search_fields = ('text_post',) 
    list_filter = ('pub_date',) 

admin.site.register(Post, PostAdmin)  