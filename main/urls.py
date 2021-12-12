from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('addcontestant/', views.addcontestant, name='addcontestant'),
    path('updel/', views.updel, name='updel'),
    path('signin/', views.signin, name='signin'),
    path('panel/', views.panel, name='panel'),
    path('create/', views.create, name='create'),
    path('setall/', views.setall, name='setall'),
    path('voting/', views.voting, name='voting'),
    path('payment/', views.payment, name='payment'),
    path('choice/<int:pk>', views.choice, name='choice'),
    path('update/<int:pk>/', views.update, name='update'),
]