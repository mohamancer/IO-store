from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/', views.post, name='offer-home'),
]

    
