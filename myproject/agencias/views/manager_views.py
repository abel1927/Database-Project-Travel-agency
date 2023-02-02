from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Avg
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from ..models import *
from ..forms.manager_forms import * 


def manager_required(user:User):
    if not user.is_manager:
        if user.is_turist:
            return redirect('turista-home')
        return redirect('admin/')

###### Manager Area
@login_required
def manager_home(request):
    manager_required(request.user)
    return render(request, 'manager_perfil.html')

@login_required
def manager_perfil(request):
    manager_required(request.user)
    return render(request, 'manager_perfil.html')

@login_required
def manager_perfil_editar(request):
    manager_required(request.user)
    if request.method =='POST':
        form = ManagerPerfilEditar(request.POST)
        if form.is_valid():
            u = User.objects.filter(username=form.cleaned_data['NombreUsuario'])
            if u.count() == 0 or u[0] == request.user:
                request.user.username = form.cleaned_data['NombreUsuario']
                request.user.first_name = form.cleaned_data['Nombre']
                request.user.last_name = form.cleaned_data['Apellido']
                request.user.email = form.cleaned_data['Email']
                request.user.set_password(form.cleaned_data['Contrasena'])
                request.user.save()
                login(request,request.user)
                return redirect('manager-perfil')

    form= ManagerPerfilEditar(initial={'Nombre':request.user.first_name,
                                        'Apellido':request.user.last_name,
                                        'NombreUsuario':request.user.username,
                                        'Email':request.user.email,
                                        'Contrasena':request.user.password})
    return render(request, 'manager_perfil_editar.html',{'form': form})

@login_required
def manager_agencia_editar(request):
    manager_required(request.user)
    if request.method =='POST':
        form = ManagerAgenciaEditar(request.POST)
        if form.is_valid():
            request.user.manageragencia.agencia.nombre = form.cleaned_data['Nombre']
            request.user.manageragencia.agencia.direccion = form.cleaned_data['Direccion']
            request.user.manageragencia.agencia.email = form.cleaned_data['Email']
            request.user.manageragencia.agencia.noFax = form.cleaned_data['noFax']
            request.user.manageragencia.agencia.save()
            return redirect('manager-paquete')

    form= ManagerAgenciaEditar(initial={'Nombre':request.user.manageragencia.agencia.nombre,
                                        'Direccion':request.user.manageragencia.agencia.direccion,
                                        'Email':request.user.manageragencia.agencia.email,
                                        'noFax':request.user.manageragencia.agencia.noFax,})
    
    return render(request, 'manager_agencia_editar.html',{'form': form})


#####---->Paquete

@login_required
def manager_paquete(request):
    manager_required(request.user)
    paquetes = Paquete.objects.annotate(cant_hoteles=Count('hoteles',distinct=True),
                                        cant_facilidades=Count('facilidades', distinct=True),
                                        cant_reservaciones=Count('reservacionpaquete', distinct=True)).filter(agencia=request.user.manageragencia.agencia)
    return render(request, 'manager_paquete.html',{'paquetes':paquetes})

@login_required
def manager_paquete_editar(request,pk):
    manager_required(request.user)
    agencia = request.user.manageragencia.agencia
    paquete = Paquete.objects.get(CodigoP=pk)
    list_hoteles=Hotel.objects.all()
    #list_hoteles=Hotel.objects.all().values_list('IdH','nombre') 
    #list_hoteles=[cat for cat in list_hoteles]
    list_facilidades=Facilidad.objects.all().values_list('IdF','descripcion')
    print(list_facilidades)
    selected_hoteles=paquete.hoteles.values_list('IdH',flat=True)
    selected_facilidades=paquete.facilidades.values_list('IdF',flat=True)
    
    if request.method == 'POST':
        form =PaqueteEditar(request.POST, agencia=agencia)
        if form.is_valid():
            paquete.duracion= form.cleaned_data['Duracion']
            paquete.descripcion= form.cleaned_data['Descripcion']
            paquete.precio = form.cleaned_data['Precio']
            paquete.hoteles.set(Hotel.objects.none())
            for h in form.cleaned_data['Hoteles']:
                paquete.hoteles.add(h)
            paquete.facilidades.set(Facilidad.objects.none())
            for f in form.cleaned_data['Facilidades']:
                paquete.facilidades.add(f)
            paquete.disponible = form.cleaned_data['Disponible']
            paquete.save()
            return redirect('manager-paquete')


    form= PaqueteEditar(initial={'Descripcion':paquete.descripcion,
                                'Precio' :paquete.precio,
                                'Duracion' :paquete.duracion,
                                'Disponible' :paquete.disponible,
                                'Hoteles' :[cat for cat in selected_hoteles],
                                'Facilidades' :[cat for cat in selected_facilidades]},
                        agencia = agencia
                        )

    return render(request, 'manager_paquete_editar.html',{'form': form})

