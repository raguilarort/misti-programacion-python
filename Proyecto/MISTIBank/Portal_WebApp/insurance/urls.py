from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.hello),
    path('about/', views.about),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), 
]
