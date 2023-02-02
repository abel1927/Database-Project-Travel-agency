from django.shortcuts import render
from .models import Agencia, Oferta, Paquete, Excursion
from django.db.models import Count

def cargar_ofertas(request):
    hotel_id = request.GET.get('hotel')
    ofertas = None
    if hotel_id == -1:
        ofertas = Oferta.objects.none()
    else:
        ofertas = Oferta.objects.filter(hotel=hotel_id).order_by('descripcion')
    return render(request, 'ofertas_dropdown_list.html', {'ofertas': ofertas})

def filtrar_paquetes(request):
    inc_fac =  request.GET.get('incluir_fac')
    minimo_p = int(request.GET.get('minimo_p'))
    maximo_p = int(request.GET.get('maximo_p'))
    minimo_dur = int(request.GET.get('minimo_dur'))
    maximo_dur = int(request.GET.get('maximo_dur'))
    if minimo_p == -1:
        minimo_p = 0
    if minimo_dur == -1:
        minimo_dur = 0
    if maximo_p == -1:
        maximo_p = 50000000
    if maximo_dur == -1:
        maximo_dur = 100000
    if inc_fac == 'true':
        paquetes = Paquete.objects.annotate(cant_hoteles=Count('hoteles',distinct=True),
                                        cant_facilidades=Count('facilidades', distinct=True)).filter(
                                        disponible=True, precio__gt=minimo_p-1, precio__lt=maximo_p+1,
                                        duracion__gt=minimo_dur-1, duracion__lt=maximo_dur+1,
                                        cant_facilidades__gt=0).distinct()
    else:
        paquetes = Paquete.objects.annotate(cant_hoteles=Count('hoteles',distinct=True),
                                        cant_facilidades=Count('facilidades', distinct=True)).filter(
                                        disponible=True, precio__gt=minimo_p-1, precio__lt=maximo_p+1,
                                        duracion__gt=minimo_dur-1, duracion__lt=maximo_dur+1).distinct()
    return render(request, 'paquetes_respuesta_query.html', {'paquetes': paquetes})

def filtrar_excursiones(request):
    inc_hot =  request.GET.get('incluir_hot')
    minimo_p = int(request.GET.get('minimo_p'))
    maximo_p = int(request.GET.get('maximo_p'))
    if minimo_p == -1:
        minimo_p = 0
    if maximo_p == -1:
        maximo_p = 50000000
    if inc_hot == 'true':
        excursiones = Excursion.objects.annotate(cant_hoteles=Count('hoteles',distinct=True)).filter(
            disponible=True,agencia__gt=0,precio__gt=minimo_p-1, precio__lt=maximo_p+1,
            cant_hoteles__gt=0)
    else:
        excursiones = Excursion.objects.annotate(cant_hoteles=Count('hoteles',distinct=True)).filter(
            disponible=True,agencia__gt=0,precio__gt=minimo_p-1, precio__lt=maximo_p+1)
    return render(request, 'excursiones_respuesta_query.html', {'excursiones': excursiones})

def filtrar_ofertas(request):
    minimo_p = int(request.GET.get('minimo_p'))
    maximo_p = int(request.GET.get('maximo_p'))
    minimo_cat = int(request.GET.get('minimo_cat'))
    maximo_cat = int(request.GET.get('maximo_cat'))
    if minimo_p == -1:
        minimo_p = 0
    if minimo_cat == -1:
        minimo_cat = 1
    if maximo_p == -1:
        maximo_p = 50000000
    if maximo_cat == -1:
        maximo_cat = 5
    ofertas = Oferta.objects.filter(hotel__agencia__gt=0, precio__gt=minimo_p-1, precio__lt=maximo_p+1,
                                    hotel__categoria__gt=minimo_cat-1, hotel__categoria__lt=maximo_cat+1).distinct()    
    return render(request, 'hoteles_respuesta_query.html', {'ofertas': ofertas})

def filtrar_paquetes_manager(request):
    mayor_que_promedio = request.GET.get('mayor_que_promedio')
    agencia_id = request.GET.get('agencia')
    agencia = Agencia.objects.get(pk=agencia_id)
    #paquetes de esa agencia con precio pro encima de promedio
    if mayor_que_promedio == 'true':
        p = Paquete.objects.all().values_list('precio',flat=True)
        suma = 0
        for i in p:
            suma+=i
        promedio = suma/len(p)
        paquetes = Paquete.objects.annotate(cant_hoteles=Count('hoteles',distinct=True),
                                            cant_facilidades=Count('facilidades', distinct=True),
                                            cant_reservaciones=Count('reservacionpaquete', distinct=True)).filter(
                                            agencia=agencia,precio__gt=promedio)
    else:
        paquetes = Paquete.objects.annotate(cant_hoteles=Count('hoteles',distinct=True),
                                            cant_facilidades=Count('facilidades', distinct=True),
                                            cant_reservaciones=Count('reservacionpaquete', distinct=True)).filter(
                                            agencia=agencia)
    return render(request, 'paquetes_promedio_respuesta_query.html', {'paquetes': paquetes})

def filtrar_excursiones_finde_extendido(request):
    finde_extendido = request.GET.get('finde_extendido')
    agencia_id = request.GET.get('agencia')
    agencia = Agencia.objects.get(pk=agencia_id)
    if finde_extendido == 'true':
        excursiones=Excursion.objects.annotate(cant_hoteles=Count('hoteles',distinct=True)).filter(
                                                disponible=True,agencia=agencia,diaSalida=5,diaLlegada=7)
    else:
        excursiones=Excursion.objects.annotate(cant_hoteles=Count('hoteles',distinct=True)).filter(
                                                disponible=True,agencia=agencia)
    return render(request, 'excursiones_finde_extendido_respuesta_query.html', {'excursiones': excursiones})