@login_required
def manager_paquete_nuevo(request):
    manager_required(request.user)
    agencia=request.user.manageragencia.agencia
    if request.method == 'POST':
        form =PaqueteEditar(request.POST,agencia=agencia)
        if form.is_valid():
            paquete=Paquete()
            paquete.agencia=request.user.manageragencia.agencia
            paquete.duracion= form.cleaned_data['Duracion']
            paquete.descripcion= form.cleaned_data['Descripcion']
            paquete.precio = form.cleaned_data['Precio']
            paquete.disponible = form.cleaned_data['Disponible']
            paquete.save()
            paquete.hoteles.set(Hotel.objects.none())
            for h in form.cleaned_data['Hoteles']:
                paquete.hoteles.add(h)
            paquete.facilidades.set(Facilidad.objects.none())
            for f in form.cleaned_data['Facilidades']:
                paquete.facilidades.add(f)
            paquete.save()
            return redirect('manager-paquete')
    form =PaqueteNuevo(agencia=agencia)
    return render(request, 'manager_paquete_nuevo.html',{'form': form})



#####---->Hotel

@login_required
def manager_hotel(request):
    manager_required(request.user)
    return render(request, 'manager_hotel.html',{'hoteles': request.user.manageragencia.agencia.hoteles.all()})

@login_required
def manager_hotel_eliminar(request,pk):
    manager_required(request.user)
    hotel = Hotel.objects.get(IdH=pk)
    request.user.manageragencia.agencia.hoteles.remove(hotel)
    return redirect('manager-hotel')

@login_required
def manager_hotel_agregar(request):
    manager_required(request.user)
    if request.method == 'POST':
        form=HotelAdd(request.POST,agencia=request.user.manageragencia.agencia)
        if form.is_valid():
            for hotel in form.cleaned_data['Hoteles']:
                request.user.manageragencia.agencia.hoteles.add(hotel)
            request.user.manageragencia.agencia.save()
            return redirect('manager-hotel')
    form = HotelAdd(agencia=request.user.manageragencia.agencia)
    return render(request, 'manager_hotel_add.html',{'form': form})


#####---->Excursion

@login_required
def manager_excursion(request):
    manager_required(request.user)
    excursiones=Excursion.objects.annotate(cant_hoteles=Count('hoteles',distinct=True)).filter(disponible=True,agencia=request.user.manageragencia.agencia)
    return render(request, 'manager_excursion.html',{'excursiones': excursiones})

@login_required
def manager_excursion_eliminar(request,pk):
    manager_required(request.user)
    excursion = Excursion.objects.get(IdE=pk)
    request.user.manageragencia.agencia.excursiones.remove(excursion)
    return redirect('manager-excursion')

@login_required
def manager_excursion_agregar(request):
    manager_required(request.user)
    if request.method == 'POST':
        form=ExcursionAdd(request.POST,agencia=request.user.manageragencia.agencia)
        if form.is_valid():
            for excursion in form.cleaned_data['Excursiones']:
                request.user.manageragencia.agencia.excursiones.add(excursion)
            request.user.manageragencia.agencia.save()
            return redirect('manager-excursion')
    form = ExcursionAdd(agencia=request.user.manageragencia.agencia)
    return render(request, 'manager_excursion_add.html',{'form': form})


