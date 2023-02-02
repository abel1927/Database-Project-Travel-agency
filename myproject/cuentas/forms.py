from django import forms
from django.db.models.fields import CharField
from django_countries.fields import CountryField
from django.db import transaction
from agencias.models import Turista, User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import SolicitudAsociacionAgencia

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User



class TuristaSignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    pais = CountryField(blank_label='(Seleccionar pais)').formfield()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'email', 'pais', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_turist = True
        user.save()
        turista = Turista(user=user)
        turista.pais = (self.cleaned_data.get('pais'))
        turista.nombre = self.cleaned_data.get('first_name')
        turista.save()
        return user


class FormularioDeSolicitudMuestra(forms.Form):
    nombre = forms.CharField( label="Nombre de la agencia", max_length=50)
    direccion = forms.CharField(disabled=True,label='Direccón principal', max_length=120)
    email_agencia = forms.EmailField(disabled=True,label= 'email agencia', widget=forms.EmailInput())
    noFax = forms.CharField(disabled=True,label="Fax", max_length=20)
    entidad_bancaria = forms.CharField(disabled=True,label="Entidad bancaria de respaldo", 
                help_text="Entidad bancaria dende de la empresa maneja su cuenta principal.")
    anhos_activa = forms.IntegerField(disabled=True,min_value=0, max_value=100, label="Años de antigüedad")
    manager_nombre = forms.CharField(disabled=True,label="Manager nombre", max_length=70)
    manager_email = forms.EmailField(disabled=True,label= 'email manager', widget=forms.EmailInput())
    tiempo_con_hv = forms.IntegerField(disabled=True,label="Cuánto tiempo espera trabajar con nosotros")

    def __init__(self, *args, **kwargs):
        solicitud = kwargs.pop('solicitud')
        super(FormularioDeSolicitudMuestra, self).__init__(*args, **kwargs)
        self.fields['nombre'].initial = solicitud.nombre
        self.fields['direccion'].initial = solicitud.direccion
        self.fields['email_agencia'].initial = solicitud.email_agencia
        self.fields['noFax'].initial = solicitud.noFax
        self.fields['entidad_bancaria'].initial = solicitud.entidad_bancaria
        self.fields['abhos_activa'].initial = solicitud.anhos_activa
        self.fields["manager_nombre"].initial = solicitud.manager_nombre
        self.fields["manager_email"].initial = solicitud.manager_email
        self.fields["timepo_con_hv"].initial = solicitud.tiempo_con_hv





class SolicitudIngresoAgenciaForm(forms.ModelForm):
    class Meta:
        model = SolicitudAsociacionAgencia
        exclude = ['IdS']

