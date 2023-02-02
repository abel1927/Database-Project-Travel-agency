"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls.conf import include
from agencias.views.presentacion_view import presentacion
from agencias.views.turistas_views import * 
from agencias.views.manager_views import * 
from cuentas import views as cuentas_views
from agencias.ajax import * 

urlpatterns = [
    path('', presentacion, name='presentacion'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('turista-signup/', cuentas_views.TuristatSignUpView.as_view(), name='turista-signup'),
    path('agencia-solicitud/validada<int:pk>/', cuentas_views.solicitud_validada, name='solicitud-validada'),
    path('agencia-solicitud/', cuentas_views.solicitud_agencia, name='agencia-solicitud'),
    

    path('turista-home/', turista_home, name='turista-home'),
    
    path('turista-perfil/', turista_perfil, name='turista-perfil'),
    path('turista-home/perfil/editar/', turista_perfil_editar, name='turista-perfil-editar'),
    path('turista-home/estadisticas/', turista_estadisticas, name='turista-estadisticas'),
    

    path('turista-home/paquetes/', turista_paquetes, name='turista-paquetes'),
    path('turista-home/paquetes/reserva:<int:pk>/', paquete_reserva, name='paquete-reserva'),
    path('turista-home/paquetes/reserva-completada:<int:pk>/', 
    reserva_paquete_completada, name='reserva-paquete-completada'),
    path('ajax/filtrar-paquetes/', filtrar_paquetes, name='ajax-filtrar-paquetes'),

    path('turista-home/hoteles/', turista_hoteles, name='turista-hoteles'),
    path('turista-home/hoteles/reserva:<int:pk>/', hotel_reserva, name='hotel-reserva'),
    path('ajax/filtrar-ofertas/', filtrar_ofertas, name='ajax-filtrar-ofertas'),
    
    path('turista-home/excursiones/', turista_excursiones, name='turista-excursiones'),
    path('turista-home/excursion/reserva:<int:pk>/', excursion_reserva, name='excursion-reserva'),
    path('ajax/filtrar-excursiones/', filtrar_excursiones, name='ajax-filtrar-excursiones'),

    path('turista-home/reserva-por-agencias/', turista_reserva_por_agencia, name='turista-agencias'),
    path('turista-home/agencia/reserva:<int:pk>/', agencia_reserva, name='agencia-reserva'),
    path('turista-home/agencia/reserva-completada:<int:pk>/', 
    reserva_agencia_completada, name='reserva-agencia-completada'),
    path('ajax/ofertas-hotel/', cargar_ofertas, name='ajax-ofertas-hotel'),

    path('manager-home/', manager_home, name='manager-home'),

    path('manager-home/', manager_home, name='manager-home'),
    path('manager-home/perfil/', manager_perfil, name='manager-perfil'),
    path('manager-home/perfil/editar/', manager_perfil_editar, name='manager-perfil-editar'),
    path('manager-home/estadisticas/', manager_estadisticas, name='manager-estadisticas'),
    path('manager-home/estadisticas/comparar/', manager_estadisticas_comparar, name='manager-estadisticas-comparar'),

    path('manager-home/agencia/editar/', manager_agencia_editar, name='manager-agencia-editar'),
    
    path('manager-home/paquete/', manager_paquete, name='manager-paquete'),
    path('manager-home/paquete-editar/paquete:<int:pk>/', manager_paquete_editar, name='manager-paquete-editar'),
    path('manager-home/paquete-nuevo/', manager_paquete_nuevo, name='manager-paquete-nuevo'),
    path('ajax/paquetes-promedio/', filtrar_paquetes_manager, name='ajax-paquetes-promedio'),

    path('manager-home/hotel/', manager_hotel, name='manager-hotel'),
    path('manager-home/hotel-eliminar/hotel:<int:pk>/', manager_hotel_eliminar, name='manager-hotel-eliminar'),
    path('manager-home/hotel-agregar/', manager_hotel_agregar, name='manager-hotel-agregar'),
    
    path('manager-home/excursion/', manager_excursion, name='manager-excursion'),
    path('manager-home/excursion-eliminar/excursion:<int:pk>/', manager_excursion_eliminar, name='manager-excursion-eliminar'),
    path('manager-home/excursion-agregar/', manager_excursion_agregar, name='manager-excursion-agregar'),
    path('ajax/excursiones-finde-extendido/', filtrar_excursiones_finde_extendido, name='ajax-excursion-finde_extendido'),
    

    path('manager-home/reservaciones/', manager_reservaciones, name='manager-reservaciones'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('admin/', admin.site.urls),
]

