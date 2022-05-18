from django.urls import path
from . import views

from .handle_deadline import periodically_mark_offers_inactive_by_deadline_thread

periodically_mark_offers_inactive_by_deadline_thread()

urlpatterns = [
    path('offer/<str:pk>/',views.offer, name="offer"),
    path('create-offer/', views.createOffer, name="create-offer"),
    path('update-offer/<str:pk>/', views.updateOffer, name="update-offer"),
    path('delete-offer/<str:pk>/', views.deleteOffer, name="delete-offer"),
    path('delete-bid/<str:pk>/', views.deleteBid, name="delete-bid"),
    path('accept-bid/<str:pk>/', views.acceptBid, name="accept-bid"),
]