from django.db.models.query_utils import Q
from django.db.models import Count, Sum
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.forms.formsets import formset_factory
from django.urls import reverse
from ..models import *
from ..forms.turistas_forms import * 
from ..fields import companhias


def turist_required(user:User):
    if not user.is_turist:
        if user.is_manager:
            return redirect('manager-home')
        return redirect('admin/')


####### Turista Area

@login_required
def turista_home(request):
    turist_required(request.user)
    return render(request, 'turista_perfil.html')


@login_required
def turista_perfil_editar(request):
    turist_required(request.user)
    if request.method =='POST':
        form = TuristaPerfilEditar(request.POST)
        if form.is_valid():
            u = User.objects.filter(username=form.cleaned_data['NombreUsuario'])
            if u.count() == 0 or u[0] == request.user:
                request.user.username = form.cleaned_data['NombreUsuario']
                request.user.first_name = form.cleaned_data['Nombre']
                request.user.last_name = form.cleaned_data['Apellido']
                request.user.turista.nombre = form.cleaned_data['Nombre']
                request.user.email = form.cleaned_data['Email']
                request.user.turista.pais = form.cleaned_data['Nacionalidad']
                request.user.email = form.cleaned_data['Email']
                request.user.set_password(form.cleaned_data['Contrasena'])
                request.user.turista.save()
                request.user.save()
                login(request,request.user)
                return redirect('turista-perfil')

    form = TuristaPerfilEditar(initial={'Nombre':request.user.turista.nombre,
                                        'Apellido':request.user.last_name,
                                        'NombreUsuario':request.user.username,
                                        'Email':request.user.email,
                                        'Contrasena':request.user.password,
                                        'Nacionalidad' :request.user.turista.pais})
    return render(request, 'turista_perfil_editar.html',{'form': form})

@login_required
def turista_perfil(request):
    turist_required(request.user)
    return render(request, 'turista_perfil.html')

@login_required
def turista_estadisticas(request):
    turist_required(request.user)
    paquetes = ReservacionPaquete.objects.filter(turista=request.user.turista)
    reservaciones = ReservacionIndividual.objects.filter(turista=request.user.turista)
    reservaciones = reservaciones.annotate(cantidad_hoteles=Count('reservacionhotel', distinct=True),cantidad_excursiones=Count('excursiones', distinct=True))
    dinero_total=0
    hotel_total=0
    excursion_total=0
    for p in paquetes:
        dinero_total +=p.precioTotal
    for r in reservaciones:
        excursion_total+=r.cantidad_excursiones
        hotel_total+=r.cantidad_hoteles
        dinero_total +=r.precioTotal
    paquetes_total=len(paquetes)
    agencias = Agencia.objects.all()
    max_agencias_paquete=None
    max_agencias_paquete_count=-1
    for agencia in agencias:
        res = ReservacionPaquete.objects.filter(turista=request.user.turista,paquete__agencia=agencia)
        if len(res) > max_agencias_paquete_count:
            max_agencias_paquete_count=len(res)
            max_agencias_paquete=agencia
    max_agencias_individual=None
    max_agencias_individual_count=-1
    for agencia in agencias:
        res = ReservacionIndividual.objects.filter(turista=request.user.turista,agencia=agencia)
        if len(res) > max_agencias_individual_count:
            max_agencias_individual_count=len(res)
            max_agencias_individual=agencia
    max_agencia=max_agencias_individual if max_agencias_individual_count > max_agencias_paquete_count else max_agencias_paquete

    max_compania_paquete=None
    max_compania_paquete_count=-1
    for c in companhias:
        res = ReservacionPaquete.objects.filter(turista=request.user.turista,companiaAerea=c)
        if len(res) > max_compania_paquete_count:
            max_compania_paquete_count=len(res)
            max_compania_paquete=c
    max_compania_individual=None
    max_compania_individual_count=-1
    for c in companhias:
        res = ReservacionIndividual.objects.filter(turista=request.user.turista,companiaAerea=c)
        if len(res) > max_compania_individual_count:
            max_compania_individual_count = len(res)
            max_compania_individual=c
    max_compania=max_compania_individual if max_compania_individual_count > max_compania_paquete_count else max_compania_paquete

    ctx={}
    ctx['aereolinea_max'] = companhias[max_compania]
    ctx['agencia_max'] = max_agencia.nombre
    ctx['paquetes'] = paquetes
    ctx['paquete_total'] = paquetes_total
    ctx['reservaciones'] = reservaciones
    ctx['dinero_total'] = dinero_total 
    ctx['hotel_total'] = hotel_total
    ctx['excursion_total']=excursion_total 

    return render(request, 'turista_estadisticas.html', ctx)





## ----> Paquetes

