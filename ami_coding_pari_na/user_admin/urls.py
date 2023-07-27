from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name="login" ),
    path('logout/', views.user_logout, name="logout"),
    path('registration/', views.user_registration, name="user_registration"),
    path('activate/<uidb64>/<token>/', views.ActivateAccount, name='activate'),
]
