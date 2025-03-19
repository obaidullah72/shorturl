from django.urls import path
from . import views

urlpatterns = [
    path('shorten/', views.ShortURLListCreate.as_view(), name='shorten-create'),
    path('shorten/<str:short_code>/', views.ShortURLDetail.as_view(), name='shorten-detail'),
    path('<str:short_code>/', views.ShortURLRedirect.as_view(), name='shorten-redirect'),
    path('stats/<str:short_code>/', views.ShortURLStats.as_view(), name='shorten-stats'),
]