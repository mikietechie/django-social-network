from django.contrib import admin
from .models import *
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'user','msg','timestamp','likes','dislikes'
    ]

admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'post','user','comment'
    ]

admin.site.register(Comment,CommentAdmin)

class FollowAdmin(admin.ModelAdmin):
    list_display = [
        'user','follower'
    ]

admin.site.register(Follow,FollowAdmin)