@login_required
def turista_paquetes(request):
    turist_required(request.user)
    paquetes = Paquete.objects.annotate(cant_hoteles=Count('hoteles',distinct=True),
                                        cant_facilidades=Count('facilidades', distinct=True)).filter(disponible=True)
    queryPaquetes = QueryFormPaquetes()
    return render(request, 'turista_paquete.html', {'paquetes':paquetes,
                                                    'queryPaquetes':queryPaquetes})

@login_required
def paquete_reserva(request, pk):
    turist_required(request.user)
    paquete = get_object_or_404(Paquete, pk=pk)
    if request.method == 'POST':
        form = ReservarPaqueteForm(request.POST, paquete=paquete)
        if form.is_valid():
            reserva_paquete = ReservacionPaquete()
            reserva_paquete.cantidadParticipantes = form.cleaned_data['CantidadParticipantes']
            reserva_paquete.companiaAerea = form.cleaned_data['CompAerea']
            reserva_paquete.paquete = paquete
            reserva_paquete.turista = request.user.turista
            reserva_paquete.fecha = form.cleaned_data['FechaSalida']
            reserva_paquete.precioTotal = form.cleaned_data['CantidadParticipantes']*paquete.precio
            reserva_paquete.save()
            return HttpResponseRedirect(reverse('reserva-paquete-completada', args=(reserva_paquete.IdRP,)))
    else:
        form = ReservarPaqueteForm(paquete=paquete)
    return render(request, 'paquete_reserva.html', {'form': form, 'paquete':paquete})


@login_required
def reserva_paquete_completada(request, pk):
    turist_required(request.user)
    reserva_paquete = ReservacionPaquete.objects.get(pk=pk)
    turista = request.user.turista
    tipo = turista.tipo
    if tipo != 'M':
        if tipo != 'I':
            tipo = 'P'
        else: tipo = 'M'
    turista.tipo = tipo
    turista.save()
    return render(request, 'paquete_reserva_completada.html', {'reserva': reserva_paquete})




## ----> Hoteles

@login_required
def turista_hoteles(request):
    turist_required(request.user)
    ofertas = Oferta.objects.filter(hotel__agencia__gt=0).distinct()
    queryHoteles = QueryFormHoteles()
    return render(request, 'turista_hotel.html', {'ofertas':ofertas,
                                                'queryHoteles':queryHoteles})

@login_required
def hotel_reserva(request, pk):
    turist_required(request.user)
    oferta = get_object_or_404(Oferta, pk=pk)
    hotel = oferta.hotel
    if request.method=="POST":
        form_hotel = ReservaHotelForm(request.POST, hotel=hotel, oferta_id=pk)
        if form_hotel.is_valid():
            reserva_individual = ReservacionIndividual()
            reserva_individual.turista = request.user.turista
            reserva_individual.companiaAerea = form_hotel.cleaned_data['compAerea']
            reserva_individual.agencia = form_hotel.cleaned_data['agencia']
            reserva_individual.cantidadAcompanhantes = form_hotel.cleaned_data['cantidadAcompanhantes'] 

            fecha_llegada = form_hotel.cleaned_data['fecha_llegada']
            fecha_salida = form_hotel.cleaned_data['fecha_salida']
            dias_total = (fecha_salida-fecha_llegada).days
            precioT = 0
            for ofer in form_hotel.cleaned_data['ofertas']:
                precioT = precioT + dias_total*ofer.precio
            reserva_individual.precioTotal = precioT
            reserva_individual.save()
            reserva_hotel = ReservacionHotel(reservacion=reserva_individual, hotel=hotel,
            fechaLlegada=fecha_llegada, fechaSalida=fecha_salida)
            reserva_hotel.save()
            return HttpResponseRedirect(reverse('reserva-agencia-completada', args=(reserva_individual.IdRI,)))
    else:
        form_hotel = ReservaHotelForm(hotel=hotel, oferta_id=pk)
    context = {'hotel_form' : form_hotel}
    return render(request, 'hotel_reserva.html', context=context)



# ---> Excursiones

@login_required
def turista_excursiones(request):
    turist_required(request.user)
    excursiones = Excursion.objects.annotate(cant_hoteles=Count('hoteles',distinct=True)).filter(agencia__gt=0 ,disponible=True)
    queryExcursiones = QueryFormExcursiones()
    return render(request, 'turista_excursion.html', {'excursiones':excursiones,
                                                    'queryExcursiones': queryExcursiones})

