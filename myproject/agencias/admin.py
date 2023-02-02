from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms.models import fields_for_model

# Register your models here.
from .models import *
from cuentas.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm
)

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (
            None, {
                'fields': (
                    'is_turist',
                    'is_manager'
                )
            }
        ),
    )


class UserAdmin(CustomUserAdmin):
    list_display = ('username','first_name','last_name','is_turist','is_manager','is_staff')
    #fields = ('username','first_name','last_name','email', 'password', ('is_staff','is_turist','is_manager'),'date_joined',)
    list_editable = ('is_staff','is_manager','is_turist')


class AgenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'email')
    search_fields=('nombre','email')
    filter_horizontal =('hoteles',)


class HotelAdmin(admin.ModelAdmin):
    list_display = ('nombre','direccion','categoria')


class FacilidadAdmin(admin.ModelAdmin):
    list_display=('descripcion',)
    search_fields=('descripcion',)


class TuristasAdmin(admin.ModelAdmin):
    list_display=('nombre', 'pais', 'tipo')
    list_filter=('pais','tipo')
    search_fields=('nombre',)



class ReservacionPaqueteAdmin(admin.ModelAdmin):
    list_display=('turista','paquete','companiaAerea','cantidadParticipantes','precioTotal')
    search_fields=('turista','paquete')
    readonly_fields=('precioTotal',)
    
    def turista(self, obj):
        return obj.turista.nombre
    def paquete(self,obj):
        return obj.paquete.descripcion

class ReservacionIndividualAdmin(admin.ModelAdmin):
    list_display=('turista','agencia','companiaAerea','cantidadAcompanhantes',"precio")
    search_fields=('turista','agencia')
    readonly_fields=('precioTotal',)
    list_filter=('agencia','companiaAerea')
    def precio(self,obj):
        return obj.precioTotal


class PaqueteAdmin(admin.ModelAdmin):
    list_display=('descripcion','agencia','precio','disponible')
    search_fields=('descripcion','agencia')
    filter_horizontal=('hoteles','facilidades')
    list_editable=('disponible',)
    list_filter=('agencia',)
    def agencia(self,obj):
        return obj.agencia.nombre

class ExcursionAdmin(admin.ModelAdmin):
    list_display=('lugarSalida','diaSalida','lugarLlegada','diaLlegada','precio','disponible')
    fields=('lugarSalida',('diaSalida','horaSalida'),'lugarLlegada',('diaLlegada','horaLlegada'),'precio','hoteles','disponible')
    filter_horizontal =('hoteles',)
    list_editable=('disponible',)


class OfertaAdmin(admin.ModelAdmin):
    list_display=('descripcion','hotel','precio')
    list_filter=('hotel',)


class ManagerAgenciaAdmin(admin.ModelAdmin):
    list_display=('name','agencia',)
    def name(self,obj):
        return obj.user.username
    def agencia(self,obj):
        return obj.agencia.nombre

class ReservacionHotelAdmin(admin.ModelAdmin):
    list_display=('turista','hotel','fechaLlegada','fechaSalida')
    def turista(self,obj):
        return obj.reservacion.turista.nombre

admin.site.register(Turista,TuristasAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Agencia,AgenciaAdmin)
admin.site.register(Hotel,HotelAdmin)
admin.site.register(Oferta,OfertaAdmin)
admin.site.register(Excursion,ExcursionAdmin)
admin.site.register(Paquete,PaqueteAdmin)
admin.site.register(Facilidad,FacilidadAdmin)
admin.site.register(ReservacionIndividual,ReservacionIndividualAdmin)
admin.site.register(ReservacionPaquete,ReservacionPaqueteAdmin)
admin.site.register(ReservacionHotel,ReservacionHotelAdmin)
admin.site.register(ManagerAgencia,ManagerAgenciaAdmin)



