from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from myblog.models import Post


class Comment(models.Model):
    commentator = models.ForeignKey(User,
                                    verbose_name='username',
                                    on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post,
                             verbose_name='post',
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'comments'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return '{}: {}'.format(self.commentator, self.text[:20])
