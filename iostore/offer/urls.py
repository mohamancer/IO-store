from django.urls import path
from . import views
urlpatterns = [
    path('offer/<str:pk>/',views.offer, name="offer"),
    path('create-offer/', views.createOffer, name="create-offer"),
    path('update-offer/<str:pk>/', views.updateOffer, name="update-offer"),
    path('delete-offer/<str:pk>/', views.deleteOffer, name="delete-offer"),
]