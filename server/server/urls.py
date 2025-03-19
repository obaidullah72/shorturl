# shorturl_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shorturl import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('stats/', views.stats, name='stats'),
    path('', include('shorturl.urls')),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])