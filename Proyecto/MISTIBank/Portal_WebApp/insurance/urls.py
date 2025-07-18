from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.hello, name='hello'),
    path('about/', views.about),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), 
    path('seguros/', views.seguros_contratados, name='seguros_contratados'),
    path('depositar/', views.depositar, name='depositar'),
    path('retirar/', views.retirar, name='retirar'),
    path('seguros/contratar/<int:tipo_id>/', views.contratar_seguro, name='contratar_seguro'),
    path('grafica-movimientos/', views.grafica_movimientos, name='grafica_movimientos'),
    path('grafica-seguros-marketing/', views.grafica_marketing, name='grafica_marketing'),
    path('estado-cuenta/', views.estado_cuenta_pdf, name='estado_cuenta_pdf'),

]
