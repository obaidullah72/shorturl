from django.urls import path
from .views import (
    ShortURLListCreate,
    ShortURLDetail,
    ShortURLRedirect,
    ShortURLStats,
)

urlpatterns = [
    path('shorten/', ShortURLListCreate.as_view(), name='shorten-create'),                   # GET/POST all short URLs
    path('shorten/<str:short_code>/', ShortURLDetail.as_view(), name='shorten-detail'),      # GET/PUT/DELETE a specific short URL
    path('<str:short_code>/', ShortURLRedirect.as_view(), name='shorten-redirect'),          # Redirect to original URL
    path('stats/<str:short_code>/', ShortURLStats.as_view(), name='shorten-stats'),          # GET statistics for a specific short URL
]
