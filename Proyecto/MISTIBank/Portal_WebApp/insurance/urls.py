from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.hello),
    path('about/', views.about),
    path('login/', views.login),
    path('dashboard/', views.dashboard),
    path('grafica-usuario/', views.grafica_seguros_usuario, name='grafica_usuario'),
]