"""
URL configuration for takeout project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from apps.api import app
from takeout import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.urls),

]

# 配置静态资源访问
if settings.DEBUG:
    # H5 页面
    urlpatterns += static(settings.FRONT_URL, document_root=settings.FRONT_ROOT)
    urlpatterns += static(settings.BACKEND_URL, document_root=settings.BACKEND_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^front/(?P<path>.*)$', serve, {'document_root': settings.FRONT_ROOT}, name='front'),
        re_path(r'^backend/(?P<path>.*)$', serve, {'document_root': settings.BACKEND_ROOT}, name='backend'),
        # 上传图片资源
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    ]

