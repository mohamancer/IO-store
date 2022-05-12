from django.urls import path
from . import views

urlpatterns = [
    path('login/' , views.login_page , name = "users-login"),
    path('register/' , views.register_page , name = "users-register"),
    path('logout/' , views.logout_user , name = "users-logout"),
    path('profile/<str:pk>/', views.profile_page, name="users-profile"),
    path('update-profile/', views.update_profile, name="update-profile"),
]
