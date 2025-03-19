from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shorturl.views import IndexView, StatsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('', include('shorturl.urls')),
]


# If you want to serve static files in development (optional)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
