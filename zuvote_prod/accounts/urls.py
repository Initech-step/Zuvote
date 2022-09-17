from django import urls
from django.urls import path
from . import views



urlpatterns = [
    path('', views.register, name='register'),
    path('login_zuvote/', views.login_zuvote, name='login_zuvote'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('logout/', views.logout_page, name='logout_page'),
]