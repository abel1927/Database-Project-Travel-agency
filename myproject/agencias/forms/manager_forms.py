from django import forms
from ..models import Hotel, Excursion, Facilidad




class ManagerPerfilEditar(forms.Form):
    NombreUsuario = forms.CharField(widget=forms.TextInput(),label="Nombre de usuario")
    Nombre = forms.CharField(widget=forms.TextInput())
    Apellido = forms.CharField(widget=forms.TextInput())
    Email = forms.EmailField()
    Contrasena = forms.CharField(widget=forms.PasswordInput(),label="Contraseña")


class ManagerAgenciaEditar(forms.Form):
    Nombre = forms.CharField(widget=forms.TextInput())
    Direccion = forms.CharField(widget=forms.TextInput())
    noFax = forms.CharField(widget=forms.TextInput(),label="Numero de Fax")
    Email = forms.EmailField()


class PaqueteEditar(forms.Form):
    Descripcion = forms.CharField(widget=forms.TextInput(), label="Descripción")
    Duracion = forms.IntegerField(label="Duración", min_value=1)
    Precio = forms.IntegerField(widget= forms.NumberInput())
    def __init__(self,*args,**kwargs):
        agencia= kwargs.pop('agencia')
        super().__init__(*args,**kwargs)
        self.fields['Facilidades']= forms.ModelMultipleChoiceField(queryset=Facilidad.objects.all(),required=False)
        self.fields['Hoteles']= forms.ModelMultipleChoiceField(queryset=agencia.hoteles.all())
    Disponible = forms.BooleanField(required=False)


class PaqueteNuevo(forms.Form):
    Descripcion = forms.CharField(widget=forms.TextInput(), label="Descripción")
    Duracion = forms.IntegerField(min_value=1, label="Duración")
    Precio = forms.IntegerField(min_value=1,widget= forms.NumberInput(), label="Precio")
    def __init__(self,*args,**kwargs):
        agencia= kwargs.pop('agencia')
        super().__init__(*args,**kwargs)
        self.fields['Facilidades']= forms.ModelMultipleChoiceField(queryset=Facilidad.objects.all(),required=False)
        self.fields['Hoteles']= forms.ModelMultipleChoiceField(queryset=agencia.hoteles.all())
    Disponible = forms.BooleanField(required=False)


class HotelAdd(forms.Form):
    def __init__(self, *args,**kwargs):
        agencia = kwargs.pop('agencia')
        super().__init__(*args,**kwargs)
        self.fields['Hoteles']=forms.ModelMultipleChoiceField(queryset=Hotel.objects.exclude(agencia=agencia))


class ExcursionAdd(forms.Form):
    def __init__(self, *args,**kwargs):
        agencia = kwargs.pop('agencia')
        super().__init__(*args,**kwargs)
        self.fields['Excursiones']=forms.ModelMultipleChoiceField(queryset=Excursion.objects.exclude(agencia=agencia))