#####---->Estadísticas

@login_required
def manager_estadisticas(request):
    manager_required(request.user)
    agencia = request.user.manageragencia.agencia
    excursiones = agencia.excursiones.filter(diaSalida=5,diaLlegada=7)
    paquetes =  Paquete.objects.filter(agencia=agencia)
    agencia = Agencia.objects.annotate(promedio=Coalesce(Avg('paquete__precio'),0.0),
                                        dinero_paquete=Coalesce(Sum('paquete__reservacionpaquete__precioTotal',distinct=True),0),
                                        dinero_individual=Coalesce(Sum('reservacionindividual__precioTotal',distinct=True),0),
                                        paquete_count=Count('paquete',distinct=True),
                                        hotel_count=Count('hoteles',distinct=True),
                                        excursion_count=Count('excursiones',distinct=True),
                                        reservacion_paquetes_count=Count('paquete__reservacionpaquete',distinct=True),
                                        reservacion_individual_count=Count('reservacionindividual', distinct=True)).filter(IdA=agencia.IdA)
    agencia=agencia[0]    

    paquetes_precio=paquetes.filter(precio__gt=agencia.promedio)
    paquetes_precio = paquetes_precio.annotate(cant_hoteles=Count('hoteles',distinct=True),
                                        cant_facilidades=Count('facilidades', distinct=True),
                                        cant_reservaciones=Count('reservacionpaquete', distinct=True))

    dinero_total = agencia.dinero_paquete +agencia.dinero_individual
    paquete_total= agencia.paquete_count
    hotel_total=agencia.hotel_count
    excursion_total=agencia.excursion_count
    reservacion_paquetes=agencia.reservacion_paquetes_count
    reservacion_individual=agencia.reservacion_individual_count

    ctx={}
    ctx['excursiones'] = excursiones
    #ctx['paquetes'] = paquetes
    ctx['paquetes_precio'] = paquetes_precio
    ctx['dinero_total'] = dinero_total
    ctx['paquete_total'] = paquete_total
    ctx['hotel_total'] = hotel_total
    ctx['excursion_total'] = excursion_total
    ctx['reservaciones_paquete_total'] = reservacion_paquetes
    ctx['reservaciones_individuales_total'] = reservacion_individual
    ctx['reservaciones_total'] = reservacion_paquetes+reservacion_individual
    return render(request, 'manager_estadisticas.html',ctx)

