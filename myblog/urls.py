"""simpleblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('myblog/', include('myblog.urls'))
"""
from django.urls import path

from .views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, LikeView, CategoryView, \
    AddCatView, search

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name="article_detail"),
    path('add_post/', AddPostView.as_view(), name="add_post"),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('cats/<int:pk>', CategoryView.as_view(), name='cats'),
    path('add_cat/', AddCatView.as_view(), name='add_cat'),
    path('search/', search, name='search'),

]
