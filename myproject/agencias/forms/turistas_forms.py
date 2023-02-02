from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet
from ..fields import FlyCompanyFormField, ExcursionModelMultipleChoiceField
from ..models import Hotel, Oferta, Excursion, Agencia, Facilidad
from django_countries.fields import CountryField
import datetime



class TuristaPerfilEditar(forms.Form):
    NombreUsuario = forms.CharField(widget=forms.TextInput(),label="Nombre de usuario")
    Nombre = forms.CharField(widget=forms.TextInput())
    Apellido = forms.CharField(widget=forms.TextInput())
    Email = forms.EmailField()
    Nacionalidad = CountryField().formfield()
    Contrasena = forms.CharField(widget=forms.PasswordInput(),label="Contraseña")


class ReservarPaqueteForm(forms.Form):
    Agencia = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Descripcion = forms.CharField(label='Descripción',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Facilidades = forms.ModelMultipleChoiceField(queryset=Facilidad.objects.none(), required=False,
                                widget=forms.CheckboxSelectMultiple(attrs={'disabled':'true'}))
    PrecioPorPersona = forms.IntegerField(label='Precio por Persona', 
                                        widget=forms.TextInput(attrs={'readonly':'readonly'}))
    CompAerea = FlyCompanyFormField(help_text='Elija su compañía aérea',
                                widget=forms.Select(attrs={'onclick': 'calcular();'}))
    FechaSalida = forms.DateField(help_text="Formato: YYYY-MM-DD", label='Fecha Salida',
                                    widget=forms.DateInput(attrs={'onclick': 'calcular();'}))
    CantidadParticipantes = forms.IntegerField(help_text='Indique la cantidad de participantes', 
                                            label='Cantidad de Personas' ,initial=2, min_value=2,
                                            widget=forms.NumberInput(attrs={'onchange': 'calcular();'}))

    def __init__(self, *args, **kwargs):
        paquete = kwargs.pop('paquete')
        super(ReservarPaqueteForm, self).__init__(*args, **kwargs)
        self.fields['Agencia'].initial = paquete.agencia
        self.fields['Descripcion'].initial = paquete.descripcion
        self.fields['PrecioPorPersona'].initial = paquete.precio
        facilidades = paquete.facilidades.all()
        self.fields['Facilidades'].queryset = facilidades
        self.fields['Facilidades'].initial = [f.IdF for f in facilidades]


class ReservaHotelForm(forms.Form):
    hotel = forms.CharField(label="Hotel", widget=forms.TextInput(attrs={'readonly':'readonly'}))
    agencia = forms.ModelChoiceField(queryset=Agencia.objects.all(),label="Agencia")
    fecha_llegada = forms.DateField(label='Fecha Llegada',
                                    widget=forms.DateInput(attrs={'placeholder':'YYYY-MM-DD'}))
    fecha_salida = forms.DateField(label='Fecha Salida',
                                    widget=forms.DateInput(attrs={'placeholder':'YYYY-MM-DD'}))
    ofertas = forms.ModelMultipleChoiceField(label='Ofertas', 
                                    queryset=Oferta.objects.all(), widget=forms.SelectMultiple())
    cantidadAcompanhantes = forms.IntegerField(label='Cantidad de acompañantes' ,initial=0, min_value=0,
                            widget=forms.NumberInput())
    compAerea = FlyCompanyFormField(widget=forms.Select())

    def __init__(self, *args, **kwargs):
        hotel = kwargs.pop('hotel')
        oferta_sel = kwargs.pop('oferta_id')
        super(ReservaHotelForm, self).__init__(*args, **kwargs)
        self.fields['hotel'].initial = hotel.nombre
        self.fields['agencia'].queryset = Agencia.objects.filter(hoteles__pk=hotel.IdH)
        self.fields['ofertas'].queryset = Oferta.objects.filter(hotel=hotel)
        self.fields['ofertas'].initial = [oferta_sel]

    def clean_fecha_llegada(self):
        data = self.cleaned_data["fecha_llegada"]
        if data < datetime.date.today():
            raise ValidationError('Fecha inválida - fecha en el pasado')
        return data

    def clean_fecha_salida(self):
        data = self.cleaned_data["fecha_salida"]
        if data > datetime.date.today() + datetime.timedelta(weeks=60):
            raise ValidationError("""Fecha demasiado avanzada, debe ser inferior a 400 días a 
        partir de la fecha actual""")
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_llegada = cleaned_data.get('fecha_llegada')
        fecha_salida = cleaned_data.get('fecha_salida')
        
        if fecha_llegada and fecha_salida:
            if fecha_salida <= fecha_llegada:
                msg = "Fecha de salida debe ser posterior a fecha de llegada"
                self.add_error('fecha_salida', msg)


class ReservaExcursionForm(forms.Form):
    excursion = forms.CharField(label="Excursión", widget=forms.TextInput(attrs={'readonly':'readonly'}))
    agencia = forms.ModelChoiceField(queryset=Agencia.objects.all(),label="Agencia")
    cantidadAcompanhantes = forms.IntegerField(label='Cantidad de acompañantes' ,initial=0, min_value=0,
                            widget=forms.NumberInput())
    compAerea = FlyCompanyFormField(widget=forms.Select())

    def __init__(self, *args, **kwargs):
        excursion = kwargs.pop('excursion')
        super(ReservaExcursionForm, self).__init__(*args, **kwargs)
        self.fields['excursion'].initial = str(excursion)
        self.fields['agencia'].queryset = Agencia.objects.filter(excursiones__pk=excursion.IdE)


class ReservaPorAgenciaForm(forms.Form):
    Agencia = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    CompAerea = FlyCompanyFormField(widget=forms.Select())
    CantidadAcompanhantes = forms.IntegerField(label='Cantidad de acompañantes' ,initial=0, min_value=0,
                            widget=forms.NumberInput())
    Excursiones = ExcursionModelMultipleChoiceField(queryset=Excursion.objects.all())

    def __init__(self, *args, **kwargs):
        agencia_id = kwargs.pop('agencia_id')
        super(ReservaPorAgenciaForm, self).__init__(*args, **kwargs)
        self.fields["Excursiones"].queryset = Excursion.objects.filter(agencia=agencia_id, disponible=True)


class HotelesParaReservaForm(forms.Form):
    hotel = forms.ModelChoiceField(label='Hotel', queryset=Hotel.objects.all(),
                                    widget=forms.Select(attrs={'class': 'hotel_class',
                                                                'onchange':'cambio(this);'} 
                                    ))
    fecha_llegada = forms.DateField(label='Fecha Llegada',
                                    widget=forms.DateInput(attrs={'placeholder':'YYYY-MM-DD'}))
    fecha_salida = forms.DateField(label='Fecha Salida',
                                    widget=forms.DateInput(attrs={'placeholder':'YYYY-MM-DD'}))
    ofertas = forms.ModelMultipleChoiceField(label='Ofertas', 
                                    queryset=Oferta.objects.all(), widget=forms.SelectMultiple(
                                        {'style':'display:None',
                                        "onchange":"oferta_opcionChange(this);"}
                                    ))

    def __init__(self, *args, **kwargs):
        agencia_id = kwargs.pop('agencia_id')
        super(HotelesParaReservaForm, self).__init__(*args, **kwargs)
        self.fields["hotel"].queryset = Hotel.objects.filter( agencia=agencia_id, oferta__gt=0).distinct()

    def clean_fecha_llegada(self):
        data = self.cleaned_data["fecha_llegada"]
        if data < datetime.date.today():
            raise ValidationError('Fecha inválida - fecha en el pasado')
        return data

    def clean_fecha_salida(self):
        data = self.cleaned_data["fecha_salida"]
        if data > datetime.date.today() + datetime.timedelta(weeks=60):
            raise ValidationError("""Fecha demasiado avanzada, debe ser inferior a 400 días a 
        partir de la fecha actual""")
        return data
    

    def clean(self):
        cleaned_data = super().clean()
        fecha_llegada = cleaned_data.get('fecha_llegada')
        fecha_salida = cleaned_data.get('fecha_salida')
        
        if fecha_llegada and fecha_salida:
            if fecha_salida <= fecha_llegada:
                msg = "Fecha de salida debe ser posterior a fecha de llegada"
                self.add_error('fecha_salida', msg)


class BaseHotelesFormset(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        hoteles = []
        ofertas = []
        duplicados = False
        for form in self.forms:
            if form.cleaned_data:
                hotel = form.cleaned_data['hotel']
                ofertas = form.cleaned_data['ofertas']
                # Dos hoteles iguales
                if hotel:
                    if hotel in hoteles:
                        duplicados = True
                    hoteles.append(hotel)

                if duplicados:
                    raise forms.ValidationError(
                        'Debe seleccionar una sola vez cada hotel.',
                        code='duplicate_hoteles'
                    )
                # Cada hotel debe tener al menos una oferta
                if hotel and len(ofertas)==0:
                    raise forms.ValidationError(
                        'Debe elegir al menos una oferta para el hotel seleccionado.',
                        code='missing_oferta'
                    )


class QueryFormPaquetes(forms.Form):
    minimo_p = forms.IntegerField(min_value=0, label_suffix="Precio Min", label="Precio Mínimo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_minimo_p'}))
    maximo_p = forms.IntegerField(min_value=0, label_suffix="Precio Max", label="Precio Máximo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_maximo_p'}))
    minimo_dur = forms.IntegerField(min_value=0, label_suffix="Duración Min", label="Duración Minimo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_minimo_dur'}))
    maximo_dur = forms.IntegerField(min_value=0, label_suffix="Duración Max", label="Duración Máximo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_maximo_dur'}))
    incluir_facilidades = forms.BooleanField(label="Solo paquetes con facilidades",
                                            label_suffix="Incluir facilidades",required=False,
                                            widget=forms.CheckboxInput(attrs={'id':'id_incluir_fac'}))

class QueryFormExcursiones(forms.Form):
    minimo_p = forms.IntegerField(min_value=0, label_suffix="Precio Min", label="Precio Mínimo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_minimo_p'}))
    maximo_p = forms.IntegerField(min_value=0, label_suffix="Precio Max", label="Precio Máximo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_maximo_p'}))
    incluir_hoteles = forms.BooleanField(label="Solo excursiones con hoteles",
                                            label_suffix="Incluir hoteles",required=False,
                                            widget=forms.CheckboxInput(attrs={'id':'id_incluir_hot'}))

class QueryFormHoteles(forms.Form):
    minimo_p = forms.IntegerField(min_value=0, label_suffix="Precio Min", label="Precio Mínimo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_minimo_p'}))
    maximo_p = forms.IntegerField(min_value=0, label_suffix="Precio Max", label="Precio Máximo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_maximo_p'}))
    minimo_cat = forms.IntegerField(min_value=1, label_suffix="Categoría Min", label="Categoría Minimo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_minimo_cat'}),
                                    max_value=5)
    maximo_cat = forms.IntegerField(min_value=1, label_suffix="Categoría Max", label="Categoría Máximo",
                                    required=False, widget=forms.NumberInput(attrs={'id':'id_maximo_cat'}),
                                    max_value=5)

