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
import notifications.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('myblog.urls')),
                  path('', include('comments.urls', namespace='comment')),
                  path('members/', include('django.contrib.auth.urls')),
                  path('members/', include('members.urls')),
                  path('inbox/notifications/',
                       include(notifications.urls, namespace='notifications')),
                  path('notice/', include('notice.urls', namespace='notice')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
