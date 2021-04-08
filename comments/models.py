from django.db import models
from django.utils import timezone


class Comment(models.Model):
    name = models.CharField(blank=True, max_length=50)
    text = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('myblog.Post', verbose_name='post', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'comments'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:100])
