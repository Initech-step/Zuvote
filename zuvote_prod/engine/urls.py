from django import urls
from django.urls import path
from . import views



urlpatterns = [
    path('', views.panel, name='panel'),
    path('main_panel/', views.main_panel, name='main_panel'),
    path('view_contestant_stat/', views.view_stat, name='view_stat'),
    path('view_transactions/', views.view_transactions, name='view_transactions'),
    path('create_competition/', views.create_competition, name='create_competition'),
    path('set_managing/', views.set_managing, name='set_managing'),
    path('set_managing_b/<str:slug>/', views.set_managing_b, name='set_managing_b'),
    path('add_contestant/', views.add_contestant, name='add_contestant'),
    path('view_all_contestants/', views.view_all_contestants, name='view_all_contestants'),
    path('view_all_contestants/delete_contestant/<int:pk>/', views.delete_contestant, name='delete_contestant'),
    path('view_all_contestants/edit_contestant/<int:pk>/', views.edit_contestant, name='edit_contestant'),
    path('set_active_state/', views.set_active_state, name='set_active_state'),
    path('take_pay/', views.take_pay, name='take_pay'),
]