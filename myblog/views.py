import re

import markdown
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm, EditForm \
    # , CommentForm
from .models import Post, Category


# Create your views here.
# def home(request):
#     return render(request, 'home.html', {})

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']

    # ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        cats_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cats_menu'] = cats_menu
        return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_detail.html'

    def get_context_data(self, *args, **kwargs):
        cats_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

        post = get_object_or_404(Post, id=self.kwargs['pk'])
        post.increase_views()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        toc = m.group(1) if m is not None else ''
        total_likes = post.total_like()
        total_views = post.views
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        else:
            liked = False
        context['cats_menu'] = cats_menu
        context['total_likes'] = total_likes
        context['liked'] = liked
        context['total_views'] = total_views
        context['body'] = post.body
        context['toc'] = toc

        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    # 从models中调用哪些field
    # fields = '__all__'


# class AddCommentView(CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'add_comment.html'
#     ordering = ['-post_date']
#     # 从models中调用哪些field
#
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         form.instance.post_id = self.kwargs['pk']
#         return super().form_valid(form)


class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    success_url = reverse_lazy('home')


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    cats_menu_list = Category.objects.all()
    return render(request, 'category.html', {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts,
                                             'cat_menu_list': cats_menu_list})


def CategoryListView(request):
    cats_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cats_menu_list})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse_lazy('article_detail', args=[str(pk)]))
