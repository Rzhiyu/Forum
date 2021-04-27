from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['commentator', 'post', 'text', 'created_time']
    fields = ['commentator', 'post', 'text', 'created_time']


admin.site.register(Comment, CommentAdmin)
