from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='feed-home'),
    path('post/<str:pk>/', views.post, name='feed-post'),
]