@login_required
def manager_estadisticas_comparar(request):
    manager_required(request.user)
    agencia = request.user.manageragencia.agencia
    agencias = Agencia.objects.annotate(paquete_promedio=Coalesce(Avg('paquete__precio'),0.0),
                                        dinero_paquete=Coalesce(Sum('paquete__reservacionpaquete__precioTotal',distinct=True),0),
                                        dinero_individual=Coalesce(Sum('reservacionindividual__precioTotal',distinct=True),0),
                                        dinero_total=Coalesce(Sum('paquete__reservacionpaquete__precioTotal',distinct=True)+Sum('reservacionindividual__precioTotal',distinct=True),0),
                                        paquete_count=Count('paquete',distinct=True),
                                        hotel_count=Count('hoteles',distinct=True),
                                        excursion_count=Count('excursiones',distinct=True),
                                        reservacion_paquetes_count=Count('paquete__reservacionpaquete',distinct=True),
                                        reservacion_individual_count=Count('reservacionindividual', distinct=True),
                                        reservacion_total=Count('paquete__reservacionpaquete',distinct=True)+Count('reservacionindividual', distinct=True),
                                        turistas_count=Count('paquete__reservacionpaquete__turista',distinct=True))
    agencia = agencias.get(IdA=agencia.IdA)
    agencia_dinero_total = agencia.dinero_total
    ranking_por_ganancias = agencias.filter(dinero_total__gt=agencia_dinero_total).count()+1
    suma=0
    for s in agencias:
        suma += 0 if s.dinero_total==None else s.dinero_total
    promedio_ganacias_por_agencias = round(suma/agencias.count(),2)

    agencia_reservaciones_total = agencia.reservacion_total
    ranking_por_reservaciones_total = agencias.filter(reservacion_total__gt=agencia_reservaciones_total).count()+1
    
    suma=0
    for s in agencias:
        suma += s.reservacion_total
    promedio_reservaciones_total_por_agencia = round(suma/agencias.count(),2)

    agencia_reservaciones_paquete=agencia.reservacion_paquetes_count
    ranking_por_reservaciones_paquete=agencias.filter(reservacion_paquetes_count__gt=agencia_reservaciones_paquete).count()+1

    suma=0
    for s in agencias:
        suma += s.reservacion_paquetes_count
    promedio_reserciones_paquete_por_agencias = round(suma/agencias.count(),2)

    agencia_reservaciones_individuales=agencia.reservacion_individual_count
    ranking_por_reservaciones_ind=agencias.filter(reservacion_individual_count__gt=agencia_reservaciones_individuales).count()+1

    suma=0
    for s in agencias:
        suma += s.reservacion_individual_count
    promedio_reserciones_individuales_por_agencias = round(suma/agencias.count(),2)

    #cantidad_distintos_turistas_reservaron=Turista.objects.filter(reservacionpaquete__in=ReservacionPaquete.objects.filter(paquete__in=Paquete.objects.filter(agencia=agencia))).count()
    cantidad_distintos_turistas_reservaron=agencia.turistas_count
    ranking_por_cantidad_turistas=agencias.filter(turistas_count__gt=cantidad_distintos_turistas_reservaron).count()+1
    suma=0
    for s in agencias:
        suma += s.turistas_count
    promedio_cantidad_turistas_por_agencia = round(suma/agencias.count(),2)

    agencia_cantidad_paquetes_disponibles=agencia.paquete_count
    ranking_cantidad_paquetes_disponibles=agencias.filter(paquete_count__gt=agencia_cantidad_paquetes_disponibles).count()+1
    suma=0
    for s in agencias:
        suma += s.paquete_count
    promedio_cantidad_paquetes_disponibles = round(suma/agencias.count(),2)

    #promedio_precio = Promedio(Paquete.objects.all().values_list('precio'))
    agencia_precio_promedio_por_paquete=agencia.paquete_promedio
    ranking_precio_promedio_por_paquete=agencias.filter(paquete_promedio__gt=agencia_precio_promedio_por_paquete).count()+1
    suma=0
    for s in agencias:
        suma += 0 if s.paquete_promedio==None else s.paquete_promedio
    promedio_precio_paquetes_disponibles_total = round(suma/agencias.count(),2)

    agencia_cantidad_hoteles=agencia.hotel_count
    ranking_por_cantidad_hoteles=agencias.filter(hotel_count__gt=agencia_cantidad_hoteles).count()+1
    suma=0
    for s in agencias:
        suma += s.hotel_count
    promedio_cantidad_hoteles = round(suma/agencias.count(),2)

    agencia_cantidad_excursiones=agencia.excursion_count
    ranking_cantidad_excursiones=agencias.filter(excursion_count__gt=agencia_cantidad_excursiones).count()+1
    suma=0
    for s in agencias:
        suma += s.excursion_count
    promedio_cantidad_excursiones = round(suma/agencias.count(),2)

    hoteles = Hotel.objects.annotate(cantidad_reservaciones=Count('reservacionhotel',distinct=True)).order_by('-cantidad_reservaciones')
    hotel_mas_reservado = hoteles[0]

    excursiones = Excursion.objects.annotate(cantidad_reservaciones=Count('reservacionindividual__excursiones',distinct=True)).order_by('-cantidad_reservaciones')
    excursion_mas_reservada = excursiones[0]
    #######
    ctx = {}
    ctx['dinero_total'] = agencia_dinero_total
    ctx['ranking_ganacias'] = ranking_por_ganancias
    ctx['Promedio_dinero_agencias'] = promedio_ganacias_por_agencias
    ctx['reservaciones_total'] = agencia_reservaciones_total
    ctx['ranking_reservaciones_total'] = ranking_por_reservaciones_total
    ctx['Promedio_reservaciones_total'] = promedio_reservaciones_total_por_agencia
    ctx['reservaciones_paquetes_total'] = agencia_reservaciones_paquete
    ctx['ranking_reservaciones_paquetes'] = ranking_por_reservaciones_paquete
    ctx['Promedio_reservaciones_paquetes'] = promedio_reserciones_paquete_por_agencias
    ctx['reservaciones_individuales_total'] = agencia_reservaciones_individuales
    ctx['ranking_reservaciones_individuales'] = ranking_por_reservaciones_ind
    ctx['Promedio_reservaciones_individuales'] = promedio_reserciones_individuales_por_agencias
    ctx['diferentes_turistas_reservaciones'] = cantidad_distintos_turistas_reservaron
    ctx['ranking_cantidad_turistas'] = ranking_por_cantidad_turistas
    ctx['Promedio_cantidad_turistas'] = promedio_cantidad_turistas_por_agencia
    ctx['Cantidad_paquetes'] = agencia_cantidad_paquetes_disponibles
    ctx['ranking_cantidad_paquetes'] = ranking_cantidad_paquetes_disponibles
    ctx['Promedio_cantidad_paquetes'] = promedio_cantidad_paquetes_disponibles
    ctx['agencia_promedio_precio_paquetes'] = agencia_precio_promedio_por_paquete
    ctx['ranking_precio_promedio_paquetes'] = ranking_precio_promedio_por_paquete
    ctx['Promedio_precio_paquetes'] = promedio_precio_paquetes_disponibles_total
    ctx['Cantidad_hoteles'] = agencia_cantidad_hoteles
    ctx['ranking_cantidad_hoteles'] = ranking_por_cantidad_hoteles
    ctx['Promedio_cantidad_hoteles'] = promedio_cantidad_hoteles
    ctx['Cantidad_excursiones'] = agencia_cantidad_excursiones
    ctx['ranking_cantidad_excursiones'] = ranking_cantidad_excursiones
    ctx['Promedio_cantidad_excursiones'] = promedio_cantidad_excursiones
    ctx['hotel_mas_reservado'] = hotel_mas_reservado
    ctx['excursion_mas_reservada'] = excursion_mas_reservada


    return render(request, 'manager_estadisticas_comparar.html',ctx)