@login_required
def excursion_reserva(request, pk):
    turist_required(request.user)
    excursion = get_object_or_404(Excursion, pk=pk)
    if request.method=="POST":
        form_exc = ReservaExcursionForm(request.POST, excursion=excursion)
        if form_exc.is_valid():
            reserva_individual = ReservacionIndividual()
            reserva_individual.turista = request.user.turista
            reserva_individual.companiaAerea = form_exc.cleaned_data['compAerea']
            reserva_individual.agencia = form_exc.cleaned_data['agencia']
            personasT = 1 + form_exc.cleaned_data['cantidadAcompanhantes']
            reserva_individual.cantidadAcompanhantes = personasT - 1
            reserva_individual.precioTotal = personasT*excursion.precio
            reserva_individual.save()
            reserva_individual.excursiones.add(excursion)
            reserva_individual.save()
            return HttpResponseRedirect(reverse('reserva-agencia-completada', args=(reserva_individual.IdRI,)))
    else:
        form_exc = ReservaExcursionForm(excursion=excursion)
    context = {'excursion_form' : form_exc}
    return render(request, 'excursion_reserva.html', context=context)



# ---> Reserva por Agencias

@login_required
def turista_reserva_por_agencia(request):
    turist_required(request.user)
    agencias = Agencia.objects.annotate(cant_exc=Count('excursiones',distinct=True), cant_hot=Count('hoteles',distinct=True,filter=Q(hoteles__oferta__gt=0)),
                                        avg_precio_exc=Sum('excursiones__precio',distinct=True)/Count('excursiones',distinct=True),
                                        avg_precio_hot=Sum('hoteles__oferta__precio',distinct=True)/Count('hoteles',distinct=True)).filter(
                                        Q(cant_exc__gt=0)| Q(cant_hot__gt=0))
                                        
    return render(request, 'turista_reserva_por_agencia.html', {'agencias':agencias})


@login_required
def agencia_reserva(request, pk):
    turist_required(request.user)
    agencia = get_object_or_404(Agencia, pk=pk)
    HotelesFormset = formset_factory(form=HotelesParaReservaForm, formset=BaseHotelesFormset)
    
    if request.method == 'POST':
        form_agencia = ReservaPorAgenciaForm(request.POST, agencia_id=pk)
        hoteles_formset = HotelesFormset(data=request.POST,form_kwargs={'agencia_id':pk})

        if form_agencia.is_valid() and hoteles_formset.is_valid():
            
            reserva_individual = ReservacionIndividual()
            reserva_individual.turista = request.user.turista
            reserva_individual.companiaAerea = form_agencia.cleaned_data['CompAerea']
            reserva_individual.agencia = agencia
            personasT = 1 + form_agencia.cleaned_data['CantidadAcompanhantes'] 
            reserva_individual.cantidadAcompanhantes = personasT-1
            precioT = 0
            reserva_individual.precioTotal = precioT
            reserva_individual.save()
            if form_agencia.cleaned_data['Excursiones']:
                for exc in form_agencia.cleaned_data['Excursiones']:
                    precioT = precioT + personasT*exc.precio
                    reserva_individual.excursiones.add(exc)
            hoteles_reservados = []
            for form in hoteles_formset:
                if form.cleaned_data:
                    hotel = form.cleaned_data['hotel']
                    fecha_llegada = form.cleaned_data['fecha_llegada']
                    fecha_salida = form.cleaned_data['fecha_salida']
                    dias_total = (fecha_salida-fecha_llegada).days
                    hoteles_reservados.append({'h':hotel, 'fll':fecha_llegada, 'fs':fecha_salida})
                    for ofer in form.cleaned_data['ofertas']:
                        precioT = precioT + dias_total*ofer.precio
            reserva_individual.precioTotal = precioT
            reserva_individual.save()
            for res_hot in hoteles_reservados:
                reserva_hotel = ReservacionHotel(reservacion=reserva_individual, hotel=res_hot['h'],
                fechaLlegada=res_hot['fll'], fechaSalida=res_hot['fs'])
                reserva_hotel.save()

            return HttpResponseRedirect(reverse('reserva-agencia-completada', args=(reserva_individual.IdRI,)))
    else:
        hoteles_formset = HotelesFormset(form_kwargs={'agencia_id':pk})
        form_agencia = ReservaPorAgenciaForm(initial={'Agencia': agencia},agencia_id=pk)
    context = {'agencia_form' : form_agencia,
                'hoteles_formset': hoteles_formset}
    return render(request, 'agencia_reserva.html', context=context)

@login_required
def reserva_agencia_completada(request, pk):
    turist_required(request.user)
    reserva = get_object_or_404(ReservacionIndividual, pk=pk)
    turista = request.user.turista
    tipo = turista.tipo
    if tipo != 'M':
        if tipo != 'P':
            tipo = 'I'
        else: tipo = 'M'
    turista.tipo = tipo
    turista.save()
    return render(request, 'agencia_reserva_completada.html', {'reserva': reserva})

