from django.urls import path
from feed import views

urlpatterns = [
    path('', views.home, name='feed-home'),
    path('review/<str:pk>/', views.review, name='review')
]
