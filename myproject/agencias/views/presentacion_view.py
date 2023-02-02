from django.shortcuts import render, redirect
from ..models import * 

def presentacion(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin/')
        elif request.user.is_turist:
            return redirect('turista-paquetes')
        else:
            return redirect('manager-home')
    turistas = Turista.objects.filter(user__in=User.objects.filter(is_active=True)).count()
    agencias = Agencia.objects.all().count()
    paquetes = Paquete.objects.filter(disponible=True).count()
    excursiones = Excursion.objects.filter(disponible=True).count()
    reservaciones = ReservacionPaquete.objects.all().count() + ReservacionIndividual.objects.all().count()
    hoteles = Hotel.objects.all().count()
    ctx={}
    ctx['turistas']=turistas
    ctx['agencias']=agencias
    ctx['paquetes']=paquetes
    ctx['excursiones']=excursiones
    ctx['reservaciones']=reservaciones
    ctx['hoteles']=hoteles
    return render(request, 'presentacion.html',ctx)