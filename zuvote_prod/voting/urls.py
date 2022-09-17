from django import urls
from django.urls import path
from . import views


urlpatterns = [
    path('', views.voting_preview, name='voting_preview'),
    path('voting_page/<str:pubcode>/', views.voting_page, name='voting_page'),
    path('voting_page/<str:pubcode>/<int:pk>/', views.vote, name='vote'),
    path('verifypayment/', views.verifypayment, name='verifypayment'),
]