@login_required
def manager_reservaciones(request):
    manager_required(request.user)
    agencia = request.user.manageragencia.agencia
    turistas_paquete = Turista.objects.filter(reservacionpaquete__in = ReservacionPaquete.objects.filter(paquete__in=Paquete.objects.filter(agencia=agencia)))
    turistas_individual = Turista.objects.filter(reservacionindividual__in = ReservacionIndividual.objects.filter(agencia=agencia))
    turistas = turistas_paquete.union(turistas_individual)

    for turista in turistas:
        turista.paq=ReservacionPaquete.objects.filter(paquete__in=Paquete.objects.filter(agencia=agencia),turista=turista).count()
        turista.ind=ReservacionIndividual.objects.filter(agencia=agencia,turista=turista).count()
        turista.total=turista.paq+turista.ind
    
    reservaciones_paquete = ReservacionPaquete.objects.filter(paquete__in=Paquete.objects.filter(agencia=agencia))
    reservaciones_individual = ReservacionIndividual.objects.filter(agencia=agencia).annotate(cant_hoteles=Count('reservacionhotel',distinct=True),
                                                                                              cant_excursiones=Count('excursiones',distinct=True))
    for reserva in reservaciones_individual:
        reserva.reservacion_hoteles=ReservacionHotel.objects.filter(reservacion=reserva)
    ctx={}
    ctx['turistas']=turistas
    ctx['reservaciones_paquete']=reservaciones_paquete
    ctx['reservaciones_individual']=reservaciones_individual
    return render(request, 'manager_reservaciones.html',ctx)