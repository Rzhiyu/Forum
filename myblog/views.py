import re

import markdown
from django.contrib import messages
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from markdown.extensions.toc import TocExtension

from .forms import PostForm, EditForm, CatForm
from .models import Post, Category


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-views']

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        category_list = Category.objects.annotate(posts_num=Count('post')).order_by('-posts_num')
        context['category_list'] = category_list
        return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        post.increase_views()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        total_likes = post.total_like()
        total_views = post.views
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        else:
            liked = False
        context['total_likes'] = total_likes
        context['liked'] = liked
        context['total_views'] = total_views
        context['body'] = post.body
        context['toc'] = post.toc

        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('home')


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    success_url = reverse_lazy('home')


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


class CategoryView(ListView):
    model = Post
    template_name = 'cats.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class AddCatView(CreateView):
    model = Category
    form_class = CatForm
    template_name = 'add_cat.html'
    success_url = reverse_lazy('home')


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


def search(request):
    q = request.GET.get('q')

    if not q:
        messages.add_message(request, messages.ERROR, "😱，搜索出错惹", extra_tags='danger')
        return redirect('home')
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q) | Q(author__username__icontains=q))
    messages.add_message(request, messages.SUCCESS, "φ(゜▽゜*)♪", extra_tags='success')
    return render(request, 'home.html', {'post_list': post_list})
