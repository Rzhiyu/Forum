from myblog.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView


class CommentNoticeListView(LoginRequiredMixin, ListView):
    context_object_name = 'notices'
    template_name = 'notice/list.html'
    login_url = 'login'

    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):

    def get(self, request):

        notice_id = request.GET.get('notice_id')

        if notice_id:
            article = Post.objects.get(id=request.GET.get('post_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)

        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')
